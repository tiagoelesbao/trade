import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
import pytz
import sys
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
        with open(INDICATOR_FILE, "w", encoding="ansi") as f:
            f.write("HEADER\n") 
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
        if not invalidated: valid_zones.append({'type': z['type'], 'price': z['price'], 'time': z['time']})
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
    high, low, open_p, close_p = candle['high'], candle['low'], candle['open'], candle['close']
    total_size = high - low
    if total_size == 0: return 0, 0, 0
    top_wick = high - max(open_p, close_p)
    bottom_wick = min(open_p, close_p) - low
    return total_size, top_wick, bottom_wick

def log_ml_features(trigger, zone, last_candle, prev_candle, total_size, top_wick, bottom_wick):
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ml_dataset.csv")
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("time,magic,direction,body_size,top_wick_pct,bottom_wick_pct,volume_momentum,distance_to_zone\n")
        direction = 1 if trigger['type'] == mt5.ORDER_TYPE_BUY_LIMIT else -1
        top_pct = round(top_wick / total_size, 3) if total_size > 0 else 0
        bot_pct = round(bottom_wick / total_size, 3) if total_size > 0 else 0
        vol_momentum = last_candle['tick_volume'] - prev_candle['tick_volume']
        dist_zone = round(abs(last_candle['close'] - zone['price']), 5)
        f.write(f"{last_candle['time']},{MAGIC_NUMBER},{direction},{total_size:.5f},{top_pct},{bot_pct},{vol_momentum},{dist_zone:.5f}\n")

def check_m5_trigger(df_m5, zones_h1, point, cooldowns, current_time):
    if df_m5 is None or len(df_m5) < 2 or not zones_h1: return None, None
    last_candle = df_m5.iloc[-2]
    prev_candle = df_m5.iloc[-3]
    total_size, top_wick, bottom_wick = calculate_wick_metrics(last_candle)
    if total_size == 0: return None, None
    if CFG.get('require_volume_momentum', True):
        if last_candle['tick_volume'] <= prev_candle['tick_volume']: return None, None
    if CFG.get('require_color_reversal', True):
        last_is_bull = last_candle['close'] > last_candle['open']
        prev_is_bull = prev_candle['close'] > prev_candle['open']
        if last_is_bull == prev_is_bull: return None, None
    min_wick, max_wick = CFG.get('min_wick_pct', 0.30), CFG.get('max_wick_pct', 0.70)
    for zone in zones_h1:
        price_zone = zone['price']
        z_key = f"{zone['type']}_{round(price_zone, 5)}"
        if z_key in cooldowns and current_time - cooldowns[z_key] < timedelta(minutes=5 * COOLDOWN_CANDLES):
            continue
        if zone['type'] == 'RESISTANCE' and last_candle['high'] >= price_zone:
            wick_pct = top_wick / total_size
            if min_wick <= wick_pct <= max_wick:
                entry_price = last_candle['high'] - (top_wick * ENTRY_RETRACEMENT_PCT)
                trigger = {'type': mt5.ORDER_TYPE_SELL_LIMIT, 'price': entry_price, 'sl': last_candle['high'] + (STOP_BUFFER * point), 'tp': prev_candle['low'], 'comment': "Liquidez Resistencia"}
                log_ml_features(trigger, zone, last_candle, prev_candle, total_size, top_wick, bottom_wick)
                return trigger, zone
        elif zone['type'] == 'SUPPORT' and last_candle['low'] <= price_zone:
            wick_pct = bottom_wick / total_size
            if min_wick <= wick_pct <= max_wick:
                entry_price = last_candle['low'] + (bottom_wick * ENTRY_RETRACEMENT_PCT)
                trigger = {'type': mt5.ORDER_TYPE_BUY_LIMIT, 'price': entry_price, 'sl': last_candle['low'] - (STOP_BUFFER * point), 'tp': prev_candle['high'], 'comment': "Liquidez Suporte"}
                log_ml_features(trigger, zone, last_candle, prev_candle, total_size, top_wick, bottom_wick)
                return trigger, zone
    return None, None

def send_order(order_data):
    mode = CFG.get('execution_mode', 'limit').lower()
    
    if mode == 'market':
        tick = mt5.symbol_info_tick(SYMBOL)
        price = tick.bid if order_data['type'] == mt5.ORDER_TYPE_SELL_LIMIT else tick.ask
        order_type = mt5.ORDER_TYPE_SELL if order_data['type'] == mt5.ORDER_TYPE_SELL_LIMIT else mt5.ORDER_TYPE_BUY
        action = mt5.TRADE_ACTION_DEAL
    else:
        price = order_data['price']
        order_type = order_data['type']
        action = mt5.TRADE_ACTION_PENDING

    # Lista de modos de preenchimento para tentar (FOK é o mais comum em contas Hedge/Demo)
    filling_modes = [mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN]
    
    for f_mode in filling_modes:
        request = {
            "action": action, 
            "symbol": SYMBOL, 
            "volume": CFG.get('lot_size', 1.0),
            "type": order_type, 
            "price": price, 
            "sl": order_data['sl'], 
            "tp": order_data['tp'],
            "magic": MAGIC_NUMBER, 
            "comment": order_data['comment'], 
            "type_time": mt5.ORDER_TIME_GTC, 
            "type_filling": f_mode,
        }
        
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Ordem {mode.upper()} enviada com sucesso (Mode: {f_mode})")
            return result
        elif result.retcode == 10030: # Unsupported filling mode
            continue # Tenta o próximo modo
        else:
            print(f"Erro ao enviar ordem: {result.comment} ({result.retcode})")
            return result
            
    return result

def get_daily_pnl():
    from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    to_date = datetime.now()
    deals = mt5.history_deals_get(from_date, to_date, group=f"*{SYMBOL}*")
    if deals is None: return 0.0
    daily_pnl = 0.0
    for deal in deals:
        if deal.magic == MAGIC_NUMBER:
            daily_pnl += (deal.profit + deal.commission + deal.swap)
    return daily_pnl

def check_session_limits(current_pnl):
    target = CFG.get('daily_profit_target', 100.0)
    max_loss = CFG.get('daily_max_loss', 50.0)
    if current_pnl >= target:
        print(f"\n[META BATIDA] Lucro: ${current_pnl:.2f} (Alvo: ${target:.2f})")
        return True, "target_hit"
    if current_pnl <= -max_loss:
        print(f"\n[STOP DIARIO] Perda: ${current_pnl:.2f} (Limite: -${max_loss:.2f})")
        return True, "stop_hit"
    return False, "running"

def wait_for_agent_consensus(signal_id):
    """Aguarda os agentes, mas se houver timeout, APROVA AUTOMATICAMENTE (Fallback)."""
    timeout = CFG.get('consensus_timeout_secs', 30)
    start_time = time.time()
    print(f"[CONSENSO] Solicitando aval da IA para sinal {signal_id}...")
    while (time.time() - start_time) < timeout:
        try:
            res = db_manager.client.table("signals_liquidez").select("status").eq("id", signal_id).execute()
            if res.data:
                status = res.data[0]['status']
                if status == 'approved':
                    print(f"✅ CONSENSO OBTIDO: IA confirmou a entrada.")
                    return True
                if status == 'rejected':
                    print(f"❌ VETO: IA negou, mas seguiremos o Fallback de Aprovação Total.")
                    return True # Forçamos True conforme pedido
        except: pass
        time.sleep(1)
    print(f"🚀 FALLBACK: Agentes silentes. Executando trade por autonomia direta!")
    try: db_manager.client.table("signals_liquidez").update({"status": "approved"}).eq("id", signal_id).execute()
    except: pass
    return True

def manage_active_trades(signal_id=None):
    positions = mt5.positions_get(magic=MAGIC_NUMBER)
    if positions:
        for pos in positions:
            if signal_id: db_manager.update_signal_status(signal_id, "active")
            duration_minutes = (datetime.now(pytz.utc) - datetime.fromtimestamp(pos.time, tz=pytz.utc)).total_seconds() / 60
            if duration_minutes >= (EXIT_CANDLES_MAX * 5):
                mt5.order_send({"action": mt5.TRADE_ACTION_DEAL, "symbol": pos.symbol, "volume": pos.volume, "type": mt5.ORDER_TYPE_BUY if pos.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL, "position": pos.ticket, "magic": MAGIC_NUMBER, "comment": "Saida Temporal", "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_RETURN})
            elif duration_minutes >= (BREAKEVEN_CANDLES * 5):
                point = mt5.symbol_info(pos.symbol).point
                new_sl = None
                if pos.type == mt5.ORDER_TYPE_BUY and pos.price_current > pos.price_open and pos.sl < pos.price_open: new_sl = pos.price_open + (10 * point)
                elif pos.type == mt5.ORDER_TYPE_SELL and pos.price_current < pos.price_open and (pos.sl > pos.price_open or pos.sl == 0): new_sl = pos.price_open - (10 * point)
                if new_sl: mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": new_sl, "tp": pos.tp, "magic": MAGIC_NUMBER})
    elif signal_id:
        # Se não há posições ativas, mas temos um signal_id, verificamos o histórico de forma ampla
        # Usamos uma janela de tempo agressiva para cobrir fuso horários diferentes (Broker vs Local)
        from_date = datetime.now() - timedelta(days=2)
        to_date = datetime.now() + timedelta(days=2)
        deals = mt5.history_deals_get(from_date, to_date)
        if deals:
            # Filtra apenas deals que fecharam posições (entry out) deste robô
            relevant_deals = [d for d in deals if d.magic == MAGIC_NUMBER and d.entry == 1]
            if relevant_deals:
                last_deal = relevant_deals[-1]
                pnl_final = last_deal.profit + last_deal.commission + last_deal.swap
                print(f"💰 Operação Detectada no Histórico! PNL: ${pnl_final:.2f} | Sinal: {signal_id}")
                db_manager.update_signal_pnl(signal_id, pnl_final)
                return True 
    return False

def main():
    if not initialize_mt5(): return
    mode = CFG.get('execution_mode', 'limit').upper()
    
    # Captura o lucro acumulado no momento do start para calcular o P&L da sessão
    initial_pnl = get_daily_pnl()
    
    print(f"Monitorando {SYMBOL} | Modo: OFENSIVO | Execução: {mode}")
    try:
        cooldowns = {}
        last_signal_time = 0
        active_trigger = None
        current_signal_id = None
        
        while True:
            point = mt5.symbol_info(SYMBOL).point
            now_utc = datetime.now(pytz.utc)
            
            # P&L da Sessão = Lucro Atual - Lucro no Momento do Start
            total_daily_pnl = get_daily_pnl()
            session_pnl = total_daily_pnl - initial_pnl
            
            stop_needed, status_str = check_session_limits(session_pnl)
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*60)
            print(f" SQUAD LIQUIDEZ | {now_utc.strftime('%H:%M:%S')} | P&L SESSÃO: ${session_pnl:.2f} | STATUS: {status_str.upper()}")
            print(f" MODO DE EXECUÇÃO: {mode}")
            print("="*60)
            
            if stop_needed and CFG.get('stop_after_target', True):
                db_manager.log_heartbeat(SYMBOL, status_str, 0)
                break

            df_h1 = get_rates(SYMBOL, TIMEFRAME_H1, LOOKBACK_H1)
            zones_h1 = get_validated_h1_zones(df_h1, point)
            df_m5 = get_rates(SYMBOL, TIMEFRAME_M5, 10)
            trigger, z_triggered = check_m5_trigger(df_m5, zones_h1, point, cooldowns, now_utc)
            
            if trigger and not mt5.orders_get(magic=MAGIC_NUMBER) and not mt5.positions_get(magic=MAGIC_NUMBER):
                active_trigger = trigger
                last_signal_time = time.time()
                
                # Registra sinal inicial e captura o ID
                total, top, bot = calculate_wick_metrics(df_m5.iloc[-2])
                wick_pct = top/total if trigger['type'] == mt5.ORDER_TYPE_SELL_LIMIT else bot/total
                
                initial_status = "awaiting_consensus" if CFG.get('use_agent_consensus', False) else "approved"
                res = db_manager.log_signal(trigger, wick_pct, status=initial_status)
                current_signal_id = res.data[0]['id'] if res and res.data else None
                
                if CFG.get('use_agent_consensus', False):
                    if current_signal_id and wait_for_agent_consensus(current_signal_id):
                        result = send_order(trigger)
                        if result.retcode == mt5.TRADE_RETCODE_DONE:
                            db_manager.update_signal_status(current_signal_id, "placed" if mode == 'LIMIT' else "active")
                        else:
                            db_manager.update_signal_status(current_signal_id, "failed")
                            print(f"⚠️ Ordem recusada pelo MT5: {result.comment}")
                else:
                    result = send_order(trigger)
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        if current_signal_id: db_manager.update_signal_status(current_signal_id, "placed" if mode == 'LIMIT' else "active")
                    else:
                        if current_signal_id: db_manager.update_signal_status(current_signal_id, "failed")
                        print(f"⚠️ Ordem recusada pelo MT5: {result.comment}")
                
                cooldowns[f"{z_triggered['type']}_{round(z_triggered['price'], 5)}"] = now_utc

            # Mantem a seta no MT5 por 15 minutos (900s) para visibilidade garantida
            if active_trigger and (time.time() - last_signal_time) > 900:
                active_trigger = None

            db_manager.log_heartbeat(SYMBOL, "scanning", len(zones_h1))
            export_dynamic_data(zones_h1, active_trigger)
            
            if manage_active_trades(current_signal_id):
                current_signal_id = None # Reset para o próximo sinal
                
            time.sleep(60)
    except KeyboardInterrupt: pass
    finally: mt5.shutdown()

if __name__ == "__main__":
    main()
