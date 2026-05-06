"""
Auto War Room v6.2.0-ict (Sprint 1 — Calibragem ICT)
===============================================
Scoring enxuto com 5 critérios (100 pts) — RSI como alpha:

  1. RSI Extremo    (35 pts) — ALPHA: tese central da estratégia
  2. Wick %         (25 pts) — força do pavio de rejeição
  3. Pin Bar        (20 pts) — qualidade corpo/pavio (o bot não verifica)
  4. Sessão         (15 pts) — janelas ICT (Daily Range Algorithm — Aula 2)
  5. Histórico      ( 5 pts) — win rate 30 dias do símbolo

Mudanças v6.2.0 — Sprint 1 (2026-04-28):
- MIN_CONFIDENCE_SCORE 65 -> 75 (filtro mais restritivo após dados 27-28/04).
- session_score_label REESCRITA com 8 janelas ICT (Asia early/Judas/London open/
  London cont/news embargo/NY expansion/London close/NY afternoon) — Aula 2.
  Pesos lidos do config.yaml (session_windows).
- CORRELATED_PAIRS ampliado para cobrir USD-quote bundle inteiro (AUD/NZD/CAD/GBP
  movem juntos quando dólar mexe).
- Removidas referências aos toggles legados (slope/reversal) que sumiram do bot.

Mudanças v6.1.2 (2026-04-22):
- Slope H1 e Volume removidos do scoring; RSI promovido a alpha (35 pts).
- FASE 1 STRATEGY FIRE antes do scoring (FASE 2).

Mudanças v6.1.1 (2026-04-21):
- Timezone UTC-aware na query de histórico.
- Exception handler loga via SystemLogger.
"""

import time
import os
import sys
import yaml
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from trade_lifecycle_manager import TradeLifecycleManager

# v6.2.0 Sprint 2 — ICT Context Engine
sys.path.insert(0, os.path.dirname(__file__))
from ict_context_engine import get_context as ict_get_context, render_context_card

# v6.2.0 Sprint 6 — Cooldown direcional pós-loss (cache compartilhado com bot via JSON)
from cooldown_manager import CooldownManager
cooldown_mgr = CooldownManager()

# Carregar credenciais
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

# Carregar configurações
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

MAGIC_NUMBER   = CFG['magic_number']
RSI_OVERBOUGHT = CFG.get('rsi_overbought', 70)
RSI_OVERSOLD   = CFG.get('rsi_oversold', 30)
RSI_PERIOD     = CFG.get('rsi_period', 14)  # v6.2.0 Sprint 6: 9 -> 14 (Wilder default, alinha com MT5)

# Timezone MT5 server — logs do terminal casam com o chart da corretora
MT5_UTC_OFFSET = int(CFG.get('mt5_server_utc_offset', 3))
MT5_TZ = timezone(timedelta(hours=MT5_UTC_OFFSET))

def mt5_time_str(fmt="%H:%M:%S"):
    """Retorna hora formatada no fuso do servidor MT5 (mesmo do chart)."""
    return datetime.now(MT5_TZ).strftime(fmt)

# Inicializar lifecycle e logger
lifecycle = TradeLifecycleManager()
from system_logger import SystemLogger
logger = SystemLogger("WAR_ROOM")

# v6.2.0 Sprint 1: score mínimo 65 -> 75 (dados 27-28/04: trades <75 majoritariamente losers)
MIN_CONFIDENCE_SCORE = int(CFG.get('min_confidence_score', 75))
MAX_PENDING_SIGNALS  = 10

# v6.2.0 Sprint 3 — Pool-then-Pick. Janela de espera para acumular sinais correlatos.
CLUSTER_POOL_WINDOW_S = int(CFG.get('cluster_pool_window_seconds', 30))
CLUSTER_POOL_POLL_S   = int(CFG.get('cluster_pool_poll_seconds', 3))

# v6.2.0 Sprint 1 — CORRELATED_PAIRS ampliado.
# Padrão observado em 27-28/04: cluster 10:56 UTC = AUD+EUR+CAD simultâneos (todos USD-quote).
# Quando o dólar mexe, todos os USD-quote movem juntos; o "1º que dispara ganha" é arbitrário
# se scoring não tem awareness de macro. Sprint 3 adiciona pool+tie-breaker direcional;
# por ora ampliamos a malha pra rejeitar mais correlatos depois do 1º.
CORRELATED_PAIRS = [
    # USD-quote bundle (todos movem juntos quando dólar mexe)
    ['AUDUSD', 'NZDUSD'],
    ['AUDUSD', 'GBPUSD'],
    ['NZDUSD', 'GBPUSD'],
    # USD-base bundle (par fortalece/fraqueja contra USD na mesma direção)
    ['USDCAD', 'USDCHF'],
    # Cross-correlations comuns (commodities + risk-on)
    ['AUDUSD', 'USDCAD'],   # AUD ↑ tipicamente coincide com USDCAD ↓ (risk-on)
    ['NZDUSD', 'USDCAD'],
    ['AUDUSD', 'USDCHF'],
    ['NZDUSD', 'USDCHF'],
    ['GBPUSD', 'USDCAD'],
    ['GBPUSD', 'USDCHF'],
    # EUR (pares ainda comentados em config, mas mantidos no array p/ caso reativem)
    ['EURUSD', 'GBPUSD'],
    ['EURUSD', 'USDCHF'],
    ['EURUSD', 'AUDUSD'],
    ['EURUSD', 'NZDUSD'],
    ['EURUSD', 'USDCAD'],
    ['GBPUSD', 'EURGBP'],
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def initialize_mt5():
    if not mt5.initialize():
        logger.error("mt5_init_failed", "War Room: Falha ao conectar MT5 (initialize() retornou False)")
        return False
    return True

def calculate_rsi(series, period=None):
    """
    RSI com Wilder's Smoothing (SMMA) — alinhado com MetaTrader 5 default.
    Fix v6.2.0 Sprint 5 (ver bot_liquidez.calculate_rsi para fundamentação).
    """
    if period is None:
        period = RSI_PERIOD
    delta = series.diff()
    gain  = delta.where(delta > 0, 0.0)
    loss  = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs    = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_rates(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# v6.2.0 Sprint 1 — Janelas de sessão ICT (Aula 2 — Daily Range Algorithm).
# Lê do config.yaml/session_windows com fallback embutido (defaults idênticos ao yaml).
_SESSION_WINDOWS_DEFAULT = {
    'asia_early':      {'start': 21, 'end': 24, 'weight': 8,  'label': 'Asia early (post-NY)'},
    'asia_judas':      {'start':  0, 'end':  7, 'weight': 1,  'label': 'Asia continuation/Judas'},
    'london_open':     {'start':  7, 'end': 10, 'weight': 14, 'label': 'London open expansion'},
    'london_cont':     {'start': 10, 'end': 13, 'weight': 11, 'label': 'London continuation'},
    'ny_news_embargo': {'start': 13, 'end': 14, 'weight': 0,  'label': 'NY 8-8:30 news embargo'},
    'ny_expansion':    {'start': 14, 'end': 15, 'weight': 13, 'label': 'NY open expansion'},
    'london_close':    {'start': 15, 'end': 16, 'weight': 12, 'label': 'London close reversal'},
    'ny_afternoon':    {'start': 16, 'end': 21, 'weight': 7,  'label': 'NY afternoon / end-of-day'},
}
_SESSION_WINDOWS = CFG.get('session_windows', _SESSION_WINDOWS_DEFAULT) or _SESSION_WINDOWS_DEFAULT


def session_score_label(hour_utc):
    """
    Retorna (pts, label) baseado na hora UTC. Mapeamento ICT (Aula 2).

    Janelas avaliadas em ordem de precedência:
      asia_early (21-24) — premiada (exhaustion após NY close)
      asia_judas (00-07) — penalizada (manipulação pré-London)
      london_open (07-10) — prime time (expansion forma high/low do dia)
      london_cont (10-13) — bom (follow-through London)
      ny_news_embargo (13-14) — peso 0 (também bloqueado no bot como gate)
      ny_expansion (14-15) — bom (NY abre expansion)
      london_close (15-16) — bom (reversal London close)
      ny_afternoon (16-21) — fraco (end-of-day consolidation)

    NOTE: 0-7 é processado como asia_judas; 7-10 como london_open; etc.
    Janelas que cruzam meia-noite (asia_early 21-24) tratadas separadamente.
    """
    h = int(hour_utc) % 24

    # Janelas que terminam em 24 cobrem hora 21-23
    for key, win in _SESSION_WINDOWS.items():
        start, end = win['start'], win['end']
        # Janela normal (não cruza meia-noite)
        if start < end and start <= h < end:
            return int(win['weight']), str(win['label'])

    return 0, "Fora de sessão"

def mini_bar(pts, max_pts, width=16):
    filled = round((pts / max_pts) * width) if max_pts else 0
    return "#" * filled + "-" * (width - filled)

# ─── Strategy context (re-derivado do mercado) ────────────────────────────────

def derive_strategy_context(signal):
    """
    Re-deriva o contexto técnico/estratégico que disparou o sinal.
    Faz UM fetch de M15+H1 e devolve um dict rico que é consumido tanto
    pelo print_strategy_fire (logs ANTES da pontuação) quanto pelo
    analyze_signal_strength (cálculo do score).

    Retorna dict com: ok, symbol, type, df_m15, df_h1, candle, rsi_current,
    body_ratio, wick_top, wick_bot, wick_pct_real, slope_pips, sess_pts,
    sess_label, hour_utc, color_reversal, zone_type, distances, rr,
    symbol_wr, hist_total, mt5_time, utc_time
    """
    symbol     = signal['symbol']
    trade_type = signal['type']
    price      = signal.get('price', 0) or 0
    sl         = signal.get('sl', 0) or 0
    tp         = signal.get('tp', 0) or 0
    wick_pct_signal = signal.get('wick_pct', 0) or 0

    df_m15 = get_rates(symbol, mt5.TIMEFRAME_M15, 50)
    df_h1  = get_rates(symbol, mt5.TIMEFRAME_H1, 30)

    if df_m15 is None or len(df_m15) < 3:
        return {'ok': False, 'symbol': symbol, 'type': trade_type}

    df_m15['rsi'] = calculate_rsi(df_m15['close'])
    last  = df_m15.iloc[-2]   # vela fechada (a que o bot usou)
    rsi_current = df_m15['rsi'].iloc[-2]

    o, h, l, c = float(last['open']), float(last['high']), float(last['low']), float(last['close'])
    candle_range = h - l
    body         = abs(c - o)
    body_ratio   = (body / candle_range) if candle_range > 0 else 1.0
    upper_body   = max(o, c)
    lower_body   = min(o, c)
    wick_top     = h - upper_body
    wick_bot     = lower_body - l
    if trade_type == 'SELL':
        wick_pct_real = (wick_top / candle_range) if candle_range > 0 else 0.0
        zone_type     = "RESISTÊNCIA (rejeição superior)"
        rejection_wick= "superior"
    else:
        wick_pct_real = (wick_bot / candle_range) if candle_range > 0 else 0.0
        zone_type     = "SUPORTE (rejeição inferior)"
        rejection_wick= "inferior"

    last_color = "verde" if c >= o else "vermelha"

    # Ponto do símbolo (para converter SL/TP em pips)
    point = 0.00001
    info  = mt5.symbol_info(symbol)
    if info is not None:
        point = info.point

    # Sessão
    hour_utc = datetime.now(timezone.utc).hour
    sess_pts, sess_label = session_score_label(hour_utc)

    # Histórico 30d
    try:
        cutoff  = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        history = lifecycle.client.table("signals_liquidez")\
            .select("pnl").eq("symbol", symbol).eq("status", "closed")\
            .gte("created_at", cutoff).execute()
        if history.data:
            wins       = sum(1 for t in history.data if (t.get('pnl') or 0) > 0)
            hist_total = len(history.data)
            symbol_wr  = wins / hist_total
        else:
            hist_total, symbol_wr = 0, 0.0
    except Exception as e:
        logger.warning("history_query_failed", f"{symbol}: {e}", symbol=symbol)
        hist_total, symbol_wr = 0, 0.0

    # Distâncias / RR
    if point > 0:
        dist_sl_pts = abs(price - sl) / point
        dist_tp_pts = abs(tp - price) / point
    else:
        dist_sl_pts = dist_tp_pts = 0
    rr_real = (dist_tp_pts / dist_sl_pts) if dist_sl_pts > 0 else 0.0

    # v6.2.0 Sprint 2 — ICT Context (com cache de 5min, custo amortizado)
    try:
        ict_ctx = ict_get_context(symbol, mt5_module=mt5)
    except Exception as e:
        logger.warning("ict_context_failed", f"{symbol}: {e}", symbol=symbol)
        ict_ctx = {'ok': False, 'reason': str(e),
                   'trade_alignment_score': lambda t: 12,
                   'trade_alignment_explain': lambda t: 'erro — score neutro 12'}

    return {
        'ok':              True,
        'symbol':          symbol,
        'type':            trade_type,
        'df_m15':          df_m15,
        'df_h1':           df_h1,
        'candle':          {'open': o, 'high': h, 'low': l, 'close': c,
                            'range': candle_range, 'body': body,
                            'time':  str(last['time'])},
        'rsi_current':     float(rsi_current) if not pd.isna(rsi_current) else 50.0,
        'body_ratio':      body_ratio,
        'wick_top':        wick_top,
        'wick_bot':        wick_bot,
        'wick_pct_real':   wick_pct_real,
        'wick_pct_signal': wick_pct_signal,
        'rejection_wick':  rejection_wick,
        'zone_type':       zone_type,
        'last_color':      last_color,
        'sess_pts':        sess_pts,
        'sess_label':      sess_label,
        'hour_utc':        hour_utc,
        'symbol_wr':       symbol_wr,
        'hist_total':      hist_total,
        'price':           price,
        'sl':              sl,
        'tp':              tp,
        'dist_sl_pts':     dist_sl_pts,
        'dist_tp_pts':     dist_tp_pts,
        'rr_real':         rr_real,
        'point':           point,
        'ict_ctx':         ict_ctx,
    }


def print_strategy_fire(signal, ctx):
    """
    FASE 1 — Imprime o card que descreve a ESTRATÉGIA e as CONDIÇÕES DE MERCADO
    no instante em que o bot disparou o sinal. Aparece ANTES da análise de score.

    Estratégia atual (v6.1.2): apenas 3 gatilhos — Zona + Wick + RSI (+Sessão como
    contexto). Slope MA20 H1 e Color Reversal foram DESATIVADOS nas Fases 1+2
    (parecer técnico, itens A/B/E) e não são mais computados aqui. Slope também
    foi removido do scoring (consistência). Futuro MA100/MA200 virá como score-only,
    nunca como gate (ver feedback_strategy_macro_trend.md).
    """
    sym  = signal['symbol']
    typ  = signal['type']
    if not ctx.get('ok'):
        print(f"\n  ┌── STRATEGY FIRE  |  {sym} {typ}  |  contexto indisponível (falta de candles)")
        print(f"  └──")
        return

    candle = ctx['candle']
    o, h, l, c = candle['open'], candle['high'], candle['low'], candle['close']
    rng        = candle['range']
    body_pct   = ctx['body_ratio'] * 100
    wick_real  = ctx['wick_pct_real'] * 100
    wick_sig   = ctx['wick_pct_signal'] * 100
    rsi        = ctx['rsi_current']
    point      = ctx['point'] or 0.00001
    pip        = point * 10
    rng_pips   = rng / pip if pip > 0 else 0
    rr         = ctx['rr_real']
    sl_pips    = ctx['dist_sl_pts'] / 10 if point > 0 else 0
    tp_pips    = ctx['dist_tp_pts'] / 10 if point > 0 else 0
    rsi_thr    = RSI_OVERBOUGHT if typ == 'SELL' else RSI_OVERSOLD
    rsi_op     = ">=" if typ == 'SELL' else "<="
    rsi_pass   = (rsi >= RSI_OVERBOUGHT) if typ == 'SELL' else (rsi <= RSI_OVERSOLD)
    wick_pass  = wick_real >= 30.0
    sess_pass  = ctx['sess_pts'] > 0

    def chk(b): return "OK " if b else "-- "

    print(f"\n  ┌── [FASE 1] STRATEGY FIRE  |  {sym} {typ}  |  zona: {ctx['zone_type']}")
    print(f"  │  Vela M15 fechada @ {candle['time']}  ({ctx['last_color']})")
    print(f"  │     OHLC : O={o:.5f}  H={h:.5f}  L={l:.5f}  C={c:.5f}")
    print(f"  │     range={rng_pips:.1f} pips   corpo={body_pct:.0f}% do range")
    print(f"  │  ")
    print(f"  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):")
    print(f"  │     [{chk(wick_pass)}] Wick {ctx['rejection_wick']}: {wick_real:.0f}%  "
          f"(min 30%)   [bot reportou {wick_sig:.0f}%]")
    print(f"  │     [{chk(rsi_pass)}] RSI({RSI_PERIOD})    : {rsi:.1f}    (cond {rsi_op} {rsi_thr})")
    print(f"  │     [{chk(sess_pass)}] Sessao UTC : h={ctx['hour_utc']:02d}h -> {ctx['sess_label']}  "
          f"(contexto)")
    print(f"  │  ")
    print(f"  │  Plano de trade enviado:")
    print(f"  │     entry={ctx['price']:.5f}  SL={ctx['sl']:.5f} ({sl_pips:.1f} pips)  "
          f"TP={ctx['tp']:.5f} ({tp_pips:.1f} pips)  RR={rr:.2f}")
    print(f"  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring")

    # v6.2.0 Sprint 2 — Card ICT CONTEXT (entre FASE 1 e FASE 2)
    ict_ctx = ctx.get('ict_ctx', {}) or {}
    if ict_ctx.get('ok'):
        print(render_context_card(ict_ctx, prefix="  "))
    else:
        reason = ict_ctx.get('reason', 'indisponível')
        print(f"  [ICT CONTEXT]  {sym}  -- contexto indisponivel ({reason}) — score neutro 12/25\n")


# ─── Scoring ──────────────────────────────────────────────────────────────────

def analyze_signal_strength(signal, ctx=None):
    """
    Analisa força técnica do sinal (FASE 2 — pontuação matemática).
    Recebe `ctx` opcional vindo de derive_strategy_context para evitar refetch.
    Retorna: (total_score, opinions, scores_dict, raw_dict)
    """
    try:
        symbol     = signal['symbol']
        trade_type = signal['type']

        if ctx is None or not ctx.get('ok'):
            ctx = derive_strategy_context(signal)
        if not ctx.get('ok'):
            return 50, [], {}, {}

        rsi_current = ctx['rsi_current']
        body_ratio  = ctx['body_ratio']
        symbol_wr   = ctx['symbol_wr']
        hist_total  = ctx['hist_total']
        sess_pts_old = ctx['sess_pts']      # pts da sessão calculados em v6.2.0 Sprint 1 (max 15)
        sess_label  = ctx['sess_label']
        hour_utc    = ctx['hour_utc']
        wick_pct    = ctx['wick_pct_real']
        ict_ctx     = ctx.get('ict_ctx', {}) or {}

        # ── v6.2.0 Sprint 2 — 6 critérios (100 pts), agora com ICT Context ─────
        # RSI 35→25, Wick 25→20, PinBar 20→15, Session 15→10, ICT 25 (NEW), Hist 5
        # Constraint memória: ICT é SCORE-ONLY, não é gate. Sempre dá 0-25 pts.

        # 1. RSI Extremo (0-25 pts)  — ALPHA: tese central da estratégia
        #    SELL: RSI 70 → 11 | RSI 80 → 20 | RSI 85+ → 25
        #    BUY : RSI 30 → 11 | RSI 20 → 20 | RSI 15- → 25
        if trade_type == 'SELL':
            if rsi_current >= RSI_OVERBOUGHT:
                rsi_extreme = rsi_current - RSI_OVERBOUGHT          # 0..30
                rsi_score   = min(25.0, 11.0 + rsi_extreme * (14.0 / 15.0))
            else:
                rsi_score = 0.0
        else:
            if rsi_current <= RSI_OVERSOLD:
                rsi_extreme = RSI_OVERSOLD - rsi_current
                rsi_score   = min(25.0, 11.0 + rsi_extreme * (14.0 / 15.0))
            else:
                rsi_score = 0.0

        # 2. Wick % (0-20 pts)  — 30% → 12 pts | 50%+ → 20 pts
        wick_score = min(20.0, (wick_pct / 0.50) * 20)

        # 3. Pin Bar — qualidade do corpo (0-15 pts)
        if   body_ratio <= 0.15: pin_score = 15.0
        elif body_ratio <= 0.30: pin_score = 10.0
        elif body_ratio <= 0.50: pin_score = 5.0
        else:                    pin_score = max(0.0, round((1 - body_ratio) * 4, 1))

        # 4. Sessão (0-10 pts) — janelas ICT, lê de ctx mas re-escala 15→10
        #    sess_pts_old está em base 15 (max do Sprint 1) — dividimos por 1.5
        session_score = round(float(sess_pts_old) * (10.0 / 15.0), 1)

        # 5. ICT Context (0-25 pts) — NEW Sprint 2 — closure do context engine
        try:
            ict_score = float(ict_ctx.get('trade_alignment_score', lambda t: 12)(trade_type))
        except Exception as e:
            ict_score = 12.0  # fallback neutro
        ict_score = max(0.0, min(25.0, ict_score))

        # 6. Histórico (0-5 pts) — WR 40% → 0 | WR 60% → 5
        history_score = min(5, ((symbol_wr - 0.4) / 0.2) * 5) if symbol_wr > 0.4 else 0

        scores = {
            'rsi':     round(rsi_score,     1),
            'wick':    round(wick_score,    1),
            'pin_bar': round(pin_score,     1),
            'session': round(session_score, 1),
            'ict':     round(ict_score,     1),
            'history': round(history_score, 1),
        }
        total_score = round(sum(scores.values()), 1)

        # Raw context para o log estruturado
        ict_explain = ""
        try:
            ict_explain = ict_ctx.get('trade_alignment_explain', lambda t: '')(trade_type)
        except Exception:
            pass

        raw = {
            'rsi':          round(rsi_current, 1),
            'body_ratio':   round(body_ratio * 100, 1),
            'symbol_wr':    round(symbol_wr * 100, 1),
            'hist_trades':  hist_total,
            'session':      sess_label,
            'hour_utc':     hour_utc,
            'ict_bias':     ict_ctx.get('daily_bias', '?'),
            'ict_state':    ict_ctx.get('daily_range_state', '?'),
            'ict_h4':       (f"{ict_ctx['h4_phase'].phase}/{ict_ctx['h4_phase'].direction}"
                              if ict_ctx.get('h4_phase') else "?"),
            'ict_h1':       (f"{ict_ctx['h1_phase'].phase}/{ict_ctx['h1_phase'].direction}"
                              if ict_ctx.get('h1_phase') else "?"),
            'ict_explain':  ict_explain,
        }

        # ── Audit Checklist (v6.1.3) ──────────────────────────────────────────
        # Substitui as antigas "opiniões" mockadas de Simons/Druckenmiller/Taleb.
        # São 3 eixos auditáveis, derivados DIRETAMENTE dos scores acima — sem
        # lógica paralela, sem inferência subjetiva, sem confidence fabricada.
        #
        #   Momentum (0-35) = rsi_score       — força do extremo de RSI
        #   Rejeição (0-45) = wick + pin_bar  — qualidade da rejeição do pavio
        #   Contexto (0-20) = sessão + hist.  — momento e histórico do símbolo
        #
        # Cada eixo vem com: score bruto, % de preenchimento e veredito textual
        # derivado de faixas fixas (nada adaptativo, nada randomizado).
        sentiment = "bullish" if trade_type == 'BUY' else "bearish"

        def _verdict(pct):
            if pct >= 0.75: return "forte"
            if pct >= 0.50: return "ok"
            if pct >= 0.25: return "fraco"
            return "insuficiente"

        # v6.2.0 Sprint 2 — eixos atualizados (4 ao invés de 3, ICT como Macro)
        momentum_max  = 25.0   # rsi (Sprint 2: 35→25)
        rejection_max = 35.0   # wick(20) + pin_bar(15)  (Sprint 2: 45→35)
        context_max   = 15.0   # session(10) + history(5)
        macro_max     = 25.0   # ICT — NEW

        momentum_val  = round(rsi_score, 1)
        rejection_val = round(wick_score + pin_score, 1)
        context_val   = round(session_score + history_score, 1)
        macro_val     = round(ict_score, 1)

        momentum_pct  = momentum_val  / momentum_max
        rejection_pct = rejection_val / rejection_max
        context_pct   = context_val   / context_max
        macro_pct     = macro_val     / macro_max

        opinions = [
            {
                "agent": "Momentum",
                "avatar": "M",
                "comment": (f"RSI({RSI_PERIOD}) {rsi_current:.1f} -> {momentum_val:.1f}/{momentum_max:.0f} pts. "
                            f"Gate: {RSI_OVERBOUGHT if trade_type=='SELL' else RSI_OVERSOLD}."),
                "sentiment": sentiment,
                "confidence": round(momentum_pct * 100),
                "verdict": _verdict(momentum_pct),
            },
            {
                "agent": "Rejeicao",
                "avatar": "R",
                "comment": (f"Pavio {wick_pct*100:.0f}% (wick {wick_score:.1f}), "
                            f"corpo {body_ratio*100:.0f}% (pin {pin_score:.1f}) "
                            f"-> {rejection_val:.1f}/{rejection_max:.0f} pts."),
                "sentiment": sentiment,
                "confidence": round(rejection_pct * 100),
                "verdict": _verdict(rejection_pct),
            },
            {
                "agent": "Contexto",
                "avatar": "C",
                "comment": (f"Sessao {sess_label} ({session_score:.1f}/10), "
                            f"WR 30d {symbol_wr*100:.0f}% em {hist_total}T ({history_score:.1f}/5) "
                            f"-> {context_val:.1f}/{context_max:.0f} pts."),
                "sentiment": "neutral",
                "confidence": round(context_pct * 100),
                "verdict": _verdict(context_pct),
            },
            {
                "agent": "ICT Macro",
                "avatar": "I",
                "comment": (f"D1 bias={raw['ict_bias']} | H4={raw['ict_h4']} | H1={raw['ict_h1']} | "
                            f"daily_state={raw['ict_state']} -> {macro_val:.1f}/{macro_max:.0f} pts. "
                            f"{ict_explain}"),
                "sentiment": "neutral",
                "confidence": round(macro_pct * 100),
                "verdict": _verdict(macro_pct),
            },
        ]

        return total_score, opinions, scores, raw

    except Exception as e:
        logger.error("analyze_signal_failed", f"Erro ao analisar sinal: {e}",
                     data={"error": str(e), "signal_id": signal.get('id') if signal else None})
        import traceback; traceback.print_exc()
        return 50, [], {}, {}

# ─── Display ──────────────────────────────────────────────────────────────────

# v6.2.0 Sprint 2 — 6 critérios. Pesos redistribuídos para acomodar ICT (25 pts).
SCORE_MAX = {'rsi': 25, 'wick': 20, 'pin_bar': 15,
             'session': 10, 'ict': 25, 'history': 5}

SCORE_LABELS = {
    'rsi':     'RSI      ',
    'wick':    'Wick %   ',
    'pin_bar': 'Pin Bar  ',
    'session': 'Sessão   ',
    'ict':     'ICT Macro',
    'history': 'Histórico',
}

def print_signal_card(signal, score, scores, raw, dash):
    """Imprime card completo de análise do sinal."""
    sym  = signal['symbol']
    typ  = signal['type']
    wk   = signal.get('wick_pct', 0) * 100

    verdict = "APROVADO" if score >= MIN_CONFIDENCE_SCORE else "REJEITADO"
    diff    = score - MIN_CONFIDENCE_SCORE

    print(f"\n  ┌── {sym} {typ}  |  pavio {wk:.0f}%  |  {verdict}  {score:.1f}/100 "
          f"({'+'  if diff >= 0 else ''}{diff:.1f} pts)")

    for key, pts in scores.items():
        mx    = SCORE_MAX[key]
        label = SCORE_LABELS[key]
        bar   = mini_bar(pts, mx)

        # Detalhe contextual inline
        if key == 'wick':
            detail = f"pavio {wk:.0f}%"
        elif key == 'pin_bar':
            br = raw.get('body_ratio', 0)
            quality = ("perfeito" if pts >= 12 else "bom" if pts >= 8 else "aceitável" if pts >= 4 else "suja")
            detail = f"corpo {br:.0f}% range  [{quality}]"
        elif key == 'rsi':
            detail = f"RSI {raw.get('rsi', 0):.1f}"
        elif key == 'session':
            detail = raw.get('session', '?')
        elif key == 'ict':
            detail = f"D1={raw.get('ict_bias','?')} H4={raw.get('ict_h4','?')} H1={raw.get('ict_h1','?')}"
        elif key == 'history':
            wr = raw.get('symbol_wr', 50)
            ht = raw.get('hist_trades', 0)
            detail = f"WR {wr:.0f}%  ({ht}T / 30d)"
        else:
            detail = ''

        print(f"  │  {label}  [{bar}]  {pts:>4}/{mx}   {detail}")

    print(f"  │  {'─'*55}")
    total_bar = mini_bar(score, 100, width=20)
    print(f"  │  {'TOTAL    '}  [{total_bar}]  {score:>5}/100")
    print(f"  └── {'→ execução' if score >= MIN_CONFIDENCE_SCORE else f'faltam {abs(diff):.1f} pts para {MIN_CONFIDENCE_SCORE}'}")

def print_opinions(opinions):
    """Imprime as opiniões dos agentes."""
    for op in opinions:
        conf = op.get('confidence', 0)
        print(f"  [{op['avatar']}] {op['agent']:<15} {conf:>3}%  \"{op['comment']}\"")

# ─── Correlation ──────────────────────────────────────────────────────────────

def check_correlation_conflict(signal, active_positions):
    symbol = signal['symbol']
    for position in active_positions:
        pos_symbol = position.symbol
        for pair in CORRELATED_PAIRS:
            if symbol in pair and pos_symbol in pair and symbol != pos_symbol:
                return True, pos_symbol
    return False, None


def are_symbols_correlated(sym_a: str, sym_b: str) -> bool:
    """Retorna True se sym_a e sym_b estão em CORRELATED_PAIRS (ordem não importa)."""
    if sym_a == sym_b:
        return False
    for pair in CORRELATED_PAIRS:
        if sym_a in pair and sym_b in pair:
            return True
    return False

# ─── Cluster decision (Sprint 3 — Pool-then-Pick) ─────────────────────────────

def _ict_alignment_of(item: dict) -> float:
    """Extrai o componente ICT do score (0-25). Usado como chave primária do tie-breaker."""
    return float(item.get('scores', {}).get('ict', 0))


def _wick_of(item: dict) -> float:
    """Extrai pavio % real da análise — usado como tie-breaker terciário."""
    return float(item.get('ctx', {}).get('wick_pct_real', 0) or 0)


def pick_best_from_correlated(analyzed: list) -> dict:
    """
    Pool-then-Pick (Sprint 3): dado uma lista de sinais analisados, identifica
    grupos de correlatos via CORRELATED_PAIRS e escolhe 1 vencedor por grupo.

    Algoritmo:
      1. Ordena candidates DESC por (ict_alignment, total_score, wick_pct_real)
      2. Greedy: itera do melhor para o pior
         - Se candidate ainda livre: vira winner
         - Marca todos os correlatos a este winner como losers (com beat_reason)
      3. Retorna {winners: [...], losers: [(item, beat_by, reason)]}

    Tie-breaker:
      - Primário:  ict_alignment (maior contexto macro vence)
      - Secundário: total_score (qualidade técnica)
      - Terciário:  wick_pct_real (força do pavio)

    Por que ICT vem antes do score: cluster de 28/04 10:56 mostrou que aprovar
    pelo "maior score técnico" sem ICT awareness deixa passar trades contra-trend.
    """
    if not analyzed:
        return {'winners': [], 'losers': []}

    # Ordenar do melhor para o pior
    sorted_items = sorted(
        analyzed,
        key=lambda it: (_ict_alignment_of(it), it.get('score', 0), _wick_of(it)),
        reverse=True,
    )

    winners: list = []
    losers:  list = []     # (loser_item, winner_item, reason)
    consumed_ids: set = set()

    for item in sorted_items:
        sig_id = item['signal']['id']
        if sig_id in consumed_ids:
            continue

        # Esse vira winner
        winners.append(item)
        consumed_ids.add(sig_id)

        # Marcar todos os correlatos restantes como losers desse winner
        winner_sym = item['signal']['symbol']
        for other in sorted_items:
            other_id = other['signal']['id']
            if other_id in consumed_ids:
                continue
            other_sym = other['signal']['symbol']
            if are_symbols_correlated(winner_sym, other_sym):
                ict_w = _ict_alignment_of(item)
                ict_o = _ict_alignment_of(other)
                reason = (f"perdeu para {winner_sym} {item['signal']['type']} "
                          f"(ICT {ict_w:.0f} vs {ict_o:.0f}, "
                          f"score {item.get('score',0):.1f} vs {other.get('score',0):.1f})")
                losers.append((other, item, reason))
                consumed_ids.add(other_id)

    return {'winners': winners, 'losers': losers}


def render_cluster_decision_card(decision: dict, dash: str) -> None:
    """Imprime resumo da decisão do cluster: winners + losers com motivos."""
    winners = decision.get('winners', [])
    losers  = decision.get('losers',  [])
    if len(winners) <= 1 and not losers:
        return  # sem cluster real — sinal isolado, não vale renderizar
    print(f"\n  ┌── [CLUSTER DECISION]  {len(winners)} winner(s)  /  {len(losers)} loser(s)")
    for w in winners:
        sig = w['signal']
        print(f"  │  ✓ WINNER  {sig['symbol']} {sig['type']}  "
              f"ICT={_ict_alignment_of(w):.0f}/25  Score={w.get('score',0):.1f}/100")
    for loser, winner, reason in losers:
        sig = loser['signal']
        print(f"  │  ✗ LOSER   {sig['symbol']} {sig['type']}  -- {reason}")
    print(f"  └──")


# ─── Main loop ────────────────────────────────────────────────────────────────

def run_auto_war_room():
    W    = 67
    sep  = "=" * W
    dash = "-" * W

    tz_offset = MT5_UTC_OFFSET
    tz_sign   = "+" if tz_offset >= 0 else ""

    # Resumo das janelas de sessão ICT carregadas
    sess_summary = " ".join(
        f"{k}({v['weight']})" for k, v in _SESSION_WINDOWS.items()
    )

    # Sintetiza pares ativos no scoring (correlação ainda referencia EUR mas pode estar pausado)
    active_syms = ",".join(CFG.get('symbols', []))

    print(sep)
    print(f"  WAR ROOM v6.2.0-ict  --  ANALISE TECNICA AGENTICA + Pool-then-Pick")
    print(dash)
    print(f"  Score minimo : {MIN_CONFIDENCE_SCORE}/100   |   Correlacao: ATIVA ({len(CORRELATED_PAIRS)} pares)   |   Max sinais: {MAX_PENDING_SIGNALS}")
    print(f"  Estrategia   : Zona + Wick + RSI({RSI_PERIOD})  +  ICT Context Engine (Sprint 2)")
    print(f"  Criterios    : RSI(25) Wick(20) PinBar(15) Sessao(10) ICT(25) Hist(5)")
    print(f"  Sessoes ICT  : {sess_summary}")
    print(f"  Pares ativos : {active_syms or '<vazio>'}")
    print(f"  Pool-then-Pick: janela {CLUSTER_POOL_WINDOW_S}s  (poll {CLUSTER_POOL_POLL_S}s)  [Sprint 3]")
    print(f"  Timezone logs: MT5 server (UTC{tz_sign}{tz_offset:02d}:00) — casa com o chart")
    print(f"  Pipeline log : [FASE 1] STRATEGY FIRE -> [ICT CONTEXT] -> [FASE 2] score -> [CLUSTER DECISION]")
    print(sep)

    if not initialize_mt5():
        logger.error("mt5_init_failed", "War Room: não foi possível conectar ao MT5")
        return

    logger.info(
        "war_room_started",
        f"War Room v6.2.0-ict iniciada | Score mínimo: {MIN_CONFIDENCE_SCORE}/100 | "
        f"6 criterios (incl ICT) | pool={CLUSTER_POOL_WINDOW_S}s | "
        f"correlated_pairs={len(CORRELATED_PAIRS)} | TZ=UTC{tz_sign}{tz_offset}"
    )
    print("  MT5 conectado. Aguardando sinais do bot...\n")

    cycle = 0

    try:
        while True:
            try:
                # ── Sprint 3: Pool-then-Pick. Espera janela antes de processar. ──
                pending = lifecycle.get_pending_signals('awaiting_consensus')
                if not pending:
                    time.sleep(5)
                    continue

                # Janela de pool — re-fetch durante a espera para capturar correlatos
                pool_start = time.time()
                pool_initial_count = len(pending)
                ts_open = mt5_time_str('%H:%M:%S')
                print(f"\n[{ts_open}] POOL OPEN — {pool_initial_count} sinal(is) iniciais. "
                      f"Aguardando {CLUSTER_POOL_WINDOW_S}s para acumular correlatos...")
                while (time.time() - pool_start) < CLUSTER_POOL_WINDOW_S:
                    time.sleep(CLUSTER_POOL_POLL_S)
                    fresh = lifecycle.get_pending_signals('awaiting_consensus')
                    if len(fresh) > len(pending):
                        delta = len(fresh) - len(pending)
                        elapsed = time.time() - pool_start
                        print(f"  + {delta} novo(s) sinal(is) entraram no pool "
                              f"(t={elapsed:.0f}s, total={len(fresh)})")
                    pending = fresh

                cycle += 1
                ts = mt5_time_str('%H:%M:%S')
                n  = len(pending)
                print(f"\n[{ts}] POOL CLOSED — ciclo #{cycle}  --  {n} sinal(is) processado(s)")
                print(dash)

                # Proteção contra acúmulo excessivo
                if n > MAX_PENDING_SIGNALS:
                    excess = n - MAX_PENDING_SIGNALS
                    print(f"  ! ACUMULO: {n} sinais. Descartando {excess} mais antigos...")
                    logger.warning("signal_overflow", f"{n} sinais acumulados, descartando {excess}")
                    for old in pending[MAX_PENDING_SIGNALS:]:
                        lifecycle.reject_signal(old['id'], reason="Timeout: acumulacao excessiva")
                    pending = pending[:MAX_PENDING_SIGNALS]

                # Análise de cada sinal — FASE 1 (strategy fire) + FASE 2 (score)
                analyzed_signals = []
                for signal in pending:
                    ctx = derive_strategy_context(signal)
                    print_strategy_fire(signal, ctx)          # [FASE 1] + card ICT
                    score, opinions, scores, raw = analyze_signal_strength(signal, ctx)
                    analyzed_signals.append({
                        'signal': signal, 'score': score,
                        'opinions': opinions, 'scores': scores,
                        'raw': raw, 'ctx': ctx,
                    })

                active_positions = mt5.positions_get() or []
                active_positions = [p for p in active_positions if p.magic == MAGIC_NUMBER]

                # ── Sprint 6: Pre-filter Cooldown (defesa em camada extra) ──
                # Bot já bloqueia, mas se cooldown ativou entre detecção e análise,
                # ou se cache do bot estava stale, captura aqui.
                cooldown_items: list = []
                non_cooldown:  list = []
                for it in analyzed_signals:
                    sig = it['signal']
                    cd_blocked, cd_until = cooldown_mgr.check(sig['symbol'], sig['type'])
                    if cd_blocked:
                        cooldown_items.append((it, cd_until))
                    else:
                        non_cooldown.append(it)

                for item, cd_until in cooldown_items:
                    sig = item['signal']
                    sig_info = {
                        'symbol': sig['symbol'], 'type': sig['type'],
                        'price': sig.get('price', 0), 'sl': sig.get('sl', 0),
                        'tp': sig.get('tp', 0), 'wick_pct': sig.get('wick_pct', 0),
                    }
                    rem_min = int((cd_until - datetime.now(timezone.utc)).total_seconds() / 60)
                    reason = f"Cooldown pos-loss ativo (libera em {rem_min}min — {cd_until.strftime('%H:%MZ')})"
                    lifecycle.reject_signal(sig['id'], reason=reason)
                    logger.signal_analysis(sig_info, item['scores'], item['raw'],
                                           item['opinions'], verdict="REJEITADO_COOLDOWN",
                                           reason=reason)

                # ── Sprint 3: Pool-then-Pick decision ──
                # 1) Pré-filtra REJEITADO_CLIFF (ICT == 0) — descarta antes do tie-breaker
                cliff_items = [it for it in non_cooldown if it['scores'].get('ict', 0) == 0]
                viable      = [it for it in non_cooldown if it['scores'].get('ict', 0) > 0]

                for item in cliff_items:
                    sig = item['signal']
                    sig_info = {
                        'symbol': sig['symbol'], 'type': sig['type'],
                        'price': sig.get('price', 0), 'sl': sig.get('sl', 0),
                        'tp': sig.get('tp', 0), 'wick_pct': sig.get('wick_pct', 0),
                    }
                    ict_explain = item.get('raw', {}).get('ict_explain', 'CLIFF')
                    reason = f"ICT CLIFF | {ict_explain}"
                    lifecycle.reject_signal(sig['id'], reason=reason)
                    logger.signal_analysis(sig_info, item['scores'], item['raw'],
                                           item['opinions'], verdict="REJEITADO_CLIFF",
                                           reason=reason)

                # 2) Tie-breaker via pick_best_from_correlated (ICT > Score > Wick)
                decision = pick_best_from_correlated(viable)
                render_cluster_decision_card(decision, dash)

                # 3) Logar losers do cluster como PRETERIDO_CLUSTER
                for loser_item, winner_item, beat_reason in decision['losers']:
                    sig = loser_item['signal']
                    sig_info = {
                        'symbol': sig['symbol'], 'type': sig['type'],
                        'price': sig.get('price', 0), 'sl': sig.get('sl', 0),
                        'tp': sig.get('tp', 0), 'wick_pct': sig.get('wick_pct', 0),
                    }
                    lifecycle.reject_signal(sig['id'], reason=beat_reason)
                    logger.signal_analysis(sig_info, loser_item['scores'], loser_item['raw'],
                                           loser_item['opinions'], verdict="PRETERIDO_CLUSTER",
                                           reason=beat_reason)
                    # Estruturado para auditoria do cluster
                    logger.info("cluster_decision",
                        f"{sig['symbol']} {sig['type']} preterido: {beat_reason}",
                        symbol=sig['symbol'],
                        data={
                            'loser':  {'symbol': sig['symbol'], 'type': sig['type'],
                                       'ict': loser_item['scores'].get('ict', 0),
                                       'score': loser_item.get('score', 0)},
                            'winner': {'symbol': winner_item['signal']['symbol'],
                                       'type':   winner_item['signal']['type'],
                                       'ict':    winner_item['scores'].get('ict', 0),
                                       'score':  winner_item.get('score', 0)},
                        })

                # 4) Para cada winner: aplica gates de score, correlação com posições abertas
                print(f"\n{dash}")
                approved_count = 0

                for item in decision['winners']:
                    signal   = item['signal']
                    score    = item['score']
                    scores   = item['scores']
                    raw      = item['raw']
                    opinions = item['opinions']

                    sig_info = {
                        'symbol':   signal['symbol'],
                        'type':     signal['type'],
                        'price':    signal.get('price', 0),
                        'sl':       signal.get('sl', 0),
                        'tp':       signal.get('tp', 0),
                        'wick_pct': signal.get('wick_pct', 0),
                    }

                    # Gate de score (>= MIN_CONFIDENCE_SCORE)
                    if score < MIN_CONFIDENCE_SCORE:
                        weakest = min(scores, key=lambda k: scores[k] / SCORE_MAX.get(k, 1))
                        reason  = (f"Score {score:.1f} < {MIN_CONFIDENCE_SCORE} | "
                                   f"fraco: {SCORE_LABELS[weakest].strip()} "
                                   f"{scores[weakest]:.1f}/{SCORE_MAX[weakest]}")
                        lifecycle.reject_signal(signal['id'], reason=reason)
                        logger.signal_analysis(sig_info, scores, raw, opinions,
                                               verdict="REJEITADO", reason=reason)
                        continue

                    # Gate de correlação com POSIÇÕES JÁ ABERTAS no MT5
                    has_conflict, conflicting = check_correlation_conflict(signal, active_positions)
                    if has_conflict:
                        reason = f"Correlação com {conflicting} (posição ativa no MT5)"
                        lifecycle.reject_signal(signal['id'], reason=reason)
                        logger.signal_analysis(sig_info, scores, raw, opinions,
                                               verdict="REJEITADO", reason=reason)
                        continue

                    # APROVADO
                    lifecycle.approve_signal(signal['id'], agent_opinions=opinions)
                    approved_count += 1
                    logger.signal_analysis(sig_info, scores, raw, opinions,
                                           verdict="APROVADO",
                                           reason=f"Score {score:.1f}/{MIN_CONFIDENCE_SCORE} -> execução (winner do cluster)")
                    # Sprint 3: aprova até 1 winner por ciclo (mantém regra anterior)
                    break

                print(dash)
                print(f"  Ciclo #{cycle}: {approved_count} aprovado(s) / "
                      f"{len(decision['winners'])} winners / {len(decision['losers'])} preteridos cluster / "
                      f"{len(cooldown_items)} cooldown-rejected / "
                      f"{len(cliff_items)} cliff-rejected / {len(analyzed_signals)} total")

            except Exception as e:
                print(f"\n  [ERRO] Loop de analise: {e}")
                logger.error("war_room_loop_error", str(e))
                import traceback; traceback.print_exc()

            time.sleep(2)

    finally:
        mt5.shutdown()
        print("\n[INFO] War Room encerrada.")

if __name__ == "__main__":
    run_auto_war_room()
