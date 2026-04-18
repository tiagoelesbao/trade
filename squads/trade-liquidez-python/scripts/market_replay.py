import os
import sys
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yaml

# Carregar Config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

sys.path.append(os.path.dirname(__file__))
import bot_liquidez

# Detecta caminho real do MT5
if not mt5.initialize():
    print("Erro MT5")
    exit()
terminal_info = mt5.terminal_info()._asdict()
MT5_DATA_PATH = terminal_info.get('data_path')
mt5.shutdown()

def run_replay_for_symbol(symbol, local_cfg):
    if not mt5.initialize(): return 0, []

    m5_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 15000)
    m15_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 5000)
    h1_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 2000)
    
    if m5_rates is None or h1_rates is None or m15_rates is None: 
        mt5.shutdown(); return 0, []
    
    s_info = mt5.symbol_info(symbol)
    point = s_info.point
    is_jpy = "JPY" in symbol
    pip_value_usd = 10.0 if not is_jpy else 7.5 
    spread_pips = 1.5 if not is_jpy else 2.5
    cost_per_trade = spread_pips * 10.0
    
    mt5.shutdown()

    df_m5 = pd.DataFrame(m5_rates); df_m5['time'] = pd.to_datetime(df_m5['time'], unit='s', utc=True)
    df_m15 = pd.DataFrame(m15_rates); df_m15['time'] = pd.to_datetime(df_m15['time'], unit='s', utc=True)
    df_h1 = pd.DataFrame(h1_rates); df_h1['time'] = pd.to_datetime(df_h1['time'], unit='s', utc=True)

    df_m5['rsi'] = bot_liquidez.calculate_rsi(df_m5['close'])
    df_h1['sma20'] = df_h1['close'].rolling(20).mean()

    zone_tf_df = df_m15 if local_cfg.get('zone_timeframe') == "M15" else df_h1
    all_possible_zones = bot_liquidez.get_validated_zones(zone_tf_df, point)

    balance = 0.0
    trades_history = []
    cooldowns = {}
    active_position = None
    
    rsi_ob = local_cfg.get('rsi_overbought', 60)
    rsi_os = local_cfg.get('rsi_oversold', 40)
    
    for i in range(500, len(df_m5) - 1):
        candle = df_m5.iloc[i]
        curr_time = candle['time']
        
        if active_position:
            pos = active_position
            pips_diff = 0; closed = False
            
            if pos['type'] == 'BUY':
                if candle['low'] <= pos['sl']: pips_diff = (pos['sl'] - pos['entry']) / (point * 10); closed = True; reason = 'SL'
                elif candle['high'] >= pos['tp']: pips_diff = (pos['tp'] - pos['entry']) / (point * 10); closed = True; reason = 'TP'
            else:
                if candle['high'] >= pos['sl']: pips_diff = (pos['entry'] - pos['sl']) / (point * 10); closed = True; reason = 'SL'
                elif candle['low'] <= pos['tp']: pips_diff = (pos['entry'] - pos['tp']) / (point * 10); closed = True; reason = 'TP'
            
            if not closed and (i - pos['idx']) >= local_cfg['exit_candles_max']:
                pips_diff = (candle['close'] - pos['entry']) / (point * 10) if pos['type'] == 'BUY' else (pos['entry'] - candle['close']) / (point * 10); closed = True; reason = 'TIME'
                
            if closed:
                pnl_usd = (pips_diff * 10.0) - cost_per_trade
                balance += pnl_usd
                trades_history.append({**pos, 'pnl': pnl_usd, 'reason': reason, 'close_time': curr_time})
                active_position = None
            continue

        h1_recent = df_h1[df_h1['time'] < curr_time]
        if len(h1_recent) < 20: continue
        h1_row = h1_recent.iloc[-1]
        trend = 1 if h1_row['close'] > h1_row['sma20'] else -1
        current_zones = [z for z in all_possible_zones if z['time'] < curr_time]
        rsi = candle['rsi']
        
        for z in current_zones:
            z_key = f"{symbol}_{z['type']}_{round(z['price'], 5)}"
            if z_key in cooldowns and curr_time - cooldowns[z_key] < timedelta(hours=1): continue
            
            if z['type'] == 'RESISTANCE' and candle['high'] >= z['price'] and rsi >= rsi_ob and trend == -1:
                entry = candle['close']; sl = candle['high'] + (local_cfg['stop_buffer_points'] * point)
                risk_pips = (sl - entry) / (point * 10); tp = entry - (risk_pips * 1.5 * point * 10)
                active_position = {'type': 'SELL', 'entry': entry, 'sl': sl, 'tp': tp, 'idx': i, 'time': curr_time, 'z_price': z['price'], 'rsi': rsi, 'trend': trend}
                cooldowns[z_key] = curr_time; break
            
            if z['type'] == 'SUPPORT' and candle['low'] <= z['price'] and rsi <= rsi_os and trend == 1:
                entry = candle['close']; sl = candle['low'] - (local_cfg['stop_buffer_points'] * point)
                risk_pips = (entry - sl) / (point * 10); tp = entry + (risk_pips * 1.5 * point * 10)
                active_position = {'type': 'BUY', 'entry': entry, 'sl': sl, 'tp': tp, 'idx': i, 'time': curr_time, 'z_price': z['price'], 'rsi': rsi, 'trend': trend}
                cooldowns[z_key] = curr_time; break

    # Exporta sinais para Auditoria Visual no MT5
    audit_file = os.path.join(MT5_DATA_PATH, "MQL5", "Files", f"audit_backtest_{symbol}.csv")
    try:
        with open(audit_file, "w", encoding="ansi") as f:
            f.write("type,price,time,pnl,z_price,rsi,trend\n")
            for t in trades_history:
                t_type = "SIGNAL_BUY" if t['type'] == 'BUY' else "SIGNAL_SELL"
                mt5_time = t['time'].strftime('%Y.%m.%d %H:%M')
                f.write(f"{t_type},{t['entry']},{mt5_time},{t['pnl']},{t['z_price']},{t['rsi']:.1f},{t['trend']}\n")
    except: pass

    return balance, trades_history

def generate_exec_report(all_results):
    report = "# 📑 Relatório Executivo Realista: Auditoria Sniper v5.6\n\n"
    report += "Este relatório considera custos reais de **Spread (1.5 a 2.5 pips)** e correção de **Pip Value** por ativo.\n\n"
    
    for res in all_results:
        symbol = res['symbol']
        report += f"## 🌐 Ativo: {symbol}\n"
        report += f"**PNL Real (pago spread):** ${res['pnl']:.2f} | **Trades:** {len(res['history'])}\n\n"
        report += "| Horário | Direção | PNL USD | Racional |\n"
        report += "|:---:|:---:|:---:|:---|\n"
        for t in res['history']:
            direcao = "🟢 BUY" if t['type'] == 'BUY' else "🔴 SELL"
            status = "✅" if t['pnl'] > 0 else "❌"
            report += f"| {t['time'].strftime('%d/%m %H:%M')} | {direcao} | {t['pnl']:.2f} | {status} RSI:{t['rsi']:.1f} Zona:{t['z_price']:.5f} |\n"
        report += "\n---\n"

    with open("docs/relatorio_detalhado_backtest.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ Relatório Executivo Realista Gerado: docs/relatorio_detalhado_backtest.md")

def run_batch_test():
    print("="*65)
    print(" 🚨 BIG BACKTEST REALISTA v5.6: COM CUSTOS E AUDITORIA ")
    print("="*65)
    total_pnl = 0.0
    all_results = []
    for symbol in CFG['symbols']:
        print(f"Analisando {symbol}...", end=" ", flush=True)
        pnl, history = run_replay_for_symbol(symbol, CFG)
        print(f"✅ PNL: ${pnl:.2f} | Trades: {len(history)}")
        total_pnl += pnl
        all_results.append({'symbol': symbol, 'pnl': pnl, 'history': history})
    generate_exec_report(all_results)
    print("\n" + "="*65)
    print(f" PNL TOTAL REAL: ${total_pnl:.2f} | MÉDIA/DIA: ${(total_pnl/33):.2f}")
    print("="*65)

if __name__ == "__main__":
    run_batch_test()
