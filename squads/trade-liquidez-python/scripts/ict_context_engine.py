"""
ICT Context Engine — Orquestrador de análise multi-timeframe ICT.
=======================================================================
Sprint 2 (v6.2.0-ict).

Centraliza chamada aos 4 módulos do pacote `ict/`:
  - structure       (swings, BOS)
  - phase_detector  (expansion/retracement/reversal/consolidation)
  - liquidity_levels (untested + equal levels)
  - daily_range_algo (estado do dia ICT — Aula 2)

Função principal:
  get_context(symbol, mt5_module=None) -> dict

Uso pelo War Room:
  ctx = get_context('AUDUSD')
  pts = ctx['trade_alignment_score']('SELL')   # 0-25 pts

CONSTRAINT DE MEMÓRIA: macro/ICT é SCORE-ONLY, NUNCA gate. Bot não chama esse
módulo para bloquear entradas — apenas o War Room usa para pontuar.

Cache TTL: 5 minutos por símbolo (evita re-fetch a cada signal_analysis).
"""

import time
from datetime import datetime, timezone
from typing import Optional

from ict.structure import detect_swings, classify_structure, bias_from_structure
from ict.phase_detector import classify_phase, PhaseResult
from ict.liquidity_levels import (
    find_untested_levels, find_equal_levels, next_levels, LiquidityLevel,
)
from ict.daily_range_algo import load_or_init_state, save_state, get_current_phase


# Cache simples — chave: symbol, valor: (timestamp, ctx_dict)
_CACHE: dict = {}
_CACHE_TTL_SECONDS = 300   # 5 min — alinha com objetivo do Sprint 2


def _cache_get(symbol: str) -> Optional[dict]:
    entry = _CACHE.get(symbol)
    if not entry:
        return None
    ts, ctx = entry
    if (time.time() - ts) > _CACHE_TTL_SECONDS:
        _CACHE.pop(symbol, None)
        return None
    return ctx


def _cache_put(symbol: str, ctx: dict):
    _CACHE[symbol] = (time.time(), ctx)


def _empty_context(symbol: str, reason: str) -> dict:
    """Contexto neutro quando dados são insuficientes — não penaliza o trade."""
    return {
        'symbol':              symbol,
        'ok':                  False,
        'reason':              reason,
        'daily_bias':          'neutral',
        'h4_phase':            None,
        'h1_phase':            None,
        'next_liquidity_above': None,
        'next_liquidity_below': None,
        'daily_range_state':   'unknown',
        'daily_range_label':   '',
        'untested_levels':     [],
        'equal_levels':        [],
        'current_price':       0.0,
        # Retorna 12 pts (~50% do max 25) para não penalizar quando não temos dados
        'trade_alignment_score': lambda trade_type: 12,
        'trade_alignment_explain': lambda trade_type: f"contexto indisponível ({reason}) — score neutro 12/25",
    }


def _build_alignment_scorer(daily_bias: str, h4_phase: PhaseResult, h1_phase: PhaseResult,
                            next_above: Optional[LiquidityLevel],
                            next_below: Optional[LiquidityLevel],
                            current_price: float):
    """
    Closure que devolve (score, explanation) para um trade BUY ou SELL.

    Faixa: 0-25 pts.

    Lógica (alinha com tese ICT — Aula 1):
      - Trade A FAVOR do daily_bias E h4_phase = expansion na direção  -> 25
      - Trade A FAVOR do daily_bias E h4_phase = retracement (pullback) -> 22
      - Trade A FAVOR do daily_bias E phases neutras                    -> 18
      - Daily neutro E h1_phase = reversal alinhado com trade           -> 18
      - Trade CONTRA daily_bias MAS h1_phase = reversal alinhado        -> 15
      - Trade CONTRA daily_bias E phase = consolidation                 -> 10
      - Trade CONTRA daily_bias E phase = retracement contrária         -> 5
      - Trade CONTRA daily_bias E phase = expansion contrária (CLIFF!)  -> 0

    Bonus liquidity (até +3, dentro do max 25):
      - Se trade vai EM DIREÇÃO a liquidity level próximo (<30 pips)
        ANTES de inverter → ICT vê isso como "raid" — premia.
      - Se trade vai CONTRA liquidity level próximo (vai bater logo) → penalty.
    """
    def score_for(trade_type: str):
        # Direção do trade
        trade_dir = 'up' if trade_type == 'BUY' else 'down'

        # Fase H4 e H1 (PhaseResult ou None)
        h4_dir = h4_phase.direction if h4_phase else 'neutral'
        h1_dir = h1_phase.direction if h1_phase else 'neutral'
        h4_kind = h4_phase.phase if h4_phase else 'unknown'
        h1_kind = h1_phase.phase if h1_phase else 'unknown'

        # Alinhamento com daily_bias
        bias_aligned = (daily_bias == 'bullish' and trade_dir == 'up') or \
                       (daily_bias == 'bearish' and trade_dir == 'down')
        bias_against = (daily_bias == 'bullish' and trade_dir == 'down') or \
                       (daily_bias == 'bearish' and trade_dir == 'up')
        bias_neutral = (daily_bias == 'neutral')

        # Núcleo
        base = 12   # default neutro
        why  = ""

        if bias_aligned:
            if h4_kind == 'expansion' and h4_dir == trade_dir:
                base, why = 25, "a-favor do bias D1 + H4 expansion na direção"
            elif h4_kind == 'retracement' and h4_dir == trade_dir:
                base, why = 22, "a-favor do bias D1 + H4 retracement (pullback)"
            elif h4_kind == 'consolidation':
                base, why = 16, "a-favor do bias D1 + H4 consolidation (range)"
            else:
                base, why = 18, "a-favor do bias D1, fases mistas"

        elif bias_neutral:
            # Sem viés direcional — vale o setup local (H1)
            if h1_kind == 'reversal' and h1_dir == trade_dir:
                base, why = 18, "bias D1 neutro, H1 reversal alinhado com trade"
            elif h1_kind == 'expansion' and h1_dir == trade_dir:
                base, why = 16, "bias D1 neutro, H1 expansion alinhado"
            else:
                base, why = 12, "bias D1 neutro, fases sem alinhamento claro"

        elif bias_against:
            # Trade contra daily_bias — ICT é cauteloso aqui
            if h1_kind == 'reversal' and h1_dir == trade_dir:
                base, why = 15, "contra bias D1 mas H1 reversal alinhado (BOS recente)"
            elif h4_kind == 'consolidation' or h1_kind == 'consolidation':
                base, why = 10, "contra bias D1 mas em consolidation"
            elif h4_kind == 'retracement' and h4_dir != trade_dir:
                base, why = 5, "contra bias D1 + H4 retracement contrária"
            elif h4_kind == 'expansion' and h4_dir != trade_dir:
                base, why = 0, "CLIFF: contra bias D1 + H4 expansion contrária"
            else:
                base, why = 7, "contra bias D1, contexto fraco"

        # Bonus liquidity (até +3, dentro do max 25)
        bonus = 0
        bonus_note = ""
        if current_price > 0:
            if trade_type == 'BUY':
                # BUY mira above (raid) → premia se há liquidez logo acima
                if next_above and 0 < (next_above.price - current_price) <= (30 * 0.0001):
                    bonus = +2
                    bonus_note = f" + raid liquidity above @{next_above.price:.5f}"
                elif next_below and 0 < (current_price - next_below.price) <= (15 * 0.0001):
                    bonus = -2
                    bonus_note = f" - liquidity below @{next_below.price:.5f} próxima (risco)"
            else:  # SELL
                if next_below and 0 < (current_price - next_below.price) <= (30 * 0.0001):
                    bonus = +2
                    bonus_note = f" + raid liquidity below @{next_below.price:.5f}"
                elif next_above and 0 < (next_above.price - current_price) <= (15 * 0.0001):
                    bonus = -2
                    bonus_note = f" - liquidity above @{next_above.price:.5f} próxima (risco)"

        final = max(0, min(25, base + bonus))
        explanation = f"{base}/25 — {why}{bonus_note} = {final}/25"
        return final, explanation

    def score_only(trade_type: str) -> int:
        s, _ = score_for(trade_type)
        return int(s)

    def explain(trade_type: str) -> str:
        _, e = score_for(trade_type)
        return e

    return score_only, explain


def get_context(symbol: str, mt5_module=None) -> dict:
    """
    Retorna contexto ICT consolidado para `symbol`.

    Args:
      symbol: par (ex: 'AUDUSD')
      mt5_module: módulo MetaTrader5 já inicializado (passado pelo chamador
                  para evitar import circular e garantir conexão única)

    Returns:
      dict com bias, fases, levels, daily_range_state e função de score.
      Em caso de falha de fetch, retorna _empty_context (score neutro 12/25).
    """
    cached = _cache_get(symbol)
    if cached is not None:
        return cached

    if mt5_module is None:
        return _empty_context(symbol, "mt5_module não fornecido")

    try:
        info = mt5_module.symbol_info(symbol)
        point = float(info.point) if info else 0.00001
        tick = mt5_module.symbol_info_tick(symbol)
        current_price = float(tick.bid) if tick else 0.0

        # Fetch multi-timeframe (Aula 3 — quantidades aproximadas):
        #   D1: 200 candles ~= 9 meses úteis
        #   H4: 200 candles ~= 33 dias úteis
        #   H1: 300 candles ~= 12 dias úteis  (3 semanas em 5d/wk)
        #   M15: 50 candles ~= 12h
        import pandas as pd  # late import — pandas só usado aqui
        def _fetch(tf, count):
            rates = mt5_module.copy_rates_from_pos(symbol, tf, 0, count)
            if rates is None or len(rates) == 0:
                return None
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df

        df_d1 = _fetch(mt5_module.TIMEFRAME_D1, 200)
        df_h4 = _fetch(mt5_module.TIMEFRAME_H4, 200)
        df_h1 = _fetch(mt5_module.TIMEFRAME_H1, 300)

        if df_d1 is None or df_h4 is None or df_h1 is None:
            return _empty_context(symbol, "fetch incompleto (D1/H4/H1)")

        # 1) Daily bias — estrutura D1
        d1_pivots = detect_swings(df_d1, depth=3, point=point)
        d1_structure = classify_structure(d1_pivots, lookback=4)
        daily_bias = bias_from_structure(d1_structure)

        # 2) Phases H4 e H1
        h4_phase = classify_phase(df_h4, depth=4, point=point)
        h1_phase = classify_phase(df_h1, depth=5, point=point)

        # 3) Liquidity levels (em H1 — granularidade de execução)
        h1_pivots = detect_swings(df_h1, depth=5, point=point)
        untested = find_untested_levels(df_h1, h1_pivots, last_n_candles=20,
                                        tolerance_pips=3.0, point=point)
        equal = find_equal_levels(h1_pivots, tolerance_pips=5.0, point=point,
                                  max_distance_candles=50)
        all_levels = untested + equal
        nl = next_levels(current_price, all_levels, point=point) if current_price > 0 else \
             {'above': None, 'below': None, 'above_distance_pips': 0, 'below_distance_pips': 0}

        # 4) Daily range state
        date_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        state = load_or_init_state(symbol, date_iso)
        state.update_from_dataframe(df_h1, point=point)
        save_state(state)

        phase_id, phase_label, _ = get_current_phase()

        # 5) Trade alignment scorer
        score_fn, explain_fn = _build_alignment_scorer(
            daily_bias, h4_phase, h1_phase,
            nl.get('above'), nl.get('below'), current_price
        )

        ctx = {
            'symbol':                symbol,
            'ok':                    True,
            'daily_bias':            daily_bias,
            'd1_structure':          d1_structure,
            'h4_phase':              h4_phase,
            'h1_phase':              h1_phase,
            'next_liquidity_above':  nl.get('above'),
            'next_liquidity_below':  nl.get('below'),
            'above_distance_pips':   nl.get('above_distance_pips', 0),
            'below_distance_pips':   nl.get('below_distance_pips', 0),
            'untested_levels':       untested,
            'equal_levels':          equal,
            'daily_range_state':     phase_id,
            'daily_range_label':     phase_label,
            'current_price':         current_price,
            'point':                 point,
            'trade_alignment_score': score_fn,
            'trade_alignment_explain': explain_fn,
        }

        _cache_put(symbol, ctx)
        return ctx

    except Exception as e:
        return _empty_context(symbol, f"exception: {e}")


def render_context_card(ctx: dict, prefix: str = "  ") -> str:
    """
    Renderiza card de texto ASCII com o contexto ICT — usado no War Room
    FASE 1 (antes do scoring).
    """
    if not ctx.get('ok'):
        return f"{prefix}[ICT CONTEXT] indisponível ({ctx.get('reason','?')}) — score neutro\n"

    sym = ctx['symbol']
    bias = ctx['daily_bias']
    bias_arrow = "↑" if bias == 'bullish' else ("↓" if bias == 'bearish' else "→")
    h4 = ctx['h4_phase']
    h1 = ctx['h1_phase']
    state = ctx.get('daily_range_label', '?')

    above = ctx.get('next_liquidity_above')
    below = ctx.get('next_liquidity_below')
    above_str = (f"{above.price:.5f} ({above.kind}, {ctx.get('above_distance_pips',0):.1f}p)"
                 if above else "—")
    below_str = (f"{below.price:.5f} ({below.kind}, {ctx.get('below_distance_pips',0):.1f}p)"
                 if below else "—")

    score_buy  = ctx['trade_alignment_score']('BUY')
    score_sell = ctx['trade_alignment_score']('SELL')

    lines = []
    lines.append(f"{prefix}┌── [ICT CONTEXT] {sym}  |  Daily bias: {bias.upper()} {bias_arrow}")
    lines.append(f"{prefix}│  H4: {h4.phase}/{h4.direction} (conf {h4.confidence:.2f}) — {h4.note}")
    lines.append(f"{prefix}│  H1: {h1.phase}/{h1.direction} (conf {h1.confidence:.2f}) — {h1.note}")
    lines.append(f"{prefix}│  Daily Range: {state}")
    lines.append(f"{prefix}│  Liquidity above: {above_str}")
    lines.append(f"{prefix}│  Liquidity below: {below_str}")
    lines.append(f"{prefix}│  Alignment BUY: {score_buy}/25  |  SELL: {score_sell}/25")
    lines.append(f"{prefix}└──")
    return "\n".join(lines) + "\n"
