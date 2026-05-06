"""
Simulação Sprint 4: Exit War Room — regras a-f.

Roda standalone (sem MT5/Supabase). Usa stubs para testar evaluate_position
com diferentes cenários de posição:
  - Cenário 1: profit 1.2R + nada -> regra (a) BE
  - Cenário 2: profit 0.8R + reversal candle -> regra (b) partial+BE
  - Cenário 3: profit 0.6R + 4 candles + RSI cruzou -> regra (c) BE clássico
  - Cenário 4: profit -0.3R + BOS contra -> regra (e) close
  - Cenário 5: profit 0.1R + 8 candles range pequeno -> regra (f) flag
  - Cenário 6: profit 0.2R + nada -> nenhuma regra (aguardar)
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(__file__))

# Vamos importar funções diretamente do módulo após stubar mt5/supabase
class _MT5Stub:
    POSITION_TYPE_BUY = 0
    TIMEFRAME_M15 = 15
    TIMEFRAME_H1 = 60
    def __getattr__(self, name): return lambda *a, **k: None
sys.modules['MetaTrader5'] = _MT5Stub()

# Stub mínimo de supabase (nunca chamado)
import types
supabase_mod = types.ModuleType('supabase')
def _create_client(*a, **k):
    class _Stub:
        def table(self, *a, **k):
            class _T:
                def __getattr__(self, n): return lambda *a, **k: self
                def execute(self): return type('R', (), {'data': []})
            return _T()
    return _Stub()
supabase_mod.create_client = _create_client
sys.modules['supabase'] = supabase_mod

# Agora podemos importar
import importlib.util
spec = importlib.util.spec_from_file_location("ewr", "exit_war_room.py")
ewr = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(ewr)
except Exception as e:
    print(f"erro ao carregar exit_war_room: {e}")
    sys.exit(1)

PositionStats = ewr.PositionStats


def make_df_with_reversal(against_buy=True, n=30):
    """Gera df_m15 onde a última vela é reversal forte."""
    np.random.seed(7)
    times = [datetime(2026, 4, 28) - timedelta(minutes=15 * (n - i)) for i in range(n)]
    base = np.linspace(1.10, 1.105, n)
    o = base + np.random.normal(0, 0.0001, n)
    c = base + np.random.normal(0, 0.0001, n)
    h = np.maximum(o, c) + 0.0002
    l = np.minimum(o, c) - 0.0002

    # Última vela: reversal forte
    last = -2  # iloc[-2] é a vela "fechada"
    if against_buy:
        # Bearish forte: open > close, body grande
        o[last], c[last] = 1.106, 1.103
        h[last], l[last] = 1.1062, 1.1028
    else:
        o[last], c[last] = 1.103, 1.106
        h[last], l[last] = 1.1062, 1.1028

    return pd.DataFrame({'time': times, 'open': o, 'high': h, 'low': l, 'close': c})


def make_df_no_reversal(n=30):
    """df_m15 sem reversal forte — velas pequenas."""
    np.random.seed(42)
    times = [datetime(2026, 4, 28) - timedelta(minutes=15 * (n - i)) for i in range(n)]
    base = np.linspace(1.10, 1.103, n)
    o = base + np.random.normal(0, 0.00005, n)
    c = base + np.random.normal(0, 0.00005, n)
    h = np.maximum(o, c) + 0.0001
    l = np.minimum(o, c) - 0.0001
    return pd.DataFrame({'time': times, 'open': o, 'high': h, 'low': l, 'close': c})


def make_df_stuck(n=30):
    """df_m15 onde as últimas 6 velas têm range minúsculo (< 0.3R com risco 10p)."""
    np.random.seed(99)
    times = [datetime(2026, 4, 28) - timedelta(minutes=15 * (n - i)) for i in range(n)]
    # Primeiras (n-6) velas variam normal
    base_old = np.linspace(1.10, 1.102, n - 6)
    base_new = np.full(6, 1.1020)   # últimas 6 velas no mesmo nível
    base = np.concatenate([base_old, base_new])
    o = base + np.random.normal(0, 0.00002, n)
    c = base + np.random.normal(0, 0.00002, n)
    h = np.maximum(o, c) + 0.00003
    l = np.minimum(o, c) - 0.00003
    return pd.DataFrame({'time': times, 'open': o, 'high': h, 'low': l, 'close': c})


def make_df_with_bos(against_buy=True, n=60):
    """
    Gera df_h1 com swings claros formando trend (LH+LL = bearish, ou HH+HL = bullish).
    Trend não é monotônico — tem oscilação de ~0.005 com bias direcional, o que cria
    pivots detectáveis pela função detect_swings.
    """
    np.random.seed(11)
    times = [datetime(2026, 4, 28) - timedelta(hours=n - i) for i in range(n)]

    # Oscilação senoidal + bias direcional
    t = np.arange(n)
    oscillation = np.sin(t / 4.0) * 0.005   # ~5 ondulações no range
    if against_buy:
        # Bearish: começa em 1.11 e termina em 1.09, oscilando
        bias = np.linspace(1.110, 1.090, n)
    else:
        bias = np.linspace(1.090, 1.110, n)
    base = bias + oscillation
    noise = np.random.normal(0, 0.0001, n)
    c = base + noise
    o = c + np.random.normal(0, 0.0001, n)
    h = np.maximum(o, c) + np.abs(np.random.normal(0, 0.0003, n))
    l = np.minimum(o, c) - np.abs(np.random.normal(0, 0.0003, n))
    return pd.DataFrame({'time': times, 'open': o, 'high': h, 'low': l, 'close': c})


def stats_template(profit_R, candles_open, is_buy=True, sl=None):
    """Cria PositionStats com profit_R desejado para teste."""
    entry = 1.10000
    risk_pips = 10.0
    pip = 0.0001
    if is_buy:
        sl_calc = entry - risk_pips * pip
        current = entry + profit_R * risk_pips * pip
    else:
        sl_calc = entry + risk_pips * pip
        current = entry - profit_R * risk_pips * pip

    return PositionStats(
        ticket=1001 + int(profit_R*100),
        symbol="AUDUSD", type=("BUY" if is_buy else "SELL"), is_buy=is_buy,
        volume=1.0, entry=entry, current=current,
        sl=sl if sl is not None else sl_calc, tp=entry + (2 * risk_pips * pip if is_buy else -2*risk_pips*pip),
        risk_pips=risk_pips, profit_pips=profit_R * risk_pips, profit_R=profit_R,
        candles_open=candles_open, point=0.00001, pip_size=0.0001,
    )


def main():
    print("=" * 72)
    print(" SIMULAÇÃO SPRINT 4 — Exit War Room (regras a-f)")
    print("=" * 72)

    df_normal = make_df_no_reversal()
    df_rev_buy = make_df_with_reversal(against_buy=True)
    df_stuck = make_df_stuck()
    df_h1_normal = make_df_with_bos(against_buy=False)  # uptrend (a-favor BUY)
    df_h1_against_buy = make_df_with_bos(against_buy=True)  # trend bearish forte

    ict_empty = {'ok': False, 'next_liquidity_above': None, 'next_liquidity_below': None}

    cases = [
        # (nome, stats, ict_ctx, df_m15, df_h1, regra_esperada)
        ("1) profit 1.2R + nada", stats_template(1.2, candles_open=2), ict_empty, df_normal, df_h1_normal, 'a'),
        ("2) profit 0.8R + reversal candle", stats_template(0.8, candles_open=3), ict_empty, df_rev_buy, df_h1_normal, 'b'),
        ("3) profit 0.6R + 4 candles", stats_template(0.6, candles_open=4), ict_empty, df_normal, df_h1_normal, 'c'),
        ("4) profit -0.3R + structure contra (trend bearish)", stats_template(-0.3, candles_open=5), ict_empty, df_normal, df_h1_against_buy, 'e'),
        ("5) profit 0.1R + 8 candles sem progresso", stats_template(0.1, candles_open=8), ict_empty, df_stuck, df_h1_normal, 'f'),
        ("6) profit 0.2R + nada (aguardar)", stats_template(0.2, candles_open=2), ict_empty, df_normal, df_h1_normal, None),
    ]

    print()
    for name, stats, ctx, dm, dh, expected in cases:
        # reset state pra cada teste
        ewr._position_state.clear()
        decision = ewr.evaluate_position(stats, ctx, dm, dh)
        rule = decision.get('rule')
        action = decision.get('action')
        ok = (rule == expected) or (expected is None and rule is None)
        mark = "OK " if ok else "!! "
        print(f"{mark} {name}")
        print(f"     -> regra={rule}  action={action}")
        print(f"        {decision.get('reason','')}")
        if not ok:
            print(f"     ESPERADO regra={expected}")
        print()

    print("=" * 72)


if __name__ == "__main__":
    main()
