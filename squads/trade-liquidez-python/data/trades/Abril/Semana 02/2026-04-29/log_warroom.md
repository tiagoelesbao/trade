===================================================================
  WAR ROOM v6.2.0-ict  --  ANALISE TECNICA AGENTICA + Pool-then-Pick
-------------------------------------------------------------------
  Score minimo : 75/100   |   Correlacao: ATIVA (16 pares)   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)  +  ICT Context Engine (Sprint 2)
  Criterios    : RSI(25) Wick(20) PinBar(15) Sessao(10) ICT(25) Hist(5)
  Sessoes ICT  : asia_early(8) asia_judas(1) london_open(14) london_cont(11) ny_news_embargo(0) ny_expansion(13) london_close(12) ny_afternoon(7)
  Pares ativos : AUDUSD,GBPUSD,USDCAD,USDCHF,NZDUSD
  Pool-then-Pick: janela 30s  (poll 3s)  [Sprint 3]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE -> [ICT CONTEXT] -> [FASE 2] score -> [CLUSTER DECISION]
===================================================================
[01:30:51][WAR_ROOM]   war_room_started: War Room v6.2.0-ict iniciada | Score mínimo: 75/100 | 6 criterios (incl ICT) | pool=30s | correlated_pairs=16 | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[02:41:17] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[02:41:49] POOL CLOSED — ciclo #1  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 02:30:00  (verde)
  │     OHLC : O=1.36813  H=1.36823  L=1.36808  C=1.36814
  │     range=1.5 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 60%  (min 30%)   [bot reportou 60%]
  │     [OK ] RSI(9)    : 84.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=23h -> Asia early (post-NY)  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36814  SL=1.36873 (5.9 pips)  TP=1.36725 (8.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: expansion/up (conf 1.00) — último swing 61pips vs mediana 18pips
  │  Daily Range: Asia early (exhaustion post-NY)
  │  Liquidity above: 1.36994 (high, 17.9p)
  │  Liquidity below: 1.36809 (equal_high, 0.6p)
  │  Alignment BUY: 18/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[02:41:49][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD SELL  @1.36814  SL:1.36873  TP:1.36725  pavio:60%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  24.5/25  ( 98.0%)  RSI 84.4
   Wick     [##############]  20.0/20  (100.0%)  pavio 60%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [#######-------]   5.3/10  ( 53.0%)  Asia early (post-NY)
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=expansion/up
   Hist     [#####---------]   1.8/5  ( 36.0%)  WR 47%  (19T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   80.6/100  (+5.6 pts vs mínimo 75)
   Pior critério: Hist 1.8/5  (36% do máximo)
   → APROVADO  —  Score 80.6/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          98%  "RSI(9) 84.4 -> 24.5/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 60% (wick 20.0), corpo 7% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          47%  "Sessao Asia early (post-NY) (5.3/10), WR 30d 47% em 19T (1.8/5) -> 7.1/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=expansion/up | daily_state=asia_early -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
-------------------------------------------------------------------
  Ciclo #1: 1 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[03:11:32] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[03:12:04] POOL CLOSED — ciclo #2  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 03:00:00  (verde)
  │     OHLC : O=1.35236  H=1.35277  L=1.35236  C=1.35253
  │     range=4.1 pips   corpo=41% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 59%  (min 30%)   [bot reportou 59%]
  │     [OK ] RSI(9)    : 88.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=00h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35253  SL=1.35327 (7.4 pips)  TP=1.35142 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/up (conf 0.91) — último swing 128pips vs mediana 70pips
  │  H1: consolidation/neutral (conf 0.70) — range 78pips ~ swing médio 76pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35328 (equal_high, 7.5p)
  │  Liquidity below: 1.34818 (equal_low, 43.5p)
  │  Alignment BUY: 14/25  |  SELL: 10/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 03:00:00  (verde)
  │     OHLC : O=0.58872  H=0.58915  L=0.58872  C=0.58881
  │     range=4.3 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 79%  (min 30%)   [bot reportou 79%]
  │     [OK ] RSI(9)    : 84.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=00h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58881  SL=0.58965 (8.4 pips)  TP=0.58755 (12.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: BULLISH ↑
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 0.58885 (equal_low, 0.3p)
  │  Liquidity below: 0.58790 (equal_low, 9.2p)
  │  Alignment BUY: 20/25  |  SELL: 9/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=10/25  Score=60.7/100
  │  ✗ LOSER   NZDUSD SELL  -- perdeu para GBPUSD SELL (ICT 10 vs 9, score 60.7 vs 69.3)
  └──

[03:12:05][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD SELL  @0.58881  SL:0.58965  TP:0.58755  pavio:79%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  24.6/25  ( 98.4%)  RSI 84.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 79%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 21% range  [bom]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [#####---------]   9.0/25  ( 36.0%)  D1=bullish H4=reversal/down H1=unknown/down
   Hist     [##############]     5/5  (100.0%)  WR 67%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.3/100  (-5.7 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 10 vs 9, score 60.7 vs 69.3)
   ────────────────────────────────────────────────────────────
   [M] Momentum          98%  "RSI(9) 84.5 -> 24.6/25 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 79% (wick 20.0), corpo 21% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          38%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 67% em 15T (5.0/5) -> 5.7/15 pts."
   [I] ICT Macro         36%  "D1 bias=bullish | H4=reversal/down | H1=unknown/down | daily_state=asia_judas -> 9.0/25 pts. 7/25 — contra bias D1, contexto fraco + raid liquidity below @0.58790 = 9/25"
[03:12:05][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD SELL preterido: perdeu para GBPUSD SELL (ICT 10 vs 9, score 60.7 vs 69.3)

-------------------------------------------------------------------

[03:12:05][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35253  SL:1.35327  TP:1.35142  pavio:59%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 88.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 59%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 42% range  [aceitável]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [######--------]  10.0/25  ( 40.0%)  D1=neutral H4=expansion/up H1=consolidation/neutral
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.7/100  (-14.3 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 60.7 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 88.9 -> 25.0/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 59% (wick 20.0), corpo 41% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         40%  "D1 bias=neutral | H4=expansion/up | H1=consolidation/neutral | daily_state=asia_judas -> 10.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro - liquidity above @1.35328 próxima (risco) = 10/25"
-------------------------------------------------------------------
  Ciclo #2: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[06:11:28] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[06:12:00] POOL CLOSED — ciclo #3  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 06:00:00  (verde)
  │     OHLC : O=0.58599  H=0.58625  L=0.58559  C=0.58599
  │     range=6.6 pips   corpo=0% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 61%  (min 30%)   [bot reportou 61%]
  │     [OK ] RSI(9)    : 20.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58599  SL=0.58509 (9.0 pips)  TP=0.58734 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: BULLISH ↑
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 0.58738 (equal_low, 13.9p)
  │  Liquidity below: 0.58487 (low, 11.2p)
  │  Alignment BUY: 20/25  |  SELL: 9/25
  └──


-------------------------------------------------------------------

[06:12:00][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD BUY  @0.58599  SL:0.58509  TP:0.58734  pavio:61%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  20.2/25  ( 80.8%)  RSI 20.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 61%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 0% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=bullish H4=reversal/down H1=unknown/down
   Hist     [##############]     5/5  (100.0%)  WR 67%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   80.9/100  (+5.9 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → APROVADO  —  Score 80.9/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          81%  "RSI(9) 20.2 -> 20.2/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 61% (wick 20.0), corpo 0% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          38%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 67% em 15T (5.0/5) -> 5.7/15 pts."
   [I] ICT Macro         80%  "D1 bias=bullish | H4=reversal/down | H1=unknown/down | daily_state=asia_judas -> 20.0/25 pts. 18/25 — a-favor do bias D1, fases mistas + raid liquidity above @0.58738 = 20/25"
-------------------------------------------------------------------
  Ciclo #3: 1 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[06:41:35] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[06:42:06] POOL CLOSED — ciclo #4  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 06:30:00  (verde)
  │     OHLC : O=0.71621  H=0.71636  L=0.71613  C=0.71626
  │     range=2.3 pips   corpo=22% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 35%  (min 30%)   [bot reportou 35%]
  │     [OK ] RSI(9)    : 23.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71626  SL=0.71563 (6.3 pips)  TP=0.71720 (9.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: BULLISH ↑
  │  H4: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  H1: consolidation/neutral (conf 0.70) — range 43pips ~ swing médio 36pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 0.71647 (equal_high, 1.8p)
  │  Liquidity below: 0.71567 (equal_high, 6.2p)
  │  Alignment BUY: 20/25  |  SELL: 12/25
  └──


-------------------------------------------------------------------

[06:42:07][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD BUY  @0.71626  SL:0.71563  TP:0.71720  pavio:35%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.3/25  ( 69.2%)  RSI 23.2
   Wick     [##########----]  13.9/20  ( 69.5%)  pavio 35%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 22% range  [bom]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=bullish H4=unknown/neutral H1=consolidation/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.0/100  (-12.0 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 63.0 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          69%  "RSI(9) 23.2 -> 17.3/25 pts. Gate: 30."
   [R] Rejeicao          68%  "Pavio 35% (wick 13.9), corpo 22% (pin 10.0) -> 23.9/35 pts."
   [C] Contexto          12%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 44% em 27T (1.1/5) -> 1.8/15 pts."
   [I] ICT Macro         80%  "D1 bias=bullish | H4=unknown/neutral | H1=consolidation/neutral | daily_state=asia_judas -> 20.0/25 pts. 18/25 — a-favor do bias D1, fases mistas + raid liquidity above @0.71647 = 20/25"
-------------------------------------------------------------------
  Ciclo #4: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[06:56:29] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[06:57:00] POOL CLOSED — ciclo #5  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 06:45:00  (vermelha)
  │     OHLC : O=1.35118  H=1.35124  L=1.35101  C=1.35111
  │     range=2.3 pips   corpo=30% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 26.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35111  SL=1.35051 (6.0 pips)  TP=1.35201 (9.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: consolidation/neutral (conf 0.70) — range 78pips ~ swing médio 76pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35328 (equal_high, 22.0p)
  │  Liquidity below: 1.34818 (equal_low, 29.0p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[06:57:01][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.35111  SL:1.35051  TP:1.35201  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  14.1/25  ( 56.4%)  RSI 26.7
   Wick     [############--]  17.4/20  ( 87.0%)  pavio 43%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 30% range  [aceitável]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=consolidation/neutral
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   51.2/100  (-23.8 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 51.2 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          56%  "RSI(9) 26.7 -> 14.1/25 pts. Gate: 30."
   [R] Rejeicao          64%  "Pavio 43% (wick 17.4), corpo 30% (pin 5.0) -> 22.4/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.35328 = 14/25"
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[07:26:35] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[07:27:07] POOL CLOSED — ciclo #6  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 07:15:00  (vermelha)
  │     OHLC : O=1.35132  H=1.35133  L=1.35118  C=1.35131
  │     range=1.5 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 87%  (min 30%)   [bot reportou 87%]
  │     [OK ] RSI(9)    : 28.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35131  SL=1.35068 (6.3 pips)  TP=1.35225 (9.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: consolidation/neutral (conf 0.70) — range 78pips ~ swing médio 76pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35328 (equal_high, 18.7p)
  │  Liquidity below: 1.34818 (equal_low, 32.3p)
  │  Alignment BUY: 14/25  |  SELL: 12/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 07:15:00  (verde)
  │     OHLC : O=1.36859  H=1.36872  L=1.36858  C=1.36862
  │     range=1.4 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 71%  (min 30%)   [bot reportou 71%]
  │     [OK ] RSI(9)    : 82.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36862  SL=1.36922 (6.0 pips)  TP=1.36772 (9.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.36994 (high, 13.5p)
  │  Liquidity below: 1.36809 (equal_high, 5.0p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCAD SELL  ICT=14/25  Score=69.8/100
  │  ✗ LOSER   GBPUSD BUY  -- perdeu para USDCAD SELL (ICT 14 vs 14, score 69.8 vs 62.3)
  └──

[07:27:07][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ○ GBPUSD BUY  @1.35131  SL:1.35068  TP:1.35225  pavio:87%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  12.6/25  ( 50.4%)  RSI 28.3
   Wick     [##############]  20.0/20  (100.0%)  pavio 87%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=consolidation/neutral
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   62.3/100  (-12.7 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCAD SELL (ICT 14 vs 14, score 69.8 vs 62.3)
   ────────────────────────────────────────────────────────────
   [M] Momentum          50%  "RSI(9) 28.3 -> 12.6/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 87% (wick 20.0), corpo 7% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.35328 = 14/25"
[07:27:08][WAR_ROOM] [GBPUSD]   cluster_decision: GBPUSD BUY preterido: perdeu para USDCAD SELL (ICT 14 vs 14, score 69.8 vs 62.3)

-------------------------------------------------------------------

[07:27:08][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD SELL  @1.36862  SL:1.36922  TP:1.36772  pavio:71%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  22.6/25  ( 90.4%)  RSI 82.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 71%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 21% range  [bom]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=unknown/neutral
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.8/100  (-5.2 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 69.8 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          90%  "RSI(9) 82.5 -> 22.6/25 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 71% (wick 20.0), corpo 21% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          21%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 50% em 20T (2.5/5) -> 3.2/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=unknown/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
-------------------------------------------------------------------
  Ciclo #6: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[08:26:23] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[08:26:54] POOL CLOSED — ciclo #7  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 08:15:00  (verde)
  │     OHLC : O=1.36887  H=1.36904  L=1.36885  C=1.36887
  │     range=1.9 pips   corpo=0% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 89%  (min 30%)   [bot reportou 89%]
  │     [OK ] RSI(9)    : 82.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36887  SL=1.36954 (6.7 pips)  TP=1.36787 (10.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.36994 (high, 10.9p)
  │  Liquidity below: 1.36809 (equal_high, 7.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 08:15:00  (verde)
  │     OHLC : O=0.78934  H=0.78947  L=0.78931  C=0.78936
  │     range=1.6 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 69%  (min 30%)   [bot reportou 69%]
  │     [OK ] RSI(9)    : 90.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78936  SL=0.78997 (6.1 pips)  TP=0.78844 (9.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 114pips ~ swing médio 81pips
  │  H1: unknown/up (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 0.79336 (high, 40.5p)
  │  Liquidity below: 0.78755 (equal_high, 17.6p)
  │  Alignment BUY: 10/25  |  SELL: 18/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF SELL  ICT=18/25  Score=79.8/100
  │  ✗ LOSER   USDCAD SELL  -- perdeu para USDCHF SELL (ICT 18 vs 14, score 79.8 vs 74.9)
  └──

[08:26:55][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD SELL  @1.36887  SL:1.36954  TP:1.36787  pavio:89%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  22.7/25  ( 90.8%)  RSI 82.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 89%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 0% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/neutral
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.9/100  (-0.1 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF SELL (ICT 18 vs 14, score 79.8 vs 74.9)
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 82.5 -> 22.7/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 89% (wick 20.0), corpo 0% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          21%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 50% em 20T (2.5/5) -> 3.2/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
[08:26:55][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD SELL preterido: perdeu para USDCHF SELL (ICT 18 vs 14, score 79.8 vs 74.9)

-------------------------------------------------------------------

[08:26:55][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78936  SL:0.78997  TP:0.78844  pavio:69%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 90.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 69%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=bearish H4=consolidation/neutral H1=unknown/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.8/100  (+4.8 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 90.2 -> 25.0/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 69% (wick 20.0), corpo 12% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          12%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 44% em 9T (1.1/5) -> 1.8/15 pts."
   [I] ICT Macro         72%  "D1 bias=bearish | H4=consolidation/neutral | H1=unknown/up | daily_state=asia_judas -> 18.0/25 pts. 16/25 — a-favor do bias D1 + H4 consolidation (range) + raid liquidity below @0.78755 = 18/25"
-------------------------------------------------------------------
  Ciclo #7: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[08:41:11] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[08:41:43] POOL CLOSED — ciclo #8  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 08:30:00  (vermelha)
  │     OHLC : O=1.35077  H=1.35089  L=1.35028  C=1.35060
  │     range=6.1 pips   corpo=28% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 52%  (min 30%)   [bot reportou 52%]
  │     [OK ] RSI(9)    : 18.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35060  SL=1.34978 (8.2 pips)  TP=1.35183 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: consolidation/neutral (conf 0.70) — range 78pips ~ swing médio 65pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35328 (equal_high, 26.8p)
  │  Liquidity below: 1.34818 (equal_low, 24.2p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 08:30:00  (vermelha)
  │     OHLC : O=1.36887  H=1.36913  L=1.36881  C=1.36886
  │     range=3.2 pips   corpo=3% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 81%  (min 30%)   [bot reportou 81%]
  │     [OK ] RSI(9)    : 78.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36886  SL=1.36963 (7.7 pips)  TP=1.36770 (11.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.36994 (high, 10.7p)
  │  Liquidity below: 1.36809 (equal_high, 7.8p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCAD SELL  ICT=14/25  Score=71.5/100
  │  ✗ LOSER   GBPUSD BUY  -- perdeu para USDCAD SELL (ICT 14 vs 14, score 71.5 vs 66.7)
  └──

[08:41:44][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ○ GBPUSD BUY  @1.35060  SL:1.34978  TP:1.35183  pavio:52%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  22.0/25  ( 88.0%)  RSI 18.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 52%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 28% range  [bom]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=consolidation/neutral
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   66.7/100  (-8.3 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCAD SELL (ICT 14 vs 14, score 71.5 vs 66.7)
   ────────────────────────────────────────────────────────────
   [M] Momentum          88%  "RSI(9) 18.2 -> 22.0/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 52% (wick 20.0), corpo 28% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.35328 = 14/25"
[08:41:44][WAR_ROOM] [GBPUSD]   cluster_decision: GBPUSD BUY preterido: perdeu para USDCAD SELL (ICT 14 vs 14, score 71.5 vs 66.7)

-------------------------------------------------------------------

[08:41:44][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD SELL  @1.36886  SL:1.36963  TP:1.36770  pavio:81%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.3/25  ( 77.2%)  RSI 78.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 81%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 3% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/neutral
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.5/100  (-3.5 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 71.5 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          77%  "RSI(9) 78.9 -> 19.3/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 81% (wick 20.0), corpo 3% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          21%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 50% em 20T (2.5/5) -> 3.2/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
-------------------------------------------------------------------
  Ciclo #8: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[08:41:57] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[08:42:29] POOL CLOSED — ciclo #9  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 08:30:00  (verde)
  │     OHLC : O=0.78936  H=0.78975  L=0.78927  C=0.78951
  │     range=4.8 pips   corpo=31% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 90.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78951  SL=0.79025 (7.4 pips)  TP=0.78840 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 114pips ~ swing médio 81pips
  │  H1: retracement/down (conf 0.70) — retraçao ~33% do último swing
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 0.79336 (high, 38.8p)
  │  Liquidity below: 0.78755 (equal_high, 19.3p)
  │  Alignment BUY: 10/25  |  SELL: 18/25
  └──


-------------------------------------------------------------------

[08:42:29][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78951  SL:0.79025  TP:0.78840  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 90.4
   Wick     [##############]  20.0/20  (100.0%)  pavio 50%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 31% range  [aceitável]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=bearish H4=consolidation/neutral H1=retracement/down
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.8/100  (-5.2 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 69.8 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 90.4 -> 25.0/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 50% (wick 20.0), corpo 31% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          12%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 44% em 9T (1.1/5) -> 1.8/15 pts."
   [I] ICT Macro         72%  "D1 bias=bearish | H4=consolidation/neutral | H1=retracement/down | daily_state=asia_judas -> 18.0/25 pts. 16/25 — a-favor do bias D1 + H4 consolidation (range) + raid liquidity below @0.78755 = 18/25"
-------------------------------------------------------------------
  Ciclo #9: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[08:56:23] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[08:56:55] POOL CLOSED — ciclo #10  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 08:45:00  (verde)
  │     OHLC : O=1.36886  H=1.36899  L=1.36875  C=1.36890
  │     range=2.4 pips   corpo=17% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 37%  (min 30%)   [bot reportou 37%]
  │     [OK ] RSI(9)    : 72.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36890  SL=1.36949 (5.9 pips)  TP=1.36802 (8.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.36994 (high, 10.6p)
  │  Liquidity below: 1.36809 (equal_high, 7.9p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 08:45:00  (verde)
  │     OHLC : O=0.78951  H=0.78960  L=0.78937  C=0.78953
  │     range=2.3 pips   corpo=9% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 30%  (min 30%)   [bot reportou 30%]
  │     [OK ] RSI(9)    : 89.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78953  SL=0.79010 (5.7 pips)  TP=0.78868 (8.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 114pips ~ swing médio 81pips
  │  H1: unknown/up (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: —
  │  Liquidity below: 0.78755 (equal_high, 18.3p)
  │  Alignment BUY: 10/25  |  SELL: 18/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF SELL  ICT=18/25  Score=72.0/100
  │  ✗ LOSER   USDCAD SELL  -- perdeu para USDCHF SELL (ICT 18 vs 14, score 72.0 vs 55.3)
  └──

[08:56:56][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD SELL  @1.36890  SL:1.36949  TP:1.36802  pavio:37%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  13.1/25  ( 52.4%)  RSI 72.2
   Wick     [##########----]  15.0/20  ( 75.0%)  pavio 37%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 17% range  [bom]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/neutral
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   55.3/100  (-19.7 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF SELL (ICT 18 vs 14, score 72.0 vs 55.3)
   ────────────────────────────────────────────────────────────
   [M] Momentum          52%  "RSI(9) 72.2 -> 13.1/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 37% (wick 15.0), corpo 17% (pin 10.0) -> 25.0/35 pts."
   [C] Contexto          21%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 50% em 20T (2.5/5) -> 3.2/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/neutral | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
[08:56:56][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD SELL preterido: perdeu para USDCHF SELL (ICT 18 vs 14, score 72.0 vs 55.3)

-------------------------------------------------------------------

[08:56:56][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78953  SL:0.79010  TP:0.78868  pavio:30%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 89.0
   Wick     [#########-----]  12.2/20  ( 61.0%)  pavio 30%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 9% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=bearish H4=consolidation/neutral H1=unknown/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.0/100  (-3.0 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 72.0 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 89.0 -> 25.0/25 pts. Gate: 70."
   [R] Rejeicao          78%  "Pavio 30% (wick 12.2), corpo 9% (pin 15.0) -> 27.2/35 pts."
   [C] Contexto          12%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 44% em 9T (1.1/5) -> 1.8/15 pts."
   [I] ICT Macro         72%  "D1 bias=bearish | H4=consolidation/neutral | H1=unknown/up | daily_state=asia_judas -> 18.0/25 pts. 16/25 — a-favor do bias D1 + H4 consolidation (range) + raid liquidity below @0.78755 = 18/25"
-------------------------------------------------------------------
  Ciclo #10: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[09:26:27] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[09:26:59] POOL CLOSED — ciclo #11  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 09:15:00  (verde)
  │     OHLC : O=1.34988  H=1.35000  L=1.34959  C=1.34989
  │     range=4.1 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 71%  (min 30%)   [bot reportou 71%]
  │     [OK ] RSI(9)    : 3.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34989  SL=1.34909 (8.0 pips)  TP=1.35109 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: consolidation/neutral (conf 0.70) — range 73pips ~ swing médio 65pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35328 (equal_high, 36.0p)
  │  Liquidity below: 1.34818 (equal_low, 15.0p)
  │  Alignment BUY: 10/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 09:15:00  (vermelha)
  │     OHLC : O=0.78949  H=0.78960  L=0.78924  C=0.78931
  │     range=3.6 pips   corpo=50% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 73.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78931  SL=0.79010 (7.9 pips)  TP=0.78812 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 114pips ~ swing médio 81pips
  │  H1: retracement/down (conf 0.70) — retraçao ~34% do último swing
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: —
  │  Liquidity below: 0.78755 (equal_high, 19.6p)
  │  Alignment BUY: 10/25  |  SELL: 18/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF SELL  ICT=18/25  Score=47.8/100
  │  ✗ LOSER   GBPUSD BUY  -- perdeu para USDCHF SELL (ICT 18 vs 10, score 47.8 vs 70.7)
  └──

[09:27:00][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ○ GBPUSD BUY  @1.34989  SL:1.34909  TP:1.35109  pavio:71%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 3.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 71%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [######--------]  10.0/25  ( 40.0%)  D1=neutral H4=consolidation/neutral H1=consolidation/neutral
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.7/100  (-4.3 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF SELL (ICT 18 vs 10, score 47.8 vs 70.7)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 3.9 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 71% (wick 20.0), corpo 2% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         40%  "D1 bias=neutral | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=asia_judas -> 10.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro - liquidity below @1.34818 próxima (risco) = 10/25"
[09:27:00][WAR_ROOM] [GBPUSD]   cluster_decision: GBPUSD BUY preterido: perdeu para USDCHF SELL (ICT 18 vs 10, score 47.8 vs 70.7)

-------------------------------------------------------------------

[09:27:00][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78931  SL:0.79010  TP:0.78812  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.8/25  ( 55.2%)  RSI 73.0
   Wick     [#########-----]  12.2/20  ( 61.0%)  pavio 31%
   PinBar   [##------------]   2.0/15  ( 13.3%)  corpo 50% range  [suja]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=bearish H4=consolidation/neutral H1=retracement/down
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   47.8/100  (-27.2 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 47.8 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          55%  "RSI(9) 73.0 -> 13.8/25 pts. Gate: 70."
   [R] Rejeicao          41%  "Pavio 31% (wick 12.2), corpo 50% (pin 2.0) -> 14.2/35 pts."
   [C] Contexto          12%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 44% em 9T (1.1/5) -> 1.8/15 pts."
   [I] ICT Macro         72%  "D1 bias=bearish | H4=consolidation/neutral | H1=retracement/down | daily_state=asia_judas -> 18.0/25 pts. 16/25 — a-favor do bias D1 + H4 consolidation (range) + raid liquidity below @0.78755 = 18/25"
-------------------------------------------------------------------
  Ciclo #11: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[09:41:20] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[09:41:52] POOL CLOSED — ciclo #12  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 09:30:00  (verde)
  │     OHLC : O=1.34989  H=1.35041  L=1.34945  C=1.34996
  │     range=9.6 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 8.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34996  SL=1.34895 (10.1 pips)  TP=1.35147 (15.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: consolidation/neutral (conf 0.70) — range 73pips ~ swing médio 65pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35328 (equal_high, 33.1p)
  │  Liquidity below: 1.34818 (equal_low, 17.8p)
  │  Alignment BUY: 12/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[09:41:52][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34996  SL:1.34895  TP:1.35147  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 8.1
   Wick     [#############-]  18.3/20  ( 91.5%)  pavio 46%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [#######-------]  12.0/25  ( 48.0%)  D1=neutral H4=consolidation/neutral H1=consolidation/neutral
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.0/100  (-4.0 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 71.0 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 8.1 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          95%  "Pavio 46% (wick 18.3), corpo 7% (pin 15.0) -> 33.3/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         48%  "D1 bias=neutral | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=asia_judas -> 12.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro = 12/25"
-------------------------------------------------------------------
  Ciclo #12: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[10:41:21] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[10:41:53] POOL CLOSED — ciclo #13  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 10:30:00  (vermelha)
  │     OHLC : O=1.36837  H=1.36838  L=1.36799  C=1.36813
  │     range=3.9 pips   corpo=62% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 25.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=07h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36813  SL=1.36749 (6.4 pips)  TP=1.36909 (9.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~57% do último swing
  │  Daily Range: London open expansion
  │  Liquidity above: 1.36994 (high, 17.9p)
  │  Liquidity below: 1.36809 (equal_high, 0.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[10:41:53][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36813  SL:1.36749  TP:1.36909  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  15.4/25  ( 61.6%)  RSI 25.3
   Wick     [##########----]  14.4/20  ( 72.0%)  pavio 36%
   PinBar   [#-------------]   1.5/15  ( 10.0%)  corpo 62% range  [suja]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   57.1/100  (-17.9 pts vs mínimo 75)
   Pior critério: PinBar 1.5/15  (10% do máximo)
   → REJEITADO  —  Score 57.1 < 75 | fraco: Pin Bar 1.5/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          62%  "RSI(9) 25.3 -> 15.4/25 pts. Gate: 30."
   [R] Rejeicao          45%  "Pavio 36% (wick 14.4), corpo 62% (pin 1.5) -> 15.9/35 pts."
   [C] Contexto          79%  "Sessao London open expansion (9.3/10), WR 30d 50% em 20T (2.5/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36994 = 14/25"
-------------------------------------------------------------------
  Ciclo #13: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[10:56:14] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[10:56:45] POOL CLOSED — ciclo #14  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 10:45:00  (vermelha)
  │     OHLC : O=1.36813  H=1.36820  L=1.36780  C=1.36800
  │     range=4.0 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 23.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=07h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36800  SL=1.36730 (7.0 pips)  TP=1.36905 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~42% do último swing
  │  Daily Range: London open expansion
  │  Liquidity above: 1.36782 (equal_high, 0.2p)
  │  Liquidity below: 1.36747 (equal_high, 3.2p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[10:56:46][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36800  SL:1.36730  TP:1.36905  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.1/25  ( 68.4%)  RSI 23.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 50%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 32% range  [aceitável]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   67.9/100  (-7.1 pts vs mínimo 75)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → REJEITADO  —  Score 67.9 < 75 | fraco: Pin Bar 5.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          68%  "RSI(9) 23.5 -> 17.1/25 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 50% (wick 20.0), corpo 33% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          79%  "Sessao London open expansion (9.3/10), WR 30d 50% em 20T (2.5/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36782 = 14/25"
-------------------------------------------------------------------
  Ciclo #14: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[11:11:28] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[11:11:59] POOL CLOSED — ciclo #15  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 11:00:00  (verde)
  │     OHLC : O=1.36802  H=1.36816  L=1.36763  C=1.36815
  │     range=5.3 pips   corpo=25% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 74%  (min 30%)   [bot reportou 74%]
  │     [OK ] RSI(9)    : 28.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36815  SL=1.36713 (10.2 pips)  TP=1.36968 (15.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~57% do último swing
  │  Daily Range: London open expansion
  │  Liquidity above: 1.36994 (high, 17.9p)
  │  Liquidity below: 1.36809 (equal_high, 0.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[11:12:00][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36815  SL:1.36713  TP:1.36968  pavio:74%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  12.6/25  ( 50.4%)  RSI 28.3
   Wick     [##############]  20.0/20  (100.0%)  pavio 74%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 24% range  [bom]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.4/100  (-6.6 pts vs mínimo 75)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → REJEITADO  —  Score 68.4 < 75 | fraco: Histórico 2.5/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          50%  "RSI(9) 28.3 -> 12.6/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 74% (wick 20.0), corpo 25% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          79%  "Sessao London open expansion (9.3/10), WR 30d 50% em 20T (2.5/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36994 = 14/25"
-------------------------------------------------------------------
  Ciclo #15: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[11:26:21] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[11:26:52] POOL CLOSED — ciclo #16  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 11:15:00  (vermelha)
  │     OHLC : O=1.36815  H=1.36831  L=1.36789  C=1.36806
  │     range=4.2 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 40%  (min 30%)   [bot reportou 40%]
  │     [OK ] RSI(9)    : 16.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36806  SL=1.36739 (6.7 pips)  TP=1.36906 (10.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~51% do último swing
  │  Daily Range: London open expansion
  │  Liquidity above: 1.36809 (equal_high, 0.9p)
  │  Liquidity below: 1.36782 (equal_high, 1.8p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[11:26:53][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD BUY  @1.36806  SL:1.36739  TP:1.36906  pavio:40%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  23.3/25  ( 93.2%)  RSI 16.9
   Wick     [###########---]  16.2/20  ( 81.0%)  pavio 40%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 21% range  [bom]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.3/100  (+0.3 pts vs mínimo 75)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 75.3/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          93%  "RSI(9) 16.9 -> 23.3/25 pts. Gate: 30."
   [R] Rejeicao          75%  "Pavio 40% (wick 16.2), corpo 21% (pin 10.0) -> 26.2/35 pts."
   [C] Contexto          79%  "Sessao London open expansion (9.3/10), WR 30d 50% em 20T (2.5/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36809 = 14/25"
-------------------------------------------------------------------
  Ciclo #16: 1 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[14:41:25] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[14:41:57] POOL CLOSED — ciclo #17  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 14:30:00  (vermelha)
  │     OHLC : O=0.78916  H=0.78924  L=0.78880  C=0.78915
  │     range=4.4 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 80%  (min 30%)   [bot reportou 80%]
  │     [OK ] RSI(9)    : 27.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=11h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78915  SL=0.78830 (8.5 pips)  TP=0.79043 (12.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 94pips ~ swing médio 81pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: London continuation
  │  Liquidity above: 0.79112 (high, 20.4p)
  │  Liquidity below: 0.78847 (equal_low, 6.1p)
  │  Alignment BUY: 12/25  |  SELL: 18/25
  └──


-------------------------------------------------------------------

[14:41:57][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78915  SL:0.78830  TP:0.79043  pavio:80%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.5/25  ( 54.0%)  RSI 27.3
   Wick     [##############]  20.0/20  (100.0%)  pavio 80%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [#######-------]  12.0/25  ( 48.0%)  D1=bearish H4=consolidation/neutral H1=unknown/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.9/100  (-6.1 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → REJEITADO  —  Score 68.9 < 75 | fraco: Histórico 1.1/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          54%  "RSI(9) 27.3 -> 13.5/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 80% (wick 20.0), corpo 2% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          56%  "Sessao London continuation (7.3/10), WR 30d 44% em 9T (1.1/5) -> 8.4/15 pts."
   [I] ICT Macro         48%  "D1 bias=bearish | H4=consolidation/neutral | H1=unknown/neutral | daily_state=london_cont -> 12.0/25 pts. 10/25 — contra bias D1 mas em consolidation + raid liquidity above @0.79112 = 12/25"
-------------------------------------------------------------------
  Ciclo #17: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[15:11:28] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[15:11:59] POOL CLOSED — ciclo #18  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 15:00:00  (vermelha)
  │     OHLC : O=1.36796  H=1.36800  L=1.36729  C=1.36755
  │     range=7.1 pips   corpo=58% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 37%  (min 30%)   [bot reportou 37%]
  │     [OK ] RSI(9)    : 20.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36755  SL=1.36679 (7.6 pips)  TP=1.36869 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~32% do último swing
  │  Daily Range: London continuation
  │  Liquidity above: 1.36782 (equal_high, 2.5p)
  │  Liquidity below: 1.36747 (equal_high, 0.9p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 15:00:00  (vermelha)
  │     OHLC : O=0.78932  H=0.78938  L=0.78873  C=0.78905
  │     range=6.5 pips   corpo=42% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 13.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78905  SL=0.78823 (8.2 pips)  TP=0.79028 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 94pips ~ swing médio 81pips
  │  H1: consolidation/neutral (conf 0.70) — range 29pips ~ swing médio 24pips
  │  Daily Range: London continuation
  │  Liquidity above: 0.79112 (high, 20.7p)
  │  Liquidity below: 0.78847 (equal_low, 5.8p)
  │  Alignment BUY: 12/25  |  SELL: 18/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCAD BUY  ICT=14/25  Score=60.5/100
  │  ✗ LOSER   USDCHF BUY  -- perdeu para USDCAD BUY (ICT 14 vs 12, score 60.5 vs 70.1)
  └──

[15:11:59][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ○ USDCHF BUY  @0.78905  SL:0.78823  TP:0.79028  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 13.7
   Wick     [##############]  19.7/20  ( 98.5%)  pavio 49%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 42% range  [aceitável]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [#######-------]  12.0/25  ( 48.0%)  D1=bearish H4=consolidation/neutral H1=consolidation/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.1/100  (-4.9 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCAD BUY (ICT 14 vs 12, score 60.5 vs 70.1)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 13.7 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 49% (wick 19.7), corpo 42% (pin 5.0) -> 24.7/35 pts."
   [C] Contexto          56%  "Sessao London continuation (7.3/10), WR 30d 44% em 9T (1.1/5) -> 8.4/15 pts."
   [I] ICT Macro         48%  "D1 bias=bearish | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=london_cont -> 12.0/25 pts. 10/25 — contra bias D1 mas em consolidation + raid liquidity above @0.79112 = 12/25"
[15:12:00][WAR_ROOM] [USDCHF]   cluster_decision: USDCHF BUY preterido: perdeu para USDCAD BUY (ICT 14 vs 12, score 60.5 vs 70.1)

-------------------------------------------------------------------

[15:12:00][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36755  SL:1.36679  TP:1.36869  pavio:37%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.8/25  ( 79.2%)  RSI 20.6
   Wick     [##########----]  14.6/20  ( 73.0%)  pavio 37%
   PinBar   [##------------]   1.7/15  ( 11.3%)  corpo 58% range  [suja]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.5/100  (-14.5 pts vs mínimo 75)
   Pior critério: PinBar 1.7/15  (11% do máximo)
   → REJEITADO  —  Score 60.5 < 75 | fraco: Pin Bar 1.7/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          79%  "RSI(9) 20.6 -> 19.8/25 pts. Gate: 30."
   [R] Rejeicao          47%  "Pavio 37% (wick 14.6), corpo 58% (pin 1.7) -> 16.3/35 pts."
   [C] Contexto          69%  "Sessao London continuation (7.3/10), WR 30d 52% em 21T (3.1/5) -> 10.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36782 = 14/25"
-------------------------------------------------------------------
  Ciclo #18: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[15:26:21] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[15:26:52] POOL CLOSED — ciclo #19  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 15:15:00  (vermelha)
  │     OHLC : O=0.71630  H=0.71661  L=0.71611  C=0.71620
  │     range=5.0 pips   corpo=20% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 62%  (min 30%)   [bot reportou 62%]
  │     [OK ] RSI(9)    : 70.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71620  SL=0.71711 (9.1 pips)  TP=0.71483 (13.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: BULLISH ↑
  │  H4: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  H1: consolidation/neutral (conf 0.70) — range 40pips ~ swing médio 36pips
  │  Daily Range: London continuation
  │  Liquidity above: 0.71647 (equal_high, 4.6p)
  │  Liquidity below: 0.71567 (equal_high, 3.4p)
  │  Alignment BUY: 20/25  |  SELL: 12/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 15:15:00  (verde)
  │     OHLC : O=0.78905  H=0.78912  L=0.78877  C=0.78906
  │     range=3.5 pips   corpo=3% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 80%  (min 30%)   [bot reportou 80%]
  │     [OK ] RSI(9)    : 20.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78906  SL=0.78827 (7.9 pips)  TP=0.79024 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 94pips ~ swing médio 81pips
  │  H1: consolidation/neutral (conf 0.70) — range 29pips ~ swing médio 24pips
  │  Daily Range: London continuation
  │  Liquidity above: 0.79112 (high, 18.5p)
  │  Liquidity below: 0.78847 (equal_low, 8.0p)
  │  Alignment BUY: 12/25  |  SELL: 18/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF BUY  ICT=12/25  Score=75.1/100
  │  ✗ LOSER   AUDUSD SELL  -- perdeu para USDCHF BUY (ICT 12 vs 12, score 75.1 vs 61.4)
  └──

[15:26:53][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ○ AUDUSD SELL  @0.71620  SL:0.71711  TP:0.71483  pavio:62%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  11.0/25  ( 44.0%)  RSI 70.0
   Wick     [##############]  20.0/20  (100.0%)  pavio 62%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 20% range  [bom]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [#######-------]  12.0/25  ( 48.0%)  D1=bullish H4=unknown/neutral H1=consolidation/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.4/100  (-13.6 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF BUY (ICT 12 vs 12, score 75.1 vs 61.4)
   ────────────────────────────────────────────────────────────
   [M] Momentum          44%  "RSI(9) 70.0 -> 11.0/25 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 62% (wick 20.0), corpo 20% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          56%  "Sessao London continuation (7.3/10), WR 30d 44% em 27T (1.1/5) -> 8.4/15 pts."
   [I] ICT Macro         48%  "D1 bias=bullish | H4=unknown/neutral | H1=consolidation/neutral | daily_state=london_cont -> 12.0/25 pts. 10/25 — contra bias D1 mas em consolidation + raid liquidity below @0.71567 = 12/25"
[15:26:53][WAR_ROOM] [AUDUSD]   cluster_decision: AUDUSD SELL preterido: perdeu para USDCHF BUY (ICT 12 vs 12, score 75.1 vs 61.4)

-------------------------------------------------------------------

[15:26:53][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF BUY  @0.78906  SL:0.78827  TP:0.79024  pavio:80%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.7/25  ( 78.8%)  RSI 20.7
   Wick     [##############]  20.0/20  (100.0%)  pavio 80%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 3% range  [perfeito]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [#######-------]  12.0/25  ( 48.0%)  D1=bearish H4=consolidation/neutral H1=consolidation/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.1/100  (+0.1 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → APROVADO  —  Score 75.1/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          79%  "RSI(9) 20.7 -> 19.7/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 80% (wick 20.0), corpo 3% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          56%  "Sessao London continuation (7.3/10), WR 30d 44% em 9T (1.1/5) -> 8.4/15 pts."
   [I] ICT Macro         48%  "D1 bias=bearish | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=london_cont -> 12.0/25 pts. 10/25 — contra bias D1 mas em consolidation + raid liquidity above @0.79112 = 12/25"
-------------------------------------------------------------------
  Ciclo #19: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[15:41:29] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[15:42:00] POOL CLOSED — ciclo #20  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 15:30:00  (vermelha)
  │     OHLC : O=1.36770  H=1.36786  L=1.36742  C=1.36758
  │     range=4.4 pips   corpo=27% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 19.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36758  SL=1.36692 (6.6 pips)  TP=1.36857 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~36% do último swing
  │  Daily Range: London continuation
  │  Liquidity above: 1.36782 (equal_high, 1.6p)
  │  Liquidity below: 1.36747 (equal_high, 1.8p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[15:42:01][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36758  SL:1.36692  TP:1.36857  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  20.4/25  ( 81.6%)  RSI 19.9
   Wick     [##########----]  14.5/20  ( 72.5%)  pavio 36%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 27% range  [bom]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.3/100  (-5.7 pts vs mínimo 75)
   Pior critério: ICT 14.0/25  (56% do máximo)
   → REJEITADO  —  Score 69.3 < 75 | fraco: ICT Macro 14.0/25
   ────────────────────────────────────────────────────────────
   [M] Momentum          82%  "RSI(9) 19.9 -> 20.4/25 pts. Gate: 30."
   [R] Rejeicao          70%  "Pavio 36% (wick 14.5), corpo 27% (pin 10.0) -> 24.5/35 pts."
   [C] Contexto          69%  "Sessao London continuation (7.3/10), WR 30d 52% em 21T (3.1/5) -> 10.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36782 = 14/25"
-------------------------------------------------------------------
  Ciclo #20: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[15:56:20] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[15:56:52] POOL CLOSED — ciclo #21  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 15:45:00  (verde)
  │     OHLC : O=1.36758  H=1.36784  L=1.36734  C=1.36770
  │     range=5.0 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 48%  (min 30%)   [bot reportou 48%]
  │     [OK ] RSI(9)    : 18.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36770  SL=1.36684 (8.6 pips)  TP=1.36899 (12.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: retracement/down (conf 0.70) — retraçao ~40% do último swing
  │  Daily Range: London continuation
  │  Liquidity above: 1.36782 (equal_high, 0.9p)
  │  Liquidity below: 1.36747 (equal_high, 2.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[15:56:52][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36770  SL:1.36684  TP:1.36899  pavio:48%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  21.5/25  ( 86.0%)  RSI 18.8
   Wick     [#############-]  19.2/20  ( 96.0%)  pavio 48%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 24% range  [bom]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=retracement/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.1/100  (+0.1 pts vs mínimo 75)
   Pior critério: ICT 14.0/25  (56% do máximo)
   → REJEITADO  —  Correlação com USDCHF (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          86%  "RSI(9) 18.8 -> 21.5/25 pts. Gate: 30."
   [R] Rejeicao          83%  "Pavio 48% (wick 19.2), corpo 24% (pin 10.0) -> 29.2/35 pts."
   [C] Contexto          69%  "Sessao London continuation (7.3/10), WR 30d 52% em 21T (3.1/5) -> 10.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=retracement/down | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36782 = 14/25"
-------------------------------------------------------------------
  Ciclo #21: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[17:00:12] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[17:00:44] POOL CLOSED — ciclo #22  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 16:45:00  (vermelha)
  │     OHLC : O=1.34872  H=1.34883  L=1.34732  C=1.34779
  │     range=15.1 pips   corpo=62% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 21.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34779  SL=1.34682 (9.7 pips)  TP=1.34924 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: reversal/up (conf 0.51) — BOS detectado (LH/HL)
  │  Daily Range: NY open expansion
  │  Liquidity above: 1.34766 (equal_low, 1.2p)
  │  Liquidity below: 1.34746 (equal_low, 0.8p)
  │  Alignment BUY: 20/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 16:45:00  (verde)
  │     OHLC : O=1.36934  H=1.37107  L=1.36932  C=1.36984
  │     range=17.5 pips   corpo=29% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 70%  (min 30%)   [bot reportou 70%]
  │     [OK ] RSI(9)    : 78.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36984  SL=1.37157 (17.3 pips)  TP=1.36725 (25.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY open expansion
  │  Liquidity above: 1.37142 (high, 11.6p)
  │  Liquidity below: 1.36809 (equal_high, 21.7p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD BUY  ICT=20/25  Score=62.1/100
  │  ✗ LOSER   USDCAD SELL  -- perdeu para GBPUSD BUY (ICT 20 vs 14, score 62.1 vs 74.5)
  └──

[17:00:44][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD SELL  @1.36984  SL:1.37157  TP:1.36725  pavio:70%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  18.7/25  ( 74.8%)  RSI 78.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 70%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 29% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=unknown/neutral
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.5/100  (-0.5 pts vs mínimo 75)
   Pior critério: ICT 14.0/25  (56% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD BUY (ICT 20 vs 14, score 62.1 vs 74.5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          75%  "RSI(9) 78.2 -> 18.7/25 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 70% (wick 20.0), corpo 29% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          79%  "Sessao NY open expansion (8.7/10), WR 30d 52% em 21T (3.1/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=unknown/neutral | daily_state=ny_expansion -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
[17:00:45][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD SELL preterido: perdeu para GBPUSD BUY (ICT 20 vs 14, score 62.1 vs 74.5)

-------------------------------------------------------------------

[17:00:45][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34779  SL:1.34682  TP:1.34924  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.4/25  ( 77.6%)  RSI 21.0
   Wick     [#########-----]  12.5/20  ( 62.5%)  pavio 31%
   PinBar   [#-------------]   1.5/15  ( 10.0%)  corpo 62% range  [suja]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=neutral H4=consolidation/neutral H1=reversal/up
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   62.1/100  (-12.9 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 62.1 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          78%  "RSI(9) 21.0 -> 19.4/25 pts. Gate: 30."
   [R] Rejeicao          40%  "Pavio 31% (wick 12.5), corpo 62% (pin 1.5) -> 14.0/35 pts."
   [C] Contexto          58%  "Sessao NY open expansion (8.7/10), WR 30d 22% em 9T (0.0/5) -> 8.7/15 pts."
   [I] ICT Macro         80%  "D1 bias=neutral | H4=consolidation/neutral | H1=reversal/up | daily_state=ny_expansion -> 20.0/25 pts. 18/25 — bias D1 neutro, H1 reversal alinhado com trade + raid liquidity above @1.34766 = 20/25"
-------------------------------------------------------------------
  Ciclo #22: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[17:00:53] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[17:01:24] POOL CLOSED — ciclo #23  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 16:45:00  (vermelha)
  │     OHLC : O=0.79130  H=0.79161  L=0.79103  C=0.79116
  │     range=5.8 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 53%  (min 30%)   [bot reportou 53%]
  │     [OK ] RSI(9)    : 82.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.79116  SL=0.79211 (9.5 pips)  TP=0.78973 (14.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: consolidation/neutral (conf 0.70) — range 85pips ~ swing médio 81pips
  │  H1: consolidation/neutral (conf 0.70) — range 34pips ~ swing médio 24pips
  │  Daily Range: NY open expansion
  │  Liquidity above: —
  │  Liquidity below: 0.78847 (equal_low, 27.2p)
  │  Alignment BUY: 10/25  |  SELL: 18/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 16:45:00  (vermelha)
  │     OHLC : O=0.58399  H=0.58402  L=0.58346  C=0.58386
  │     range=5.6 pips   corpo=23% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 71%  (min 30%)   [bot reportou 71%]
  │     [OK ] RSI(9)    : 1.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58386  SL=0.58296 (9.0 pips)  TP=0.58521 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  Daily Range: NY open expansion
  │  Liquidity above: 0.58398 (equal_low, 4.4p)
  │  Liquidity below: 0.58149 (low, 20.5p)
  │  Alignment BUY: 14/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF SELL  ICT=18/25  Score=81.5/100
  │  ✗ LOSER   NZDUSD BUY  -- perdeu para USDCHF SELL (ICT 18 vs 14, score 81.5 vs 82.7)
  └──

[17:01:25][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD BUY  @0.58386  SL:0.58296  TP:0.58521  pavio:71%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 1.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 71%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 23% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=reversal/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   82.7/100  (+7.7 pts vs mínimo 75)
   Pior critério: ICT 14.0/25  (56% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF SELL (ICT 18 vs 14, score 81.5 vs 82.7)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 1.5 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 71% (wick 20.0), corpo 23% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          91%  "Sessao NY open expansion (8.7/10), WR 30d 69% em 16T (5.0/5) -> 13.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=reversal/down | daily_state=ny_expansion -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @0.58398 = 14/25"
[17:01:25][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD BUY preterido: perdeu para USDCHF SELL (ICT 18 vs 14, score 81.5 vs 82.7)

-------------------------------------------------------------------

[17:01:25][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF SELL  @0.79116  SL:0.79211  TP:0.78973  pavio:53%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  22.3/25  ( 89.2%)  RSI 82.1
   Wick     [##############]  20.0/20  (100.0%)  pavio 53%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 24% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=bearish H4=consolidation/neutral H1=consolidation/neutral
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   81.5/100  (+6.5 pts vs mínimo 75)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 81.5/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          89%  "RSI(9) 82.1 -> 22.3/25 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 53% (wick 20.0), corpo 24% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          75%  "Sessao NY open expansion (8.7/10), WR 30d 50% em 10T (2.5/5) -> 11.2/15 pts."
   [I] ICT Macro         72%  "D1 bias=bearish | H4=consolidation/neutral | H1=consolidation/neutral | daily_state=ny_expansion -> 18.0/25 pts. 16/25 — a-favor do bias D1 + H4 consolidation (range) + raid liquidity below @0.78847 = 18/25"
-------------------------------------------------------------------
  Ciclo #23: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[17:11:18] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[17:11:50] POOL CLOSED — ciclo #24  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 17:00:00  (verde)
  │     OHLC : O=0.71285  H=0.71330  L=0.71232  C=0.71319
  │     range=9.8 pips   corpo=35% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 20.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71319  SL=0.71182 (13.7 pips)  TP=0.71524 (20.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: BULLISH ↑
  │  H4: reversal/up (conf 0.79) — BOS detectado (LH/HL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY open expansion
  │  Liquidity above: 0.71427 (equal_low, 10.6p)
  │  Liquidity below: 0.71316 (equal_low, 0.6p)
  │  Alignment BUY: 20/25  |  SELL: 9/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 17:00:00  (verde)
  │     OHLC : O=1.34779  H=1.34802  L=1.34711  C=1.34794
  │     range=9.1 pips   corpo=16% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 75%  (min 30%)   [bot reportou 75%]
  │     [OK ] RSI(9)    : 23.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34794  SL=1.34661 (13.3 pips)  TP=1.34993 (19.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: reversal/up (conf 0.51) — BOS detectado (LH/HL)
  │  Daily Range: NY open expansion
  │  Liquidity above: 1.34816 (equal_low, 0.2p)
  │  Liquidity below: 1.34804 (equal_low, 0.9p)
  │  Alignment BUY: 20/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD BUY  ICT=20/25  Score=75.6/100
  │  ✗ LOSER   AUDUSD BUY  -- perdeu para GBPUSD BUY (ICT 20 vs 20, score 75.6 vs 74.5)
  └──

[17:11:51][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ○ AUDUSD BUY  @0.71319  SL:0.71182  TP:0.71524  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.7/25  ( 78.8%)  RSI 20.7
   Wick     [##############]  20.0/20  (100.0%)  pavio 54%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 35% range  [aceitável]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=bullish H4=reversal/up H1=unknown/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.5/100  (-0.5 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD BUY (ICT 20 vs 20, score 75.6 vs 74.5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          79%  "RSI(9) 20.7 -> 19.7/25 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 54% (wick 20.0), corpo 35% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          65%  "Sessao NY open expansion (8.7/10), WR 30d 44% em 27T (1.1/5) -> 9.8/15 pts."
   [I] ICT Macro         80%  "D1 bias=bullish | H4=reversal/up | H1=unknown/neutral | daily_state=ny_expansion -> 20.0/25 pts. 18/25 — a-favor do bias D1, fases mistas + raid liquidity above @0.71427 = 20/25"
[17:11:51][WAR_ROOM] [AUDUSD]   cluster_decision: AUDUSD BUY preterido: perdeu para GBPUSD BUY (ICT 20 vs 20, score 75.6 vs 74.5)

-------------------------------------------------------------------

[17:11:51][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34794  SL:1.34661  TP:1.34993  pavio:75%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  16.9/25  ( 67.6%)  RSI 23.7
   Wick     [##############]  20.0/20  (100.0%)  pavio 75%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 16% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=neutral H4=consolidation/neutral H1=reversal/up
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.6/100  (+0.6 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCHF (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          68%  "RSI(9) 23.7 -> 16.9/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 75% (wick 20.0), corpo 16% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          58%  "Sessao NY open expansion (8.7/10), WR 30d 22% em 9T (0.0/5) -> 8.7/15 pts."
   [I] ICT Macro         80%  "D1 bias=neutral | H4=consolidation/neutral | H1=reversal/up | daily_state=ny_expansion -> 20.0/25 pts. 18/25 — bias D1 neutro, H1 reversal alinhado com trade + raid liquidity above @1.34816 = 20/25"
-------------------------------------------------------------------
  Ciclo #24: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[17:11:59] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[17:12:30] POOL CLOSED — ciclo #25  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-29 17:00:00  (vermelha)
  │     OHLC : O=1.36984  H=1.37049  L=1.36924  C=1.36944
  │     range=12.5 pips   corpo=32% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 52%  (min 30%)   [bot reportou 52%]
  │     [OK ] RSI(9)    : 71.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36944  SL=1.37099 (15.5 pips)  TP=1.36712 (23.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY open expansion
  │  Liquidity above: 1.37142 (high, 21.2p)
  │  Liquidity below: 1.36809 (equal_high, 12.1p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 17:00:00  (vermelha)
  │     OHLC : O=0.58387  H=0.58392  L=0.58301  C=0.58369
  │     range=9.1 pips   corpo=20% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 75%  (min 30%)   [bot reportou 75%]
  │     [OK ] RSI(9)    : 1.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58369  SL=0.58251 (11.8 pips)  TP=0.58546 (17.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  Daily Range: NY open expansion
  │  Liquidity above: 0.58398 (equal_low, 1.6p)
  │  Liquidity below: 0.58149 (low, 23.3p)
  │  Alignment BUY: 14/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  NZDUSD BUY  ICT=14/25  Score=82.7/100
  │  ✗ LOSER   USDCAD SELL  -- perdeu para NZDUSD BUY (ICT 14 vs 14, score 82.7 vs 63.6)
  └──

[17:12:31][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD SELL  @1.36944  SL:1.37099  TP:1.36712  pavio:52%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  12.8/25  ( 51.2%)  RSI 71.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 52%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 32% range  [aceitável]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=unknown/neutral
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.6/100  (-11.4 pts vs mínimo 75)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para NZDUSD BUY (ICT 14 vs 14, score 82.7 vs 63.6)
   ────────────────────────────────────────────────────────────
   [M] Momentum          51%  "RSI(9) 71.9 -> 12.8/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 52% (wick 20.0), corpo 32% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          79%  "Sessao NY open expansion (8.7/10), WR 30d 52% em 21T (3.1/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=unknown/neutral | daily_state=ny_expansion -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.36809 = 14/25"
[17:12:31][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD SELL preterido: perdeu para NZDUSD BUY (ICT 14 vs 14, score 82.7 vs 63.6)

-------------------------------------------------------------------

[17:12:31][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58369  SL:0.58251  TP:0.58546  pavio:75%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 1.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 75%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 20% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=reversal/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   82.7/100  (+7.7 pts vs mínimo 75)
   Pior critério: ICT 14.0/25  (56% do máximo)
   → REJEITADO  —  Correlação com USDCHF (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 1.5 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 75% (wick 20.0), corpo 20% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          91%  "Sessao NY open expansion (8.7/10), WR 30d 69% em 16T (5.0/5) -> 13.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=reversal/down | daily_state=ny_expansion -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @0.58398 = 14/25"
-------------------------------------------------------------------
  Ciclo #25: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[17:41:26] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[17:41:58] POOL CLOSED — ciclo #26  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 17:30:00  (vermelha)
  │     OHLC : O=0.71376  H=0.71391  L=0.71356  C=0.71370
  │     range=3.5 pips   corpo=17% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 40%  (min 30%)   [bot reportou 40%]
  │     [OK ] RSI(9)    : 22.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71370  SL=0.71306 (6.4 pips)  TP=0.71466 (9.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: BULLISH ↑
  │  H4: reversal/up (conf 0.79) — BOS detectado (LH/HL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY open expansion
  │  Liquidity above: 0.71427 (equal_low, 6.7p)
  │  Liquidity below: 0.71316 (equal_low, 4.5p)
  │  Alignment BUY: 20/25  |  SELL: 9/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-29 17:30:00  (vermelha)
  │     OHLC : O=0.58420  H=0.58428  L=0.58396  C=0.58412
  │     range=3.2 pips   corpo=25% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 19.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58412  SL=0.58346 (6.6 pips)  TP=0.58511 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  Daily Range: NY open expansion
  │  Liquidity above: 0.58738 (equal_low, 33.3p)
  │  Liquidity below: 0.58398 (equal_low, 0.7p)
  │  Alignment BUY: 10/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  AUDUSD BUY  ICT=20/25  Score=73.4/100
  │  ✗ LOSER   NZDUSD BUY  -- perdeu para AUDUSD BUY (ICT 20 vs 10, score 73.4 vs 74.5)
  └──

[17:41:58][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD BUY  @0.58412  SL:0.58346  TP:0.58511  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  20.8/25  ( 83.2%)  RSI 19.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 50%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 25% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [######--------]  10.0/25  ( 40.0%)  D1=neutral H4=reversal/down H1=reversal/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.5/100  (-0.5 pts vs mínimo 75)
   Pior critério: ICT 10.0/25  (40% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para AUDUSD BUY (ICT 20 vs 10, score 73.4 vs 74.5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          83%  "RSI(9) 19.5 -> 20.8/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 50% (wick 20.0), corpo 25% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          91%  "Sessao NY open expansion (8.7/10), WR 30d 69% em 16T (5.0/5) -> 13.7/15 pts."
   [I] ICT Macro         40%  "D1 bias=neutral | H4=reversal/down | H1=reversal/down | daily_state=ny_expansion -> 10.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro - liquidity below @0.58398 próxima (risco) = 10/25"
[17:41:59][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD BUY preterido: perdeu para AUDUSD BUY (ICT 20 vs 10, score 73.4 vs 74.5)

-------------------------------------------------------------------

[17:41:59][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD BUY  @0.71370  SL:0.71306  TP:0.71466  pavio:40%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.6/25  ( 70.4%)  RSI 22.9
   Wick     [###########---]  16.0/20  ( 80.0%)  pavio 40%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 17% range  [bom]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=bullish H4=reversal/up H1=unknown/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.4/100  (-1.6 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → REJEITADO  —  Score 73.4 < 75 | fraco: Histórico 1.1/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          70%  "RSI(9) 22.9 -> 17.6/25 pts. Gate: 30."
   [R] Rejeicao          74%  "Pavio 40% (wick 16.0), corpo 17% (pin 10.0) -> 26.0/35 pts."
   [C] Contexto          65%  "Sessao NY open expansion (8.7/10), WR 30d 44% em 27T (1.1/5) -> 9.8/15 pts."
   [I] ICT Macro         80%  "D1 bias=bullish | H4=reversal/up | H1=unknown/neutral | daily_state=ny_expansion -> 20.0/25 pts. 18/25 — a-favor do bias D1, fases mistas + raid liquidity above @0.71427 = 20/25"
-------------------------------------------------------------------
  Ciclo #26: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total
