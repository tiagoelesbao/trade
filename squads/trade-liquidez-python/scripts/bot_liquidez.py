"""
Bot de Trading - Liquidez v6.1.5 (Dedup in-memory por vela M15)
=======================================================================
Integração com TradeLifecycleManager para gerenciamento de estados.

Fluxo de Estados:
1. signal_detected    - Sinal técnico detectado
2. approved           - Auto-aprovado (ou via war room)
3. filled             - Ordem executada no MT5
4. open               - Posição ativa
5. closed             - Trade finalizado com P&L

Mudanças v6.1.5 (2026-04-23):
- Reintroduzido dedup in-memory por (symbol, type, trigger_candle_time).
  Diferente de Kill-Zone/One-Shot (v<=6.1.3, persistiam em disco e bloqueavam
  zona por horas): este é apenas um set() em memória que evita reenviar o
  MESMO sinal da MESMA vela M15 a cada ciclo de 20s. Reseta ao reiniciar bot.
  Não priva trades entre velas diferentes. Motivo: logs mostravam 10+ envios
  duplicados do mesmo sinal na mesma vela fechada, saturando a War Room.

Mudanças v6.1.4 (2026-04-22):
- Removidos: Kill-Zone (check_cooldown), One-Shot de zonas (consumed_zones
  load/save/prune), trava por vela persistida. Persistência .consumed_zones.json
  descontinuada. Motivo (decisão do trader): estavam privando bons trades sem
  ganho estatístico comprovado. Proteções remanescentes: 1 posição aberta por
  símbolo, correlação entre pares (War Room), stop/meta diários.

Mudanças v6.1.3 (2026-04-22):
- RSI(9) promovido a default, stop_buffer 15→50, breakeven desativado,
  scoring War Room reformado (5 critérios, RSI alpha 35pts).

Mudanças v6.1.2 (2026-04-22):
- Timezone de log do terminal = MT5 server (config.mt5_server_utc_offset).

Mudanças v6.0:
- TradeLifecycleManager para todos os estados
- position_id como chave única (0 duplicatas)
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta, timezone
from collections import deque


def utc_now_iso():
    """ISO timestamp UTC-aware — usar sempre em queries/inserts Supabase."""
    return datetime.now(timezone.utc).isoformat()
import time
import pytz
import yaml
import os

# Rolling log de eventos para exibição no terminal
recent_events: deque = deque(maxlen=10)

# v6.1.5: dedup in-memory de sinais já enviados na mesma vela M15.
# Chave: (symbol, type, trigger_candle_time). Limpo periodicamente por prune_sent_signals().
sent_signals: set = set()

# Timestamp de início da sessão (reset a cada reinício do bot)
SESSION_START = datetime.now()

# Carregar configurações
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

# TradeLifecycleManager v6.0
from trade_lifecycle_manager import TradeLifecycleManager
from system_logger import SystemLogger

lifecycle = TradeLifecycleManager()
logger = SystemLogger("BOT")

# Configurações Globais
MAGIC_NUMBER        = CFG['magic_number']
STOP_BUFFER         = CFG['stop_buffer_points']
SLOPE_THRESHOLD_PIPS= CFG.get('slope_threshold_pips', 0.5)
MIN_WICK_PCT        = CFG.get('min_wick_pct', 0.30)
RSI_OVERBOUGHT      = CFG.get('rsi_overbought', 70)
RSI_OVERSOLD        = CFG.get('rsi_oversold', 30)
RSI_PERIOD          = CFG.get('rsi_period', 9)  # v6.1.3: 14 -> 9 (clássico, mais reativo)
RR_RATIO            = CFG.get('risk_reward_ratio', 1.5)
LOOKBACK_ZONES      = CFG.get('lookback_zones', 100)
MIN_DISPLACEMENT    = CFG.get('min_displacement_candles', 7)
USE_TREND_FILTER    = CFG.get('use_trend_filter', True)
REQUIRE_REVERSAL    = CFG.get('require_color_reversal', True)
DAILY_PROFIT_TARGET = CFG.get('daily_profit_target', 500.0)
BREAKEVEN_CANDLES   = CFG.get('breakeven_candles', 0)   # 0 = desativado

# Timezone MT5 server — usado em todos os timestamps de log do terminal
# para que a hora do sinal case com o chart da corretora.
_MT5_TZ = timezone(timedelta(hours=CFG.get('mt5_server_utc_offset', 3)))

def mt5_time_str(fmt="%H:%M:%S"):
    """Hora formatada no fuso do servidor MT5 (o mesmo do chart)."""
    return datetime.now(_MT5_TZ).strftime(fmt)
BREAKEVEN_BUFFER_PT = 2                                  # pontos acima/abaixo da entrada

# Diretório MT5 Files
MT5_DATA_PATH = r"C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"


def initialize_mt5():
    """Inicializa conexão com MT5."""
    if not mt5.initialize():
        print("[ERROR] Falha ao conectar MT5")
        return False
    return True

def calculate_wick_metrics(candle):
    """Calcula métricas de pavio para o gatilho Sniper."""
    high, low, open_p, close_p = candle['high'], candle['low'], candle['open'], candle['close']
    total = high - low
    if total <= 0:
        return 0.00001, 0, 0
    top = high - max(open_p, close_p)
    bot = min(open_p, close_p) - low
    return total, top, bot

def get_session_pnl():
    """Calcula P&L da sessão atual (desde o início do bot nesta execução)."""
    deals = mt5.history_deals_get(SESSION_START, datetime.now() + timedelta(days=1))
    return sum([d.profit + d.commission + d.swap for d in deals if d.magic == MAGIC_NUMBER]) if deals else 0.0

def get_account_pnl():
    """Calcula P&L total da conta."""
    deals = mt5.history_deals_get(datetime(2020, 1, 1), datetime.now() + timedelta(days=1))
    return sum([d.profit + d.commission + d.swap for d in deals if d.magic == MAGIC_NUMBER]) if deals else 0.0

def get_rates(symbol, timeframe, count):
    """Busca dados de candles do MT5."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def get_validated_zones(df_zones, point):
    """Identifica zonas de suporte/resistência validadas (displacement = MIN_DISPLACEMENT candles)."""
    zones = []
    min_required = MIN_DISPLACEMENT + 2
    if df_zones is None or len(df_zones) < min_required:
        return zones
    for i in range(len(df_zones) - (MIN_DISPLACEMENT + 1)):
        high, low = df_zones.iloc[i]['high'], df_zones.iloc[i]['low']
        if all(df_zones.iloc[i+j]['high'] < high for j in range(1, MIN_DISPLACEMENT + 1)):
            zones.append({'type': 'RESISTANCE', 'price': high, 'time': df_zones.iloc[i]['time']})
        if all(df_zones.iloc[i+j]['low'] > low for j in range(1, MIN_DISPLACEMENT + 1)):
            zones.append({'type': 'SUPPORT', 'price': low, 'time': df_zones.iloc[i]['time']})
    return zones

def calculate_rsi(series, period=None):
    """Calcula RSI. Default lido do config (`rsi_period`, v6.1.3 = 9)."""
    if period is None:
        period = RSI_PERIOD
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_trigger(symbol, df_m15, zones, point, df_h1=None):
    """
    Verifica se há gatilho Sniper válido usando os parâmetros do config.yaml.
    Retorna: (trigger_data, zone) ou (None, None).

    Observação (v6.1.3+): removidos cooldown (kill-zone), one-shot de zona e
    trava por vela. O filtro de qualidade passa a ser feito apenas por: gatilho
    técnico (wick+RSI), War Room (score ≥65), correlação e posição já aberta no
    símbolo. Não há mais persistência de estado entre ciclos.
    """
    if df_m15 is None or len(df_m15) < 15 or not zones:
        return None, None

    pip_size = point * 10

    df_m15['rsi'] = calculate_rsi(df_m15['close'])
    last = df_m15.iloc[-2]
    prev = df_m15.iloc[-3]
    rsi = df_m15['rsi'].iloc[-2]

    # Calcular slope H1 apenas se filtro de tendência estiver ativo
    trend_slope = None  # None = dados não disponíveis
    if USE_TREND_FILTER:
        if df_h1 is not None and len(df_h1) >= 21:
            sma = df_h1['close'].rolling(20).mean()
            slope_pips = (sma.iloc[-1] - sma.iloc[-2]) / pip_size
            if slope_pips > SLOPE_THRESHOLD_PIPS:
                trend_slope = 1    # Ascendente
            elif slope_pips < -SLOPE_THRESHOLD_PIPS:
                trend_slope = -1   # Descendente
            else:
                trend_slope = 0    # Neutro
        else:
            # H1 indisponível: bloquear trade quando filtro está ativo
            return None, None

    total, top, bot_wick = calculate_wick_metrics(last)

    is_reversal = (last['close'] > last['open'] and prev['close'] < prev['open']) or \
                  (last['close'] < last['open'] and prev['close'] > prev['open'])

    for z in zones:
        # SELL em RESISTÊNCIA
        if z['type'] == 'RESISTANCE' and \
           last['high'] >= z['price'] and \
           (top / total) >= MIN_WICK_PCT and \
           rsi >= RSI_OVERBOUGHT and \
           (not USE_TREND_FILTER or trend_slope < 0) and \
           (not REQUIRE_REVERSAL or is_reversal):

            sl = last['high'] + (STOP_BUFFER * point)
            dist = abs(sl - last['close'])
            return {
                'symbol':   symbol,
                'type':     'SELL',
                'mt5_type': mt5.ORDER_TYPE_SELL,
                'price':    last['close'],
                'sl':       sl,
                'tp':       last['close'] - (dist * RR_RATIO),
                'comment':  f"LIQ-{symbol}-S",
                'wick_pct': top / total,
                'trigger_time': last['time'],
            }, z

        # BUY em SUPORTE
        elif z['type'] == 'SUPPORT' and \
             last['low'] <= z['price'] and \
             (bot_wick / total) >= MIN_WICK_PCT and \
             rsi <= RSI_OVERSOLD and \
             (not USE_TREND_FILTER or trend_slope > 0) and \
             (not REQUIRE_REVERSAL or is_reversal):

            sl = last['low'] - (STOP_BUFFER * point)
            dist = abs(last['close'] - sl)
            return {
                'symbol':   symbol,
                'type':     'BUY',
                'mt5_type': mt5.ORDER_TYPE_BUY,
                'price':    last['close'],
                'sl':       sl,
                'tp':       last['close'] + (dist * RR_RATIO),
                'comment':  f"LIQ-{symbol}-B",
                'wick_pct': bot_wick / total,
                'trigger_time': last['time'],
            }, z

    return None, None

def push_event(tag: str, msg: str):
    """Adiciona evento ao rolling log do terminal."""
    ts = mt5_time_str("%H:%M:%S")
    recent_events.append(f"{ts}  {tag:<10}  {msg}")

def prune_sent_signals(max_age_hours: float = 2.0):
    """Remove entries antigas de sent_signals para evitar crescimento indefinido.

    Trigger_time vem como pd.Timestamp naive (hora do servidor MT5). A vela M15
    mais recente usada no dedup nunca vai ter mais que 15min de idade; 2h é margem
    de segurança para cobrir pausas de mercado.
    """
    if not sent_signals:
        return
    cutoff = pd.Timestamp.now() - pd.Timedelta(hours=max_age_hours)
    stale = {key for key in sent_signals if key[2] < cutoff}
    sent_signals.difference_update(stale)

def print_dashboard(pnl_session, pnl_total):
    """Exibe dashboard formatado no terminal do bot."""
    W = 67
    daily_limit = CFG.get('daily_max_loss', 350.0)
    used_pct = min(1.0, abs(pnl_session) / daily_limit) if pnl_session < 0 else 0.0
    bar_size = 22
    filled = int(used_pct * bar_size)
    bar = '#' * filled + '-' * (bar_size - filled)
    remaining_pct = max(0.0, 100.0 - used_pct * 100)

    open_pos = mt5.positions_get() or []
    open_count = len([p for p in open_pos if p.magic == MAGIC_NUMBER])

    pnl_ses_sign = "+" if pnl_session >= 0 else ""
    pnl_total_sign = "+" if pnl_total >= 0 else ""

    os.system('cls' if os.name == 'nt' else 'clear')
    sep  = "=" * W
    dash = "-" * W
    now  = mt5_time_str("%H:%M:%S")

    print(sep)
    trend_state = "ON" if USE_TREND_FILTER else "OFF"
    reversal_state = "ON" if REQUIRE_REVERSAL else "OFF"
    tz_offset = CFG.get('mt5_server_utc_offset', 3)
    tz_sign = "+" if tz_offset >= 0 else ""
    print(f"  BOT LIQUIDEZ v6.1.2  |  {now} MT5 (UTC{tz_sign}{tz_offset:02d})  |  {len(CFG['symbols'])} pares  |  Magic {MAGIC_NUMBER}")
    print(f"  Filtros: trend={trend_state}  reversal={reversal_state}  wick>={MIN_WICK_PCT*100:.0f}%  RSI({RSI_PERIOD}) {RSI_OVERSOLD}/{RSI_OVERBOUGHT}")
    print(sep)
    print(f"  P&L SESSAO : ${pnl_ses_sign}{pnl_session:.2f}".ljust(36) + f"  P&L TOTAL  : ${pnl_total_sign}{pnl_total:.2f}")
    print(f"  STOP DIARIO: [{bar}] {remaining_pct:.0f}% restante  (limite ${daily_limit:.0f})")
    print(dash)
    print(f"  POSICOES ABERTAS: {open_count}")
    print(sep)
    if recent_events:
        print("  ATIVIDADE RECENTE")
        print(dash)
        for ev in recent_events:
            print(f"  {ev}")
    else:
        print("  Aguardando sinais...")
    print(sep)

def send_heartbeat(pnl_session, pnl_total, active_zones):
    """Envia heartbeat para o Supabase (mantém dashboard atualizado)."""
    try:
        lifecycle.client.table("bot_heartbeats").upsert({
            "symbol": "GLOBAL",
            "status": "running",
            "active_zones": active_zones,
            "pnl_today": round(pnl_session, 2),
            "pnl_total": round(pnl_total, 2),
            "created_at": utc_now_iso()
        }, on_conflict="symbol").execute()
    except Exception as e:
        print(f"[WARNING] Heartbeat falhou: {e}")

def sync_open_positions():
    """
    Sincroniza posições abertas no MT5 com banco de dados.
    - Trades "filled" que têm posição aberta → marca como "open"
    - Trades "open" que não têm mais posição → verifica se fechou e calcula P&L
    """
    try:
        # Buscar trades "filled" ou "open" no banco
        active_trades = lifecycle.client.table("signals_liquidez")\
            .select("*")\
            .in_("status", ["filled", "open"])\
            .execute()

        if not active_trades.data:
            return

        # Buscar posições abertas no MT5
        mt5_positions = mt5.positions_get()
        mt5_position_ids = {p.ticket: p for p in (mt5_positions or []) if p.magic == MAGIC_NUMBER}

        for trade in active_trades.data:
            position_id = trade.get('position_id')

            if not position_id:
                continue

            # Verificar se posição está aberta no MT5
            if position_id in mt5_position_ids:
                # Posição aberta → marcar como "open" se ainda estiver "filled"
                if trade['status'] == 'filled':
                    lifecycle.mark_as_open(trade['id'])
            else:
                # Posição não está mais aberta → verificar se fechou
                check_if_closed(trade)

    except Exception as e:
        print(f"[WARNING] Erro ao sincronizar posições: {e}")

def check_if_closed(trade):
    """Verifica se um trade foi fechado no MT5 e atualiza P&L."""
    try:
        position_id = trade.get('position_id')
        if not position_id:
            return

        deals = mt5.history_deals_get(position=position_id)
        if not deals or len(deals) < 2:
            return

        exit_deal = None
        for d in deals:
            if d.entry == 1:
                exit_deal = d
                break

        if not exit_deal:
            return

        pnl_real = exit_deal.profit + exit_deal.commission + exit_deal.swap
        exit_price = exit_deal.price

        lifecycle.close_trade(position_id, pnl_real, exit_price)
        pnl_sign = "+" if pnl_real >= 0 else ""
        push_event("FECHADO", f"{trade.get('symbol')} {trade.get('type')}  PNL: ${pnl_sign}{pnl_real:.2f}  saida @ {exit_price}")
        logger.trade("trade_closed",
            f"{trade.get('symbol')} {trade.get('type')} fechado | PNL: ${pnl_real:.2f} | Saída: {exit_price}",
            symbol=trade.get('symbol'),
            data={"position_id": position_id, "pnl": pnl_real, "exit_price": exit_price}
        )

    except Exception as e:
        logger.error("check_closed_error", f"Erro ao verificar fechamento: {e}",
                     data={"trade_id": trade.get('id')})

def check_breakeven():
    """
    Move o SL para o preço de entrada (+ buffer) quando:
      1. breakeven_candles > 0 no config.yaml  (feature ativa)
      2. Trade 'open' completou >= breakeven_candles velas M15 desde filled_at
      3. Preço atual está favorável (trade em lucro)
      4. SL ainda está do lado de risco (não foi movido antes)

    Executa via TRADE_ACTION_SLTP — modificação direta no MT5 sem abrir nova ordem.
    TP é preservado intacto.
    """
    if BREAKEVEN_CANDLES <= 0:
        return  # Feature desativada via config.yaml

    try:
        mt5_positions = mt5.positions_get() or []
        positions = [p for p in mt5_positions if p.magic == MAGIC_NUMBER]
        if not positions:
            return

        from datetime import timezone as tz

        for pos in positions:
            # Buscar registro do trade no Supabase
            res = lifecycle.client.table("signals_liquidez")\
                .select("id,symbol,type,price,sl,filled_at,status")\
                .eq("position_id", pos.ticket)\
                .eq("status", "open")\
                .execute()

            if not res.data:
                continue

            trade       = res.data[0]
            entry_price = trade.get('price')
            trade_type  = trade.get('type')
            filled_at   = trade.get('filled_at')

            if not entry_price or not filled_at:
                continue

            # Quantas velas M15 desde a abertura
            filled_dt      = datetime.fromisoformat(filled_at.replace('Z', '+00:00'))
            elapsed_sec    = (datetime.now(tz.utc) - filled_dt).total_seconds()
            elapsed_candles = int(elapsed_sec / (15 * 60))

            if elapsed_candles < BREAKEVEN_CANDLES:
                continue  # Ainda aguardando o número de velas

            # Calcular SL de breakeven
            info   = mt5.symbol_info(pos.symbol)
            point  = info.point
            buf    = BREAKEVEN_BUFFER_PT * point

            if trade_type == 'BUY':
                be_sl = entry_price + buf
                already_be = pos.sl >= (be_sl - point)
                in_profit  = pos.price_current > entry_price
            else:  # SELL
                be_sl = entry_price - buf
                already_be = pos.sl <= (be_sl + point)
                in_profit  = pos.price_current < entry_price

            if already_be:
                continue  # SL já está no breakeven ou melhor
            if not in_profit:
                continue  # Trade no prejuízo — não mover (protege de fechar no negativo)

            # Enviar modificação ao MT5
            request = {
                "action":   mt5.TRADE_ACTION_SLTP,
                "symbol":   pos.symbol,
                "position": pos.ticket,
                "sl":       round(be_sl, info.digits),
                "tp":       pos.tp,
            }
            result = mt5.order_send(request)

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                push_event("BREAKEVEN",
                    f"{pos.symbol} {trade_type} SL → {be_sl:.5f}  "
                    f"(entrada {entry_price:.5f}  candles:{elapsed_candles})")
                logger.info("breakeven_moved",
                    f"{pos.symbol} {trade_type} | SL {pos.sl:.5f} → {be_sl:.5f} "
                    f"(entrada:{entry_price:.5f} | candles abertos:{elapsed_candles})",
                    symbol=pos.symbol,
                    data={
                        "position_id":    pos.ticket,
                        "entry_price":    entry_price,
                        "old_sl":         pos.sl,
                        "new_sl":         round(be_sl, info.digits),
                        "elapsed_candles": elapsed_candles,
                        "buffer_points":  BREAKEVEN_BUFFER_PT,
                    })
            else:
                logger.warning("breakeven_failed",
                    f"{pos.symbol} {trade_type}: falha SLTP | retcode={result.retcode} {result.comment}",
                    symbol=pos.symbol,
                    data={"retcode": result.retcode, "position_id": pos.ticket})

    except Exception as e:
        logger.error("breakeven_error", f"Erro no check_breakeven: {e}")


def execute_approved_signals():
    """
    Executa sinais que foram aprovados pela War Room.
    Busca sinais com status 'approved' e executa no MT5.
    """
    try:
        # Buscar sinais aprovados
        approved_signals = lifecycle.get_pending_signals('approved')

        if not approved_signals:
            return 0

        executed_count = 0

        for signal in approved_signals:
            try:
                symbol = signal['symbol']
                trade_type = signal['type']

                # Verificar se já tem posição aberta para este símbolo
                all_pos = mt5.positions_get(symbol=symbol)
                pos = [p for p in (all_pos or []) if p.magic == MAGIC_NUMBER]

                if pos:
                    # Já tem posição aberta, rejeitar sinal
                    lifecycle.reject_signal(
                        signal['id'],
                        reason=f"Posição já aberta para {symbol}"
                    )
                    continue

                # Montar dados da ordem
                tick = mt5.symbol_info_tick(symbol)
                price = tick.bid if trade_type == 'SELL' else tick.ask

                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": CFG.get('lot_size', 1.0),
                    "type": mt5.ORDER_TYPE_SELL if trade_type == 'SELL' else mt5.ORDER_TYPE_BUY,
                    "price": price,
                    "sl": signal['sl'],
                    "tp": signal['tp'],
                    "magic": MAGIC_NUMBER,
                    "comment": f"LIQ-{symbol}-{trade_type[0]}",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_FOK
                }

                # Executar ordem
                exec_res = mt5.order_send(request)

                if exec_res.retcode == mt5.TRADE_RETCODE_DONE:
                    lifecycle.mark_as_filled(signal['id'], exec_res.order)
                    executed_count += 1
                    push_event("EXECUTADO", f"{symbol} {trade_type} @ {price:.5f}  pos:{exec_res.order}")
                    logger.trade("order_executed",
                        f"{symbol} {trade_type} @ {price:.5f} | Position: {exec_res.order}",
                        symbol=symbol,
                        data={"position_id": exec_res.order, "price": price, "type": trade_type}
                    )
                else:
                    error_msg = f"MT5 retcode={exec_res.retcode}, comment={exec_res.comment}"
                    lifecycle.mark_as_error(signal['id'], error_msg)
                    logger.error("order_failed", f"{symbol} {trade_type}: {error_msg}", symbol=symbol)

            except Exception as e:
                print(f"[ERROR] Erro ao executar sinal {signal.get('id')}: {e}")
                lifecycle.mark_as_error(signal['id'], str(e))

        return executed_count

    except Exception as e:
        print(f"[ERROR] Erro ao buscar sinais aprovados: {e}")
        return 0

def _merge_zone_list(zones, threshold):
    """Mescla zonas com preços muito próximos, fazendo média dos preços."""
    if not zones:
        return []
    sorted_z = sorted(zones, key=lambda z: z['price'])
    merged = [dict(sorted_z[0])]
    for z in sorted_z[1:]:
        if z['price'] - merged[-1]['price'] <= threshold:
            merged[-1]['price'] = (merged[-1]['price'] + z['price']) / 2
        else:
            merged.append(dict(z))
    return merged


def export_zones_to_mt5(symbol, zones, pnl_session, pnl_total, current_price):
    """
    Exporta zonas para o MT5 com merge de proximidade, ordenação e limite de 6 por lado.
    Inclui linha BOT_STATUS para o painel do indicador.
    """
    file_path = os.path.join(MT5_DATA_PATH, "MQL5", "Files", f"liquidez_data_{symbol}.csv")

    info = mt5.symbol_info(symbol)
    if info is None:
        return
    pip_size = info.point * 10
    merge_threshold = 15 * pip_size

    # Separar por tipo (todas as zonas detectadas — sem filtro de consumo)
    resistances = []
    supports    = []
    for z in zones:
        if z['type'] == 'RESISTANCE':
            resistances.append(z)
        else:
            supports.append(z)

    # Mesclar zonas próximas
    resistances = _merge_zone_list(resistances, merge_threshold)
    supports    = _merge_zone_list(supports,    merge_threshold)

    # Ordenar por proximidade ao preço atual e limitar a 6 por lado
    resistances.sort(key=lambda z: abs(z['price'] - current_price))
    supports.sort(   key=lambda z: abs(z['price'] - current_price))
    resistances = resistances[:6]
    supports    = supports[:6]

    def _fmt_time(t):
        # MQL5 StringToTime exige formato "YYYY.MM.DD HH:MM:SS" com pontos
        if hasattr(t, 'strftime'):
            return t.strftime("%Y.%m.%d %H:%M:%S")
        return str(t).replace("-", ".").replace("T", " ").split(".")[0]

    try:
        with open(file_path, "w", encoding="ansi") as f:
            f.write("HEADER\n")
            f.write(f"BOT_STATUS,{pnl_session:.2f},{pnl_total:.2f},0\n")
            for z in resistances:
                f.write(f"ZONE_RESISTANCE,{z['price']:.5f},{_fmt_time(z['time'])}\n")
            for z in supports:
                f.write(f"ZONE_SUPPORT,{z['price']:.5f},{_fmt_time(z['time'])}\n")
            # Exportar posições com SL em breakeven para visualização no MT5
            positions = mt5.positions_get(symbol=symbol) or []
            for pos in positions:
                if pos.magic != MAGIC_NUMBER or pos.sl == 0.0:
                    continue
                pt = info.point
                is_buy = (pos.type == mt5.POSITION_TYPE_BUY)
                # Detecta BE: SL dentro de 5 pontos da entrada (margem p/ float)
                at_be = (is_buy     and pos.sl >= pos.price_open - 5 * pt) or \
                        (not is_buy and pos.sl <= pos.price_open + 5 * pt)
                if at_be:
                    ttype = "BUY" if is_buy else "SELL"
                    f.write(f"BREAKEVEN,{pos.price_open:.5f},{ttype}\n")
    except Exception:
        pass


def main():
    """Loop principal do bot."""
    if not initialize_mt5():
        logger.error("mt5_init_failed", "Não foi possível conectar ao MT5")
        return

    logger.info("bot_started", f"Bot v6.1.5 iniciado | {len(CFG['symbols'])} símbolos | Magic: {MAGIC_NUMBER} | trend={'ON' if USE_TREND_FILTER else 'OFF'} reversal={'ON' if REQUIRE_REVERSAL else 'OFF'} | TZ=UTC{'+' if CFG.get('mt5_server_utc_offset',3)>=0 else ''}{CFG.get('mt5_server_utc_offset',3)}")
    push_event("INICIO", f"Bot v6.1.5 conectado | {len(CFG['symbols'])} pares | Magic {MAGIC_NUMBER}")

    trade_executed_this_cycle = False

    try:
        while True:
            # Poda dedup in-memory (v6.1.5)
            prune_sent_signals()

            # Sincronizar posições abertas
            sync_open_positions()

            # Mover SL para breakeven se configurado
            check_breakeven()

            # Executar sinais aprovados pela War Room
            execute_approved_signals()

            # Calcular P&L
            pnl_session = get_session_pnl()
            pnl_total   = get_account_pnl()

            # Heartbeat para o dashboard
            send_heartbeat(pnl_session, pnl_total, 0)

            # Exibir dashboard no terminal
            print_dashboard(pnl_session, pnl_total)

            # Verificar stop loss diário
            daily_max = CFG.get('daily_max_loss', 350.0)
            if pnl_session <= -daily_max:
                logger.error("daily_stop_hit",
                    f"Stop Loss diário atingido: ${pnl_session:.2f} (limite: -${daily_max:.2f})",
                    data={"pnl_session": pnl_session}
                )
                push_event("STOP", f"Stop loss diario atingido! P&L sessao: ${pnl_session:.2f}")
                break

            # Verificar meta de lucro diário
            if pnl_session >= DAILY_PROFIT_TARGET:
                logger.info("daily_target_hit",
                    f"Meta diária atingida: ${pnl_session:.2f} (meta: ${DAILY_PROFIT_TARGET:.2f})",
                    data={"pnl_session": pnl_session}
                )
                push_event("META", f"Meta diaria atingida! P&L sessao: ${pnl_session:.2f}")
                break

            # Resetar flag de trade executado
            trade_executed_this_cycle = False

            # Processar cada símbolo
            for symbol in CFG['symbols']:
                # Verificar se já tem posição aberta
                all_pos = mt5.positions_get(symbol=symbol)
                pos = [p for p in (all_pos or []) if p.magic == MAGIC_NUMBER]

                if pos:
                    continue  # Já tem posição aberta, pular

                # Buscar dados
                df_m15 = get_rates(symbol, mt5.TIMEFRAME_M15, LOOKBACK_ZONES)
                if df_m15 is None:
                    continue

                zones = get_validated_zones(df_m15, mt5.symbol_info(symbol).point)
                df_h1 = get_rates(symbol, mt5.TIMEFRAME_H1, 50)

                # Verificar trigger
                trigger, z_trig = check_trigger(
                    symbol, df_m15, zones,
                    mt5.symbol_info(symbol).point,
                    df_h1
                )

                # Executar trade se trigger válido
                if trigger and not trade_executed_this_cycle:
                    # v6.1.5: dedup — não reenviar o mesmo sinal da mesma vela M15
                    dedup_key = (trigger['symbol'], trigger['type'], trigger['trigger_time'])
                    if dedup_key in sent_signals:
                        continue

                    try:
                        # ETAPA 1: Criar sinal detectado
                        signal = lifecycle.create_signal(
                            symbol=trigger['symbol'],
                            trade_type=trigger['type'],
                            price=trigger['price'],
                            sl=trigger['sl'],
                            tp=trigger['tp'],
                            wick_pct=trigger['wick_pct'],
                            magic_number=MAGIC_NUMBER
                        )

                        if not signal:
                            push_event("ERRO", f"Falha ao criar sinal para {symbol}")
                            continue

                        # ETAPA 2: Enviar para War Room (awaiting_consensus)
                        lifecycle.transition_to_awaiting_consensus(signal['id'])
                        sent_signals.add(dedup_key)  # Marca vela como já-enviada
                        push_event("SINAL", f"{symbol} {trigger['type']} @ {trigger['price']:.5f}  pavio {trigger['wick_pct']*100:.0f}%  -> War Room")
                        logger.signal("signal_detected",
                            f"{symbol} {trigger['type']} @ {trigger['price']:.5f} | Pavio: {trigger['wick_pct']*100:.0f}% | -> War Room",
                            symbol=symbol,
                            data={"type": trigger['type'], "price": trigger['price'],
                                  "sl": trigger['sl'], "tp": trigger['tp'], "wick_pct": trigger['wick_pct']}
                        )

                        trade_executed_this_cycle = True  # Apenas 1 sinal por ciclo

                    except Exception as e:
                        push_event("ERRO", f"{symbol} excecao: {e}")
                        logger.error("signal_exception", str(e), symbol=symbol)

                # Exportar zonas para MT5 com merge e limite
                tick = mt5.symbol_info_tick(symbol)
                current_price = tick.bid if tick else (zones[0]['price'] if zones else 0)
                export_zones_to_mt5(symbol, zones, pnl_session, pnl_total, current_price)

            # Aguardar próximo ciclo
            time.sleep(20)

    finally:
        mt5.shutdown()
        print("\n  Bot encerrado.")

if __name__ == "__main__":
    main()
