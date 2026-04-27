import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
import pytz
import sys
import yaml
import os
import random
import json

# Carrega Configurações
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

from supabase_client import SupabaseManager
db_manager = SupabaseManager()

# Configurações Globais
MAGIC_NUMBER = CFG['magic_number']
STOP_BUFFER = CFG['stop_buffer_points']
COOLDOWN_HOURS = 4 
PROXIMITY_PIPS = 10 
SLOPE_THRESHOLD_PIPS = 0.5 

# Diretório de Files do MT5
MT5_DATA_PATH = r"C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"

# Arquivo de persistência de zonas consumidas
CONSUMED_ZONES_FILE = os.path.join(os.path.dirname(__file__), ".consumed_zones.json")

def load_consumed_zones():
    """Carrega zonas consumidas do arquivo JSON. Remove zonas com mais de 24h."""
    if not os.path.exists(CONSUMED_ZONES_FILE):
        return set()
    try:
        with open(CONSUMED_ZONES_FILE, 'r') as f:
            data = json.load(f)
        # Filtrar zonas antigas (> 24h)
        now = datetime.now()
        consumed = set()
        for item in data:
            if 'timestamp' in item:
                zone_time = datetime.fromisoformat(item['timestamp'])
                if (now - zone_time).total_seconds() < 86400:  # 24h
                    consumed.add(item['z_key'])
            else:
                consumed.add(item['z_key'])  # Zonas sem timestamp (compatibilidade)
        return consumed
    except Exception as e:
        print(f"⚠️ Erro ao carregar consumed_zones: {e}")
        return set()

def save_consumed_zones(consumed_zones):
    """Salva zonas consumidas no arquivo JSON com timestamp."""
    try:
        data = []
        now = datetime.now().isoformat()
        for z_key in consumed_zones:
            data.append({'z_key': z_key, 'timestamp': now})
        with open(CONSUMED_ZONES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ Erro ao salvar consumed_zones: {e}")

def initialize_mt5():
    if not mt5.initialize(): return False
    return True

def calculate_wick_metrics(candle):
    """Calcula métricas de pavio para o gatilho Sniper."""
    high, low, open_p, close_p = candle['high'], candle['low'], candle['open'], candle['close']
    total = high - low
    if total <= 0: return 0.00001, 0, 0
    top = high - max(open_p, close_p)
    bot = min(open_p, close_p) - low
    return total, top, bot

def sync_with_mt5_history(session_start, full_sync=False):
    """
    FIX #5: Sincronização correta MT5 → Supabase
    - Usar position_id como identificador único (evita duplicatas)
    - Atualizar trades zerados com P&L real do MT5
    """
    if not db_manager.client: return
    try:
        lookback = session_start if full_sync else (datetime.now() - timedelta(minutes=60))
        deals = mt5.history_deals_get(lookback, datetime.now() + timedelta(days=1))
        if not deals: return

        processed_positions = set()

        for d in deals:
            if d.magic != MAGIC_NUMBER or d.entry != 1: continue
            if d.position_id in processed_positions: continue  # Evitar processar mesma posição 2x

            in_deals = mt5.history_deals_get(position=d.position_id)
            if not in_deals or len(in_deals) < 2: continue  # Precisa ter entrada E saída

            entry_time = datetime.fromtimestamp(in_deals[0].time).isoformat()
            pnl_real = d.profit + d.commission + d.swap

            # Procurar por position_id (identificador único) ou por símbolo+tempo
            check = db_manager.client.table("signals_liquidez").select("id, status, pnl").eq("magic", d.position_id).execute()

            if not check.data:
                # Tentar buscar por símbolo e tempo (compatibilidade com registros antigos)
                check = db_manager.client.table("signals_liquidez").select("id, status, pnl").eq("symbol", d.symbol).eq("created_at", entry_time).execute()

            if not check.data:
                # Não existe: Inserir novo
                db_manager.client.table("signals_liquidez").insert({
                    "symbol": d.symbol,
                    "type": "BUY" if in_deals[0].type == 0 else "SELL",
                    "price": in_deals[0].price,
                    "status": "closed",
                    "pnl": pnl_real,
                    "magic": d.position_id,  # Usar position_id como identificador único
                    "wick_pct": 0.5,
                    "created_at": entry_time,
                    "closed_at": datetime.fromtimestamp(d.time).isoformat()
                }).execute()
            else:
                # Existe: Atualizar se necessário
                existing = check.data[0]
                if existing['status'] != 'closed' or existing.get('pnl', 0) == 0 or existing.get('pnl') is None:
                    db_manager.client.table("signals_liquidez").update({
                        "status": "closed",
                        "pnl": pnl_real,
                        "magic": d.position_id,  # Garantir position_id
                        "closed_at": datetime.fromtimestamp(d.time).isoformat()
                    }).eq("id", existing['id']).execute()

            processed_positions.add(d.position_id)

    except Exception as e:
        print(f"⚠️ [Network] Erro temporário na sincronia Supabase: {e}")

def get_daily_pnl():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    deals = mt5.history_deals_get(today, datetime.now() + timedelta(days=1))
    return sum([d.profit + d.commission + d.swap for d in deals if d.magic == MAGIC_NUMBER]) if deals else 0.0

def get_account_pnl():
    deals = mt5.history_deals_get(datetime(2020, 1, 1), datetime.now() + timedelta(days=1))
    return sum([d.profit + d.commission + d.swap for d in deals if d.magic == MAGIC_NUMBER]) if deals else 0.0

def get_rates(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0: return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def get_validated_zones(df_zones, point):
    zones = []
    if df_zones is None or len(df_zones) < 10: return zones
    for i in range(len(df_zones) - 8):
        high, low = df_zones.iloc[i]['high'], df_zones.iloc[i]['low']
        if all(df_zones.iloc[i+j]['high'] < high for j in range(1, 8)):
            zones.append({'type': 'RESISTANCE', 'price': high, 'time': df_zones.iloc[i]['time']})
        if all(df_zones.iloc[i+j]['low'] > low for j in range(1, 8)):
            zones.append({'type': 'SUPPORT', 'price': low, 'time': df_zones.iloc[i]['time']})
    return zones

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_trigger(symbol, df_m15, zones, point, session_trade_log, consumed_zones, now_utc, df_h1=None):
    if df_m15 is None or len(df_m15) < 15 or not zones: return None, None
    pip_size = point * 10
    # FIX #1: Usar candle fechado (iloc[-2]) ao invés de candle atual (iloc[-1])
    current_price = df_m15.iloc[-2]['close']
    for past_trade in session_trade_log:
        if past_trade['symbol'] == symbol:
            if abs(current_price - past_trade['price']) <= (PROXIMITY_PIPS * pip_size):
                if now_utc - past_trade['time'] < timedelta(hours=COOLDOWN_HOURS):
                    return None, None
    df_m15['rsi'] = calculate_rsi(df_m15['close'])
    last = df_m15.iloc[-2]; prev = df_m15.iloc[-3]; rsi = df_m15['rsi'].iloc[-2]
    trend_slope = 0 
    if df_h1 is not None and len(df_h1) >= 21:
        sma = df_h1['close'].rolling(20).mean()
        slope_pips = (sma.iloc[-1] - sma.iloc[-2]) / pip_size
        if slope_pips > SLOPE_THRESHOLD_PIPS: trend_slope = 1
        elif slope_pips < -SLOPE_THRESHOLD_PIPS: trend_slope = -1
    total, top, bot = calculate_wick_metrics(last)
    is_reversal = (last['close'] > last['open'] and prev['close'] < prev['open']) or \
                  (last['close'] < last['open'] and prev['close'] > prev['open'])
    for z in zones:
        z_key = f"{symbol}_{z['type']}_{round(z['price'], 5)}"
        if z_key in consumed_zones: continue
        if z['type'] == 'RESISTANCE' and last['high'] >= z['price'] and (top/total) >= 0.3 and rsi >= 60 and trend_slope <= 0 and is_reversal:
            return {'symbol': symbol, 'type': mt5.ORDER_TYPE_SELL_LIMIT, 'price': last['close'], 'sl': last['high'] + (STOP_BUFFER * point), 'tp': last['close'] - (abs(last['high']-last['close'])*1.5), 'comment': f"LIQ-{symbol}-S", 'z_key': z_key}, z
        elif z['type'] == 'SUPPORT' and last['low'] <= z['price'] and (bot/total) >= 0.3 and rsi <= 40 and trend_slope >= 0 and is_reversal:
            return {'symbol': symbol, 'type': mt5.ORDER_TYPE_BUY_LIMIT, 'price': last['close'], 'sl': last['low'] - (STOP_BUFFER * point), 'tp': last['close'] + (abs(last['low']-last['close'])*1.5), 'comment': f"LIQ-{symbol}-B", 'z_key': z_key}, z
    return None, None

def send_order(symbol, order_data):
    tick = mt5.symbol_info_tick(symbol)
    price = tick.bid if order_data['type'] == mt5.ORDER_TYPE_SELL_LIMIT else tick.ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": CFG.get('lot_size', 1.0),
        "type": mt5.ORDER_TYPE_SELL if order_data['type'] == mt5.ORDER_TYPE_SELL_LIMIT else mt5.ORDER_TYPE_BUY,
        "price": price, "sl": order_data['sl'], "tp": order_data['tp'], "magic": MAGIC_NUMBER,
        "comment": order_data['comment'], "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_FOK
    }
    return mt5.order_send(request)

def main():
    if not initialize_mt5(): return
    SESSION_START = datetime.now()
    session_trade_log = []
    # FIX #2: Carregar consumed_zones do arquivo (persistência entre reinícios)
    consumed_zones = load_consumed_zones()
    sync_with_mt5_history(SESSION_START, full_sync=True)
    print(f"🚀 MOTOR v5.9.6 (SYNC-FIX): {len(CFG['symbols'])} ATIVOS | Zonas Persistidas: {len(consumed_zones)}")
    try:
        while True:
            sync_with_mt5_history(SESSION_START, full_sync=False)
            pnl_today, pnl_total = get_daily_pnl(), get_account_pnl()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*65)
            print(f" SQUAD LIQUIDEZ v5.9.6 | {datetime.now().strftime('%H:%M:%S')}")
            print(f" LUCRO HOJE (MT5):  ${pnl_today:.2f}")
            print(f" LUCRO TOTAL CONTA: ${pnl_total:.2f}")
            print(f" ZONAS EXAURIDAS:   {len(consumed_zones)}")
            print("="*65)
            if pnl_today <= -CFG.get('daily_max_loss', 150.0):
                print(f"🛑 STOP LOSS DIÁRIO ATINGIDO! ENCERRANDO."); break
            # FIX #4: Limitar a 1 trade por ciclo (prevenir race condition)
            trade_executed_this_cycle = False
            for symbol in CFG['symbols']:
                all_pos = mt5.positions_get(symbol=symbol)
                pos = [p for p in (all_pos or []) if p.magic == MAGIC_NUMBER]
                df_m15 = get_rates(symbol, mt5.TIMEFRAME_M15, 100)
                zones = get_validated_zones(df_m15, mt5.symbol_info(symbol).point)
                df_h1 = get_rates(symbol, mt5.TIMEFRAME_H1, 50)
                trigger, z_trig = check_trigger(symbol, df_m15, zones, mt5.symbol_info(symbol).point, session_trade_log, consumed_zones, datetime.now(pytz.utc), df_h1)
                # FIX #4: Só executar se não houve trade neste ciclo
                if trigger and not pos and not mt5.orders_get(symbol=symbol, magic=MAGIC_NUMBER) and not trade_executed_this_cycle:
                    try:
                        # FIX #5: NÃO criar registro no Supabase na abertura
                        # sync_with_mt5_history() fará isso quando o trade fechar
                        exec_res = send_order(symbol, trigger)
                        if exec_res.retcode == mt5.TRADE_RETCODE_DONE:
                            session_trade_log.append({'symbol': symbol, 'price': trigger['price'], 'time': datetime.now(pytz.utc)})
                            consumed_zones.add(trigger['z_key'])
                            trade_executed_this_cycle = True  # FIX #4: Marcar trade executado
                            print(f"✅ {symbol} trade aberto: {trigger['type']} @ {trigger['price']}")
                        else:
                            # FIX #3: Logar erro específico e consumir zona para evitar loop
                            print(f"⚠️ {symbol} ordem falhou: retcode={exec_res.retcode}, comment={exec_res.comment}")
                            consumed_zones.add(trigger['z_key'])
                    except Exception as e:
                        # FIX #3: Logar exceção e consumir zona para evitar loop infinito
                        print(f"❌ {symbol} erro ao processar trade: {e}")
                        consumed_zones.add(trigger['z_key'])
                file_path = os.path.join(MT5_DATA_PATH, "MQL5", "Files", f"liquidez_data_{symbol}.csv")
                try:
                    with open(file_path, "w", encoding="ansi") as f:
                        f.write("HEADER\n") 
                        for z in zones: 
                            z_key = f"{symbol}_{z['type']}_{round(z['price'], 5)}"
                            if z_key not in consumed_zones: f.write(f"ZONE_{z['type']},{z['price']},{z['time']}\n")
                except: pass
            try: db_manager.log_heartbeat("GLOBAL", "running", len(CFG['symbols']), pnl_today, pnl_total)
            except: pass
            # FIX #2: Salvar consumed_zones periodicamente
            save_consumed_zones(consumed_zones)
            time.sleep(20)
    finally:
        # Salvar consumed_zones ao encerrar
        save_consumed_zones(consumed_zones)
        mt5.shutdown()

if __name__ == "__main__":
    main()
