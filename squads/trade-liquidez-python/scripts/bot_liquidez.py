import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
import pytz

import yaml
import os

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

from supabase_client import SupabaseManager
db_manager = SupabaseManager()

# Configurações do Squad (squad.yaml)
SYMBOL = CFG['symbol']
TIMEFRAME_H1 = mt5.TIMEFRAME_H1
TIMEFRAME_M5 = mt5.TIMEFRAME_M5
MAGIC_NUMBER = CFG['magic_number']
LOOKBACK_H1 = CFG['lookback_h1']
MIN_DISPLACEMENT_CANDLES = CFG['min_displacement_candles']
EXIT_CANDLES_MAX = CFG['exit_candles_max']
BREAKEVEN_CANDLES = CFG['breakeven_candles']
ENTRY_RETRACEMENT_PCT = CFG['entry_retracement_pct']
STOP_BUFFER = CFG['stop_buffer_points']
ZONE_MERGE_POINTS = CFG['zone_merge_points']
COOLDOWN_CANDLES = CFG['cooldown_candles']

# Diretório de Files do MT5 para o Indicador
MT5_DATA_PATH = r"C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
INDICATOR_FILE = os.path.join(MT5_DATA_PATH, "MQL5", "Files", "liquidez_data.csv")

def export_dynamic_data(zones, trigger):
    """Exporta as zonas atuais e o sinal pendente para o Indicador MQL5 ler."""
    try:
        with open(INDICATOR_FILE, "w", encoding="utf-8") as f:
            # Header: type, price, time
            f.write("type,price,time\n")
            for z in zones:
                f.write(f"ZONE_{z['type']},{z['price']},{z['time']}\n")
            if trigger:
                type_str = "SIGNAL_SELL" if trigger['type'] == mt5.ORDER_TYPE_SELL_LIMIT else "SIGNAL_BUY"
                f.write(f"{type_str},{trigger['price']},{datetime.now()}\n")
    except Exception as e:
        print(f"Erro ao exportar para o indicador: {e}")

def initialize_mt5():
    """Inicializa a conexão com o MetaTrader 5."""
    if not mt5.initialize():
        print(f"Erro ao inicializar MT5: {mt5.last_error()}")
        return False
    print("MetaTrader 5 inicializado com sucesso.")
    return True

def get_rates(symbol, timeframe, count):
    """Obtém dados históricos de candles."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def get_validated_h1_zones(df_h1, point):
    """Identifica zonas de H1 validadas, executa invalidação e merge."""
    zones = []
    if df_h1 is None or len(df_h1) < MIN_DISPLACEMENT_CANDLES + 1:
        return zones

    raw_zones = []
    for i in range(len(df_h1) - MIN_DISPLACEMENT_CANDLES - 1):
        high, low = df_h1.iloc[i]['high'], df_h1.iloc[i]['low']
        
        is_resistance = True
        for j in range(1, MIN_DISPLACEMENT_CANDLES + 1):
            if df_h1.iloc[i+j]['high'] > high:
                is_resistance = False; break
        if is_resistance: raw_zones.append({'type': 'RESISTANCE', 'price': high, 'time': df_h1.iloc[i]['time'], 'idx': i})

        is_support = True
        for j in range(1, MIN_DISPLACEMENT_CANDLES + 1):
            if df_h1.iloc[i+j]['low'] < low:
                is_support = False; break
        if is_support: raw_zones.append({'type': 'SUPPORT', 'price': low, 'time': df_h1.iloc[i]['time'], 'idx': i})

    valid_zones = []
    for z in raw_zones:
        invalidated = False
        start_check = z['idx'] + MIN_DISPLACEMENT_CANDLES + 1
        for k in range(start_check, len(df_h1)):
            c_close, c_open = df_h1.iloc[k]['close'], df_h1.iloc[k]['open']
            if z['type'] == 'RESISTANCE' and c_close > z['price'] and c_open > z['price']:
                invalidated = True; break
            if z['type'] == 'SUPPORT' and c_close < z['price'] and c_open < z['price']:
                invalidated = True; break
        if not invalidated:
            valid_zones.append({'type': z['type'], 'price': z['price'], 'time': z['time']})

    merged_zones = []
    merge_threshold = ZONE_MERGE_POINTS * point
    for z in valid_zones:
        merged = False
        for mz in merged_zones:
            if mz['type'] == z['type'] and abs(mz['price'] - z['price']) <= merge_threshold:
                if z['type'] == 'RESISTANCE': mz['price'] = max(mz['price'], z['price'])
                else: mz['price'] = min(mz['price'], z['price'])
                merged = True; break
        if not merged: merged_zones.append(z)

    return merged_zones

def calculate_wick_metrics(candle):
    """Calcula tamanho do pavio e corpo em percentual."""
    high = candle['high']
    low = candle['low']
    open_p = candle['open']
    close_p = candle['close']
    total_size = high - low
    if total_size == 0: return 0, 0, 0
    
    body_size = abs(close_p - open_p)
    top_wick = high - max(open_p, close_p)
    bottom_wick = min(open_p, close_p) - low
    
    return total_size, top_wick, bottom_wick

def log_ml_features(trigger, zone, last_candle, prev_candle, total_size, top_wick, bottom_wick):
    """Grava as nuances quantitativas de uma entrada recém descoberta para Treino futuro"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ml_dataset.csv")
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, "a", encoding="utf-8") as f:
        # Header
        if not file_exists:
            f.write("time,magic,direction,body_size,top_wick_pct,bottom_wick_pct,volume_momentum,distance_to_zone\n")
            
        direction = 1 if trigger['type'] == mt5.ORDER_TYPE_BUY_LIMIT else -1
        top_pct = round(top_wick / total_size, 3) if total_size > 0 else 0
        bot_pct = round(bottom_wick / total_size, 3) if total_size > 0 else 0
        vol_momentum = last_candle['tick_volume'] - prev_candle['tick_volume'] # O quanto maior foi
        dist_zone = round(abs(last_candle['close'] - zone['price']), 5)
        
        f.write(f"{last_candle['time']},{MAGIC_NUMBER},{direction},{total_size:.5f},{top_pct},{bot_pct},{vol_momentum},{dist_zone:.5f}\n")

def check_m5_trigger(df_m5, zones_h1, point, cooldowns, current_time):
    """Monitora anatomia, volume, violinação e cooldown."""
    if df_m5 is None or len(df_m5) < 2 or not zones_h1: return None, None

    last_candle = df_m5.iloc[-2] # Candle fechado
    prev_candle = df_m5.iloc[-3]
    
    total_size, top_wick, bottom_wick = calculate_wick_metrics(last_candle)
    if total_size == 0: return None, None
    if last_candle['tick_volume'] <= prev_candle['tick_volume']: return None, None

    last_is_bull = last_candle['close'] > last_candle['open']
    prev_is_bull = prev_candle['close'] > prev_candle['open']
    if last_is_bull == prev_is_bull: return None, None

    for zone in zones_h1:
        price_zone = zone['price']
        z_key = f"{zone['type']}_{round(price_zone, 5)}"
        
        if z_key in cooldowns and current_time - cooldowns[z_key] < timedelta(minutes=5 * COOLDOWN_CANDLES):
            continue
        
        if zone['type'] == 'RESISTANCE':
            if last_candle['high'] >= price_zone:
                wick_pct = top_wick / total_size
                if 0.30 <= wick_pct <= 0.70:
                    entry_price = last_candle['high'] - (top_wick * ENTRY_RETRACEMENT_PCT)
                    stop_loss = last_candle['high'] + (STOP_BUFFER * point)
                    take_profit = prev_candle['low'] 
                    trigger = {
                        'type': mt5.ORDER_TYPE_SELL_LIMIT, 'price': entry_price,
                        'sl': stop_loss, 'tp': take_profit, 'comment': "Liquidez Resistência"
                    }
                    log_ml_features(trigger, zone, last_candle, prev_candle, total_size, top_wick, bottom_wick)
                    db_manager.log_signal(trigger, wick_pct)
                    return trigger, zone

        elif zone['type'] == 'SUPPORT':
            if last_candle['low'] <= price_zone:
                wick_pct = bottom_wick / total_size
                if 0.30 <= wick_pct <= 0.70:
                    entry_price = last_candle['low'] + (bottom_wick * ENTRY_RETRACEMENT_PCT)
                    stop_loss = last_candle['low'] - (STOP_BUFFER * point)
                    take_profit = prev_candle['high']
                    trigger = {
                        'type': mt5.ORDER_TYPE_BUY_LIMIT, 'price': entry_price,
                        'sl': stop_loss, 'tp': take_profit, 'comment': "Liquidez Suporte"
                    }
                    log_ml_features(trigger, zone, last_candle, prev_candle, total_size, top_wick, bottom_wick)
                    db_manager.log_signal(trigger, wick_pct)
                    return trigger, zone
                    
    return None, None

def send_limit_order(order_data):
    """
    Task: Envio de Ordem Limitada (send-order-limit)
    """
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": SYMBOL,
        "volume": 1.0, # Lote padrão (ajustar conforme risco)
        "type": order_data['type'],
        "price": order_data['price'],
        "sl": order_data['sl'],
        "tp": order_data['tp'],
        "magic": MAGIC_NUMBER,
        "comment": order_data['comment'],
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Erro ao enviar ordem: {result.comment} ({result.retcode})")
    else:
        print(f"Ordem {order_data['comment']} enviada: {order_data['price']}")
    return result

def manage_active_trades():
    """
    Monitoramento Misto: Saída por tempo (6 candles) + Breakeven (3 candles).
    """
    positions = mt5.positions_get(magic=MAGIC_NUMBER)
    if positions:
        for pos in positions:
            time_open = datetime.fromtimestamp(pos.time, tz=pytz.utc)
            now = datetime.now(pytz.utc)
            duration_minutes = (now - time_open).total_seconds() / 60
            
            # 6 candles M5 = Saída por Tempo Final
            if duration_minutes >= (EXIT_CANDLES_MAX * 5):
                print(f"Expirando posição {pos.ticket} por tempo (6 candles).")
                close_request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": pos.symbol,
                    "volume": pos.volume,
                    "type": mt5.ORDER_TYPE_BUY if pos.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL,
                    "position": pos.ticket,
                    "magic": MAGIC_NUMBER,
                    "comment": "Saída Temporal 6-Candles",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_RETURN,
                }
                mt5.order_send(close_request)
                continue
                
            # 3 candles = Breakeven
            if duration_minutes >= (BREAKEVEN_CANDLES * 5):
                point = mt5.symbol_info(pos.symbol).point
                spread_safety = 10 * point
                new_sl = None

                if pos.type == mt5.ORDER_TYPE_BUY and pos.price_current > pos.price_open:
                    if pos.sl < pos.price_open: # Se não moveu pro zero a zero
                        new_sl = pos.price_open + spread_safety
                elif pos.type == mt5.ORDER_TYPE_SELL and pos.price_current < pos.price_open:
                    if pos.sl > pos.price_open or pos.sl == 0:
                        new_sl = pos.price_open - spread_safety
                        
                if new_sl is not None:
                    print(f"Acionando Breakeven para posição {pos.ticket}. Movendo SL para {new_sl}")
                    sl_request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": pos.ticket,
                        "symbol": pos.symbol,
                        "sl": new_sl,
                        "tp": pos.tp,
                        "magic": MAGIC_NUMBER
                    }
                    mt5.order_send(sl_request)

def main():
    if not initialize_mt5():
        return

    print(f"Monitorando {SYMBOL} em M5 com contexto H1...")
    
    try:
        cooldowns = {}
        while True:
            # Ponto de Cálculo e Offset dinâmico
            point = mt5.symbol_info(SYMBOL).point
            last_price = mt5.symbol_info_tick(SYMBOL).bid
            now_utc = datetime.now(pytz.utc)
            
            # Limpa Terminal e Mostra Dashboard
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*60)
            print(f" SQUAD LIQUIDEZ: DASHBOARD OPERACIONAL | {now_utc.strftime('%H:%M:%S')} ")
            print(f" DASHBOARD CLOUD: http://localhost:3000 ")
            print("="*60)
            print(f" ATIVO: {SYMBOL} | PRECO: {last_price:.5f} ")
            
            # 1. Validação de Contexto H1
            df_h1 = get_rates(SYMBOL, TIMEFRAME_H1, LOOKBACK_H1)
            zones_h1 = get_validated_h1_zones(df_h1, point)
            
            print(f" ZONAS H1 ATIVAS: {len(zones_h1)}")
            
            # 2. Detecção de Gatilho M5
            df_m5 = get_rates(SYMBOL, TIMEFRAME_M5, 10)
            trigger, z_triggered = check_m5_trigger(df_m5, zones_h1, point, cooldowns, now_utc)
            
            if trigger:
                if not mt5.orders_get(magic=MAGIC_NUMBER) and not mt5.positions_get(magic=MAGIC_NUMBER):
                    send_limit_order(trigger)
                    z_key = f"{z_triggered['type']}_{round(z_triggered['price'], 5)}"
                    cooldowns[z_key] = now_utc

            # 3. Cloud Sync & Heartbeat
            db_manager.log_heartbeat(SYMBOL, "scanning", len(zones_h1))
            export_dynamic_data(zones_h1, trigger)
            
            # 4. Gestões Livres
            manage_active_trades()
            
            print("="*60)
            print(" AGUARDANDO PROXIMO SCAN (60s)... ")
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("Robô encerrado pelo usuário.")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    main()
