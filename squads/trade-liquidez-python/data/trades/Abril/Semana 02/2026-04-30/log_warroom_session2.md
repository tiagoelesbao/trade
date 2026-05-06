===================================================================
  WAR ROOM v6.2.0-ict  --  ANALISE TECNICA AGENTICA + Pool-then-Pick
-------------------------------------------------------------------
  Score minimo : 70/100   |   Correlacao: ATIVA (16 pares)   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)  +  ICT Context Engine (Sprint 2)
  Criterios    : RSI(25) Wick(20) PinBar(15) Sessao(10) ICT(25) Hist(5)
  Sessoes ICT  : asia_early(8) asia_judas(1) london_open(14) london_cont(11) ny_news_embargo(0) ny_expansion(13) london_close(12) ny_afternoon(7)
  Pares ativos : AUDUSD,GBPUSD,USDCAD,USDCHF,NZDUSD
  Pool-then-Pick: janela 30s  (poll 3s)  [Sprint 3]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE -> [ICT CONTEXT] -> [FASE 2] score -> [CLUSTER DECISION]
===================================================================
[14:35:52][WAR_ROOM]   war_room_started: War Room v6.2.0-ict iniciada | Score mínimo: 70/100 | 6 criterios (incl ICT) | pool=30s | correlated_pairs=16 | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[14:35:58] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[14:36:30] POOL CLOSED — ciclo #1  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 14:15:00  (vermelha)
  │     OHLC : O=0.78542  H=0.78559  L=0.78470  C=0.78504
  │     range=8.9 pips   corpo=43% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 38%  (min 30%)   [bot reportou 38%]
  │     [OK ] RSI(9)    : 9.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=11h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78504  SL=0.78420 (8.4 pips)  TP=0.78630 (12.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: London continuation
  │  Liquidity above: 0.78717 (equal_high, 22.2p)
  │  Liquidity below: 0.78443 (equal_high, 5.2p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


-------------------------------------------------------------------

[14:36:30][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF BUY  @0.78504  SL:0.78420  TP:0.78630  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 9.2
   Wick     [###########---]  15.3/20  ( 76.5%)  pavio 38%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 43% range  [aceitável]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.1/100  (+1.1 pts vs mínimo 70)
   Pior critério: Hist 1.5/5  (30% do máximo)
   → APROVADO  —  Score 71.1/70 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 9.2 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          58%  "Pavio 38% (wick 15.3), corpo 43% (pin 5.0) -> 20.3/35 pts."
   [C] Contexto          59%  "Sessao London continuation (7.3/10), WR 30d 46% em 13T (1.5/5) -> 8.8/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=london_cont -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78717 = 17/25"
-------------------------------------------------------------------
  Ciclo #1: 1 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[15:56:19] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[15:56:50] POOL CLOSED — ciclo #2  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 15:45:00  (vermelha)
  │     OHLC : O=0.78503  H=0.78507  L=0.78338  C=0.78393
  │     range=16.9 pips   corpo=65% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 23.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78393  SL=0.78288 (10.5 pips)  TP=0.78551 (15.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: London continuation
  │  Liquidity above: 0.78395 (equal_high, 1.1p)
  │  Liquidity below: 0.78376 (equal_high, 0.7p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


-------------------------------------------------------------------

[15:56:51][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78393  SL:0.78288  TP:0.78551  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  16.9/25  ( 67.6%)  RSI 23.7
   Wick     [#########-----]  13.0/20  ( 65.0%)  pavio 33%
   PinBar   [#-------------]   1.4/15  (  9.3%)  corpo 65% range  [suja]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [##------------]   0.7/5  ( 14.0%)  WR 43%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   56.3/100  (-13.7 pts vs mínimo 70)
   Pior critério: PinBar 1.4/15  (9% do máximo)
   → REJEITADO  —  Score 56.3 < 70 | fraco: Pin Bar 1.4/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          68%  "RSI(9) 23.7 -> 16.9/25 pts. Gate: 30."
   [R] Rejeicao          41%  "Pavio 33% (wick 13.0), corpo 65% (pin 1.4) -> 14.4/35 pts."
   [C] Contexto          53%  "Sessao London continuation (7.3/10), WR 30d 43% em 14T (0.7/5) -> 8.0/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=london_cont -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78395 = 17/25"
-------------------------------------------------------------------
  Ciclo #2: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[17:26:13] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[17:26:45] POOL CLOSED — ciclo #3  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 17:15:00  (vermelha)
  │     OHLC : O=1.36479  H=1.36480  L=1.36355  C=1.36404
  │     range=12.5 pips   corpo=60% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 22.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36404  SL=1.36305 (9.9 pips)  TP=1.36552 (14.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY open expansion
  │  Liquidity above: 1.36671 (equal_low, 26.2p)
  │  Liquidity below: 1.36329 (equal_low, 8.0p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 17:15:00  (verde)
  │     OHLC : O=0.78234  H=0.78250  L=0.78172  C=0.78236
  │     range=7.8 pips   corpo=3% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 79%  (min 30%)   [bot reportou 79%]
  │     [OK ] RSI(9)    : 23.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> NY open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78236  SL=0.78122 (11.4 pips)  TP=0.78407 (17.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: NY open expansion
  │  Liquidity above: 0.78313 (equal_low, 6.8p)
  │  Liquidity below: 0.78064 (low, 18.1p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF BUY  ICT=17/25  Score=78.7/100
  │  ✗ LOSER   USDCAD BUY  -- perdeu para USDCHF BUY (ICT 17 vs 14, score 78.7 vs 60.9)
  └──

[17:26:45][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD BUY  @1.36404  SL:1.36305  TP:1.36552  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.8/25  ( 71.2%)  RSI 22.7
   Wick     [###########---]  15.7/20  ( 78.5%)  pavio 39%
   PinBar   [#-------------]   1.6/15  ( 10.7%)  corpo 60% range  [suja]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.9/100  (-9.1 pts vs mínimo 70)
   Pior critério: PinBar 1.6/15  (11% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF BUY (ICT 17 vs 14, score 78.7 vs 60.9)
   ────────────────────────────────────────────────────────────
   [M] Momentum          71%  "RSI(9) 22.7 -> 17.8/25 pts. Gate: 30."
   [R] Rejeicao          49%  "Pavio 39% (wick 15.7), corpo 60% (pin 1.6) -> 17.3/35 pts."
   [C] Contexto          79%  "Sessao NY open expansion (8.7/10), WR 30d 52% em 21T (3.1/5) -> 11.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=ny_expansion -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36671 = 14/25"
[17:26:46][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD BUY preterido: perdeu para USDCHF BUY (ICT 17 vs 14, score 78.7 vs 60.9)

-------------------------------------------------------------------

[17:26:46][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF BUY  @0.78236  SL:0.78122  TP:0.78407  pavio:79%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.3/25  ( 69.2%)  RSI 23.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 79%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 3% range  [perfeito]
   Sessao   [############--]   8.7/10  ( 87.0%)  NY open expansion
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [##------------]   0.7/5  ( 14.0%)  WR 43%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   78.7/100  (+8.7 pts vs mínimo 70)
   Pior critério: Hist 0.7/5  (14% do máximo)
   → APROVADO  —  Score 78.7/70 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          69%  "RSI(9) 23.2 -> 17.3/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 79% (wick 20.0), corpo 3% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          63%  "Sessao NY open expansion (8.7/10), WR 30d 43% em 14T (0.7/5) -> 9.4/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=ny_expansion -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78313 = 17/25"
-------------------------------------------------------------------
  Ciclo #3: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[18:11:28] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=27s, total=2)

[18:11:58] POOL CLOSED — ciclo #4  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 18:00:00  (verde)
  │     OHLC : O=0.71881  H=0.71912  L=0.71825  C=0.71885
  │     range=8.7 pips   corpo=5% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 79.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71885  SL=0.71962 (7.7 pips)  TP=0.71770 (11.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: reversal/up (conf 0.73) — BOS detectado (LH/HL)
  │  Daily Range: London close reversal
  │  Liquidity above: 0.71971 (high, 8.4p)
  │  Liquidity below: 0.71881 (equal_high, 0.6p)
  │  Alignment BUY: 20/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 18:00:00  (verde)
  │     OHLC : O=1.35823  H=1.35934  L=1.35763  C=1.35847
  │     range=17.1 pips   corpo=14% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 51%  (min 30%)   [bot reportou 51%]
  │     [OK ] RSI(9)    : 78.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35847  SL=1.35984 (13.7 pips)  TP=1.35642 (20.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 146pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London close reversal
  │  Liquidity above: 1.35968 (equal_high, 13.0p)
  │  Liquidity below: 1.35787 (equal_high, 5.0p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=14/25  Score=75.8/100
  │  ✗ LOSER   AUDUSD SELL  -- perdeu para GBPUSD SELL (ICT 14 vs 14, score 75.8 vs 70.0)
  └──

[18:11:59][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ○ AUDUSD SELL  @0.71885  SL:0.71962  TP:0.71770  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.5/25  ( 78.0%)  RSI 79.1
   Wick     [#########-----]  12.4/20  ( 62.0%)  pavio 31%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 5% range  [perfeito]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=reversal/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.0/100  (+0.0 pts vs mínimo 70)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 14 vs 14, score 75.8 vs 70.0)
   ────────────────────────────────────────────────────────────
   [M] Momentum          78%  "RSI(9) 79.1 -> 19.5/25 pts. Gate: 70."
   [R] Rejeicao          78%  "Pavio 31% (wick 12.4), corpo 5% (pin 15.0) -> 27.4/35 pts."
   [C] Contexto          61%  "Sessao London close reversal (8.0/10), WR 30d 44% em 27T (1.1/5) -> 9.1/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=reversal/up | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71881 = 14/25"
[18:11:59][WAR_ROOM] [AUDUSD]   cluster_decision: AUDUSD SELL preterido: perdeu para GBPUSD SELL (ICT 14 vs 14, score 75.8 vs 70.0)

-------------------------------------------------------------------

[18:11:59][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✓ GBPUSD SELL  @1.35847  SL:1.35984  TP:1.35642  pavio:51%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  18.8/25  ( 75.2%)  RSI 78.4
   Wick     [##############]  20.0/20  (100.0%)  pavio 51%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 14% range  [perfeito]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.8/100  (+5.8 pts vs mínimo 70)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 75.8/70 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          75%  "RSI(9) 78.4 -> 18.8/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 51% (wick 20.0), corpo 14% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          53%  "Sessao London close reversal (8.0/10), WR 30d 22% em 9T (0.0/5) -> 8.0/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.35787 = 14/25"
-------------------------------------------------------------------
  Ciclo #4: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[18:41:23] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[18:41:54] POOL CLOSED — ciclo #5  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 18:30:00  (verde)
  │     OHLC : O=0.71854  H=0.71906  L=0.71854  C=0.71882
  │     range=5.2 pips   corpo=54% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 75.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71882  SL=0.71956 (7.4 pips)  TP=0.71771 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: reversal/up (conf 0.73) — BOS detectado (LH/HL)
  │  Daily Range: London close reversal
  │  Liquidity above: 0.71881 (equal_high, 3.2p)
  │  Liquidity below: 0.71840 (equal_high, 0.9p)
  │  Alignment BUY: 20/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 18:30:00  (verde)
  │     OHLC : O=1.35793  H=1.35895  L=1.35786  C=1.35799
  │     range=10.9 pips   corpo=6% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 88%  (min 30%)   [bot reportou 88%]
  │     [OK ] RSI(9)    : 74.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35799  SL=1.35945 (14.6 pips)  TP=1.35580 (21.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 146pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London close reversal
  │  Liquidity above: 1.35785 (equal_high, 1.8p)
  │  Liquidity below: 1.35549 (equal_low, 21.8p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=14/25  Score=71.8/100
  │  ✗ LOSER   AUDUSD SELL  -- perdeu para GBPUSD SELL (ICT 14 vs 14, score 71.8 vs 59.1)
  └──

[18:41:55][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ○ AUDUSD SELL  @0.71882  SL:0.71956  TP:0.71771  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  15.7/25  ( 62.8%)  RSI 75.1
   Wick     [#############-]  18.5/20  ( 92.5%)  pavio 46%
   PinBar   [##------------]   1.8/15  ( 12.0%)  corpo 54% range  [suja]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=reversal/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   59.1/100  (-10.9 pts vs mínimo 70)
   Pior critério: PinBar 1.8/15  (12% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 14 vs 14, score 71.8 vs 59.1)
   ────────────────────────────────────────────────────────────
   [M] Momentum          63%  "RSI(9) 75.1 -> 15.7/25 pts. Gate: 70."
   [R] Rejeicao          58%  "Pavio 46% (wick 18.5), corpo 54% (pin 1.8) -> 20.3/35 pts."
   [C] Contexto          61%  "Sessao London close reversal (8.0/10), WR 30d 44% em 27T (1.1/5) -> 9.1/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=reversal/up | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71840 = 14/25"
[18:41:55][WAR_ROOM] [AUDUSD]   cluster_decision: AUDUSD SELL preterido: perdeu para GBPUSD SELL (ICT 14 vs 14, score 71.8 vs 59.1)

-------------------------------------------------------------------

[18:41:55][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✓ GBPUSD SELL  @1.35799  SL:1.35945  TP:1.35580  pavio:88%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  14.8/25  ( 59.2%)  RSI 74.1
   Wick     [##############]  20.0/20  (100.0%)  pavio 88%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 6% range  [perfeito]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 30%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.8/100  (+1.8 pts vs mínimo 70)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 71.8/70 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          59%  "RSI(9) 74.1 -> 14.8/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 88% (wick 20.0), corpo 6% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          53%  "Sessao London close reversal (8.0/10), WR 30d 30% em 10T (0.0/5) -> 8.0/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.35549 = 14/25"
-------------------------------------------------------------------
  Ciclo #5: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[18:42:03] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[18:42:34] POOL CLOSED — ciclo #6  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 18:30:00  (vermelha)
  │     OHLC : O=1.36122  H=1.36122  L=1.36036  C=1.36083
  │     range=8.6 pips   corpo=45% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 55%  (min 30%)   [bot reportou 55%]
  │     [OK ] RSI(9)    : 17.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36083  SL=1.35986 (9.7 pips)  TP=1.36228 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London close reversal
  │  Liquidity above: 1.36329 (equal_low, 23.7p)
  │  Liquidity below: 1.35975 (low, 11.7p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 18:30:00  (verde)
  │     OHLC : O=0.58888  H=0.58939  L=0.58888  C=0.58922
  │     range=5.1 pips   corpo=67% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 72.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58922  SL=0.58989 (6.7 pips)  TP=0.58822 (10.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: London close reversal
  │  Liquidity above: 0.58893 (equal_low, 0.1p)
  │  Liquidity below: 0.58885 (equal_low, 0.7p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCAD BUY  ICT=14/25  Score=72.5/100
  │  ✗ LOSER   NZDUSD SELL  -- perdeu para USDCAD BUY (ICT 14 vs 14, score 72.5 vs 55.3)
  └──

[18:42:35][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD SELL  @0.58922  SL:0.58989  TP:0.58822  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.7/25  ( 54.8%)  RSI 72.9
   Wick     [#########-----]  13.3/20  ( 66.5%)  pavio 33%
   PinBar   [#-------------]   1.3/15  (  8.7%)  corpo 67% range  [suja]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/neutral
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   55.3/100  (-14.7 pts vs mínimo 70)
   Pior critério: PinBar 1.3/15  (9% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCAD BUY (ICT 14 vs 14, score 72.5 vs 55.3)
   ────────────────────────────────────────────────────────────
   [M] Momentum          55%  "RSI(9) 72.9 -> 13.7/25 pts. Gate: 70."
   [R] Rejeicao          42%  "Pavio 33% (wick 13.3), corpo 67% (pin 1.3) -> 14.6/35 pts."
   [C] Contexto          87%  "Sessao London close reversal (8.0/10), WR 30d 69% em 16T (5.0/5) -> 13.0/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/neutral | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.58885 = 14/25"
[18:42:35][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD SELL preterido: perdeu para USDCAD BUY (ICT 14 vs 14, score 72.5 vs 55.3)

-------------------------------------------------------------------

[18:42:35][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36083  SL:1.35986  TP:1.36228  pavio:55%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  22.4/25  ( 89.6%)  RSI 17.8
   Wick     [##############]  20.0/20  (100.0%)  pavio 55%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 45% range  [aceitável]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.5/100  (+2.5 pts vs mínimo 70)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → REJEITADO  —  Correlação com GBPUSD (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          90%  "RSI(9) 17.8 -> 22.4/25 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 55% (wick 20.0), corpo 45% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          74%  "Sessao London close reversal (8.0/10), WR 30d 52% em 21T (3.1/5) -> 11.1/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36329 = 14/25"
-------------------------------------------------------------------
  Ciclo #6: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[18:56:13] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[18:56:45] POOL CLOSED — ciclo #7  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 18:45:00  (verde)
  │     OHLC : O=1.36084  H=1.36113  L=1.36056  C=1.36113
  │     range=5.7 pips   corpo=51% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 22.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=15h -> London close reversal  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36113  SL=1.36006 (10.7 pips)  TP=1.36273 (16.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London close reversal
  │  Liquidity above: 1.36329 (equal_low, 21.7p)
  │  Liquidity below: 1.35975 (low, 13.7p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[18:56:45][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36113  SL:1.36006  TP:1.36273  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  18.1/25  ( 72.4%)  RSI 22.4
   Wick     [##############]  19.6/20  ( 98.0%)  pavio 49%
   PinBar   [##------------]   2.0/15  ( 13.3%)  corpo 51% range  [suja]
   Sessao   [###########---]   8.0/10  ( 80.0%)  London close reversal
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   64.8/100  (-5.2 pts vs mínimo 70)
   Pior critério: PinBar 2.0/15  (13% do máximo)
   → REJEITADO  —  Score 64.8 < 70 | fraco: Pin Bar 2.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          72%  "RSI(9) 22.4 -> 18.1/25 pts. Gate: 30."
   [R] Rejeicao          62%  "Pavio 49% (wick 19.6), corpo 51% (pin 2.0) -> 21.6/35 pts."
   [C] Contexto          74%  "Sessao London close reversal (8.0/10), WR 30d 52% em 21T (3.1/5) -> 11.1/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=london_close -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36329 = 14/25"
-------------------------------------------------------------------
  Ciclo #7: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[19:11:25] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[19:11:56] POOL CLOSED — ciclo #8  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 19:00:00  (vermelha)
  │     OHLC : O=1.36113  H=1.36125  L=1.36055  C=1.36097
  │     range=7.0 pips   corpo=23% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 60%  (min 30%)   [bot reportou 60%]
  │     [OK ] RSI(9)    : 21.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=16h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36097  SL=1.36005 (9.2 pips)  TP=1.36235 (13.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 1.36329 (equal_low, 22.4p)
  │  Liquidity below: 1.35975 (low, 13.0p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[19:11:57][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36097  SL:1.36005  TP:1.36235  pavio:60%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  18.8/25  ( 75.2%)  RSI 21.6
   Wick     [##############]  20.0/20  (100.0%)  pavio 60%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 23% range  [bom]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.6/100  (+0.6 pts vs mínimo 70)
   Pior critério: Sessao 4.7/10  (47% do máximo)
   → REJEITADO  —  Correlação com GBPUSD (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          75%  "RSI(9) 21.6 -> 18.8/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 60% (wick 20.0), corpo 23% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          52%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 52% em 21T (3.1/5) -> 7.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36329 = 14/25"
-------------------------------------------------------------------
  Ciclo #8: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[19:41:24] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[19:41:55] POOL CLOSED — ciclo #9  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 19:30:00  (verde)
  │     OHLC : O=1.36102  H=1.36107  L=1.36058  C=1.36102
  │     range=4.9 pips   corpo=0% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 90%  (min 30%)   [bot reportou 90%]
  │     [OK ] RSI(9)    : 22.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=16h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36102  SL=1.36008 (9.4 pips)  TP=1.36243 (14.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 1.36329 (equal_low, 21.1p)
  │  Liquidity below: 1.35975 (low, 14.3p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[19:41:56][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36102  SL:1.36008  TP:1.36243  pavio:90%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  18.0/25  ( 72.0%)  RSI 22.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 90%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 0% range  [perfeito]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.8/100  (+4.8 pts vs mínimo 70)
   Pior critério: Sessao 4.7/10  (47% do máximo)
   → REJEITADO  —  Correlação com GBPUSD (posição ativa no MT5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          72%  "RSI(9) 22.5 -> 18.0/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 90% (wick 20.0), corpo 0% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          52%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 52% em 21T (3.1/5) -> 7.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36329 = 14/25"
-------------------------------------------------------------------
  Ciclo #9: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[20:26:22] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[20:26:54] POOL CLOSED — ciclo #10  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 20:15:00  (vermelha)
  │     OHLC : O=1.36139  H=1.36155  L=1.36087  C=1.36123
  │     range=6.8 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 53%  (min 30%)   [bot reportou 53%]
  │     [OK ] RSI(9)    : 28.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=17h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36123  SL=1.36037 (8.6 pips)  TP=1.36252 (12.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 1.36329 (equal_low, 21.2p)
  │  Liquidity below: 1.35975 (low, 14.2p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[20:26:54][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD BUY  @1.36123  SL:1.36037  TP:1.36252  pavio:53%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  12.2/25  ( 48.8%)  RSI 28.8
   Wick     [##############]  20.0/20  (100.0%)  pavio 53%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 24% range  [bom]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   64.0/100  (-6.0 pts vs mínimo 70)
   Pior critério: Sessao 4.7/10  (47% do máximo)
   → REJEITADO  —  Score 64.0 < 70 | fraco: Sessão 4.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          49%  "RSI(9) 28.8 -> 12.2/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 53% (wick 20.0), corpo 24% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          52%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 52% em 21T (3.1/5) -> 7.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36329 = 14/25"
-------------------------------------------------------------------
  Ciclo #10: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[21:26:11] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[21:26:43] POOL CLOSED — ciclo #11  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 21:15:00  (verde)
  │     OHLC : O=0.71898  H=0.71928  L=0.71896  C=0.71912
  │     range=3.2 pips   corpo=44% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 72.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=18h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71912  SL=0.71978 (6.6 pips)  TP=0.71813 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: reversal/up (conf 0.73) — BOS detectado (LH/HL)
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 0.71971 (high, 5.4p)
  │  Liquidity below: 0.71881 (equal_high, 3.6p)
  │  Alignment BUY: 20/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 21:15:00  (verde)
  │     OHLC : O=1.35873  H=1.35944  L=1.35871  C=1.35902
  │     range=7.3 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 58%  (min 30%)   [bot reportou 58%]
  │     [OK ] RSI(9)    : 77.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=18h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35902  SL=1.35994 (9.2 pips)  TP=1.35764 (13.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 141pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 1.35968 (equal_high, 6.5p)
  │  Liquidity below: 1.35787 (equal_high, 11.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=14/25  Score=61.6/100
  │  ✗ LOSER   AUDUSD SELL  -- perdeu para GBPUSD SELL (ICT 14 vs 14, score 61.6 vs 58.5)
  └──

[21:26:43][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ○ AUDUSD SELL  @0.71912  SL:0.71978  TP:0.71813  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.7/25  ( 54.8%)  RSI 72.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 50%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 44% range  [aceitável]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=reversal/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   58.5/100  (-11.5 pts vs mínimo 70)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 14 vs 14, score 61.6 vs 58.5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          55%  "RSI(9) 72.9 -> 13.7/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 50% (wick 20.0), corpo 44% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          39%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 44% em 27T (1.1/5) -> 5.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=reversal/up | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71881 = 14/25"
[21:26:44][WAR_ROOM] [AUDUSD]   cluster_decision: AUDUSD SELL preterido: perdeu para GBPUSD SELL (ICT 14 vs 14, score 61.6 vs 58.5)

-------------------------------------------------------------------

[21:26:44][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35902  SL:1.35994  TP:1.35764  pavio:58%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.9/25  ( 71.6%)  RSI 77.4
   Wick     [##############]  20.0/20  (100.0%)  pavio 58%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 40% range  [aceitável]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 27%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.6/100  (-8.4 pts vs mínimo 70)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 61.6 < 70 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          72%  "RSI(9) 77.4 -> 17.9/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 58% (wick 20.0), corpo 40% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          31%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 27% em 11T (0.0/5) -> 4.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.35787 = 14/25"
-------------------------------------------------------------------
  Ciclo #11: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[21:56:15] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[21:56:47] POOL CLOSED — ciclo #12  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 21:45:00  (verde)
  │     OHLC : O=0.71958  H=0.72004  L=0.71958  C=0.71984
  │     range=4.6 pips   corpo=57% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 79.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=18h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71984  SL=0.72054 (7.0 pips)  TP=0.71879 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: BULLISH ↑
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: reversal/up (conf 0.73) — BOS detectado (LH/HL)
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 0.72218 (high, 21.5p)
  │  Liquidity below: 0.71881 (equal_high, 12.2p)
  │  Alignment BUY: 20/25  |  SELL: 9/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 21:45:00  (verde)
  │     OHLC : O=1.35983  H=1.36071  L=1.35975  C=1.36014
  │     range=9.6 pips   corpo=32% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 59%  (min 30%)   [bot reportou 59%]
  │     [OK ] RSI(9)    : 83.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=18h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36014  SL=1.36121 (10.7 pips)  TP=1.35853 (16.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 154pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: —
  │  Liquidity below: 1.35968 (equal_high, 9.0p)
  │  Alignment BUY: 10/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=14/25  Score=67.0/100
  │  ✗ LOSER   AUDUSD SELL  -- perdeu para GBPUSD SELL (ICT 14 vs 9, score 67.0 vs 54.0)
  └──

[21:56:47][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ○ AUDUSD SELL  @0.71984  SL:0.72054  TP:0.71879  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  20.1/25  ( 80.4%)  RSI 79.7
   Wick     [############--]  17.4/20  ( 87.0%)  pavio 43%
   PinBar   [##------------]   1.7/15  ( 11.3%)  corpo 56% range  [suja]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [#####---------]   9.0/25  ( 36.0%)  D1=bullish H4=expansion/down H1=reversal/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   54.0/100  (-16.0 pts vs mínimo 70)
   Pior critério: PinBar 1.7/15  (11% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 14 vs 9, score 67.0 vs 54.0)
   ────────────────────────────────────────────────────────────
   [M] Momentum          80%  "RSI(9) 79.7 -> 20.1/25 pts. Gate: 70."
   [R] Rejeicao          55%  "Pavio 43% (wick 17.4), corpo 57% (pin 1.7) -> 19.1/35 pts."
   [C] Contexto          39%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 44% em 27T (1.1/5) -> 5.8/15 pts."
   [I] ICT Macro         36%  "D1 bias=bullish | H4=expansion/down | H1=reversal/up | daily_state=ny_afternoon -> 9.0/25 pts. 7/25 — contra bias D1, contexto fraco + raid liquidity below @0.71881 = 9/25"
[21:56:48][WAR_ROOM] [AUDUSD]   cluster_decision: AUDUSD SELL preterido: perdeu para GBPUSD SELL (ICT 14 vs 9, score 67.0 vs 54.0)

-------------------------------------------------------------------

[21:56:48][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.36014  SL:1.36121  TP:1.35853  pavio:59%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  23.3/25  ( 93.2%)  RSI 83.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 59%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 32% range  [aceitável]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 27%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   67.0/100  (-3.0 pts vs mínimo 70)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 67.0 < 70 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          93%  "RSI(9) 83.2 -> 23.3/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 59% (wick 20.0), corpo 32% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          31%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 27% em 11T (0.0/5) -> 4.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.35968 = 14/25"
-------------------------------------------------------------------
  Ciclo #12: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[21:56:56] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[21:57:28] POOL CLOSED — ciclo #13  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 21:45:00  (vermelha)
  │     OHLC : O=0.78143  H=0.78151  L=0.78099  C=0.78127
  │     range=5.2 pips   corpo=31% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 29.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=18h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78127  SL=0.78049 (7.8 pips)  TP=0.78244 (11.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 0.78313 (equal_low, 22.4p)
  │  Liquidity below: 0.78042 (equal_low, 4.7p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 21:45:00  (verde)
  │     OHLC : O=0.59044  H=0.59085  L=0.59044  C=0.59060
  │     range=4.1 pips   corpo=39% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 61%  (min 30%)   [bot reportou 61%]
  │     [OK ] RSI(9)    : 81.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=18h -> NY afternoon / end-of-day  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.59060  SL=0.59135 (7.5 pips)  TP=0.58948 (11.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: NY afternoon / end-of-day
  │  Liquidity above: 0.59116 (high, 4.1p)
  │  Liquidity below: 0.58969 (equal_high, 10.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF BUY  ICT=17/25  Score=59.9/100
  │  ✗ LOSER   NZDUSD SELL  -- perdeu para USDCHF BUY (ICT 17 vs 14, score 59.9 vs 70.0)
  └──

[21:57:28][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD SELL  @0.59060  SL:0.59135  TP:0.58948  pavio:61%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  21.3/25  ( 85.2%)  RSI 81.0
   Wick     [##############]  20.0/20  (100.0%)  pavio 61%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 39% range  [aceitável]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/neutral
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.0/100  (+0.0 pts vs mínimo 70)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF BUY (ICT 17 vs 14, score 59.9 vs 70.0)
   ────────────────────────────────────────────────────────────
   [M] Momentum          85%  "RSI(9) 81.0 -> 21.3/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 61% (wick 20.0), corpo 39% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          65%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 69% em 16T (5.0/5) -> 9.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/neutral | daily_state=ny_afternoon -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.58969 = 14/25"
[21:57:28][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD SELL preterido: perdeu para USDCHF BUY (ICT 17 vs 14, score 59.9 vs 70.0)

-------------------------------------------------------------------

[21:57:29][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78127  SL:0.78049  TP:0.78244  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  11.5/25  ( 46.0%)  RSI 29.5
   Wick     [##############]  20.0/20  (100.0%)  pavio 54%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 31% range  [aceitável]
   Sessao   [#######-------]   4.7/10  ( 47.0%)  NY afternoon / end-of-day
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   59.9/100  (-10.1 pts vs mínimo 70)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → REJEITADO  —  Score 59.9 < 70 | fraco: Pin Bar 5.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          46%  "RSI(9) 29.5 -> 11.5/25 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 54% (wick 20.0), corpo 31% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          43%  "Sessao NY afternoon / end-of-day (4.7/10), WR 30d 47% em 15T (1.7/5) -> 6.4/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=ny_afternoon -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78313 = 17/25"
-------------------------------------------------------------------
  Ciclo #13: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total