"""
Exit War Room v6.2.0-ict (Sprint 4)
=======================================================================
4º processo do FULL_START.bat — monitora posições abertas em real-time
e aplica regras de saída inteligente baseadas em ICT context + price action.

Substitui o check_breakeven legado do bot (mantido desativado em config).

Fluxo (loop a cada monitor_interval_seconds, default 10s):
  1. Lista posições abertas com magic = MAGIC_NUMBER
  2. Para cada posição:
     a. Calcula profit em R (ratio risco/recompensa atingido)
     b. Conta candles abertos desde filled_at
     c. Busca contexto ICT atual via cache compartilhado
     d. Aplica regras a-f em ordem de prioridade

Regras (primeira que matchar vence):
  a) profit >= 1.0R                            -> BE imediato (sem condição extra)
  b) profit >= 0.7R + reversal ICT candle      -> close 50% + BE
  c) profit >= 0.5R + 3 candles + RSI cruzou   -> BE clássico
  d) profit > 0 + TP atingiu liquidity oposta  -> close cedo
  e) profit < 0 + ICT structure break contra   -> close imediato
  f) 6 candles sem progresso (range < 0.3R)    -> flag (não fecha)

Cada regra tem feature flag em config.yaml/exit_war_room.

NÃO modifica TP. Só altera SL (BE) ou volume (partial close) ou força close.
"""

import os
import sys
import time
import yaml
from collections import deque
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import Optional, List

import MetaTrader5 as mt5
import pandas as pd
from dotenv import load_dotenv

# Carregar credenciais
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv(os.path.join(project_root, ".env"))

# Carregar config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

# Importar módulos do projeto
sys.path.insert(0, os.path.dirname(__file__))
from trade_lifecycle_manager import TradeLifecycleManager
from system_logger import SystemLogger
from ict_context_engine import get_context as ict_get_context
from ict.structure import detect_swings, classify_structure
from terminal_log_writer import TerminalLogWriter

# ─── Configurações ──────────────────────────────────────────────────────────

MAGIC_NUMBER       = CFG['magic_number']
MT5_UTC_OFFSET     = int(CFG.get('mt5_server_utc_offset', 3))
RSI_PERIOD         = int(CFG.get('rsi_period', 14))  # v6.2.0 Sprint 6: 9 -> 14 (Wilder default, alinha com MT5)

EWR = CFG.get('exit_war_room', {}) or {}
ENABLE_BE_AT_1R           = bool(EWR.get('enable_be_at_1R', True))
ENABLE_PARTIAL_07R        = bool(EWR.get('enable_partial_at_07R_reversal', True))
ENABLE_CLASSIC_BE         = bool(EWR.get('enable_classic_be', True))
ENABLE_LIQUIDITY_CLOSE    = bool(EWR.get('enable_liquidity_target_close', True))
ENABLE_STRUCTURE_BREAK    = bool(EWR.get('enable_structure_break_close', True))
ENABLE_TIME_EXIT_FLAG     = bool(EWR.get('enable_time_exit_flag', True))
MONITOR_INTERVAL_S        = int(EWR.get('monitor_interval_seconds', 10))
PARTIAL_CLOSE_PCT         = float(EWR.get('partial_close_pct', 0.50))
BE_BUFFER_PIPS            = float(EWR.get('be_buffer_pips', 0.2))
TIME_EXIT_LOOKBACK        = int(EWR.get('time_exit_lookback_candles', 6))
TIME_EXIT_MIN_PROGRESS_R  = float(EWR.get('time_exit_min_progress_R', 0.3))

MT5_TZ = timezone(timedelta(hours=MT5_UTC_OFFSET))

# Diretório MT5 Files — onde o indicador lê os CSVs (mesmo path do bot_liquidez)
MT5_DATA_PATH = r"C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
MT5_FILES_DIR = os.path.join(MT5_DATA_PATH, "MQL5", "Files")

# ─── State / Inicialização ──────────────────────────────────────────────────

lifecycle = TradeLifecycleManager()
logger    = SystemLogger("EXIT_WR")
terminal_log = TerminalLogWriter("EXIT_WR")

# v6.2.0 Sprint 6 — Rolling log de eventos do exit war room (200 últimos).
# Aumentado de 50 para preservar mais histórico no terminal entre ciclos.
# Cada evento (BE moved, partial closed, snapshot, etc.) entra aqui E vai pro arquivo.
recent_events: deque = deque(maxlen=200)

# Marcadores em memória — evita reaplicar regra que já disparou
# Chave: position_id, valor: dict de flags (be_done, partial_done, time_flagged)
_position_state: dict = {}

# Mapping ticket -> symbol — usado para limpar exit_hint_<symbol>.csv quando
# posição fecha (ticket some das positions_get).
_ticket_to_symbol: dict = {}


def push_event(tag: str, msg: str):
    """Adiciona evento ao rolling log E escreve no arquivo persistente."""
    ts = mt5_time_str("%H:%M:%S")
    line = f"{ts}  {tag:<14}  {msg}"
    recent_events.append(line)
    terminal_log.append(line)


def mt5_time_str(fmt="%H:%M:%S") -> str:
    return datetime.now(MT5_TZ).strftime(fmt)


def initialize_mt5() -> bool:
    if not mt5.initialize():
        logger.error("mt5_init_failed", "Exit War Room: Falha ao conectar MT5 (initialize() retornou False)")
        return False
    return True


# ─── Helpers de cálculo ──────────────────────────────────────────────────────

def calculate_rsi_series(series: pd.Series, period: int = None) -> pd.Series:
    """
    RSI com Wilder's Smoothing (SMMA) — alinhado com MetaTrader 5 default.
    Fix v6.2.0 Sprint 5 (ver bot_liquidez.calculate_rsi para fundamentação).
    """
    if period is None:
        period = RSI_PERIOD
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def get_rates(symbol: str, timeframe, count: int) -> Optional[pd.DataFrame]:
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df


@dataclass
class PositionStats:
    """Estatísticas calculadas de uma posição aberta."""
    ticket: int
    symbol: str
    type: str               # 'BUY' | 'SELL'
    is_buy: bool
    volume: float
    entry: float
    current: float
    sl: float
    tp: float
    risk_pips: float
    profit_pips: float
    profit_R: float
    candles_open: int
    point: float
    pip_size: float
    filled_at: Optional[datetime] = None


def compute_stats(pos, trade_record: Optional[dict]) -> Optional[PositionStats]:
    """Computa stats de uma posição MT5 com base em (pos, trade_record do Supabase)."""
    info = mt5.symbol_info(pos.symbol)
    if info is None:
        return None
    point = float(info.point)
    pip_size = point * 10
    is_buy = (pos.type == mt5.POSITION_TYPE_BUY)

    risk_pips = abs(pos.price_open - pos.sl) / pip_size if pip_size > 0 and pos.sl > 0 else 0.0
    profit_pips = (
        (pos.price_current - pos.price_open) if is_buy else (pos.price_open - pos.price_current)
    ) / pip_size if pip_size > 0 else 0.0
    profit_R = (profit_pips / risk_pips) if risk_pips > 0 else 0.0

    # Candles abertos desde filled_at (se disponível no trade_record)
    candles_open = 0
    filled_at_dt = None
    if trade_record and trade_record.get('filled_at'):
        try:
            filled_at_dt = datetime.fromisoformat(
                trade_record['filled_at'].replace('Z', '+00:00')
            )
            elapsed_s = (datetime.now(timezone.utc) - filled_at_dt).total_seconds()
            candles_open = int(elapsed_s / (15 * 60))
        except Exception:
            candles_open = 0

    return PositionStats(
        ticket=pos.ticket, symbol=pos.symbol,
        type=('BUY' if is_buy else 'SELL'), is_buy=is_buy,
        volume=float(pos.volume),
        entry=float(pos.price_open), current=float(pos.price_current),
        sl=float(pos.sl), tp=float(pos.tp),
        risk_pips=risk_pips, profit_pips=profit_pips, profit_R=profit_R,
        candles_open=candles_open, point=point, pip_size=pip_size,
        filled_at=filled_at_dt,
    )


# ─── Helpers de modificação de posição ─────────────────────────────────────

def _modify_position_sltp(pos, new_sl: float, new_tp: Optional[float] = None) -> bool:
    """Modifica SL (e opcionalmente TP) de uma posição via TRADE_ACTION_SLTP."""
    info = mt5.symbol_info(pos.symbol)
    if info is None:
        return False
    request = {
        "action":   mt5.TRADE_ACTION_SLTP,
        "symbol":   pos.symbol,
        "position": pos.ticket,
        "sl":       round(new_sl, info.digits),
        "tp":       round(new_tp if new_tp is not None else pos.tp, info.digits),
    }
    result = mt5.order_send(request)
    return result is not None and result.retcode == mt5.TRADE_RETCODE_DONE


def _close_position(pos, volume: Optional[float] = None, comment: str = "EXIT_WR") -> bool:
    """Fecha posição (total se volume=None, parcial se volume<pos.volume)."""
    is_buy = (pos.type == mt5.POSITION_TYPE_BUY)
    tick = mt5.symbol_info_tick(pos.symbol)
    if tick is None:
        return False
    close_price = tick.bid if is_buy else tick.ask
    vol = float(volume) if volume is not None else float(pos.volume)
    request = {
        "action":   mt5.TRADE_ACTION_DEAL,
        "symbol":   pos.symbol,
        "position": pos.ticket,
        "volume":   vol,
        "type":     mt5.ORDER_TYPE_SELL if is_buy else mt5.ORDER_TYPE_BUY,
        "price":    close_price,
        "magic":    MAGIC_NUMBER,
        "comment":  comment[:31],
        "type_time":   mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    result = mt5.order_send(request)
    return result is not None and result.retcode == mt5.TRADE_RETCODE_DONE


def _be_sl_for(stats: PositionStats) -> float:
    """Calcula SL de breakeven com buffer."""
    buf = BE_BUFFER_PIPS * stats.pip_size
    return stats.entry + buf if stats.is_buy else stats.entry - buf


def _is_already_at_be(stats: PositionStats) -> bool:
    """Verifica se SL já está no BE ou melhor (5pts de margem para float)."""
    margin = 5 * stats.point
    if stats.is_buy:
        return stats.sl >= (stats.entry - margin)
    else:
        return stats.sl <= (stats.entry + margin)


# ─── Regras de saída ────────────────────────────────────────────────────────

def _detect_reversal_candle(df_m15: pd.DataFrame, against_buy: bool) -> bool:
    """
    Detecta vela de reversal recente que ameaça posição.
      against_buy=True  -> procuramos vela BEARISH forte (close < open, body grande)
      against_buy=False -> procuramos vela BULLISH forte (contra SELL)
    """
    if df_m15 is None or len(df_m15) < 3:
        return False
    last = df_m15.iloc[-2]   # vela fechada mais recente
    o, c, h, l = float(last['open']), float(last['close']), float(last['high']), float(last['low'])
    rng = h - l
    body = abs(c - o)
    if rng <= 0:
        return False
    body_ratio = body / rng

    if against_buy:
        is_bearish_strong = (c < o) and (body_ratio > 0.55)
        return is_bearish_strong
    else:
        is_bullish_strong = (c > o) and (body_ratio > 0.55)
        return is_bullish_strong


def _detect_structure_break(df_h1: pd.DataFrame, point: float, against_buy: bool) -> bool:
    """
    Detecta estrutura ICT contra a posição. Aciona em DOIS casos:
      1. BOS estrito (alternância HH/LL ou LH/HL) na direção contra ao trade
      2. Trend confirmado (LH+LL ou HH+HL consecutivos) na direção contra
         — quando entramos contra-trend e o trend continua, é "structure contra"
            mesmo sem alternância de BOS clássico.

      against_buy=True  -> bot está long; direção 'down' = contra
      against_buy=False -> bot está short; direção 'up' = contra
    """
    if df_h1 is None or len(df_h1) < 30:
        return False
    pivots = detect_swings(df_h1, depth=3, point=point)
    if len(pivots) < 4:
        return False
    structure = classify_structure(pivots, lookback=4)
    direction = structure.get('direction', 'neutral')
    bos = structure.get('bos_detected', False)

    # Caso 1: BOS clássico (alternância) na direção contra
    if bos and against_buy and direction == 'down':
        return True
    if bos and not against_buy and direction == 'up':
        return True

    # Caso 2: trend forte (LH+LL ou HH+HL) na direção contra ao trade
    # Aqui exigimos confluência: direction definida + last swing significativo
    last_high = structure.get('last_high')
    last_low  = structure.get('last_low')
    if direction == 'down' and against_buy and last_high and last_low:
        # Trend bearish confirmado contra long — structure rompida pra baixo
        return True
    if direction == 'up' and not against_buy and last_high and last_low:
        return True

    return False


def evaluate_all_rules(stats: PositionStats, ict_ctx: dict,
                       df_m15: pd.DataFrame, df_h1: pd.DataFrame) -> list:
    """
    v6.2.0 Sprint 6.2 — Avaliação verbose: retorna lista com TODAS as regras
    e seu status individual (matched/skipped + motivo). Usado pelo dashboard
    e logs para auditar PORQUÊ cada regra disparou ou não.

    Retorna lista de dicts:
      [{rule:'a', enabled:True, matched:False, status:'skipped',
        reason:'profit 0.42R < 1.0R'}, ...]
    """
    state = _position_state.setdefault(stats.ticket, {})
    results = []

    # Regra A: 1R BE
    if not ENABLE_BE_AT_1R:
        results.append({'rule': 'a', 'enabled': False, 'matched': False,
                        'status': 'disabled', 'reason': 'feature flag off'})
    elif state.get('be_done'):
        results.append({'rule': 'a', 'enabled': True, 'matched': False,
                        'status': 'already_done', 'reason': 'BE ja aplicado'})
    elif stats.profit_R < 1.0:
        results.append({'rule': 'a', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'profit {stats.profit_R:+.2f}R < 1.0R'})
    elif _is_already_at_be(stats):
        results.append({'rule': 'a', 'enabled': True, 'matched': False,
                        'status': 'already_at_be',
                        'reason': f'SL ja em BE ({stats.sl:.5f})'})
    else:
        results.append({'rule': 'a', 'enabled': True, 'matched': True,
                        'status': 'MATCH',
                        'reason': f'profit {stats.profit_R:+.2f}R >= 1.0R'})

    # Regra B: 0.7R + reversal
    if not ENABLE_PARTIAL_07R:
        results.append({'rule': 'b', 'enabled': False, 'matched': False,
                        'status': 'disabled', 'reason': 'feature flag off'})
    elif state.get('partial_done'):
        results.append({'rule': 'b', 'enabled': True, 'matched': False,
                        'status': 'already_done', 'reason': 'partial ja executado'})
    elif stats.profit_R < 0.7:
        results.append({'rule': 'b', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'profit {stats.profit_R:+.2f}R < 0.7R'})
    elif not _detect_reversal_candle(df_m15, against_buy=stats.is_buy):
        results.append({'rule': 'b', 'enabled': True, 'matched': False,
                        'status': 'no_reversal',
                        'reason': f'profit {stats.profit_R:+.2f}R OK mas sem reversal candle'})
    else:
        results.append({'rule': 'b', 'enabled': True, 'matched': True,
                        'status': 'MATCH',
                        'reason': f'profit {stats.profit_R:+.2f}R + reversal candle ICT'})

    # Regra C: 0.5R + 3 candles + RSI cruzou
    if not ENABLE_CLASSIC_BE:
        results.append({'rule': 'c', 'enabled': False, 'matched': False,
                        'status': 'disabled', 'reason': 'feature flag off'})
    elif state.get('be_done'):
        results.append({'rule': 'c', 'enabled': True, 'matched': False,
                        'status': 'already_done', 'reason': 'BE ja aplicado (regra a/c)'})
    elif stats.profit_R < 0.5:
        results.append({'rule': 'c', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'profit {stats.profit_R:+.2f}R < 0.5R'})
    elif stats.candles_open < 3:
        results.append({'rule': 'c', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'apenas {stats.candles_open} candles (precisa 3)'})
    else:
        # checa RSI
        if df_m15 is not None and len(df_m15) >= 3:
            rsi = calculate_rsi_series(df_m15['close']).iloc[-2]
            rsi_ok = (stats.is_buy and rsi >= 50) or (not stats.is_buy and rsi <= 50)
            if not rsi_ok:
                results.append({'rule': 'c', 'enabled': True, 'matched': False,
                                'status': 'rsi_unmet',
                                'reason': f'profit {stats.profit_R:+.2f}R + {stats.candles_open}c OK mas RSI={rsi:.1f} nao cruzou 50'})
            elif _is_already_at_be(stats):
                results.append({'rule': 'c', 'enabled': True, 'matched': False,
                                'status': 'already_at_be',
                                'reason': 'SL ja em BE'})
            else:
                results.append({'rule': 'c', 'enabled': True, 'matched': True,
                                'status': 'MATCH',
                                'reason': f'profit {stats.profit_R:+.2f}R + {stats.candles_open}c + RSI {rsi:.1f}'})
        else:
            results.append({'rule': 'c', 'enabled': True, 'matched': False,
                            'status': 'no_data', 'reason': 'sem dados M15'})

    # Regra D: liquidity raid
    if not ENABLE_LIQUIDITY_CLOSE:
        results.append({'rule': 'd', 'enabled': False, 'matched': False,
                        'status': 'disabled', 'reason': 'feature flag off'})
    elif stats.profit_R <= 0:
        results.append({'rule': 'd', 'enabled': True, 'matched': False,
                        'status': 'unmet', 'reason': f'profit {stats.profit_R:+.2f}R <= 0'})
    elif not ict_ctx.get('ok'):
        results.append({'rule': 'd', 'enabled': True, 'matched': False,
                        'status': 'no_ict', 'reason': 'ICT context indisponivel'})
    else:
        next_above = ict_ctx.get('next_liquidity_above')
        next_below = ict_ctx.get('next_liquidity_below')
        triggered = False
        if stats.is_buy and next_above:
            dist = (next_above.price - stats.current) / stats.pip_size if stats.pip_size > 0 else 999
            if dist <= 3:
                results.append({'rule': 'd', 'enabled': True, 'matched': True,
                                'status': 'MATCH',
                                'reason': f'liquidity above @{next_above.price:.5f} a {dist:.1f}p (raid completo)'})
                triggered = True
        elif (not stats.is_buy) and next_below:
            dist = (stats.current - next_below.price) / stats.pip_size if stats.pip_size > 0 else 999
            if dist <= 3:
                results.append({'rule': 'd', 'enabled': True, 'matched': True,
                                'status': 'MATCH',
                                'reason': f'liquidity below @{next_below.price:.5f} a {dist:.1f}p (raid completo)'})
                triggered = True
        if not triggered:
            target = next_above if stats.is_buy else next_below
            if target:
                dist = abs(target.price - stats.current) / stats.pip_size if stats.pip_size > 0 else 0
                results.append({'rule': 'd', 'enabled': True, 'matched': False,
                                'status': 'unmet',
                                'reason': f'liq target a {dist:.1f}p (precisa <= 3p)'})
            else:
                results.append({'rule': 'd', 'enabled': True, 'matched': False,
                                'status': 'no_target',
                                'reason': 'sem liquidity level no lado do trade'})

    # Regra E: structure break contra
    if not ENABLE_STRUCTURE_BREAK:
        results.append({'rule': 'e', 'enabled': False, 'matched': False,
                        'status': 'disabled', 'reason': 'feature flag off'})
    elif stats.profit_R >= 0:
        results.append({'rule': 'e', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'profit {stats.profit_R:+.2f}R >= 0 (regra so para perdedoras)'})
    elif _detect_structure_break(df_h1, stats.point, against_buy=stats.is_buy):
        results.append({'rule': 'e', 'enabled': True, 'matched': True,
                        'status': 'MATCH',
                        'reason': f'profit {stats.profit_R:+.2f}R + ICT structure quebrou contra'})
    else:
        results.append({'rule': 'e', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'profit {stats.profit_R:+.2f}R mas estrutura ICT nao quebrou'})

    # Regra F: time exit flag
    if not ENABLE_TIME_EXIT_FLAG:
        results.append({'rule': 'f', 'enabled': False, 'matched': False,
                        'status': 'disabled', 'reason': 'feature flag off'})
    elif state.get('time_flagged'):
        results.append({'rule': 'f', 'enabled': True, 'matched': False,
                        'status': 'already_flagged', 'reason': 'ja flagado'})
    elif stats.candles_open < TIME_EXIT_LOOKBACK:
        results.append({'rule': 'f', 'enabled': True, 'matched': False,
                        'status': 'unmet',
                        'reason': f'{stats.candles_open}c < {TIME_EXIT_LOOKBACK}c minimo'})
    elif df_m15 is not None and len(df_m15) >= TIME_EXIT_LOOKBACK + 1:
        recent = df_m15.tail(TIME_EXIT_LOOKBACK)
        range_pips = (float(recent['high'].max()) - float(recent['low'].min())) / stats.pip_size if stats.pip_size > 0 else 0
        if stats.risk_pips > 0:
            progress_R = range_pips / stats.risk_pips
            if progress_R < TIME_EXIT_MIN_PROGRESS_R:
                results.append({'rule': 'f', 'enabled': True, 'matched': True,
                                'status': 'MATCH',
                                'reason': f'{stats.candles_open}c, range {range_pips:.0f}p ({progress_R:.2f}R) < {TIME_EXIT_MIN_PROGRESS_R}R'})
            else:
                results.append({'rule': 'f', 'enabled': True, 'matched': False,
                                'status': 'unmet',
                                'reason': f'range {range_pips:.0f}p ({progress_R:.2f}R) >= {TIME_EXIT_MIN_PROGRESS_R}R'})
        else:
            results.append({'rule': 'f', 'enabled': True, 'matched': False,
                            'status': 'no_risk', 'reason': 'risk_pips=0'})
    else:
        results.append({'rule': 'f', 'enabled': True, 'matched': False,
                        'status': 'no_data', 'reason': 'sem dados M15'})

    return results


def evaluate_position(stats: PositionStats, ict_ctx: dict, df_m15: pd.DataFrame, df_h1: pd.DataFrame) -> dict:
    """
    Avalia uma posição contra as 6 regras (a-f). Retorna dict:
      {action: 'be'|'partial_be'|'close'|'flag'|'none',
       rule:   'a'|'b'|'c'|'d'|'e'|'f'|None,
       reason: str}

    Não executa nada — apenas decide.
    """
    state = _position_state.setdefault(stats.ticket, {})

    # ── Regra (a): profit >= 1.0R -> BE (se não feito)
    if ENABLE_BE_AT_1R and stats.profit_R >= 1.0 and not state.get('be_done'):
        if not _is_already_at_be(stats):
            return {
                'action': 'be', 'rule': 'a',
                'reason': f"profit {stats.profit_R:.2f}R >= 1.0R -> BE imediato",
            }

    # ── Regra (b): profit >= 0.7R + reversal candle -> close 50% + BE
    if ENABLE_PARTIAL_07R and stats.profit_R >= 0.7 and not state.get('partial_done'):
        if _detect_reversal_candle(df_m15, against_buy=stats.is_buy):
            return {
                'action': 'partial_be', 'rule': 'b',
                'reason': f"profit {stats.profit_R:.2f}R >= 0.7R + reversal candle ICT -> close {int(PARTIAL_CLOSE_PCT*100)}% + BE",
            }

    # ── Regra (c): profit >= 0.5R + 3 candles + RSI cruzou 50 -> BE clássico
    if ENABLE_CLASSIC_BE and stats.profit_R >= 0.5 and stats.candles_open >= 3 and not state.get('be_done'):
        if df_m15 is not None and len(df_m15) >= 3:
            rsi = calculate_rsi_series(df_m15['close']).iloc[-2]
            rsi_ok = (stats.is_buy and rsi >= 50) or (not stats.is_buy and rsi <= 50)
            if rsi_ok and not _is_already_at_be(stats):
                return {
                    'action': 'be', 'rule': 'c',
                    'reason': f"profit {stats.profit_R:.2f}R + {stats.candles_open} candles + RSI({RSI_PERIOD}) {rsi:.1f} cruzou 50 -> BE clássico",
                }

    # ── Regra (d): profit > 0 + liquidity level oposto atingido -> close cedo
    if ENABLE_LIQUIDITY_CLOSE and stats.profit_R > 0 and ict_ctx.get('ok'):
        next_above = ict_ctx.get('next_liquidity_above')
        next_below = ict_ctx.get('next_liquidity_below')
        if stats.is_buy and next_above is not None:
            # BUY mira above; quando preço cruza ou fica a <3 pips do level, fecha (raid completo)
            dist_pips = (next_above.price - stats.current) / stats.pip_size if stats.pip_size > 0 else 999
            if dist_pips <= 3:
                return {
                    'action': 'close', 'rule': 'd',
                    'reason': f"profit {stats.profit_R:.2f}R + liquidity raid completo (above {next_above.price:.5f}, dist {dist_pips:.1f}p)",
                }
        if not stats.is_buy and next_below is not None:
            dist_pips = (stats.current - next_below.price) / stats.pip_size if stats.pip_size > 0 else 999
            if dist_pips <= 3:
                return {
                    'action': 'close', 'rule': 'd',
                    'reason': f"profit {stats.profit_R:.2f}R + liquidity raid completo (below {next_below.price:.5f}, dist {dist_pips:.1f}p)",
                }

    # ── Regra (e): profit < 0 + ICT structure break contra -> close imediato
    if ENABLE_STRUCTURE_BREAK and stats.profit_R < 0:
        if _detect_structure_break(df_h1, stats.point, against_buy=stats.is_buy):
            return {
                'action': 'close', 'rule': 'e',
                'reason': f"profit {stats.profit_R:.2f}R + ICT BOS contra -> close imediato (limita perda)",
            }

    # ── Regra (f): N candles abertos sem progresso (range pequeno) -> flag
    if ENABLE_TIME_EXIT_FLAG and stats.candles_open >= TIME_EXIT_LOOKBACK and not state.get('time_flagged'):
        if df_m15 is not None and len(df_m15) >= TIME_EXIT_LOOKBACK + 1:
            recent = df_m15.tail(TIME_EXIT_LOOKBACK)
            range_pips = (float(recent['high'].max()) - float(recent['low'].min())) / stats.pip_size if stats.pip_size > 0 else 0
            if stats.risk_pips > 0:
                progress_R = range_pips / stats.risk_pips
                if progress_R < TIME_EXIT_MIN_PROGRESS_R:
                    return {
                        'action': 'flag', 'rule': 'f',
                        'reason': f"{stats.candles_open} candles abertos, range {range_pips:.0f}p ({progress_R:.2f}R) < {TIME_EXIT_MIN_PROGRESS_R}R -> SEM PROGRESSO (flag)",
                    }

    return {'action': 'none', 'rule': None, 'reason': 'aguardando — nenhuma regra disparou'}


def execute_decision(stats: PositionStats, decision: dict, pos) -> None:
    """Executa a decisão retornada por evaluate_position e loga."""
    action = decision['action']
    rule   = decision['rule']
    reason = decision['reason']

    if action == 'none':
        return

    state = _position_state.setdefault(stats.ticket, {})

    if action == 'be':
        new_sl = _be_sl_for(stats)
        ok = _modify_position_sltp(pos, new_sl, pos.tp)
        if ok:
            state['be_done'] = True
            push_event("BE_MOVED", f"{stats.symbol} {stats.type} SL->BE {new_sl:.5f} (rule {rule}) profit {stats.profit_R:+.2f}R")
            logger.trade(
                "be_moved_dynamic",
                f"{stats.symbol} {stats.type} BE @ {new_sl:.5f} (rule {rule}) | {reason}",
                symbol=stats.symbol,
                data={
                    "rule": rule, "ticket": stats.ticket,
                    "old_sl": stats.sl, "new_sl": new_sl,
                    "profit_R": stats.profit_R, "candles_open": stats.candles_open,
                },
            )

    elif action == 'partial_be':
        partial_vol = round(stats.volume * PARTIAL_CLOSE_PCT, 2)
        if partial_vol > 0:
            ok_close = _close_position(pos, volume=partial_vol, comment=f"PARTIAL_R{rule}")
            new_sl = _be_sl_for(stats)
            ok_be = _modify_position_sltp(pos, new_sl, pos.tp)
            if ok_close or ok_be:
                state['partial_done'] = True
                state['be_done'] = True
                push_event("PARTIAL+BE", f"{stats.symbol} {stats.type} {int(PARTIAL_CLOSE_PCT*100)}% closed + SL->BE (rule {rule})")
                logger.trade(
                    "partial_closed",
                    f"{stats.symbol} {stats.type} partial {int(PARTIAL_CLOSE_PCT*100)}% + BE @ {new_sl:.5f} (rule {rule}) | {reason}",
                    symbol=stats.symbol,
                    data={
                        "rule": rule, "ticket": stats.ticket,
                        "partial_volume": partial_vol, "remaining_volume": stats.volume - partial_vol,
                        "new_sl": new_sl, "profit_R": stats.profit_R,
                    },
                )

    elif action == 'close':
        comment_map = {'d': 'LIQ_RAID', 'e': 'BOS_BREAK'}
        comment = f"EXIT_{comment_map.get(rule, rule)}"
        ok = _close_position(pos, volume=None, comment=comment)
        if ok:
            event_name = "early_exit_liquidity" if rule == 'd' else "structure_break_close"
            push_event("CLOSE", f"{stats.symbol} {stats.type} CLOSE (rule {rule}) {reason[:60]}")
            logger.trade(
                event_name,
                f"{stats.symbol} {stats.type} CLOSE (rule {rule}) | {reason}",
                symbol=stats.symbol,
                data={
                    "rule": rule, "ticket": stats.ticket,
                    "profit_R": stats.profit_R, "exit_price": stats.current,
                },
            )

    elif action == 'flag':
        # Não fecha — apenas registra. Operador decide se intervém manualmente.
        state['time_flagged'] = True
        push_event("TIME_FLAG", f"{stats.symbol} {stats.type} SEM PROGRESSO (rule {rule})")
        logger.warning(
            "time_exit_flagged",
            f"{stats.symbol} {stats.type} SEM PROGRESSO (rule {rule}) | {reason}",
            symbol=stats.symbol,
            data={
                "rule": rule, "ticket": stats.ticket,
                "candles_open": stats.candles_open, "profit_R": stats.profit_R,
            },
        )


# ─── Exit Hint para Indicador MQ5 (Sprint 4 ext.) ───────────────────────────

def _write_exit_hint(stats: PositionStats, decision: dict):
    """
    Escreve hint da próxima ação prevista para a posição num CSV lido pelo
    IndicadorLiquidez.mq5: `MQL5/Files/exit_hint_<symbol>.csv`.

    Formato (1 linha por arquivo, 1 arquivo por par):
      HINT,<type>,<profit_R>,<candles>,<action>,<rule>,<reason>

    Action: 'be' | 'partial_be' | 'close' | 'flag' | 'none'
    Rule:   'a'..'f' ou '-'
    """
    fname = os.path.join(MT5_FILES_DIR, f"exit_hint_{stats.symbol}.csv")
    action = decision.get('action', 'none')
    rule = decision.get('rule') or '-'
    reason = (decision.get('reason') or '').replace(",", ";").replace("\n", " ")[:120]
    try:
        with open(fname, "w", encoding="ansi") as f:
            f.write("HEADER\n")
            f.write(
                f"HINT,{stats.type},{stats.profit_R:+.2f},{stats.candles_open},"
                f"{action},{rule},{reason}\n"
            )
    except Exception:
        pass


def _clear_exit_hint(symbol: str):
    """Apaga o arquivo de hint quando a posição fecha — indicador volta ao estado neutro."""
    fname = os.path.join(MT5_FILES_DIR, f"exit_hint_{symbol}.csv")
    try:
        if os.path.exists(fname):
            os.remove(fname)
    except Exception:
        pass


def log_position_evaluation(stats: PositionStats, decision: dict,
                            rules_breakdown: list, ict_ctx: dict):
    """
    v6.2.0 Sprint 6.2 — Evento rico no Supabase com breakdown de TODAS as regras
    avaliadas. Permite auditar PORQUÊ uma regra não disparou em qualquer ciclo.

    Também escreve uma linha resumida no rolling log do terminal a cada N ciclos
    (não a cada ciclo, pra não poluir).
    """
    matched_rules = [r['rule'] for r in rules_breakdown if r.get('matched')]
    final_action = decision.get('action', 'none')
    final_rule   = decision.get('rule') or '-'

    # Linha resumida no rolling deque a cada mudança de status significativa
    # (mantém histórico legível). Critérios pra logar evento:
    #   - profit_R cruzou marco (0.5R, 0.7R, 1.0R, -0.5R, -1.0R)
    #   - matched_rules mudou
    state = _position_state.setdefault(stats.ticket, {})
    last_evt_R = state.get('_last_event_R', None)
    last_matched = state.get('_last_matched', None)

    def _crossed(thr):
        return (last_evt_R is None) or \
               ((last_evt_R < thr <= stats.profit_R) or (last_evt_R > thr >= stats.profit_R))

    significant = (last_matched != tuple(matched_rules)) or any(
        _crossed(t) for t in (-1.0, -0.5, 0.5, 0.7, 1.0)
    )
    if significant:
        rules_str = "+".join(matched_rules) if matched_rules else "none"
        push_event("EVAL", f"{stats.symbol} {stats.type} t={stats.ticket} "
                            f"profit={stats.profit_R:+.2f}R candles={stats.candles_open} "
                            f"matched=[{rules_str}] action={final_action}/{final_rule}")
        state['_last_event_R'] = stats.profit_R
        state['_last_matched'] = tuple(matched_rules)

    # Supabase log estruturado — sempre, em cada ciclo (auditoria 100%)
    try:
        # ICT context fields
        ict_summary = "ICT n/a"
        if ict_ctx.get('ok'):
            la = ict_ctx.get('next_liquidity_above')
            lb = ict_ctx.get('next_liquidity_below')
            ict_summary = (
                f"D1={ict_ctx.get('daily_bias','?')} "
                f"state={ict_ctx.get('daily_range_state','?')}"
            )
            if la: ict_summary += f" above={la.price:.5f}"
            if lb: ict_summary += f" below={lb.price:.5f}"

        msg = (
            f"{stats.symbol} {stats.type} t={stats.ticket} "
            f"profit={stats.profit_R:+.2f}R/{stats.profit_pips:+.1f}p "
            f"candles={stats.candles_open} | "
            f"matched=[{','.join(matched_rules) if matched_rules else 'none'}] "
            f"action={final_action} rule={final_rule} | {ict_summary}"
        )
        logger.info(
            "position_evaluation",
            msg,
            symbol=stats.symbol,
            data={
                "ticket": stats.ticket,
                "symbol": stats.symbol,
                "type": stats.type,
                "profit_R": round(stats.profit_R, 3),
                "profit_pips": round(stats.profit_pips, 1),
                "candles_open": stats.candles_open,
                "current_price": stats.current,
                "sl": stats.sl, "tp": stats.tp,
                "rules_breakdown": rules_breakdown,
                "decision_action": final_action,
                "decision_rule": final_rule,
                "decision_reason": decision.get('reason', ''),
                "ict_bias": ict_ctx.get('daily_bias') if ict_ctx.get('ok') else None,
                "ict_state": ict_ctx.get('daily_range_state') if ict_ctx.get('ok') else None,
            },
        )
    except Exception:
        pass


def log_position_snapshot(stats: PositionStats, decision: dict):
    """
    v6.2.0 Sprint 5 — Snapshot de cada posição em cada ciclo no Supabase.
    Permite reconstruir trajetória completa (profit_R por tempo) para auditoria.
    Level INFO mas evento dedicado pra filtro fácil.
    """
    logger.info(
        "position_snapshot",
        f"{stats.symbol} {stats.type} t={stats.ticket} profit={stats.profit_R:+.2f}R "
        f"({stats.profit_pips:+.1f}p) {stats.candles_open} candles "
        f"-> action={decision.get('action','none')} rule={decision.get('rule')}",
        symbol=stats.symbol,
        data={
            "ticket": stats.ticket, "symbol": stats.symbol, "type": stats.type,
            "entry": stats.entry, "current": stats.current,
            "sl": stats.sl, "tp": stats.tp,
            "profit_R": round(stats.profit_R, 3),
            "profit_pips": round(stats.profit_pips, 1),
            "candles_open": stats.candles_open,
            "decision_action": decision.get('action'),
            "decision_rule": decision.get('rule'),
            "decision_reason": decision.get('reason'),
        },
    )


# ─── Dashboard ──────────────────────────────────────────────────────────────

def _profit_bar(profit_R: float, width: int = 24) -> str:
    """
    Barra visual do profit em R. Centro = 0R, esquerda = perda, direita = ganho.
    Range -2R a +2R clamped.
    """
    half = width // 2
    clamped = max(-2.0, min(2.0, profit_R))
    pos = int((clamped / 2.0) * half) + half
    bar = ['-'] * width
    if profit_R >= 0:
        for i in range(half, min(pos + 1, width)):
            bar[i] = '#'
        bar[half] = '|'
    else:
        for i in range(max(pos, 0), half):
            bar[i] = '#'
        bar[half] = '|'
    return ''.join(bar)


def print_dashboard(positions_with_stats: List[tuple], cycle: int):
    """
    v6.2.0 Sprint 6.2 — Dashboard rico do Exit War Room.

    Cada posição renderizada como bloco completo:
      - Header com symbol/type/ticket/volume
      - Linha de preço: entry / current / SL / TP / profit_R / candles
      - Barra visual de profit_R (-2R..+2R)
      - Status DETALHADO de cada regra a-f (✓ MATCH, X unmet, - disabled)
      - Decisão final + ação a tomar
      - ICT context resumido (bias, liquidity above/below)

    Histórico de eventos preservado em recent_events deque (200) +
    arquivo data/terminal_logs/EXIT_WR_<dia>.log + Supabase position_evaluation.
    """
    W = 88
    sep = "=" * W
    dash = "-" * W
    os.system('cls' if os.name == 'nt' else 'clear')
    now = mt5_time_str("%H:%M:%S")

    flags = []
    if ENABLE_BE_AT_1R:        flags.append("1R-BE")
    if ENABLE_PARTIAL_07R:     flags.append("0.7R+rev")
    if ENABLE_CLASSIC_BE:      flags.append("0.5R+RSI")
    if ENABLE_LIQUIDITY_CLOSE: flags.append("liq-raid")
    if ENABLE_STRUCTURE_BREAK: flags.append("BOS-break")
    if ENABLE_TIME_EXIT_FLAG:  flags.append("time-flag")
    flags_str = " ".join(flags)

    print(sep)
    print(f"  EXIT WAR ROOM v6.2.0-ict  |  {now} MT5 (UTC+{MT5_UTC_OFFSET})  |  ciclo #{cycle}")
    print(f"  Regras ativas: {flags_str}  |  intervalo {MONITOR_INTERVAL_S}s")
    print(sep)

    # ── Posições abertas: bloco rico por posição ──
    if not positions_with_stats:
        print("  Nenhuma posicao aberta neste momento.")
    else:
        for stats, decision, _pos in positions_with_stats:
            ict_ctx_pos = decision.get('_ict_ctx', {})
            rules_breakdown = decision.get('_rules_breakdown', [])

            sign_R = "+" if stats.profit_R >= 0 else ""
            sign_pips = "+" if stats.profit_pips >= 0 else ""
            print(f"  ┌── POSICAO  {stats.symbol} {stats.type}  ticket={stats.ticket}  vol={stats.volume:.2f}")
            print(f"  │  entry={stats.entry:.5f}  current={stats.current:.5f}  "
                  f"SL={stats.sl:.5f}  TP={stats.tp:.5f}")
            bar = _profit_bar(stats.profit_R)
            print(f"  │  profit: {sign_R}{stats.profit_R:.2f}R  ({sign_pips}{stats.profit_pips:.1f}p)  "
                  f"risk: {stats.risk_pips:.1f}p  candles: {stats.candles_open}")
            print(f"  │  [{bar}]   (-2R                 0                 +2R)")

            # ICT context resumido
            if ict_ctx_pos.get('ok'):
                bias = ict_ctx_pos.get('daily_bias', '?')
                state = ict_ctx_pos.get('daily_range_state', '?')
                la = ict_ctx_pos.get('next_liquidity_above')
                lb = ict_ctx_pos.get('next_liquidity_below')
                la_s = f"{la.price:.5f} ({ict_ctx_pos.get('above_distance_pips',0):.1f}p)" if la else "—"
                lb_s = f"{lb.price:.5f} ({ict_ctx_pos.get('below_distance_pips',0):.1f}p)" if lb else "—"
                print(f"  │  ICT: D1={bias}  state={state}")
                print(f"  │       liq above={la_s}  |  liq below={lb_s}")
            else:
                print(f"  │  ICT: contexto indisponivel ({ict_ctx_pos.get('reason','?')})")

            # Status detalhado de cada regra
            print(f"  │  Regras:")
            for r in rules_breakdown:
                rule = r.get('rule', '?')
                status = r.get('status', '?')
                reason = r.get('reason', '')
                if status == 'MATCH':
                    mark = "[v MATCH ]"
                elif status == 'disabled':
                    mark = "[- off   ]"
                elif status in ('already_done', 'already_at_be', 'already_flagged'):
                    mark = "[- done  ]"
                else:
                    mark = "[X unmet ]"
                print(f"  │    {mark} regra {rule}: {reason}")

            # Decisão final
            action = decision.get('action', 'none')
            rule_v = decision.get('rule') or '-'
            if action == 'none':
                print(f"  └── DECISAO: aguardando (nenhuma regra disparou)")
            else:
                mark_a = {'be':'MOVE TO BE', 'partial_be':'PARTIAL+BE',
                          'close':'CLOSE', 'flag':'TIME FLAG'}.get(action, action)
                print(f"  └── DECISAO: [rule {rule_v}] {mark_a}")
            print()  # linha em branco entre posições

    print(dash)

    # ── Rolling log de eventos ──
    print(f"  HISTORICO DE EVENTOS (ultimos {len(recent_events)}/{recent_events.maxlen}):")
    print(dash)
    if not recent_events:
        print("  (sem eventos ainda)")
    else:
        # Mostra últimos N (cap 30 no terminal pra não poluir; deque inteiro vai pro arquivo)
        events_to_show = list(recent_events)[-30:]
        for ev in events_to_show:
            print(f"  {ev}")
    print(sep)
    print(f"  Persistencia: data/terminal_logs/EXIT_WR_<dia>.log  +  Supabase bot_logs (events=position_snapshot, position_evaluation)")
    print(sep)


# ─── Loop principal ─────────────────────────────────────────────────────────

def run_exit_war_room():
    print("=" * 80)
    print("  EXIT WAR ROOM v6.2.0-ict (Sprint 4)")
    print("  Monitora posicoes abertas, aplica regras dinamicas de saida ICT-aware")
    print("=" * 80)

    if not initialize_mt5():
        logger.error("mt5_init_failed", "Exit War Room: falha conectar ao MT5")
        return

    logger.info(
        "exit_war_room_started",
        f"Exit War Room v6.2.0-ict iniciado | Magic: {MAGIC_NUMBER} | "
        f"intervalo {MONITOR_INTERVAL_S}s | regras a-f conforme config"
    )

    cycle = 0
    try:
        while True:
            cycle += 1
            try:
                # Buscar posições abertas com nosso magic
                all_positions = mt5.positions_get() or []
                positions = [p for p in all_positions if p.magic == MAGIC_NUMBER]

                # Buscar trade records do Supabase (para filled_at)
                trade_records_by_ticket: dict = {}
                if positions:
                    try:
                        result = lifecycle.client.table("signals_liquidez")\
                            .select("position_id,filled_at,symbol,type")\
                            .in_("status", ["filled", "open"]).execute()
                        for tr in (result.data or []):
                            pid = tr.get('position_id')
                            if pid:
                                trade_records_by_ticket[pid] = tr
                    except Exception as e:
                        logger.warning("supabase_query_failed", str(e))

                positions_with_stats = []
                # Rastreio de novas posições (detectar entrada de uma nova) e fechamentos
                current_tickets = {p.ticket for p in positions}
                last_known = set(_position_state.keys())
                for new_ticket in current_tickets - last_known:
                    pos_match = next((p for p in positions if p.ticket == new_ticket), None)
                    if pos_match:
                        side = "BUY" if pos_match.type == mt5.POSITION_TYPE_BUY else "SELL"
                        push_event("MONITOR", f"{pos_match.symbol} {side} t={new_ticket} entrou em monitoramento")
                        _ticket_to_symbol[new_ticket] = pos_match.symbol
                for closed_ticket in last_known - current_tickets:
                    push_event("UNMONITOR", f"ticket={closed_ticket} saiu do monitoramento (fechado/BE-stop)")
                    # Limpa exit_hint_<symbol>.csv para indicador voltar ao estado neutro
                    closed_symbol = _ticket_to_symbol.pop(closed_ticket, None)
                    if closed_symbol:
                        _clear_exit_hint(closed_symbol)

                for pos in positions:
                    trade_record = trade_records_by_ticket.get(pos.ticket)
                    stats = compute_stats(pos, trade_record)
                    if stats is None:
                        continue

                    # Buscar contexto ICT (cache 5min)
                    ict_ctx = ict_get_context(pos.symbol, mt5_module=mt5)

                    # M15 e H1 frescos (curtos — só para detecção de reversal e BOS)
                    df_m15 = get_rates(pos.symbol, mt5.TIMEFRAME_M15, 30)
                    df_h1  = get_rates(pos.symbol, mt5.TIMEFRAME_H1, 50)

                    decision = evaluate_position(stats, ict_ctx, df_m15, df_h1)
                    # v6.2.0 Sprint 6.2: avaliação verbose para auditoria
                    rules_breakdown = evaluate_all_rules(stats, ict_ctx, df_m15, df_h1)
                    decision['_rules_breakdown'] = rules_breakdown
                    decision['_ict_ctx'] = ict_ctx
                    positions_with_stats.append((stats, decision, pos))

                    # v6.2.0 Sprint 5: snapshot Supabase a cada ciclo (auditoria 100%)
                    log_position_snapshot(stats, decision)
                    # Sprint 6.2: evaluation rica no Supabase com breakdown de TODAS regras
                    log_position_evaluation(stats, decision, rules_breakdown, ict_ctx)
                    # Sprint 4 ext.: hint para indicador MT5 (próxima ação prevista)
                    _write_exit_hint(stats, decision)

                # Dashboard primeiro (estado antes da execução)
                print_dashboard(positions_with_stats, cycle)

                # Executa decisões
                for stats, decision, pos in positions_with_stats:
                    if decision['action'] != 'none':
                        execute_decision(stats, decision, pos)

                # Limpa state de tickets que não estão mais abertos
                open_tickets = {p.ticket for p in positions}
                for tk in list(_position_state.keys()):
                    if tk not in open_tickets:
                        _position_state.pop(tk, None)

            except Exception as e:
                logger.error("exit_war_room_loop_error", str(e))
                import traceback
                traceback.print_exc()

            time.sleep(MONITOR_INTERVAL_S)

    finally:
        mt5.shutdown()
        print("\n[INFO] Exit War Room encerrado.")


if __name__ == "__main__":
    run_exit_war_room()
