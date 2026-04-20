import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
import pytz
import sys
import yaml
import os

# Carrega Configurações
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

from supabase_client import SupabaseManager
db_manager = SupabaseManager()

# Mapeamento de Timeframes
TF_MAP = {"H1": mt5.TIMEFRAME_H1, "M30": mt5.TIMEFRAME_M30, "M15": mt5.TIMEFRAME_M15, "M5": mt5.TIMEFRAME_M5}

# Configurações Globais
SYMBOLS = CFG.get('symbols', ["EURUSD"])
TIMEFRAME_ZONES = TF_MAP.get(CFG.get('zone_timeframe', 'M15'), mt5.TIMEFRAME_M15)
TIMEFRAME_M5 = mt5.TIMEFRAME_M5
MAGIC_NUMBER = CFG['magic_number']
LOOKBACK_ZONES = CFG.get('lookback_zones', 100)
MIN_DISPLACEMENT_CANDLES = CFG['min_displacement_candles']
EXIT_CANDLES_MAX = CFG['exit_candles_max']
BREAKEVEN_CANDLES = CFG['breakeven_candles']
ENTRY_RETRACEMENT_PCT = CFG['entry_retracement_pct']
STOP_BUFFER = CFG['stop_buffer_points']
COOLDOWN_CANDLES = CFG['cooldown_candles']

# Diretório de Files do MT5 para o Indicador
MT5_DATA_PATH = r"C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"

def initialize_mt5():
    if not mt5.initialize():
        print(f"Erro ao inicializar MT5: {mt5.last_error()}")
        return False
    return True

def sync_with_mt5_history(session_start):
    if not db_manager.client: return
    from_d = datetime.now() - timedelta(days=1)
    to_d = datetime.now() + timedelta(days=1)
    deals = mt5.history_deals_get(from_d, to_d)
    if not deals: return
    for d in deals:
        if d.magic != MAGIC_NUMBER or d.entry != 1: continue 
        in_deals = mt5.history_deals_get(position=d.position_id)
        if not in_deals: continue
        entry_time = datetime.fromtimestamp(in_deals[0].time).isoformat()
        check = db_manager.client.table("signals_liquidez").select("id, status").eq("symbol", d.symbol).eq("created_at", entry_time).execute()
        if not check.data:
            new_trade = {
                "symbol": d.symbol, "type": "BUY" if in_deals[0].type == 0 else "SELL",
                "price": in_deals[0].price, "status": "closed", "pnl": d.profit + d.commission + d.swap,
                "magic": MAGIC_NUMBER, "wick_pct": 0.5, "created_at": entry_time, "closed_at": datetime.fromtimestamp(d.time).isoformat()
            }
            db_manager.client.table("signals_liquidez").insert(new_trade).execute()
        elif check.data[0]['status'] != 'closed':
            db_manager.update_signal_pnl(check.data[0]['id'], d.profit + d.commission + d.swap)

def get_daily_pnl():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    deals = mt5.history_deals_get(today, datetime.now() + timedelta(days=1))
    if not deals: return 0.0
    return sum([d.profit + d.commission + d.swap for d in deals if d.magic == MAGIC_NUMBER])

def get_account_pnl():
    deals = mt5.history_deals_get(datetime(2020, 1, 1), datetime.now() + timedelta(days=1))
    if not deals: return 0.0
    return sum([d.profit + d.commission + d.swap for d in deals if d.magic == MAGIC_NUMBER])

def get_rates(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0: return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def get_validated_zones(df_zones, point):
    zones = []
    if df_zones is None or len(df_zones) < MIN_DISPLACEMENT_CANDLES + 1: return zones
    for i in range(len(df_zones) - MIN_DISPLACEMENT_CANDLES - 1):
        high, low = df_zones.iloc[i]['high'], df_zones.iloc[i]['low']
        if all(df_zones.iloc[i+j]['high'] < high for j in range(1, MIN_DISPLACEMENT_CANDLES + 1)):
            zones.append({'type': 'RESISTANCE', 'price': high, 'time': df_zones.iloc[i]['time']})
        if all(df_zones.iloc[i+j]['low'] > low for j in range(1, MIN_DISPLACEMENT_CANDLES + 1)):
            zones.append({'type': 'SUPPORT', 'price': low, 'time': df_zones.iloc[i]['time']})
    return zones

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_trigger(symbol, df_m5, zones, point, cooldowns, now_utc, df_h1=None):
    if df_m5 is None or len(df_m5) < 15 or not zones: return None, None
    last = df_m5.iloc[-2]; rsi = calculate_rsi(df_m5['close']).iloc[-2]
    trend = 0
    if df_h1 is not None and len(df_h1) >= 20:
        sma = df_h1['close'].rolling(20).mean().iloc[-1]
        trend = 1 if df_h1['close'].iloc[-1] > sma else -1
    total = last['high'] - last['low']
    if total == 0: total = 0.0001
    top = last['high'] - max(last['open'], last['close'])
    bot = min(last['open'], last['close']) - last['low']
    
    for z in zones:
        z_key = f"{symbol}_{z['type']}_{round(z['price'], 5)}"
        if z_key in cooldowns and now_utc - cooldowns[z_key] < timedelta(hours=1): continue
        if z['type'] == 'RESISTANCE' and last['high'] >= z['price'] and (top/total) >= 0.3 and rsi >= 60 and trend <= 0:
            return {'symbol': symbol, 'type': mt5.ORDER_TYPE_SELL_LIMIT, 'price': last['close'], 'sl': last['high'] + (STOP_BUFFER * point), 'tp': last['close'] - (abs(last['high']-last['close'])*1.5), 'comment': f"LIQ-{symbol}-S"}, z
        elif z['type'] == 'SUPPORT' and last['low'] <= z['price'] and (bot/total) >= 0.3 and rsi <= 40 and trend >= 0:
            return {'symbol': symbol, 'type': mt5.ORDER_TYPE_BUY_LIMIT, 'price': last['close'], 'sl': last['low'] - (STOP_BUFFER * point), 'tp': last['close'] + (abs(last['low']-last['close'])*1.5), 'comment': f"LIQ-{symbol}-B"}, z
    return None, None

def send_order(symbol, order_data):
    tick = mt5.symbol_info_tick(symbol)
    price = tick.bid if order_data['type'] == mt5.ORDER_TYPE_SELL_LIMIT else tick.ask
    order_type = mt5.ORDER_TYPE_SELL if order_data['type'] == mt5.ORDER_TYPE_SELL_LIMIT else mt5.ORDER_TYPE_BUY
    request = {
        "action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": CFG.get('lot_size', 1.0),
        "type": order_type, "price": price, "sl": order_data['sl'], "tp": order_data['tp'],
        "magic": MAGIC_NUMBER, "comment": order_data['comment'], "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_FOK
    }
    return mt5.order_send(request)

def main():
    if not initialize_mt5(): return
    SESSION_START = datetime.now()
    cooldowns = {}
    print(f"🚀 MOTOR v5.6.2 (SOURCE OF TRUTH): {len(SYMBOLS)} ATIVOS")
    try:
        while True:
            sync_with_mt5_history(SESSION_START)
            pnl_today = get_daily_pnl()
            pnl_total = get_account_pnl()
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*65)
            print(f" SQUAD LIQUIDEZ | {datetime.now().strftime('%H:%M:%S')}")
            print(f" LUCRO HOJE (MT5):  ${pnl_today:.2f}")
            print(f" LUCRO TOTAL CONTA: ${pnl_total:.2f}")
            print("="*65)

            # REPORTA MÉTRICAS REAIS (As colunas pnl_today e pnl_total ja existem no Supabase)
            db_manager.log_heartbeat("GLOBAL", "running", len(SYMBOLS), pnl_today, pnl_total)

            if pnl_today >= CFG.get('daily_profit_target', 100.0):
                print("🏆 META DIÁRIA BATIDA!"); break

            for symbol in SYMBOLS:
                point = mt5.symbol_info(symbol).point
                df_zones = get_rates(symbol, TIMEFRAME_ZONES, LOOKBACK_ZONES)
                zones = get_validated_zones(df_zones, point)
                df_m5 = get_rates(symbol, mt5.TIMEFRAME_M5, 100)
                df_h1 = get_rates(symbol, mt5.TIMEFRAME_H1, 50)
                
                trigger, z_trig = check_trigger(symbol, df_m5, zones, point, cooldowns, datetime.now(pytz.utc), df_h1)
                
                pos = mt5.positions_get(symbol=symbol, magic=MAGIC_NUMBER)
                if trigger and not pos and not mt5.orders_get(symbol=symbol, magic=MAGIC_NUMBER):
                    res = db_manager.log_signal(trigger, 0.5, status="approved")
                    if res and res.data:
                        exec_res = send_order(symbol, trigger)
                        if exec_res.retcode == mt5.TRADE_RETCODE_DONE:
                            cooldowns[f"{symbol}_{z_trig['type']}_{round(z_trig['price'], 5)}"] = datetime.now(pytz.utc)

                # Exportação visual individual
                file_path = os.path.join(MT5_DATA_PATH, "MQL5", "Files", f"liquidez_data_{symbol}.csv")
                try:
                    with open(file_path, "w", encoding="ansi") as f:
                        f.write("HEADER\n") 
                        for z in zones: f.write(f"ZONE_{z['type']},{z['price']},{z['time']}\n")
                        if trigger: f.write(f"SIGNAL_{'SELL' if trigger['type']==mt5.ORDER_TYPE_SELL_LIMIT else 'BUY'},{trigger['price']},{datetime.now()}\n")
                except: pass
            
            time.sleep(20)
    finally: mt5.shutdown()

if __name__ == "__main__":
    main()
