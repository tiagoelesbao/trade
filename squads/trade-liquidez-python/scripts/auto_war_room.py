"""
Auto War Room v6.1.2 - Sala de Guerra Agêntica
===============================================
Scoring enxuto com 5 critérios (100 pts) — RSI como alpha:

  1. RSI Extremo    (35 pts) — ALPHA: tese central da estratégia
  2. Wick %         (25 pts) — força do pavio de rejeição
  3. Pin Bar        (20 pts) — qualidade corpo/pavio (o bot não verifica)
  4. Sessão         (15 pts) — London/NY overlap > sessão isolada > Ásia
  5. Histórico      ( 5 pts) — win rate 30 dias do símbolo

Mudanças v6.1.2 (2026-04-22):
- REMOVIDO Slope H1 do scoring (bot já não usa como gate — consistência)
- REMOVIDO Volume do scoring (trader: não casa com estratégia de reversão em zona)
- RSI promovido a alpha: peso 15 → 35 (trader: "o princípio da estratégia é o RSI")
- Wick redistribuído: 20 → 25
- Logs do terminal em timezone MT5 (mt5_server_utc_offset do config)
- NOVO: FASE 1 "STRATEGY FIRE" — card com estratégia + condições do mercado
  no instante do disparo (antes do scoring da FASE 2).
  Escopo: Zona + Wick + RSI + Sessão (contexto). Slope MA20 H1 e Color Reversal
  NÃO são mais mostrados: foram desativados nas Fases 1+2 (parecer técnico A/B/E)
  e exibi-los induzia a achar que ainda fazem parte da estratégia.

Mudanças v6.1.1 (Fase 1+2, 2026-04-21):
- Timezone UTC-aware na query de histórico (antes: naive datetime)
- Exception handler loga via SystemLogger em vez de swallow silent
- Banner mostra estado dos toggles do bot
"""

import time
import os
import yaml
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from trade_lifecycle_manager import TradeLifecycleManager

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
RSI_PERIOD     = CFG.get('rsi_period', 9)  # v6.1.3: 14 -> 9 (clássico, mais reativo)

# Toggles legados do bot (Slope + Color Reversal foram desativados nas Fases 1+2).
# Só lidos aqui para, EM CASO de reativação acidental, emitir alerta no banner.
# Não afetam scoring nem o card de strategy_fire na v6.1.2.
BOT_USE_TREND_FILTER = CFG.get('use_trend_filter', True)
BOT_REQUIRE_REVERSAL = CFG.get('require_color_reversal', True)

# Timezone MT5 server — logs do terminal casam com o chart da corretora
MT5_TZ = timezone(timedelta(hours=CFG.get('mt5_server_utc_offset', 3)))

def mt5_time_str(fmt="%H:%M:%S"):
    """Retorna hora formatada no fuso do servidor MT5 (mesmo do chart)."""
    return datetime.now(MT5_TZ).strftime(fmt)

# Inicializar lifecycle e logger
lifecycle = TradeLifecycleManager()
from system_logger import SystemLogger
logger = SystemLogger("WAR_ROOM")

# Configurações de análise
MIN_CONFIDENCE_SCORE = 65   # Aumentado de 55 para 65: mais qualidade
MAX_PENDING_SIGNALS  = 10

# Pares correlacionados
CORRELATED_PAIRS = [
    ['EURUSD', 'GBPUSD'],
    ['EURUSD', 'USDCHF'],
    ['GBPUSD', 'EURGBP'],
    ['AUDUSD', 'NZDUSD'],
    ['USDCAD', 'USDCHF'],
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def initialize_mt5():
    if not mt5.initialize():
        print("[ERROR] Falha ao conectar MT5")
        return False
    return True

def calculate_rsi(series, period=None):
    """RSI. Default lido do config (`rsi_period`, v6.1.3 = 9)."""
    if period is None:
        period = RSI_PERIOD
    delta = series.diff()
    gain  = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss  = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs    = gain / loss
    return 100 - (100 / (1 + rs))

def get_rates(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def session_score_label(hour_utc):
    """Retorna (pts, label) baseado na hora UTC."""
    if   13 <= hour_utc < 17: return 15, "London+NY overlap"
    elif  8 <= hour_utc < 13: return 10, "London"
    elif 17 <= hour_utc < 22: return 10, "New York"
    elif  0 <= hour_utc <  8: return  3, "Ásia"
    else:                      return  0, "Fora de sessão"

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
    print(f"  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):")
    print(f"  │     [{chk(wick_pass)}] Wick {ctx['rejection_wick']}: {wick_real:.0f}%  "
          f"(min 30%)   [bot reportou {wick_sig:.0f}%]")
    print(f"  │     [{chk(rsi_pass)}] RSI({RSI_PERIOD})    : {rsi:.1f}    (cond {rsi_op} {rsi_thr})")
    print(f"  │     [{chk(sess_pass)}] Sessao UTC : h={ctx['hour_utc']:02d}h -> {ctx['sess_label']}  "
          f"(contexto)")
    print(f"  │  ")
    print(f"  │  Plano de trade enviado:")
    print(f"  │     entry={ctx['price']:.5f}  SL={ctx['sl']:.5f} ({sl_pips:.1f} pips)  "
          f"TP={ctx['tp']:.5f} ({tp_pips:.1f} pips)  RR={rr:.2f}")
    print(f"  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring\n")


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
        sess_pts    = ctx['sess_pts']
        sess_label  = ctx['sess_label']
        hour_utc    = ctx['hour_utc']
        # v6.1.3: usa o wick_pct real recomputado do OHLC atual (ctx),
        # NÃO o campo do sinal — previne desalinhamento bot↔war room.
        wick_pct    = ctx['wick_pct_real']

        # ── Cálculo de scores (v6.1.3 — 5 critérios, 100 pts, RSI alpha) ─────

        # 1. RSI Extremo (0-35 pts)  — ALPHA: tese central da estratégia
        #    Curva threshold-based: passar o gate já vale 15pts (é a tese);
        #    extremo real (≥85 SELL / ≤15 BUY) satura em 35pts.
        #    SELL: RSI <70 → 0 | RSI 70 → 15 | RSI 80 → 28 | RSI 85+ → 35
        #    BUY : RSI >30 → 0 | RSI 30 → 15 | RSI 20 → 28 | RSI 15- → 35
        if trade_type == 'SELL':
            if rsi_current >= RSI_OVERBOUGHT:
                rsi_extreme = rsi_current - RSI_OVERBOUGHT          # 0..30
                rsi_score   = min(35.0, 15.0 + rsi_extreme * (20.0 / 15.0))
            else:
                rsi_score = 0.0  # defensivo: bot não deveria ter disparado
        else:
            if rsi_current <= RSI_OVERSOLD:
                rsi_extreme = RSI_OVERSOLD - rsi_current             # 0..30
                rsi_score   = min(35.0, 15.0 + rsi_extreme * (20.0 / 15.0))
            else:
                rsi_score = 0.0

        # 2. Wick % (0-25 pts)  — mínimo garantido pelo bot (≥30%)
        #    30% → 15 pts | 50%+ → 25 pts
        wick_score = min(25, (wick_pct / 0.50) * 25)

        # 3. Pin Bar — qualidade do corpo (0-20 pts)
        #    corpo < 15% do range → pin bar perfeito (20 pts)
        #    corpo 15-30%         → bom (13 pts)
        #    corpo 30-50%         → aceitável (7 pts)
        #    corpo > 50%          → vela suja (0-3 pts)
        if   body_ratio <= 0.15: pin_score = 20.0
        elif body_ratio <= 0.30: pin_score = 13.0
        elif body_ratio <= 0.50: pin_score = 7.0
        else:                    pin_score = max(0, round((1 - body_ratio) * 6, 1))

        # 4. Sessão (0-15 pts) — London+NY overlap premiado
        session_score = float(sess_pts)

        # 5. Histórico (0-5 pts)
        #    WR 40% → 0 | WR 60% → 5
        history_score = min(5, ((symbol_wr - 0.4) / 0.2) * 5) if symbol_wr > 0.4 else 0

        scores = {
            'rsi':     round(rsi_score,     1),
            'wick':    round(wick_score,    1),
            'pin_bar': round(pin_score,     1),
            'session': round(session_score, 1),
            'history': round(history_score, 1),
        }
        total_score = round(sum(scores.values()), 1)

        raw = {
            'rsi':          round(rsi_current, 1),
            'body_ratio':   round(body_ratio * 100, 1),   # %
            'symbol_wr':    round(symbol_wr * 100, 1),    # %
            'hist_trades':  hist_total,
            'session':      sess_label,
            'hour_utc':     hour_utc,
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

        momentum_max = 35.0
        rejection_max = 45.0   # wick(25) + pin_bar(20)
        context_max   = 20.0   # session(15) + history(5)

        momentum_val  = round(rsi_score, 1)
        rejection_val = round(wick_score + pin_score, 1)
        context_val   = round(session_score + history_score, 1)

        momentum_pct  = momentum_val / momentum_max
        rejection_pct = rejection_val / rejection_max
        context_pct   = context_val / context_max

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
                "comment": (f"Sessao {sess_label} ({session_score:.1f}), "
                            f"WR 30d {symbol_wr*100:.0f}% em {hist_total}T ({history_score:.1f}) "
                            f"-> {context_val:.1f}/{context_max:.0f} pts."),
                "sentiment": "neutral",
                "confidence": round(context_pct * 100),
                "verdict": _verdict(context_pct),
            },
        ]

        return total_score, opinions, scores, raw

    except Exception as e:
        print(f"[WARNING] Erro ao analisar sinal: {e}")
        import traceback; traceback.print_exc()
        return 50, [], {}, {}

# ─── Display ──────────────────────────────────────────────────────────────────

SCORE_MAX = {'rsi': 35, 'wick': 25, 'pin_bar': 20,
             'session': 15, 'history': 5}

SCORE_LABELS = {
    'rsi':     'RSI      ',
    'wick':    'Wick %   ',
    'pin_bar': 'Pin Bar  ',
    'session': 'Sessão   ',
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
            quality = ("perfeito" if pts >= 17 else "bom" if pts >= 10 else "aceitável" if pts >= 5 else "suja")
            detail = f"corpo {br:.0f}% range  [{quality}]"
        elif key == 'rsi':
            detail = f"RSI {raw.get('rsi', 0):.1f}"
        elif key == 'session':
            detail = raw.get('session', '?')
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

# ─── Main loop ────────────────────────────────────────────────────────────────

def run_auto_war_room():
    W    = 67
    sep  = "=" * W
    dash = "-" * W

    tz_offset = CFG.get('mt5_server_utc_offset', 3)
    tz_sign   = "+" if tz_offset >= 0 else ""

    # Slope/Color foram removidos nas Fases 1+2 (parecer técnico A/B/E).
    # Só logamos o estado se, por acaso, alguém reativar via config — lembrete.
    legacy_warn = []
    if BOT_USE_TREND_FILTER:
        legacy_warn.append("use_trend_filter=ON (desativado v6.1.1!)")
    if BOT_REQUIRE_REVERSAL:
        legacy_warn.append("require_color_reversal=ON (desativado v6.1.1!)")

    print(sep)
    print(f"  WAR ROOM v6.1.2  --  ANALISE TECNICA AGENTICA")
    print(dash)
    print(f"  Score minimo : {MIN_CONFIDENCE_SCORE}/100   |   Correlacao: ATIVA   |   Max sinais: {MAX_PENDING_SIGNALS}")
    print(f"  Estrategia   : Zona + Wick + RSI({RSI_PERIOD})   [Slope/ColorReversal desativados nas Fases 1+2]")
    print(f"  Criterios    : RSI(35) Wick(25) PinBar(20) Sessao(15) Hist(5)  [alpha: RSI]")
    print(f"  Timezone logs: MT5 server (UTC{tz_sign}{tz_offset:02d}:00) — casa com o chart")
    print(f"  Pipeline log : [FASE 1] STRATEGY FIRE (gatilhos+condicoes) -> [FASE 2] signal_analysis (score)")
    if legacy_warn:
        print(f"  ! ATENCAO    : {' | '.join(legacy_warn)}")
    print(sep)

    if not initialize_mt5():
        logger.error("mt5_init_failed", "War Room: não foi possível conectar ao MT5")
        return

    logger.info("war_room_started",
        f"War Room v6.1.2 iniciada | Score mínimo: {MIN_CONFIDENCE_SCORE}/100 | 5 critérios (RSI alpha) | estratégia: Zona+Wick+RSI | TZ=UTC{tz_sign}{tz_offset}"
        + (f" | legacy_ON: {', '.join(legacy_warn)}" if legacy_warn else ""))
    print("  MT5 conectado. Aguardando sinais do bot...\n")

    cycle = 0

    try:
        while True:
            try:
                pending = lifecycle.get_pending_signals('awaiting_consensus')

                if not pending:
                    time.sleep(5)
                    continue

                cycle += 1
                ts = mt5_time_str('%H:%M:%S')
                n  = len(pending)

                print(f"\n[{ts}] ciclo #{cycle}  --  {n} sinal(is) recebido(s)")
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
                    print_strategy_fire(signal, ctx)          # [FASE 1] estratégia + condições
                    score, opinions, scores, raw = analyze_signal_strength(signal, ctx)
                    analyzed_signals.append({
                        'signal': signal, 'score': score,
                        'opinions': opinions, 'scores': scores,
                        'raw': raw, 'ctx': ctx,
                    })

                analyzed_signals.sort(key=lambda x: x['score'], reverse=True)

                active_positions = mt5.positions_get() or []
                active_positions = [p for p in active_positions if p.magic == MAGIC_NUMBER]

                # Decisões
                print(f"\n{dash}")
                approved_count = 0
                processed_ids  = set()

                for item in analyzed_signals:
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

                    if score < MIN_CONFIDENCE_SCORE:
                        weakest = min(scores, key=lambda k: scores[k] / SCORE_MAX.get(k, 1))
                        reason  = (f"Score {score:.1f} < {MIN_CONFIDENCE_SCORE} | "
                                   f"fraco: {SCORE_LABELS[weakest].strip()} "
                                   f"{scores[weakest]:.1f}/{SCORE_MAX[weakest]}")
                        lifecycle.reject_signal(signal['id'], reason=reason)
                        processed_ids.add(signal['id'])
                        logger.signal_analysis(sig_info, scores, raw, opinions,
                                               verdict="REJEITADO", reason=reason)
                        continue

                    has_conflict, conflicting = check_correlation_conflict(signal, active_positions)
                    if has_conflict:
                        reason = f"Correlação com {conflicting} (posição ativa)"
                        lifecycle.reject_signal(signal['id'], reason=reason)
                        processed_ids.add(signal['id'])
                        logger.signal_analysis(sig_info, scores, raw, opinions,
                                               verdict="REJEITADO", reason=reason)
                        continue

                    lifecycle.approve_signal(signal['id'], agent_opinions=opinions)
                    approved_count += 1
                    processed_ids.add(signal['id'])
                    logger.signal_analysis(sig_info, scores, raw, opinions,
                                           verdict="APROVADO",
                                           reason=f"Score {score:.1f}/{MIN_CONFIDENCE_SCORE} → execução")
                    break  # 1 aprovação por ciclo

                # Preterir não processados
                for item in analyzed_signals:
                    if item['signal']['id'] not in processed_ids:
                        s      = item['signal']
                        reason = f"Preterido — outro sinal priorizado (score: {item['score']:.1f})"
                        lifecycle.reject_signal(s['id'], reason=reason)
                        sig_info = {
                            'symbol': s['symbol'], 'type': s['type'],
                            'price': s.get('price', 0), 'sl': s.get('sl', 0),
                            'tp': s.get('tp', 0), 'wick_pct': s.get('wick_pct', 0),
                        }
                        logger.signal_analysis(sig_info, item['scores'], item['raw'],
                                               item['opinions'], verdict="PRETERIDO",
                                               reason=reason)

                print(dash)
                print(f"  Ciclo #{cycle}: {approved_count} aprovado(s) / {len(analyzed_signals)} analisado(s)")

            except Exception as e:
                print(f"\n  [ERRO] Loop de analise: {e}")
                logger.error("war_room_loop_error", str(e))
                import traceback; traceback.print_exc()

            time.sleep(5)

    finally:
        mt5.shutdown()
        print("\n[INFO] War Room encerrada.")

if __name__ == "__main__":
    run_auto_war_room()
