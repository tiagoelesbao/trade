import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import os
import yaml

# Carrega config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

SYMBOL = CFG['symbol']

def calculate_wick_metrics(candle):
    high, low, open_p, close_p = candle['high'], candle['low'], candle['open'], candle['close']
    total_size = high - low
    if total_size == 0: return 0.00001, 0, 0
    top_wick = high - max(open_p, close_p)
    bottom_wick = min(open_p, close_p) - low
    return total_size, top_wick, bottom_wick

def diagnose():
    if not mt5.initialize():
        print("Erro ao inicializar MT5")
        return

    print(f"\n[DIAGNOSTICO] ANALISANDO HOJE ({datetime.now().strftime('%d/%m/%Y')}) - ATIVO: {SYMBOL}")
    print("-" * 60)

    # 1. Busca Zonas H1
    rates_h1 = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_H1, 0, 100)
    if rates_h1 is None:
        print("Erro ao carregar dados H1")
        return
        
    df_h1 = pd.DataFrame(rates_h1)
    df_h1['time'] = pd.to_datetime(df_h1['time'], unit='s')
    
    # Logica de zonas (simplificada para o diagnostico)
    zones = []
    min_dist = CFG['min_displacement_candles']
    for i in range(len(df_h1) - min_dist - 1):
        if all(df_h1.iloc[i]['high'] >= df_h1.iloc[i+j]['high'] for j in range(1, min_dist+1)):
            zones.append({'type': 'RESISTANCE', 'price': df_h1.iloc[i]['high'], 'time': df_h1.iloc[i]['time']})
        if all(df_h1.iloc[i]['low'] <= df_h1.iloc[i+j]['low'] for j in range(1, min_dist+1)):
            zones.append({'type': 'SUPPORT', 'price': df_h1.iloc[i]['low'], 'time': df_h1.iloc[i]['time']})

    print(f"OK: Encontradas {len(zones)} zonas de H1 no historico recente.")

    # 2. Busca data de hoje (00:00 ate agora)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    rates_m5 = mt5.copy_rates_range(SYMBOL, mt5.TIMEFRAME_M5, today, datetime.now())
    
    if rates_m5 is None or len(rates_m5) < 3:
        print("Sem dados de M5 para hoje.")
        return

    df_m5 = pd.DataFrame(rates_m5)
    df_m5['time'] = pd.to_datetime(df_m5['time'], unit='s')

    print(f"ANALISE: Analisando {len(df_m5)} candles de M5 de hoje...\n")

    rejection_reasons = {
        "VOLUME": 0,
        "COLOR": 0,
        "WICK": 0,
        "NO_ZONE": 0
    }

    for i in range(2, len(df_m5)):
        last = df_m5.iloc[i-1]
        prev = df_m5.iloc[i-2]

        # Filtro 1: Volume
        if CFG.get('require_volume_momentum', True):
            if last['tick_volume'] <= prev['tick_volume']:
                rejection_reasons["VOLUME"] += 1
                continue

        # Filtro 2: Cor
        if CFG.get('require_color_reversal', True):
            last_bull = last['close'] > last['open']
            prev_bull = prev['close'] > prev['open']
            if last_bull == prev_bull:
                rejection_reasons["COLOR"] += 1
                continue

        # Filtro 3: Zona
        in_zone = False
        zone_hit = None
        for z in zones:
            if z['type'] == 'RESISTANCE' and last['high'] >= z['price']: 
                in_zone = True; zone_hit = z; break
            if z['type'] == 'SUPPORT' and last['low'] <= z['price']: 
                in_zone = True; zone_hit = z; break

        if not in_zone:
            rejection_reasons["NO_ZONE"] += 1
            continue

        # Filtro 4: Wick
        total, top, bot = calculate_wick_metrics(last)
        if zone_hit['type'] == 'RESISTANCE':
            wick_pct = top/total 
        else:
            wick_pct = bot/total

        min_wick = CFG.get('min_wick_pct', 0.30)
        max_wick = CFG.get('max_wick_pct', 0.70)
        if not (min_wick <= wick_pct <= max_wick):
            rejection_reasons["WICK"] += 1
            continue


        print(f"SINAL ENCONTRADO! Time: {last['time']} | Price: {last['close']} | Wick: {wick_pct:.2f}")

    print("\n" + "="*60)
    print(" RELATORIO DE REJEICOES (POR QUE NAO HOUVE TRADES?) ")
    print("="*60)
    print(f" Sem Volume Momentum:   {rejection_reasons['VOLUME']} vezes")
    print(f" Sem Reversao de Cor:   {rejection_reasons['COLOR']} vezes")
    print(f" Sem Toque em Zona H1:  {rejection_reasons['NO_ZONE']} vezes")
    print(f" Anatomia de Pavio Ruim: {rejection_reasons['WICK']} vezes")
    print("="*60)
    print("\nDICA: Se 'Sem Reversao de Cor' ou 'Sem Volume' sao os maiores, o mercado esta em tendencia forte.")
    print("      Voce podera desativar esses filtros no novo config.yaml que vamos criar.")

    mt5.shutdown()

if __name__ == "__main__":
    diagnose()
