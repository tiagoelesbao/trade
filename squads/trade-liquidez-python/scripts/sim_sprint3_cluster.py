"""
Simulação Sprint 3: Pool-then-Pick + Tie-breaker direcional.

Reconstrói o cluster do dia 28/04 às 10:56 UTC (3 sinais correlatos AUDUSD/EUR/USDCAD)
e demonstra o comportamento de pick_best_from_correlated em 3 cenários:
  A. Real: todos contra-trend -> CLIFFs filtrados, nenhum aprovado
  B. Híbrido: 1 a-favor, 1 contra (cliff) -> winner alinhado
  C. Tie-breaker: score técnico alto perde p/ ICT alto

Roda standalone (sem MT5/Supabase). Usado como audit do Sprint 3.
"""

CORRELATED_PAIRS = [
    ['AUDUSD', 'NZDUSD'], ['AUDUSD', 'GBPUSD'], ['NZDUSD', 'GBPUSD'],
    ['USDCAD', 'USDCHF'],
    ['AUDUSD', 'USDCAD'], ['NZDUSD', 'USDCAD'],
    ['AUDUSD', 'USDCHF'], ['NZDUSD', 'USDCHF'],
    ['GBPUSD', 'USDCAD'], ['GBPUSD', 'USDCHF'],
    ['EURUSD', 'GBPUSD'], ['EURUSD', 'USDCHF'], ['EURUSD', 'AUDUSD'],
    ['EURUSD', 'NZDUSD'], ['EURUSD', 'USDCAD'], ['GBPUSD', 'EURGBP'],
]


def are_symbols_correlated(a, b):
    if a == b:
        return False
    return any(a in p and b in p for p in CORRELATED_PAIRS)


def _ict_alignment_of(item):
    return float(item['scores'].get('ict', 0))


def _wick_of(item):
    return float(item.get('ctx', {}).get('wick_pct_real', 0) or 0)


def pick_best_from_correlated(analyzed):
    if not analyzed:
        return {'winners': [], 'losers': []}
    sorted_items = sorted(
        analyzed,
        key=lambda it: (_ict_alignment_of(it), it.get('score', 0), _wick_of(it)),
        reverse=True,
    )
    winners = []
    losers = []
    consumed = set()
    for item in sorted_items:
        sid = item['signal']['id']
        if sid in consumed:
            continue
        winners.append(item)
        consumed.add(sid)
        winner_sym = item['signal']['symbol']
        for other in sorted_items:
            oid = other['signal']['id']
            if oid in consumed:
                continue
            other_sym = other['signal']['symbol']
            if are_symbols_correlated(winner_sym, other_sym):
                ict_w = _ict_alignment_of(item)
                ict_o = _ict_alignment_of(other)
                reason = (
                    f"perdeu para {winner_sym} {item['signal']['type']} "
                    f"(ICT {ict_w:.0f} vs {ict_o:.0f}, "
                    f"score {item.get('score', 0):.1f} vs {other.get('score', 0):.1f})"
                )
                losers.append((other, item, reason))
                consumed.add(oid)
    return {'winners': winners, 'losers': losers}


def run():
    sep = "=" * 72
    dash = "-" * 72

    print(sep)
    print(" SIMULAÇÃO SPRINT 3 — Pool-then-Pick + Tie-breaker")
    print(" Cluster real 28/04 10:56-11:31 UTC (3 sinais correlatos)")
    print(sep)

    # ── Cenário A: cluster real do dia 28/04 ─────────────────────────
    # AUDUSD/USDCAD em downtrend e uptrend respectivamente; bot tentou
    # comprar AUD em queda e vender USDCAD em alta — todos CLIFFs.
    print()
    print("CENARIO A — Cluster real (todos contra-trend)")
    print(dash)
    candidates_A = [
        {'signal': {'id': '1', 'symbol': 'EURUSD', 'type': 'BUY', 'wick_pct': 0.51},
         'score': 78.0,
         'scores': {'rsi': 25, 'wick': 18, 'pin_bar': 13, 'session': 11, 'ict': 0, 'history': 11},
         'ctx': {'wick_pct_real': 0.51},
         'raw': {'ict_explain': 'CLIFF: contra bias D1 + H4 expansion contraria'}},
        {'signal': {'id': '2', 'symbol': 'AUDUSD', 'type': 'BUY', 'wick_pct': 0.41},
         'score': 75.0,
         'scores': {'rsi': 22, 'wick': 14, 'pin_bar': 13, 'session': 11, 'ict': 0, 'history': 15},
         'ctx': {'wick_pct_real': 0.41},
         'raw': {'ict_explain': 'CLIFF: contra bias D1 + H4 expansion contraria'}},
        {'signal': {'id': '3', 'symbol': 'USDCAD', 'type': 'SELL', 'wick_pct': 0.42},
         'score': 76.0,
         'scores': {'rsi': 23, 'wick': 14, 'pin_bar': 13, 'session': 11, 'ict': 0, 'history': 15},
         'ctx': {'wick_pct_real': 0.42},
         'raw': {'ict_explain': 'CLIFF: contra bias D1 + H4 expansion contraria'}},
    ]
    cliffs_A = [c for c in candidates_A if c['scores']['ict'] == 0]
    viable_A = [c for c in candidates_A if c['scores']['ict'] > 0]
    print(f"  CLIFFs filtrados: {len(cliffs_A)}/{len(candidates_A)}")
    for c in cliffs_A:
        print(f"     X {c['signal']['symbol']} {c['signal']['type']}  -> REJEITADO_CLIFF")
    print(f"  Viaveis no pool : {len(viable_A)}")
    dec_A = pick_best_from_correlated(viable_A)
    print(f"  Winners: {len(dec_A['winners'])} / Losers: {len(dec_A['losers'])}")
    print()
    print("  RESULTADO Sprint 3: NENHUM trade aprovado (todos CLIFF).")
    print("  Historico real (sem Sprint 3): 3 trades aprovados, todos perderam.")
    print(f"  P&L evitado: -$237 (cluster 10:56) + -$26 (11:31) ~= -$263")

    # ── Cenário B: 1 a-favor, 2 contra ───────────────────────────────
    print()
    print("CENARIO B — Misto (1 a-favor, 2 contra)")
    print(dash)
    candidates_B = [
        {'signal': {'id': '4', 'symbol': 'EURUSD', 'type': 'BUY', 'wick_pct': 0.51},
         'score': 78.0,
         'scores': {'rsi': 25, 'wick': 18, 'pin_bar': 13, 'session': 11, 'ict': 0, 'history': 11},
         'ctx': {'wick_pct_real': 0.51},
         'raw': {'ict_explain': 'CLIFF'}},
        {'signal': {'id': '5', 'symbol': 'AUDUSD', 'type': 'SELL', 'wick_pct': 0.55},
         'score': 81.0,
         'scores': {'rsi': 23, 'wick': 18, 'pin_bar': 14, 'session': 11, 'ict': 22, 'history': 13},
         'ctx': {'wick_pct_real': 0.55},
         'raw': {'ict_explain': 'a-favor do bias D1 + H4 retracement'}},
        {'signal': {'id': '6', 'symbol': 'NZDUSD', 'type': 'SELL', 'wick_pct': 0.42},
         'score': 76.0,
         'scores': {'rsi': 22, 'wick': 14, 'pin_bar': 13, 'session': 11, 'ict': 18, 'history': 13},
         'ctx': {'wick_pct_real': 0.42},
         'raw': {'ict_explain': 'a-favor do bias D1, fases mistas'}},
    ]
    cliffs_B = [c for c in candidates_B if c['scores']['ict'] == 0]
    viable_B = [c for c in candidates_B if c['scores']['ict'] > 0]
    print(f"  CLIFFs filtrados: {len(cliffs_B)}  -> {[c['signal']['symbol'] for c in cliffs_B]}")
    print(f"  Viaveis no pool : {len(viable_B)}")
    dec_B = pick_best_from_correlated(viable_B)
    print(f"  Winners ({len(dec_B['winners'])}):")
    for w in dec_B['winners']:
        s = w['signal']
        print(f"     V {s['symbol']} {s['type']}  ICT={w['scores']['ict']}/25  Score={w['score']}/100")
    print(f"  Losers ({len(dec_B['losers'])}):")
    for loser, winner, reason in dec_B['losers']:
        s = loser['signal']
        print(f"     X {s['symbol']} {s['type']}  -- {reason}")

    # ── Cenário C: tie-breaker direcional ────────────────────────────
    print()
    print("CENARIO C — Tie-breaker (score tecnico alto perde p/ ICT alto)")
    print(dash)
    candidates_C = [
        {'signal': {'id': '7', 'symbol': 'AUDUSD', 'type': 'SELL', 'wick_pct': 0.45},
         'score': 88.0,
         'scores': {'rsi': 25, 'wick': 17, 'pin_bar': 14, 'session': 11, 'ict': 10, 'history': 11},
         'ctx': {'wick_pct_real': 0.45},
         'raw': {'ict_explain': 'contra bias D1 mas em consolidation'}},
        {'signal': {'id': '8', 'symbol': 'NZDUSD', 'type': 'SELL', 'wick_pct': 0.40},
         'score': 80.0,
         'scores': {'rsi': 22, 'wick': 16, 'pin_bar': 13, 'session': 11, 'ict': 22, 'history': 0},
         'ctx': {'wick_pct_real': 0.40},
         'raw': {'ict_explain': 'a-favor do bias D1 + H4 retracement'}},
    ]
    print(f"  Sinais entram no pool:")
    print(f"     AUDUSD SELL  score=88.0  ICT=10/25  (tecnico forte, ICT médio)")
    print(f"     NZDUSD SELL  score=80.0  ICT=22/25  (tecnico ok, ICT alto)")
    dec_C = pick_best_from_correlated(candidates_C)
    print(f"  Winner Sprint 3: {dec_C['winners'][0]['signal']['symbol']} {dec_C['winners'][0]['signal']['type']}")
    if dec_C['losers']:
        loser_sym = dec_C['losers'][0][0]['signal']['symbol']
        print(f"  Sprint 2 antigo (ordenacao por score puro) teria aprovado: {loser_sym}")
        print(f"  Diferenca: o vencedor agora tem alinhamento ICT 22/25 (alta probabilidade")
        print(f"             de continuação no pullback) em vez de 10/25 (consolidation).")

    print()
    print(sep)
    print(" CONCLUSAO")
    print(sep)
    print(" - Cenario A: 3 trades reais que perderam $263 -> 0 trades aprovados")
    print(" - Cenario B: cluster misto -> 1 winner alinhado, 1 loser CLIFF, 1 loser cluster")
    print(" - Cenario C: tie-breaker direcional escolhe ICT > score quando há trade-off")
    print()


if __name__ == "__main__":
    run()
