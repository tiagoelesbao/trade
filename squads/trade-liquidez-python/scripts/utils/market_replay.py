import os
import sys
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yaml
import random

# Carregar Config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

sys.path.append(os.path.dirname(__file__))
import bot_liquidez

def run_replay_for_symbol(symbol, local_cfg):
    if not mt5.initialize(): return 0, []

    # 1. DOWNLOAD DE DADOS
    m5_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 15000)
    m15_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 5000)
    h1_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 1500)
    
    if m5_rates is None or h1_rates is None or m15_rates is None: 
        mt5.shutdown(); return 0, []
    
    s_info = mt5.symbol_info(symbol)
    point = s_info.point
    pip_size = point * 10
    pip_val = 10.0 if "JPY" not in symbol else 7.5
    
    # TAXAS ZERADAS conforme solicitado (Fidelidade ao lucro bruto)
    fixed_cost = 0.0
    mt5.shutdown()

    df_m5 = pd.DataFrame(m5_rates); df_m5['time'] = pd.to_datetime(df_m5['time'], unit='s', utc=True)
    df_m15 = pd.DataFrame(m15_rates); df_m15['time'] = pd.to_datetime(df_m15['time'], unit='s', utc=True)
    df_h1 = pd.DataFrame(h1_rates); df_h1['time'] = pd.to_datetime(df_h1['time'], unit='s', utc=True)

    df_m15['rsi'] = bot_liquidez.calculate_rsi(df_m15['close'])
    df_h1['sma20'] = df_h1['close'].rolling(20).mean()
    
    # Gera todas as zonas possíveis do período
    all_raw_zones = bot_liquidez.get_validated_zones(df_m15, point)

    balance, history, consumed_zones = 0.0, [], set()
    session_trade_log = [] 

    # LOOP M15 (DETERMINA AS ENTRADAS)
    for i in range(50, len(df_m15) - 2):
        candle = df_m15.iloc[i]
        prev_candle = df_m15.iloc[i-1]
        curr_t = candle['time']
        
        # 1. Slope Guard H1
        h1_avail = df_h1[df_h1['time'] < curr_t]
        if len(h1_avail) < 21: continue
        sma = h1_avail['sma20']
        slope = (sma.iloc[-1] - sma.iloc[-2]) / pip_size
        
        # 2. Kill-Zone Proximidade (10 pips / 4h)
        is_blocked = False
        for pt in session_trade_log:
            if abs(candle['close'] - pt['price']) <= (10 * pip_size):
                if curr_t - pt['time'] < timedelta(hours=4):
                    is_blocked = True; break
        if is_blocked: continue

        # 3. Lógica de Gatilho v5.9.4
        rsi = candle['rsi']
        total, top, bot = bot_liquidez.calculate_wick_metrics(candle)
        
        # Reversão de Cor Obrigatória
        is_reversal = (candle['close'] > candle['open'] and prev_candle['close'] < prev_candle['open']) or \
                      (candle['close'] < candle['open'] and prev_candle['close'] > prev_candle['open'])
        
        # Filtro de Memória: Apenas as últimas 100 zonas (Igual ao Bot)
        # E apenas zonas confirmadas (delay de 7 candles)
        zones_confirmed = [z for z in all_raw_zones if z['time'] < (curr_t - timedelta(minutes=105))]
        zones_in_memory = zones_confirmed[-100:] # Lookback de 100 zonas
        
        entry_type = None
        z_trig = None
        for z in zones_in_memory:
            z_key = f"{symbol}_{z['type']}_{round(z['price'], 5)}"
            if z_key in consumed_zones: continue
            
            if z['type'] == 'RESISTANCE' and candle['high'] >= z['price'] and (top/total) >= 0.3 and rsi >= 60 and slope <= 0 and is_reversal:
                entry_type = 'SELL'; z_trig = z; break
            elif z['type'] == 'SUPPORT' and candle['low'] <= z['price'] and (bot/total) >= 0.3 and rsi <= 40 and slope >= 0 and is_reversal:
                entry_type = 'BUY'; z_trig = z; break
        
        if entry_type:
            # SIMULAÇÃO DE EXECUÇÃO
            entry_price = candle['close']
            if entry_type == 'SELL':
                sl = candle['high'] + (local_cfg['stop_buffer_points'] * point)
                tp = entry_price - (abs(sl - entry_price) * 1.5)
            else:
                sl = candle['low'] - (local_cfg['stop_buffer_points'] * point)
                tp = entry_price + (abs(entry_price - sl) * 1.5)

            # Busca no M5 o desfecho real
            trade_df_m5 = df_m5[df_m5['time'] > curr_t].head(16) # Máximo 80 min de trade
            pnl_pips = 0; hit = False
            exit_p = entry_price; exit_t = curr_t

            for _, m5 in trade_df_m5.iterrows():
                if entry_type == 'SELL':
                    if m5['high'] >= sl: pnl_pips = (entry_price - sl) / pip_size; exit_p, exit_t, hit = sl, m5['time'], True; break
                    if m5['low'] <= tp: pnl_pips = (entry_price - tp) / pip_size; exit_p, exit_t, hit = tp, m5['time'], True; break
                else:
                    if m5['low'] <= sl: pnl_pips = (sl - entry_price) / pip_size; exit_p, exit_t, hit = sl, m5['time'], True; break
                    if m5['high'] >= tp: pnl_pips = (tp - entry_price) / pip_size; exit_p, exit_t, hit = tp, m5['time'], True; break
            
            if not hit and len(trade_df_m5) > 0:
                exit_p = trade_df_m5.iloc[-1]['close']
                exit_t = trade_df_m5.iloc[-1]['time']
                pnl_pips = (entry_price - exit_p) / pip_size if entry_type == 'SELL' else (exit_p - entry_price) / pip_size

            pnl_usd = (pnl_pips * pip_val) # Sem taxas conforme pedido
            balance += pnl_usd
            history.append({
                'time': curr_t, 'type': entry_type, 'pnl': pnl_usd, 'rsi': rsi, 
                'entry': entry_price, 'exit_p': exit_p, 'exit_t': exit_t, 'z_price': z_trig['price'], 'trend': slope
            })
            consumed_zones.add(f"{symbol}_{z_trig['type']}_{round(z_trig['price'], 5)}")
            session_trade_log.append({'price': entry_price, 'time': curr_t})

    # Exporta para Auditoria Visual
    if mt5.initialize():
        mt5_path = mt5.terminal_info()._asdict().get('data_path')
        audit_file = os.path.join(mt5_path, "MQL5", "Files", f"audit_backtest_{symbol}.csv")
        try:
            with open(audit_file, "w", encoding="ansi") as f:
                f.write("type,price,time,pnl,z_price,rsi,trend,exit_p,exit_t\n")
                for t in history:
                    t_type = "SIGNAL_BUY" if t['type'] == 'BUY' else "SIGNAL_SELL"
                    f.write(f"{t_type},{t['entry']},{t['time'].strftime('%Y.%m.%d %H:%M')},{t['pnl']:.2f},{t['z_price']},{t['rsi']:.1f},{t['trend']:.2f},{t['exit_p']},{t['exit_t'].strftime('%Y.%m.%d %H:%M')}\n")
        except: pass

    return balance, history

def run():
    print("="*65)
    print(" 🚨 MOTOR v6.1 FIDELIDADE TOTAL (SEM TAXAS / LOGICA BOT) ")
    print("="*65)
    all_res = []
    for s in CFG['symbols']:
        print(f"Analisando {s}...", end=" ", flush=True)
        pnl, hist = run_replay_for_symbol(s, CFG)
        print(f"✅ ${pnl:.2f} ({len(hist)} trades)")
        all_res.append({'symbol': s, 'pnl': pnl, 'history': hist})
    
    total_pnl = sum([r['pnl'] for r in all_res])
    print(f"\n✨ LUCRO BRUTO TOTAL: ${total_pnl:.2f}")

if __name__ == "__main__":
    run()
