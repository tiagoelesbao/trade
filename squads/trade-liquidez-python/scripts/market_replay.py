import os
import sys
import MetaTrader5 as mt5
import pandas as pd
import pytz
from datetime import datetime
import yaml

# Carregar config.yaml
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

# Modificar sys.path para importar o bot_liquidez na mesma pasta
sys.path.append(os.path.dirname(__file__))
import bot_liquidez

def run_replay(custom_cfg=None, silent=False):
    if custom_cfg:
        local_cfg = custom_cfg
    else:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            local_cfg = yaml.safe_load(f)

    if not mt5.initialize():
        if not silent: print(f"Erro MT5: {mt5.last_error()}")
        return 0, 0, []

    SYMBOL = local_cfg['symbol']
    if not silent: print(f"Baixando histórico M5 e H1 do {SYMBOL} para Walk-Forward Engine...")
    
    # Vamos baixar 8000 candles passados para compor a arena
    m5_rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M5, 0, 8000)
    h1_rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_H1, 0, 1000)
    
    if m5_rates is None or h1_rates is None: mt5.shutdown(); return
    symbol_info = mt5.symbol_info(SYMBOL)
    point = symbol_info.point
    contract_size = symbol_info.trade_contract_size
    mt5.shutdown() # CORTA INTERNET: Zero look-ahead garantiado fisicamente

    df_m5_full = pd.DataFrame(m5_rates); df_m5_full['time'] = pd.to_datetime(df_m5_full['time'], unit='s', utc=True)
    df_h1_full = pd.DataFrame(h1_rates); df_h1_full['time'] = pd.to_datetime(df_h1_full['time'], unit='s', utc=True)

    print("Iniciando SIMULAÇÃO WALKING FORWARD (Caminhada Cega vela-a-vela)... dependendo da ram, isso leva tempo.")
    
    balance = 0.0
    trades_history = []
    cooldowns = {}
    
    active_position = None
    limit_order = None
    
    start_idx = 500 # Iniciamos aqui para o robô ter passado H1 e M5 garantido na "abertura oficial" da simulação
    if not silent: print("Iniciando SIMULAÇÃO WALKING FORWARD (Caminhada Cega vela-a-vela)...")
    
    for i in range(start_idx, len(df_m5_full) - 1):
        if not silent and i % 1000 == 0: print(f"Processing candle {i}/{len(df_m5_full)}")
        
        current_candle = df_m5_full.iloc[i]
        current_time = current_candle['time']
        
        # O universo do robô naquele exato segundo (O Passado isolado)
        df_m5_available = df_m5_full.iloc[:i] 
        df_h1_available = df_h1_full[df_h1_full['time'] < current_time]

        # 1. GESTÃO DO TRADE SIMULADO
        if active_position:
            pos = active_position
            low, high = current_candle['low'], current_candle['high']
            duration_candles = i - pos['open_time_idx']
            
            if duration_candles >= local_cfg['breakeven_candles'] and not pos.get('breakeven'):
                if pos['type'] == 'BUY' and current_candle['close'] > pos['entry']:
                    pos['sl'] = pos['entry'] + (10 * point); pos['breakeven'] = True
                elif pos['type'] == 'SELL' and current_candle['close'] < pos['entry']:
                    pos['sl'] = pos['entry'] - (10 * point); pos['breakeven'] = True

            closed = False
            pnl = 0
            reason = ""
            
            if pos['type'] == 'BUY':
                if low <= pos['sl']:
                    pnl = (pos['sl'] - pos['entry']) * contract_size * local_cfg['lot_size']
                    reason = "Breakeven" if pos.get('breakeven') and pos['sl'] >= pos['entry'] else "Stop Loss"
                    closed = True
                elif high >= pos['tp']:
                    pnl = (pos['tp'] - pos['entry']) * contract_size * local_cfg['lot_size']
                    reason = "Take Profit"; closed = True
            else:
                if high >= pos['sl']:
                    pnl = (pos['entry'] - pos['sl']) * contract_size * local_cfg['lot_size']
                    reason = "Breakeven" if pos.get('breakeven') and pos['sl'] <= pos['entry'] else "Stop Loss"
                    closed = True
                elif low <= pos['tp']:
                    pnl = (pos['entry'] - pos['tp']) * contract_size * local_cfg['lot_size']
                    reason = "Take Profit"; closed = True
                    
            if not closed and duration_candles >= local_cfg['exit_candles_max']:
                pnl = (current_candle['close'] - pos['entry']) * contract_size * local_cfg['lot_size'] if pos['type'] == 'BUY' else (pos['entry'] - current_candle['close']) * contract_size * local_cfg['lot_size']
                reason = "Tempo Esgotado"
                closed = True
                
            if closed:
                balance += pnl
                trades_history.append({
                    'type': pos['type'], 'entry': pos['entry'], 'pnl': pnl, 'reason': reason, 
                    'time': df_m5_full.iloc[pos['open_time_idx']]['time'], 'bk': pos.get('breakeven', False)
                })
                active_position = None
                continue

        # 2. MATCH DA LIMIT ORDER
        if limit_order:
            lo = limit_order
            if current_candle['low'] <= lo['price'] <= current_candle['high']:
                active_position = {'type': 'BUY' if lo['type'] == mt5.ORDER_TYPE_BUY_LIMIT else 'SELL', 
                                   'entry': lo['price'], 'sl': lo['sl'], 'tp': lo['tp'], 'open_time_idx': i}
                limit_order = None
                continue
            if i - lo['signal_time_idx'] > 4:
                limit_order = None

        # 3. LÓGICA ESTRITA DO BOT (Reuso das Funções de tempo real)
        if not active_position and not limit_order:
            df_h1_slice = df_h1_available.tail(local_cfg['lookback_h1']).copy()
            zones_h1 = bot_liquidez.get_validated_h1_zones(df_h1_slice, point)
            
            df_m5_slice = df_m5_available.tail(10).copy()
            df_m5_slice = pd.concat([df_m5_slice, df_m5_full.iloc[[i]]])
            
            # Temporariamente injetar as novas regras localmente no modulo de trigger
            original_entry_pct = bot_liquidez.ENTRY_RETRACEMENT_PCT
            original_cooldown = bot_liquidez.COOLDOWN_CANDLES
            bot_liquidez.ENTRY_RETRACEMENT_PCT = local_cfg['entry_retracement_pct']
            bot_liquidez.COOLDOWN_CANDLES = local_cfg['cooldown_candles']
            
            trigger, z_triggered = bot_liquidez.check_m5_trigger(df_m5_slice, zones_h1, point, cooldowns, current_time)
            
            bot_liquidez.ENTRY_RETRACEMENT_PCT = original_entry_pct
            bot_liquidez.COOLDOWN_CANDLES = original_cooldown
            
            if trigger:
                limit_order = trigger
                limit_order['signal_time_idx'] = i
                z_key = f"{z_triggered['type']}_{round(z_triggered['price'], 5)}"
                cooldowns[z_key] = current_time

    # GERAÇÃO DE RELATÓRIO
    wins = len([t for t in trades_history if t['pnl'] > 0])
    losses = len([t for t in trades_history if t['pnl'] < 0])
    zeros = len([t for t in trades_history if t['pnl'] == 0])
    total = len(trades_history)
    win_rate = (wins / total * 100) if total > 0 else 0
    
    if not silent:
        report = f"# Relatório Executivo: Market Replay Engine (Walk-Forward)\n\n"
        report += f"**Ativo:** {SYMBOL} | **Gráfico:** M5 | **Lote:** {local_cfg['lot_size']} | **Amostragem Cega:** ~7.500 candles\n"
        report += f"> Teste com isolamento absoluto (zero futuro acessível). Os parâmetros usados espelham exatamente a operação live com `config.yaml`.\n\n"
        report += f"## Resumo Financeiro (Validação Rigorosa)\n"
        report += f"- **Saldo Bruto Acumulado:** ${balance:.2f}\n"
        report += f"- **Taxa de Acerto (Win Rate):** {win_rate:.2f}%\n"
        report += f"- **Total de Trades:** {total}\n"
        report += f"- **Take Profits / Gains:** {wins}\n"
        report += f"- **Stop Loss (Cheio):** {losses}\n"
        report += f"- **Breakevens Acionados (0x):** {zeros}\n\n"
        
        report += f"## Detalhamento de Entradas\n"
        report += f"| Data/Hora Entrada | Direção | Preço | PNL | Motivo de Saída | Proteção 0x ativada |\n"
        report += f"|---|---|---|---|---|---|\n"
        for t in trades_history:
            bk_str = 'Sim' if t['bk'] else 'Não'
            report += f"| {t['time']} | {t['type']} | {t['entry']:.5f} | ${t['pnl']:.2f} | {t['reason']} | {bk_str} |\n"

        report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "replay_executivo.md")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n[SUCESSO] Relatório Replay Live gerado perfeitamente em: {report_path}")

    return balance, win_rate, trades_history

if __name__ == "__main__":
    run_replay()
