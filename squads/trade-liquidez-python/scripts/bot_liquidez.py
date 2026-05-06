"""
Bot de Trading - Liquidez v6.2.0-ict (Sprint 1 — Limpeza + Gates ICT)
=======================================================================
Integração com TradeLifecycleManager para gerenciamento de estados.

Fluxo de Estados:
1. signal_detected    - Sinal técnico detectado
2. approved           - Auto-aprovado (ou via war room)
3. filled             - Ordem executada no MT5
4. open               - Posição ativa
5. closed             - Trade finalizado com P&L

Mudanças v6.2.0 — Sprint 1 (2026-04-28):
- REMOVIDO dead code: SLOPE_THRESHOLD_PIPS, USE_TREND_FILTER, REQUIRE_REVERSAL.
  Esses filtros foram desativados nas Fases 1+2 (v6.1.1) e nunca reativados —
  carregavam-se apenas no path morto. Limpeza completa para legibilidade.
- ADICIONADO gates de horário (não score) baseado no Daily Range Algorithm ICT:
    * entry_cutoff_hour_mt5 (default 22 = 19 UTC) — pausa entradas no end-of-day
    * news_embargo_pause (13:00-14:00 UTC = 16:00-17:00 MT5) — janela conservadora
      cobrindo o release NY 8-8:30 + reaction.
- BE migrado conceptualmente para o Exit War Room (Sprint 4 — fica no roadmap).
  check_breakeven() continua existindo aqui mas com BREAKEVEN_CANDLES=0 (off).

Mudanças v6.1.5 (2026-04-23):
- Dedup in-memory por (symbol, type, trigger_candle_time) — set() reset a cada
  reinício; evita reenviar mesmo sinal da mesma vela M15 a cada ciclo de 20s.

Mudanças v6.1.4 (2026-04-22):
- Removidos: Kill-Zone, One-Shot de zonas, trava por vela persistida.

Mudanças v6.1.3 (2026-04-22):
- RSI(9) default, stop_buffer 50, scoring War Room reformado (5 critérios).

Mudanças v6.0:
- TradeLifecycleManager para todos os estados.
- position_id como chave única.
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

# v6.2.0 Sprint 5 — Rolling log persistente.
# maxlen 10 -> 50 (mais histórico no terminal). cls removido do dashboard.
# Cada evento também é escrito em data/terminal_logs/BOT_YYYYMMDD.log para auditoria.
recent_events: deque = deque(maxlen=50)

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

# v6.2.0 Sprint 2 — ICT Context Engine (cache de 5min compartilhado com War Room)
import sys
sys.path.insert(0, os.path.dirname(__file__))
from ict_context_engine import get_context as ict_get_context

# v6.2.0 Sprint 5 — Persistência de rolling log local
from terminal_log_writer import TerminalLogWriter

# v6.2.0 Sprint 6 — Cooldown direcional pós-loss
from cooldown_manager import CooldownManager

lifecycle = TradeLifecycleManager()
logger = SystemLogger("BOT")
terminal_log = TerminalLogWriter("BOT")
cooldown_mgr = CooldownManager()

# Configurações Globais
MAGIC_NUMBER        = CFG['magic_number']
STOP_BUFFER         = CFG['stop_buffer_points']
MIN_WICK_PCT        = CFG.get('min_wick_pct', 0.30)
RSI_OVERBOUGHT      = CFG.get('rsi_overbought', 70)
RSI_OVERSOLD        = CFG.get('rsi_oversold', 30)
RSI_PERIOD          = CFG.get('rsi_period', 14)  # v6.2.0 Sprint 6: 9 -> 14 (Wilder default, alinha com MT5)
RR_RATIO            = CFG.get('risk_reward_ratio', 1.5)
LOOKBACK_ZONES      = CFG.get('lookback_zones', 100)
MIN_DISPLACEMENT    = CFG.get('min_displacement_candles', 7)
DAILY_PROFIT_TARGET = CFG.get('daily_profit_target', 500.0)
BREAKEVEN_CANDLES   = CFG.get('breakeven_candles', 0)   # 0 = desativado (BE migrou para Exit War Room — Sprint 4)
BREAKEVEN_BUFFER_PT = 2                                  # pontos acima/abaixo da entrada

# v6.2.0 Sprint 1 — Gates de horário ICT (não score, são gates explícitos)
MT5_UTC_OFFSET            = int(CFG.get('mt5_server_utc_offset', 3))
ENTRY_CUTOFF_HOUR_MT5     = int(CFG.get('entry_cutoff_hour_mt5', 22))   # 22 MT5 = 19 UTC
NEWS_EMBARGO_PAUSE        = bool(CFG.get('news_embargo_pause', True))
NEWS_EMBARGO_START_UTC    = int(CFG.get('news_embargo_start_utc', 13))
NEWS_EMBARGO_END_UTC      = int(CFG.get('news_embargo_end_utc', 14))

# v6.2.0 Sprint 5 — Filtro de range mínimo da vela do gatilho.
# Evita gatilhos em Asia early com vela de range minúsculo (~1.5 pips) onde
# RSI torna-se errático e estratégia perde edge. 0 = sem filtro.
MIN_CANDLE_RANGE_PIPS     = float(CFG.get('min_candle_range_pips', 3.0))

# Timezone MT5 server — usado em todos os timestamps de log do terminal
# para que a hora do sinal case com o chart da corretora.
_MT5_TZ = timezone(timedelta(hours=MT5_UTC_OFFSET))

def mt5_time_str(fmt="%H:%M:%S"):
    """Hora formatada no fuso do servidor MT5 (o mesmo do chart)."""
    return datetime.now(_MT5_TZ).strftime(fmt)


def is_entry_blocked_by_time():
    """
    Gate de horário ICT (v6.2.0 Sprint 1).
    Retorna (blocked: bool, reason: str | None).

    Bloqueios:
      1. News embargo: NY 8:00-8:30 (= 13:00-14:00 UTC default, janela conservadora
         de 1h cobrindo o release + reaction). Pode ser estreitada para 13:30 depois
         de validar.
      2. End-of-day cutoff: hora MT5 >= ENTRY_CUTOFF_HOUR_MT5 (default 22 = 19 UTC).
         ICT Aula 2: end-of-day consolidation começa após NY core. Estratégia
         contra-tendência tem edge marginal aqui.

    Posições já abertas continuam sob gestão (não são fechadas pelo gate).
    """
    now_utc = datetime.now(timezone.utc)
    now_mt5 = datetime.now(_MT5_TZ)

    if NEWS_EMBARGO_PAUSE and NEWS_EMBARGO_START_UTC <= now_utc.hour < NEWS_EMBARGO_END_UTC:
        return True, f"news_embargo (UTC {now_utc.hour:02d}:xx — janela {NEWS_EMBARGO_START_UTC:02d}-{NEWS_EMBARGO_END_UTC:02d})"

    if now_mt5.hour >= ENTRY_CUTOFF_HOUR_MT5:
        return True, f"end_of_day_cutoff (MT5 {now_mt5.hour:02d}:xx >= {ENTRY_CUTOFF_HOUR_MT5:02d})"

    return False, None


def is_entry_blocked_by_ict_cliff(symbol: str, trade_type: str):
    """
    Gate ICT CLIFF (v6.2.0 Sprint 2).
    Bloqueia entradas em cenário catastrófico onde trade vai contra D1 bias E
    H4 está em expansion contrária forte (alignment_score == 0/25).

    Cache de 5min do ict_context_engine evita refetch — bot e war room
    compartilham. Custo: 1 chamada MT5 por par a cada 5min na pior hipótese.

    Retorna (blocked: bool, reason: str | None).

    Esse gate complementa o REJEITADO_CLIFF do War Room (defesa em camadas):
    - Bot bloqueia primeiro → não cria sinal nem polui War Room
    - War Room rejeita se chegou até lá (caso bot tenha cache stale)
    """
    try:
        ctx = ict_get_context(symbol, mt5_module=mt5)
        if not ctx.get('ok'):
            return False, None  # contexto indisponível — não bloqueia (default seguro)
        score = ctx['trade_alignment_score'](trade_type)
        if score == 0:
            explain = ctx['trade_alignment_explain'](trade_type)
            return True, f"ict_cliff ({explain})"
    except Exception:
        return False, None
    return False, None


# Diretório MT5 Files
MT5_DATA_PATH = r"C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"


def initialize_mt5():
    """Inicializa conexão com MT5."""
    if not mt5.initialize():
        # v6.2.0 Sprint 5: usa logger (vai pro Supabase) — antes era print direto que sumia
        logger.error("mt5_init_failed", "Falha ao conectar MT5 (initialize() retornou False)")
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
    """
    RSI com Wilder's Smoothing (SMMA) — alinhado com MetaTrader 5 default.

    Fix v6.2.0 Sprint 5: antes usava SMA simples em rolling window, o que
    causava divergência de 20-30 pontos vs MT5 chart após velas com spike
    (entrada/saída brusca da janela rolling). Wilder's suaviza progressivamente:

        gain_avg[i] = ((gain_avg[i-1] * (period-1)) + gain[i]) / period

    Equivalente a EMA com alpha = 1/period. Pandas implementa via
    `.ewm(alpha=1/period, adjust=False)`.

    Default lido do config (`rsi_period`, v6.2.0 Sprint 6 = 14, alinhado com MT5).
    """
    if period is None:
        period = RSI_PERIOD
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    # Wilder's smoothing (SMMA) via EWM
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def check_trigger(symbol, df_m15, zones, point, df_h1=None):
    """
    Verifica se há gatilho Sniper válido usando os parâmetros do config.yaml.
    Retorna: (trigger_data, zone) ou (None, None).

    Gates aplicados (v6.2.0):
      1. Sprint 1 — is_entry_blocked_by_time() — news embargo + end-of-day cutoff
      2. Dados M15 mínimos (15 velas) e zonas detectadas
      3. Gatilho técnico (wick + RSI extremo + zona tocada)
      4. Sprint 2 — is_entry_blocked_by_ict_cliff() — bloqueia se ICT alignment = 0/25
         (trade contra D1 bias + H4 expansion contrária = cliff)

    Filtros desativados/removidos:
      - Slope MA20 H1 (v6.1.1) — desativado, código removido em v6.2.0
      - Color reversal (v6.1.1) — desativado, código removido em v6.2.0
    """
    # Gate 1 — horário (não consome computação se já fora de janela)
    blocked, _reason = is_entry_blocked_by_time()
    if blocked:
        return None, None

    if df_m15 is None or len(df_m15) < 15 or not zones:
        return None, None

    df_m15['rsi'] = calculate_rsi(df_m15['close'])
    last = df_m15.iloc[-2]
    rsi = df_m15['rsi'].iloc[-2]

    total, top, bot_wick = calculate_wick_metrics(last)

    # v6.2.0 Sprint 5 — metadados da vela para auditoria
    pip_size = point * 10 if point > 0 else 0.0001
    candle_range_pips = total / pip_size if pip_size > 0 else 0
    candle_body = abs(last['close'] - last['open'])
    candle_body_ratio = (candle_body / total) if total > 0 else 1.0

    # v6.2.0 Sprint 5 — Filtro de range mínimo da vela (evita Asia early com 1.5p)
    if MIN_CANDLE_RANGE_PIPS > 0 and candle_range_pips < MIN_CANDLE_RANGE_PIPS:
        # Não loga warning a cada miss — apenas retorna. Vela morta é frequente.
        return None, None

    # Função interna pra evitar duplicação (DRY): checa ICT cliff E cooldown antes de retornar
    def _gate_cliff_ok(trade_type: str) -> bool:
        # 1) ICT cliff (Sprint 2)
        cliff_blocked, cliff_reason = is_entry_blocked_by_ict_cliff(symbol, trade_type)
        if cliff_blocked:
            push_event("ICT_CLIFF", f"{symbol} {trade_type} BLOQUEADO: {cliff_reason}")
            logger.warning("ict_cliff_block",
                           f"{symbol} {trade_type} bloqueado: {cliff_reason}",
                           symbol=symbol, data={"reason": cliff_reason})
            return False
        # 2) Cooldown direcional pós-loss (Sprint 6)
        cd_blocked, cd_until = cooldown_mgr.check(symbol, trade_type)
        if cd_blocked:
            remaining_min = int((cd_until - datetime.now(timezone.utc)).total_seconds() / 60)
            push_event("COOLDOWN", f"{symbol} {trade_type} BLOQUEADO: cooldown ativo ({remaining_min}min restantes)")
            logger.warning("cooldown_active",
                           f"{symbol} {trade_type} bloqueado por cooldown pós-loss "
                           f"(libera em {cd_until.isoformat()[:16]} = {remaining_min}min)",
                           symbol=symbol,
                           data={"cooldown_until": cd_until.isoformat(),
                                 "remaining_minutes": remaining_min})
            return False
        return True

    for z in zones:
        # SELL em RESISTÊNCIA
        if z['type'] == 'RESISTANCE' and \
           last['high'] >= z['price'] and \
           (top / total) >= MIN_WICK_PCT and \
           rsi >= RSI_OVERBOUGHT:

            if not _gate_cliff_ok('SELL'):
                return None, None

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
                # Sprint 5 — metadados RSI/vela
                'rsi_value': float(rsi) if not pd.isna(rsi) else 0.0,
                'candle_close': float(last['close']),
                'candle_range_pips': candle_range_pips,
                'candle_body_ratio': candle_body_ratio,
            }, z

        # BUY em SUPORTE
        elif z['type'] == 'SUPPORT' and \
             last['low'] <= z['price'] and \
             (bot_wick / total) >= MIN_WICK_PCT and \
             rsi <= RSI_OVERSOLD:

            if not _gate_cliff_ok('BUY'):
                return None, None

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
                # Sprint 5 — metadados RSI/vela
                'rsi_value': float(rsi) if not pd.isna(rsi) else 0.0,
                'candle_close': float(last['close']),
                'candle_range_pips': candle_range_pips,
                'candle_body_ratio': candle_body_ratio,
            }, z

    return None, None

def push_event(tag: str, msg: str):
    """
    Adiciona evento ao rolling log do terminal (deque de 50) E escreve no arquivo
    persistente data/terminal_logs/BOT_YYYYMMDD.log.

    v6.2.0 Sprint 5: persistência local independente do Supabase. Permite auditar
    erros transitórios e reconstruir cronologia mesmo sem rede.
    """
    ts = mt5_time_str("%H:%M:%S")
    line = f"{ts}  {tag:<10}  {msg}"
    recent_events.append(line)
    terminal_log.append(line)

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

    # v6.2.0 Sprint 5: cls mantido (terminal limpo a cada refresh é mais legível),
    # MAS o deque agora tem 50 eventos (vs 10 antes) E todo evento é escrito em
    # data/terminal_logs/BOT_YYYYMMDD.log permanentemente.
    # Para auditar erros transitórios: tail -f data/terminal_logs/BOT_<dia>.log
    os.system('cls' if os.name == 'nt' else 'clear')
    sep  = "=" * W
    dash = "-" * W
    now  = mt5_time_str("%H:%M:%S")

    print(sep)
    tz_offset = MT5_UTC_OFFSET
    tz_sign = "+" if tz_offset >= 0 else ""
    blocked, blk_reason = is_entry_blocked_by_time()
    gate_state = f"BLOCKED ({blk_reason})" if blocked else "OPEN"
    print(f"  BOT LIQUIDEZ v6.2.0-ict  |  {now} MT5 (UTC{tz_sign}{tz_offset:02d})  |  {len(CFG['symbols'])} pares  |  Magic {MAGIC_NUMBER}")
    print(f"  Filtros: wick>={MIN_WICK_PCT*100:.0f}%  RSI({RSI_PERIOD}) {RSI_OVERSOLD}/{RSI_OVERBOUGHT}")
    print(f"  Gate de horario: {gate_state}  |  cutoff MT5={ENTRY_CUTOFF_HOUR_MT5}h  embargo UTC={NEWS_EMBARGO_START_UTC}-{NEWS_EMBARGO_END_UTC}h")
    print(sep)
    print(f"  P&L SESSAO : ${pnl_ses_sign}{pnl_session:.2f}".ljust(36) + f"  P&L TOTAL  : ${pnl_total_sign}{pnl_total:.2f}")
    print(f"  STOP DIARIO: [{bar}] {remaining_pct:.0f}% restante  (limite ${daily_limit:.0f})")
    print(dash)
    print(f"  POSICOES ABERTAS: {open_count}")

    # v6.2.0 Sprint 6 — Cooldowns direcionais ativos
    active_cd = cooldown_mgr.list_active()
    if active_cd:
        print(dash)
        print(f"  COOLDOWNS ATIVOS ({len(active_cd)}):")
        for sym, typ, until_dt, remaining in active_cd:
            print(f"    [BLOCK] {sym} {typ}  -> libera em {remaining}min")
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
        # v6.2.0 Sprint 5: persiste no Supabase em vez de print fugaz
        logger.warning("heartbeat_failed", f"Heartbeat falhou: {e}", data={"error": str(e)})

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
        logger.warning("sync_positions_failed", f"Erro ao sincronizar posições: {e}", data={"error": str(e)})

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

        # v6.2.0 Sprint 6 — Registra loss para cooldown direcional
        # Só ativa se loss > cooldown_min_loss_pnl (default -10 USD), evita BE-stops triviais
        cd_min_loss = float(CFG.get('cooldown_min_loss_pnl', -10.0))
        if pnl_real <= cd_min_loss:
            sym = trade.get('symbol')
            typ = trade.get('type')
            until_dt = cooldown_mgr.register_loss(sym, typ)
            cd_h = cooldown_mgr.cooldown_h
            push_event("COOLDOWN_ON",
                       f"{sym} {typ} loss ${pnl_real:.2f} -> cooldown {cd_h}h ativado (libera {until_dt.strftime('%H:%M UTC')})")
            logger.warning("cooldown_started",
                f"{sym} {typ} loss ${pnl_real:.2f} -> cooldown direcional ativado por {cd_h}h",
                symbol=sym,
                data={"position_id": position_id, "pnl": pnl_real,
                      "cooldown_until": until_dt.isoformat(), "cooldown_hours": cd_h})

    except Exception as e:
        logger.error("check_closed_error", f"Erro ao verificar fechamento: {e}",
                     data={"trade_id": trade.get('id')})

def check_breakeven():
    """
    [DEPRECATED v6.2.0 Sprint 4] BE legado por tempo simples.

    Substituído pelo Exit War Room (`exit_war_room.py`) que aplica regras
    dinâmicas multi-condicionais (1R/0.7R+reversal/0.5R+RSI). Mantido aqui
    apenas como guard rail: enquanto BREAKEVEN_CANDLES=0 no config, fica off.
    Não reativar — o Exit War Room é canonical.

    Move o SL para o preço de entrada (+ buffer) quando:
      1. breakeven_candles > 0 no config.yaml  (feature ativa)
      2. Trade 'open' completou >= breakeven_candles velas M15 desde filled_at
      3. Preço atual está favorável (trade em lucro)
      4. SL ainda está do lado de risco (não foi movido antes)
    """
    if BREAKEVEN_CANDLES <= 0:
        return  # DESATIVADO desde Sprint 4 (BE migrou para Exit War Room)

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
                logger.error("execute_signal_failed",
                             f"Erro ao executar sinal {signal.get('id')}: {e}",
                             data={"signal_id": signal.get('id'), "error": str(e)})
                lifecycle.mark_as_error(signal['id'], str(e))

        return executed_count

    except Exception as e:
        logger.error("fetch_approved_failed",
                     f"Erro ao buscar sinais aprovados: {e}",
                     data={"error": str(e)})
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


def _current_session_label_utc():
    """
    Retorna (id, label, weight) da janela ICT atual baseado na hora UTC.
    Usado pelo export_zones_to_mt5 para o painel do indicador.
    """
    sw = CFG.get('session_windows', {}) or {}
    h_utc = datetime.now(timezone.utc).hour
    for sid, win in sw.items():
        start = int(win.get('start', 0))
        end   = int(win.get('end', 0))
        if start < end and start <= h_utc < end:
            return sid, str(win.get('label', sid)), int(win.get('weight', 0))
    return "unknown", "Fora de sessao", 0


def export_zones_to_mt5(symbol, zones, pnl_session, pnl_total, current_price):
    """
    Exporta dados para o MT5 — lido pelo IndicadorLiquidez.mq5.

    v6.2.0 Sprint 5+ — formato CSV ampliado para refletir Sprints 1-5:
      HEADER
      VERSION,v6.2.0-ict
      BOT_STATUS,pnl_session,pnl_total,0
      GATE,<blocked 0|1>,<reason>           Sprint 1 — gate de horário/embargo
      SESSION,<id>,<label>,<weight_pts>     Sprint 1 — janela ICT atual
      ICT_BIAS,<direction>,<h4>,<h1>,<state>,<buy_pts>,<sell_pts>   Sprint 2
      LIQ_ABOVE,<price>,<kind>,<dist_pips>  Sprint 2 — proxima liquidez above
      LIQ_BELOW,<price>,<kind>,<dist_pips>  Sprint 2 — proxima liquidez below
      ZONE_RESISTANCE,price,time            (legado) zonas detectadas
      ZONE_SUPPORT,price,time
      POSITION,<type>,<profit_R>,<candles>,<sl>,<tp>   Sprint 4 — pos aberta
      BREAKEVEN,price,type                  (legado) marca SL no BE

    Cada par tem CSV próprio: liquidez_data_<symbol>.csv
    """
    file_path = os.path.join(MT5_DATA_PATH, "MQL5", "Files", f"liquidez_data_{symbol}.csv")

    info = mt5.symbol_info(symbol)
    if info is None:
        return
    point = info.point
    pip_size = point * 10
    merge_threshold = 15 * pip_size

    # Separar zonas por tipo
    resistances = [z for z in zones if z['type'] == 'RESISTANCE']
    supports    = [z for z in zones if z['type'] != 'RESISTANCE']

    # Mesclar e limitar (mesmo comportamento legado)
    resistances = _merge_zone_list(resistances, merge_threshold)
    supports    = _merge_zone_list(supports,    merge_threshold)
    resistances.sort(key=lambda z: abs(z['price'] - current_price))
    supports.sort(   key=lambda z: abs(z['price'] - current_price))
    resistances = resistances[:6]
    supports    = supports[:6]

    def _fmt_time(t):
        # MQL5 StringToTime exige formato "YYYY.MM.DD HH:MM:SS" com pontos
        if hasattr(t, 'strftime'):
            return t.strftime("%Y.%m.%d %H:%M:%S")
        return str(t).replace("-", ".").replace("T", " ").split(".")[0]

    def _csv_safe(s):
        """Remove vírgulas/quebras pra não quebrar o parser CSV do MQL5."""
        return str(s).replace(",", ";").replace("\n", " ").replace("\r", " ")

    # ── Coletar contexto ampliado (Sprints 1-5) ──

    # Gate de horário (Sprint 1)
    blocked, reason = is_entry_blocked_by_time()
    gate_blocked = 1 if blocked else 0
    gate_reason  = _csv_safe(reason) if reason else "open"

    # Sessão ICT atual (Sprint 1)
    sess_id, sess_label, sess_weight = _current_session_label_utc()

    # ICT context do par (Sprint 2) — usa cache compartilhado
    try:
        ict_ctx = ict_get_context(symbol, mt5_module=mt5)
    except Exception:
        ict_ctx = {'ok': False}

    if ict_ctx.get('ok'):
        bias = ict_ctx.get('daily_bias', 'neutral')
        h4_phase = ict_ctx.get('h4_phase')
        h1_phase = ict_ctx.get('h1_phase')
        h4_str = (f"{h4_phase.phase}/{h4_phase.direction}" if h4_phase else "?")
        h1_str = (f"{h1_phase.phase}/{h1_phase.direction}" if h1_phase else "?")
        daily_state = ict_ctx.get('daily_range_state', 'unknown')
        try:
            buy_pts  = int(ict_ctx['trade_alignment_score']('BUY'))
            sell_pts = int(ict_ctx['trade_alignment_score']('SELL'))
        except Exception:
            buy_pts, sell_pts = 12, 12

        liq_above = ict_ctx.get('next_liquidity_above')
        liq_below = ict_ctx.get('next_liquidity_below')
        liq_above_data = (
            (liq_above.price, liq_above.kind, ict_ctx.get('above_distance_pips', 0))
            if liq_above else None
        )
        liq_below_data = (
            (liq_below.price, liq_below.kind, ict_ctx.get('below_distance_pips', 0))
            if liq_below else None
        )
    else:
        bias, h4_str, h1_str, daily_state = "neutral", "?", "?", "unknown"
        buy_pts, sell_pts = 12, 12
        liq_above_data = liq_below_data = None

    # Posições abertas no par (Sprint 4) — calcula profit_R e candles open
    positions = mt5.positions_get(symbol=symbol) or []
    open_positions_data = []
    breakeven_data = []
    for pos in positions:
        if pos.magic != MAGIC_NUMBER:
            continue
        is_buy = (pos.type == mt5.POSITION_TYPE_BUY)
        ttype = "BUY" if is_buy else "SELL"

        # profit_R — só calcula se SL existe
        if pos.sl > 0:
            risk_pips   = abs(pos.price_open - pos.sl) / pip_size if pip_size > 0 else 0
            profit_pips = ((pos.price_current - pos.price_open) if is_buy
                           else (pos.price_open - pos.price_current)) / pip_size if pip_size > 0 else 0
            profit_R = (profit_pips / risk_pips) if risk_pips > 0 else 0.0
        else:
            profit_R = 0.0

        # Candles abertos (aproximado pelo time da posição)
        try:
            elapsed_s = (datetime.now(timezone.utc).timestamp() - pos.time)
            candles_open = int(elapsed_s / (15 * 60))
        except Exception:
            candles_open = 0

        open_positions_data.append((ttype, profit_R, candles_open, pos.sl, pos.tp))

        # BE marker (legado mantido pra compatibilidade visual)
        at_be = (is_buy     and pos.sl >= pos.price_open - 5 * point) or \
                (not is_buy and pos.sl <= pos.price_open + 5 * point)
        if at_be and pos.sl != 0.0:
            breakeven_data.append((pos.price_open, ttype))

    # ── Escreve CSV ──
    try:
        with open(file_path, "w", encoding="ansi") as f:
            f.write("HEADER\n")
            f.write("VERSION,v6.2.0-ict\n")
            f.write(f"BOT_STATUS,{pnl_session:.2f},{pnl_total:.2f},0\n")
            f.write(f"GATE,{gate_blocked},{gate_reason}\n")
            f.write(f"SESSION,{sess_id},{_csv_safe(sess_label)},{sess_weight}\n")
            f.write(f"ICT_BIAS,{bias},{h4_str},{h1_str},{daily_state},{buy_pts},{sell_pts}\n")
            if liq_above_data:
                p, k, d = liq_above_data
                f.write(f"LIQ_ABOVE,{p:.5f},{k},{d:.1f}\n")
            if liq_below_data:
                p, k, d = liq_below_data
                f.write(f"LIQ_BELOW,{p:.5f},{k},{d:.1f}\n")
            for z in resistances:
                f.write(f"ZONE_RESISTANCE,{z['price']:.5f},{_fmt_time(z['time'])}\n")
            for z in supports:
                f.write(f"ZONE_SUPPORT,{z['price']:.5f},{_fmt_time(z['time'])}\n")
            for ttype, profit_R, candles, sl, tp in open_positions_data:
                f.write(f"POSITION,{ttype},{profit_R:+.2f},{candles},{sl:.5f},{tp:.5f}\n")
            for be_price, ttype in breakeven_data:
                f.write(f"BREAKEVEN,{be_price:.5f},{ttype}\n")
    except Exception:
        pass


def main():
    """Loop principal do bot."""
    if not initialize_mt5():
        logger.error("mt5_init_failed", "Não foi possível conectar ao MT5")
        return

    sym_list = ",".join(CFG['symbols'])
    logger.info(
        "bot_started",
        f"Bot v6.2.0-ict iniciado | {len(CFG['symbols'])} simbolos [{sym_list}] | Magic: {MAGIC_NUMBER} | "
        f"cutoff_mt5={ENTRY_CUTOFF_HOUR_MT5}h | embargo_utc={NEWS_EMBARGO_START_UTC}-{NEWS_EMBARGO_END_UTC}h | "
        f"TZ=UTC{'+' if MT5_UTC_OFFSET>=0 else ''}{MT5_UTC_OFFSET}"
    )
    push_event("INICIO", f"Bot v6.2.0-ict conectado | {len(CFG['symbols'])} pares | Magic {MAGIC_NUMBER}")

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

                # Verificar trigger (df_h1 não é mais necessário — Slope MA20 H1 removido v6.2.0)
                trigger, z_trig = check_trigger(
                    symbol, df_m15, zones,
                    mt5.symbol_info(symbol).point
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
                        push_event("SINAL", f"{symbol} {trigger['type']} @ {trigger['price']:.5f}  pavio {trigger['wick_pct']*100:.0f}%  RSI({RSI_PERIOD})={trigger.get('rsi_value', 0):.1f}  -> War Room")

                        # v6.2.0 Sprint 5: metadados completos do RSI no log estruturado
                        # — permite auditoria cruzada com chart MT5 sem ambiguidade.
                        log_data = {
                            "type": trigger['type'],
                            "price": trigger['price'],
                            "sl": trigger['sl'],
                            "tp": trigger['tp'],
                            "wick_pct": trigger['wick_pct'],
                            # RSI metadata (Sprint 5)
                            "rsi_period": RSI_PERIOD,
                            "rsi_value": round(trigger.get('rsi_value', 0), 2),
                            "rsi_method": "Wilder_SMMA",   # alinhado com MT5 default
                            # Vela do gatilho
                            "candle_time_mt5": str(trigger.get('trigger_time', '')),
                            "candle_close": trigger.get('candle_close', trigger['price']),
                            "candle_range_pips": round(trigger.get('candle_range_pips', 0), 2),
                            "candle_body_ratio": round(trigger.get('candle_body_ratio', 0), 3),
                        }
                        logger.signal("signal_detected",
                            f"{symbol} {trigger['type']} @ {trigger['price']:.5f} | "
                            f"Pavio: {trigger['wick_pct']*100:.0f}% | RSI({RSI_PERIOD},Wilder)={trigger.get('rsi_value', 0):.1f} | "
                            f"vela {trigger.get('trigger_time','')} range={trigger.get('candle_range_pips',0):.1f}p | -> War Room",
                            symbol=symbol,
                            data=log_data
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
