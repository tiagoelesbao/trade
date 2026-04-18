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

def run_replay_for_symbol(symbol, local_cfg, silent=True):
    if not mt5.initialize(): return 0, 0, []

    m5_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 10000)
    m15_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 4000)
    h1_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 1500)
    
    if m5_rates is None or h1_rates is None or m15_rates is None: 
        mt5.shutdown(); return 0, 0, []
    
    point = mt5.symbol_info(symbol).point
    contract_size = mt5.symbol_info(symbol).trade_contract_size
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
    
    for i in range(200, len(df_m5) - 1):
        candle = df_m5.iloc[i]
        curr_time = candle['time']
        
        if active_position:
            pos = active_position
            if pos['type'] == 'BUY':
                if candle['low'] <= pos['sl']:
                    pnl = (pos['sl'] - pos['entry']) * contract_size * local_cfg['lot_size']
                    balance += pnl; trades_history.append({'pnl': pnl}); active_position = None
                elif candle['high'] >= pos['tp']:
                    pnl = (pos['tp'] - pos['entry']) * contract_size * local_cfg['lot_size']
                    balance += pnl; trades_history.append({'pnl': pnl}); active_position = None
            else:
                if candle['high'] >= pos['sl']:
                    pnl = (pos['entry'] - pos['sl']) * contract_size * local_cfg['lot_size']
                    balance += pnl; trades_history.append({'pnl': pnl}); active_position = None
                elif candle['low'] <= pos['tp']:
                    pnl = (pos['entry'] - pos['tp']) * contract_size * local_cfg['lot_size']
                    balance += pnl; trades_history.append({'pnl': pnl}); active_position = None
            if active_position and (i - pos['idx']) >= local_cfg['exit_candles_max']:
                pnl = (candle['close'] - pos['entry']) * contract_size * local_cfg['lot_size'] if pos['type'] == 'BUY' else (pos['entry'] - candle['close']) * contract_size * local_cfg['lot_size']
                balance += pnl; trades_history.append({'pnl': pnl}); active_position = None
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
            
            if z['type'] == 'RESISTANCE' and candle['high'] >= z['price'] and rsi >= rsi_ob and trend <= 0:
                entry = candle['close']; sl = candle['high'] + (local_cfg['stop_buffer_points'] * point)
                tp = entry - ((sl - entry) * 1.5)
                active_position = {'type': 'SELL', 'entry': entry, 'sl': sl, 'tp': tp, 'idx': i}
                cooldowns[z_key] = curr_time; break
            
            if z['type'] == 'SUPPORT' and candle['low'] <= z['price'] and rsi <= rsi_os and trend >= 0:
                entry = candle['close']; sl = candle['low'] - (local_cfg['stop_buffer_points'] * point)
                tp = entry + ((entry - sl) * 1.5)
                active_position = {'type': 'BUY', 'entry': entry, 'sl': sl, 'tp': tp, 'idx': i}
                cooldowns[z_key] = curr_time; break
    return balance, len(trades_history)

def run_batch_test():
    print("="*65)
    print(" 🚀 BIG BACKTEST MULTI-PAIR v5.5: RUMO AOS $100/DIA ")
    print(f" Ativos: {', '.join(CFG['symbols'][:5])}...")
    print("="*65)
    
    total_pnl = 0.0
    total_trades = 0
    results = []

    for symbol in CFG['symbols'][:6]: # Testamos os 6 principais para velocidade
        print(f"Analisando {symbol}...", end=" ", flush=True)
        pnl, trades = run_replay_for_symbol(symbol, CFG)
        print(f"✅ PNL: ${pnl:.2f} | Trades: {trades}")
        total_pnl += pnl
        total_trades += trades
        results.append({'symbol': symbol, 'pnl': pnl, 'trades': trades})

    print("\n" + "="*65)
    print(f" 📊 RESULTADO CONSOLIDADO (Aprox. 1.5 meses) ")
    print(f" PNL TOTAL: ${total_pnl:.2f}")
    print(f" TOTAL TRADES: {total_trades}")
    print(f" MÉDIA POR DIA: ${(total_pnl / 33):.2f} (Considerando 33 dias úteis)")
    print("="*65)

    with open("docs/replay_executivo.md", "w") as f:
        f.write(f"# Relatório de Alta Performance Multi-Pair\n\nPNL Total: ${total_pnl:.2f}\nTrades: {total_trades}\nMédia Diária Estimada: ${(total_pnl / 33):.2f}")

if __name__ == "__main__":
    run_batch_test()
