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
[01:25:12][WAR_ROOM]   war_room_started: War Room v6.2.0-ict iniciada | Score mínimo: 75/100 | 6 criterios (incl ICT) | pool=30s | correlated_pairs=16 | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[03:11:27] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[03:11:58] POOL CLOSED — ciclo #1  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 03:00:00  (verde)
  │     OHLC : O=1.34880  H=1.34952  L=1.34880  C=1.34926
  │     range=7.2 pips   corpo=64% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 70.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=00h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34926  SL=1.35002 (7.6 pips)  TP=1.34812 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: expansion/down (conf 0.85) — último swing 56pips vs mediana 33pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.35180 (high, 24.5p)
  │  Liquidity below: 1.34818 (equal_low, 11.7p)
  │  Alignment BUY: 14/25  |  SELL: 18/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 03:00:00  (vermelha)
  │     OHLC : O=1.36714  H=1.36718  L=1.36671  C=1.36691
  │     range=4.7 pips   corpo=49% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 29.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=00h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36691  SL=1.36621 (7.0 pips)  TP=1.36796 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.36747 (equal_high, 5.6p)
  │  Liquidity below: 1.36675 (equal_low, 1.6p)
  │  Alignment BUY: 14/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=18/25  Score=45.7/100
  │  ✗ LOSER   USDCAD BUY  -- perdeu para GBPUSD SELL (ICT 18 vs 14, score 45.7 vs 51.7)
  └──

[03:11:59][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD BUY  @1.36691  SL:1.36621  TP:1.36796  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  11.9/25  ( 47.6%)  RSI 29.0
   Wick     [############--]  17.0/20  ( 85.0%)  pavio 43%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 49% range  [aceitável]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=reversal/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   51.7/100  (-23.3 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 18 vs 14, score 45.7 vs 51.7)
   ────────────────────────────────────────────────────────────
   [M] Momentum          48%  "RSI(9) 29.0 -> 11.9/25 pts. Gate: 30."
   [R] Rejeicao          63%  "Pavio 43% (wick 17.0), corpo 49% (pin 5.0) -> 22.0/35 pts."
   [C] Contexto          25%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 52% em 21T (3.1/5) -> 3.8/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=reversal/down | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36747 = 14/25"
[03:11:59][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD BUY preterido: perdeu para GBPUSD SELL (ICT 18 vs 14, score 45.7 vs 51.7)

-------------------------------------------------------------------

[03:12:00][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.34926  SL:1.35002  TP:1.34812  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  11.2/25  ( 44.8%)  RSI 70.2
   Wick     [##########----]  14.4/20  ( 72.0%)  pavio 36%
   PinBar   [#-------------]   1.4/15  (  9.3%)  corpo 64% range  [suja]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=neutral H4=consolidation/neutral H1=expansion/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#########-----------]   45.7/100  (-29.3 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 45.7 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 70.2 -> 11.2/25 pts. Gate: 70."
   [R] Rejeicao          45%  "Pavio 36% (wick 14.4), corpo 64% (pin 1.4) -> 15.8/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         72%  "D1 bias=neutral | H4=consolidation/neutral | H1=expansion/down | daily_state=asia_judas -> 18.0/25 pts. 16/25 — bias D1 neutro, H1 expansion alinhado + raid liquidity below @1.34818 = 18/25"
-------------------------------------------------------------------
  Ciclo #1: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[07:41:22] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[07:41:53] POOL CLOSED — ciclo #2  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 07:30:00  (vermelha)
  │     OHLC : O=1.34631  H=1.34632  L=1.34549  C=1.34602
  │     range=8.3 pips   corpo=35% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 64%  (min 30%)   [bot reportou 64%]
  │     [OK ] RSI(9)    : 22.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34602  SL=1.34499 (10.3 pips)  TP=1.34756 (15.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: expansion/down (conf 0.85) — último swing 56pips vs mediana 33pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.34746 (equal_low, 14.1p)
  │  Liquidity below: 1.34475 (low, 13.0p)
  │  Alignment BUY: 14/25  |  SELL: 18/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 07:30:00  (verde)
  │     OHLC : O=1.36840  H=1.36887  L=1.36837  C=1.36871
  │     range=5.0 pips   corpo=62% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 72.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36871  SL=1.36937 (6.6 pips)  TP=1.36772 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.86) — último swing 79pips vs mediana 46pips
  │  H1: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.37142 (high, 27.9p)
  │  Liquidity below: 1.36809 (equal_high, 5.4p)
  │  Alignment BUY: 14/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCAD SELL  ICT=20/25  Score=51.6/100
  │  ✗ LOSER   GBPUSD BUY  -- perdeu para USDCAD SELL (ICT 20 vs 14, score 51.6 vs 58.0)
  └──

[07:41:54][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ○ GBPUSD BUY  @1.34602  SL:1.34499  TP:1.34756  pavio:64%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  18.3/25  ( 73.2%)  RSI 22.2
   Wick     [##############]  20.0/20  (100.0%)  pavio 64%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 35% range  [aceitável]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=expansion/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   58.0/100  (-17.0 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCAD SELL (ICT 20 vs 14, score 51.6 vs 58.0)
   ────────────────────────────────────────────────────────────
   [M] Momentum          73%  "RSI(9) 22.2 -> 18.3/25 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 64% (wick 20.0), corpo 35% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=expansion/down | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.34746 = 14/25"
[07:41:54][WAR_ROOM] [GBPUSD]   cluster_decision: GBPUSD BUY preterido: perdeu para USDCAD SELL (ICT 20 vs 14, score 51.6 vs 58.0)

-------------------------------------------------------------------

[07:41:55][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✗ USDCAD SELL  @1.36871  SL:1.36937  TP:1.36772  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.5/25  ( 54.0%)  RSI 72.7
   Wick     [#########-----]  12.8/20  ( 64.0%)  pavio 32%
   PinBar   [#-------------]   1.5/15  ( 10.0%)  corpo 62% range  [suja]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [###########---]  20.0/25  ( 80.0%)  D1=neutral H4=expansion/down H1=reversal/down
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   51.6/100  (-23.4 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 51.6 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          54%  "RSI(9) 72.7 -> 13.5/25 pts. Gate: 70."
   [R] Rejeicao          41%  "Pavio 32% (wick 12.8), corpo 62% (pin 1.5) -> 14.3/35 pts."
   [C] Contexto          25%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 52% em 21T (3.1/5) -> 3.8/15 pts."
   [I] ICT Macro         80%  "D1 bias=neutral | H4=expansion/down | H1=reversal/down | daily_state=asia_judas -> 20.0/25 pts. 18/25 — bias D1 neutro, H1 reversal alinhado com trade + raid liquidity below @1.36809 = 20/25"
-------------------------------------------------------------------
  Ciclo #2: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[07:42:02] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[07:42:34] POOL CLOSED — ciclo #3  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 07:30:00  (verde)
  │     OHLC : O=0.79194  H=0.79229  L=0.79193  C=0.79210
  │     range=3.6 pips   corpo=44% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 53%  (min 30%)   [bot reportou 53%]
  │     [OK ] RSI(9)    : 71.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.79210  SL=0.79279 (6.9 pips)  TP=0.79107 (10.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: consolidation/neutral (conf 0.70) — range 42pips ~ swing médio 32pips
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: —
  │  Liquidity below: 0.78847 (equal_low, 35.0p)
  │  Alignment BUY: 10/25  |  SELL: 18/25
  └──


-------------------------------------------------------------------

[07:42:34][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.79210  SL:0.79279  TP:0.79107  pavio:53%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  12.8/25  ( 51.2%)  RSI 71.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 53%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 44% range  [aceitável]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [##########----]  18.0/25  ( 72.0%)  D1=bearish H4=unknown/up H1=consolidation/neutral
   Hist     [##########----]   3.6/5  ( 72.0%)  WR 54%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.1/100  (-14.9 pts vs mínimo 75)
   Pior critério: Sessao 0.7/10  (7% do máximo)
   → REJEITADO  —  Score 60.1 < 75 | fraco: Sessão 0.7/10
   ────────────────────────────────────────────────────────────
   [M] Momentum          51%  "RSI(9) 71.9 -> 12.8/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 53% (wick 20.0), corpo 44% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          29%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 55% em 11T (3.6/5) -> 4.3/15 pts."
   [I] ICT Macro         72%  "D1 bias=bearish | H4=unknown/up | H1=consolidation/neutral | daily_state=asia_judas -> 18.0/25 pts. 18/25 — a-favor do bias D1, fases mistas = 18/25"
-------------------------------------------------------------------
  Ciclo #3: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[09:11:14] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[09:11:46] POOL CLOSED — ciclo #4  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 09:00:00  (vermelha)
  │     OHLC : O=1.34592  H=1.34652  L=1.34537  C=1.34581
  │     range=11.5 pips   corpo=10% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 38%  (min 30%)   [bot reportou 38%]
  │     [OK ] RSI(9)    : 27.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Asia continuation/Judas  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34581  SL=1.34487 (9.4 pips)  TP=1.34722 (14.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: Asia continuation / Judas zone
  │  Liquidity above: 1.34746 (equal_low, 15.8p)
  │  Liquidity below: 1.34475 (low, 11.3p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[09:11:46][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34581  SL:1.34487  TP:1.34722  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  13.2/25  ( 52.8%)  RSI 27.7
   Wick     [###########---]  15.3/20  ( 76.5%)  pavio 38%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 10% range  [perfeito]
   Sessao   [#-------------]   0.7/10  (  7.0%)  Asia continuation/Judas
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   58.2/100  (-16.8 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 58.2 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          53%  "RSI(9) 27.7 -> 13.2/25 pts. Gate: 30."
   [R] Rejeicao          87%  "Pavio 38% (wick 15.3), corpo 10% (pin 15.0) -> 30.3/35 pts."
   [C] Contexto           5%  "Sessao Asia continuation/Judas (0.7/10), WR 30d 22% em 9T (0.0/5) -> 0.7/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=asia_judas -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.34746 = 14/25"
-------------------------------------------------------------------
  Ciclo #4: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[11:11:10] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[11:11:42] POOL CLOSED — ciclo #5  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 11:00:00  (verde)
  │     OHLC : O=1.34859  H=1.35002  L=1.34859  C=1.34931
  │     range=14.3 pips   corpo=50% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 73.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34931  SL=1.35052 (12.1 pips)  TP=1.34750 (18.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 1.35102 (high, 18.5p)
  │  Liquidity below: 1.34818 (equal_low, 9.9p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 11:00:00  (vermelha)
  │     OHLC : O=0.79047  H=0.79047  L=0.78868  C=0.78931
  │     range=17.9 pips   corpo=65% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 35%  (min 30%)   [bot reportou 35%]
  │     [OK ] RSI(9)    : 21.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78931  SL=0.78818 (11.3 pips)  TP=0.79100 (16.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: retracement/down (conf 0.70) — retraçao ~40% do último swing
  │  H1: consolidation/neutral (conf 0.70) — range 40pips ~ swing médio 32pips
  │  Daily Range: London open expansion
  │  Liquidity above: —
  │  Liquidity below: 0.78847 (equal_low, 9.2p)
  │  Alignment BUY: 8/25  |  SELL: 24/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  GBPUSD SELL  ICT=14/25  Score=59.7/100
  │  ✗ LOSER   USDCHF BUY  -- perdeu para GBPUSD SELL (ICT 14 vs 8, score 59.7 vs 55.7)
  └──

[11:11:42][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ○ USDCHF BUY  @0.78931  SL:0.78818  TP:0.79100  pavio:35%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  19.3/25  ( 77.2%)  RSI 21.1
   Wick     [##########----]  14.1/20  ( 70.5%)  pavio 35%
   PinBar   [#-------------]   1.4/15  (  9.3%)  corpo 65% range  [suja]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [####----------]   8.0/25  ( 32.0%)  D1=bearish H4=retracement/down H1=consolidation/neutral
   Hist     [##########----]   3.6/5  ( 72.0%)  WR 54%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   55.7/100  (-19.3 pts vs mínimo 75)
   Pior critério: PinBar 1.4/15  (9% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para GBPUSD SELL (ICT 14 vs 8, score 59.7 vs 55.7)
   ────────────────────────────────────────────────────────────
   [M] Momentum          77%  "RSI(9) 21.1 -> 19.3/25 pts. Gate: 30."
   [R] Rejeicao          44%  "Pavio 35% (wick 14.1), corpo 65% (pin 1.4) -> 15.5/35 pts."
   [C] Contexto          86%  "Sessao London open expansion (9.3/10), WR 30d 55% em 11T (3.6/5) -> 12.9/15 pts."
   [I] ICT Macro         32%  "D1 bias=bearish | H4=retracement/down | H1=consolidation/neutral | daily_state=london_open -> 8.0/25 pts. 10/25 — contra bias D1 mas em consolidation - liquidity below @0.78847 próxima (risco) = 8/25"
[11:11:42][WAR_ROOM] [USDCHF]   cluster_decision: USDCHF BUY preterido: perdeu para GBPUSD SELL (ICT 14 vs 8, score 59.7 vs 55.7)

-------------------------------------------------------------------

[11:11:43][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.34931  SL:1.35052  TP:1.34750  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  14.5/25  ( 58.0%)  RSI 73.8
   Wick     [##############]  19.9/20  ( 99.5%)  pavio 50%
   PinBar   [##------------]   2.0/15  ( 13.3%)  corpo 50% range  [suja]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   59.7/100  (-15.3 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 59.7 < 75 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          58%  "RSI(9) 73.8 -> 14.5/25 pts. Gate: 70."
   [R] Rejeicao          63%  "Pavio 50% (wick 19.9), corpo 50% (pin 2.0) -> 21.9/35 pts."
   [C] Contexto          62%  "Sessao London open expansion (9.3/10), WR 30d 22% em 9T (0.0/5) -> 9.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.34818 = 14/25"
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[11:11:55] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[11:12:27] POOL CLOSED — ciclo #6  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 11:00:00  (verde)
  │     OHLC : O=0.58392  H=0.58472  L=0.58390  C=0.58434
  │     range=8.2 pips   corpo=51% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 72.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58434  SL=0.58522 (8.8 pips)  TP=0.58302 (13.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 0.58738 (equal_low, 31.7p)
  │  Liquidity below: 0.58398 (equal_low, 2.3p)
  │  Alignment BUY: 10/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[11:12:27][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58434  SL:0.58522  TP:0.58302  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.4/25  ( 53.6%)  RSI 72.6
   Wick     [#############-]  18.5/20  ( 92.5%)  pavio 46%
   PinBar   [##------------]   2.0/15  ( 13.3%)  corpo 51% range  [suja]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   62.2/100  (-12.8 pts vs mínimo 75)
   Pior critério: PinBar 2.0/15  (13% do máximo)
   → REJEITADO  —  Score 62.2 < 75 | fraco: Pin Bar 2.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          54%  "RSI(9) 72.6 -> 13.4/25 pts. Gate: 70."
   [R] Rejeicao          59%  "Pavio 46% (wick 18.5), corpo 51% (pin 2.0) -> 20.5/35 pts."
   [C] Contexto          95%  "Sessao London open expansion (9.3/10), WR 30d 69% em 16T (5.0/5) -> 14.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.58398 = 14/25"
-------------------------------------------------------------------
  Ciclo #6: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[11:41:18] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[11:41:50] POOL CLOSED — ciclo #7  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 11:30:00  (vermelha)
  │     OHLC : O=0.78950  H=0.78968  L=0.78882  C=0.78948
  │     range=8.6 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 77%  (min 30%)   [bot reportou 77%]
  │     [OK ] RSI(9)    : 25.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78948  SL=0.78832 (11.6 pips)  TP=0.79122 (17.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: retracement/down (conf 0.70) — retraçao ~47% do último swing
  │  H1: consolidation/neutral (conf 0.70) — range 40pips ~ swing médio 32pips
  │  Daily Range: London open expansion
  │  Liquidity above: —
  │  Liquidity below: 0.78847 (equal_low, 11.4p)
  │  Alignment BUY: 8/25  |  SELL: 24/25
  └──


-------------------------------------------------------------------

[11:41:50][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78948  SL:0.78832  TP:0.79122  pavio:77%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  14.9/25  ( 59.6%)  RSI 25.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 77%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [####----------]   8.0/25  ( 32.0%)  D1=bearish H4=retracement/down H1=consolidation/neutral
   Hist     [##########----]   3.6/5  ( 72.0%)  WR 54%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.8/100  (-4.2 pts vs mínimo 75)
   Pior critério: ICT 8.0/25  (32% do máximo)
   → REJEITADO  —  Score 70.8 < 75 | fraco: ICT Macro 8.0/25
   ────────────────────────────────────────────────────────────
   [M] Momentum          60%  "RSI(9) 25.9 -> 14.9/25 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 77% (wick 20.0), corpo 2% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          86%  "Sessao London open expansion (9.3/10), WR 30d 55% em 11T (3.6/5) -> 12.9/15 pts."
   [I] ICT Macro         32%  "D1 bias=bearish | H4=retracement/down | H1=consolidation/neutral | daily_state=london_open -> 8.0/25 pts. 10/25 — contra bias D1 mas em consolidation - liquidity below @0.78847 próxima (risco) = 8/25"
-------------------------------------------------------------------
  Ciclo #7: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[12:41:29] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[12:42:01] POOL CLOSED — ciclo #8  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 12:30:00  (verde)
  │     OHLC : O=0.71343  H=0.71467  L=0.71343  C=0.71397
  │     range=12.4 pips   corpo=44% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 56%  (min 30%)   [bot reportou 56%]
  │     [OK ] RSI(9)    : 72.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=09h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71397  SL=0.71517 (12.0 pips)  TP=0.71217 (18.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 0.71427 (equal_low, 2.1p)
  │  Liquidity below: 0.71316 (equal_low, 9.0p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 12:30:00  (verde)
  │     OHLC : O=1.34932  H=1.35044  L=1.34916  C=1.34983
  │     range=12.8 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 48%  (min 30%)   [bot reportou 48%]
  │     [OK ] RSI(9)    : 70.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=09h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34983  SL=1.35094 (11.1 pips)  TP=1.34816 (16.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 1.35102 (high, 10.7p)
  │  Liquidity below: 1.34818 (equal_low, 17.7p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  AUDUSD SELL  ICT=14/25  Score=62.9/100
  │  ✗ LOSER   GBPUSD SELL  -- perdeu para AUDUSD SELL (ICT 14 vs 14, score 62.9 vs 58.5)
  └──

[12:42:01][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ○ GBPUSD SELL  @1.34983  SL:1.35094  TP:1.34816  pavio:48%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  11.1/25  ( 44.4%)  RSI 70.1
   Wick     [#############-]  19.1/20  ( 95.5%)  pavio 48%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 40% range  [aceitável]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   58.5/100  (-16.5 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para AUDUSD SELL (ICT 14 vs 14, score 62.9 vs 58.5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          44%  "RSI(9) 70.1 -> 11.1/25 pts. Gate: 70."
   [R] Rejeicao          69%  "Pavio 48% (wick 19.1), corpo 40% (pin 5.0) -> 24.1/35 pts."
   [C] Contexto          62%  "Sessao London open expansion (9.3/10), WR 30d 22% em 9T (0.0/5) -> 9.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.34818 = 14/25"
[12:42:02][WAR_ROOM] [GBPUSD]   cluster_decision: GBPUSD SELL preterido: perdeu para AUDUSD SELL (ICT 14 vs 14, score 62.9 vs 58.5)

-------------------------------------------------------------------

[12:42:02][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71397  SL:0.71517  TP:0.71217  pavio:56%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.5/25  ( 54.0%)  RSI 72.7
   Wick     [##############]  20.0/20  (100.0%)  pavio 56%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 44% range  [aceitável]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=unknown/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   62.9/100  (-12.1 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → REJEITADO  —  Score 62.9 < 75 | fraco: Histórico 1.1/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          54%  "RSI(9) 72.7 -> 13.5/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 56% (wick 20.0), corpo 44% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          69%  "Sessao London open expansion (9.3/10), WR 30d 44% em 27T (1.1/5) -> 10.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=unknown/neutral | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71316 = 14/25"
-------------------------------------------------------------------
  Ciclo #8: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[12:42:09] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[12:42:41] POOL CLOSED — ciclo #9  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 12:30:00  (verde)
  │     OHLC : O=0.58429  H=0.58533  L=0.58429  C=0.58472
  │     range=10.4 pips   corpo=41% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 59%  (min 30%)   [bot reportou 59%]
  │     [OK ] RSI(9)    : 72.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=09h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58472  SL=0.58583 (11.1 pips)  TP=0.58306 (16.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 0.58738 (equal_low, 26.4p)
  │  Liquidity below: 0.58398 (equal_low, 7.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 12:30:00  (vermelha)
  │     OHLC : O=0.78828  H=0.78835  L=0.78753  C=0.78793
  │     range=8.2 pips   corpo=43% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 15.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=09h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78793  SL=0.78703 (9.0 pips)  TP=0.78928 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: London open expansion
  │  Liquidity above: 0.78847 (equal_low, 6.4p)
  │  Liquidity below: 0.78755 (equal_high, 2.8p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF BUY  ICT=17/25  Score=78.9/100
  │  ✗ LOSER   NZDUSD SELL  -- perdeu para USDCHF BUY (ICT 17 vs 14, score 78.9 vs 66.5)
  └──

[12:42:42][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD SELL  @0.58472  SL:0.58583  TP:0.58306  pavio:59%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  13.2/25  ( 52.8%)  RSI 72.4
   Wick     [##############]  20.0/20  (100.0%)  pavio 59%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 41% range  [aceitável]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   66.5/100  (-8.5 pts vs mínimo 75)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF BUY (ICT 17 vs 14, score 78.9 vs 66.5)
   ────────────────────────────────────────────────────────────
   [M] Momentum          53%  "RSI(9) 72.4 -> 13.2/25 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 59% (wick 20.0), corpo 41% (pin 5.0) -> 25.0/35 pts."
   [C] Contexto          95%  "Sessao London open expansion (9.3/10), WR 30d 69% em 16T (5.0/5) -> 14.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.58398 = 14/25"
[12:42:42][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD SELL preterido: perdeu para USDCHF BUY (ICT 17 vs 14, score 78.9 vs 66.5)

-------------------------------------------------------------------

[12:42:42][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF BUY  @0.78793  SL:0.78703  TP:0.78928  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  24.5/25  ( 98.0%)  RSI 15.5
   Wick     [##############]  19.5/20  ( 97.5%)  pavio 49%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 43% range  [aceitável]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [##########----]   3.6/5  ( 72.0%)  WR 54%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   78.9/100  (+3.9 pts vs mínimo 75)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → APROVADO  —  Score 78.9/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          98%  "RSI(9) 15.5 -> 24.5/25 pts. Gate: 30."
   [R] Rejeicao          70%  "Pavio 49% (wick 19.5), corpo 43% (pin 5.0) -> 24.5/35 pts."
   [C] Contexto          86%  "Sessao London open expansion (9.3/10), WR 30d 55% em 11T (3.6/5) -> 12.9/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=london_open -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78847 = 17/25"
-------------------------------------------------------------------
  Ciclo #9: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[12:56:19] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[12:56:50] POOL CLOSED — ciclo #10  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 12:45:00  (verde)
  │     OHLC : O=0.71397  H=0.71475  L=0.71397  C=0.71449
  │     range=7.8 pips   corpo=67% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 77.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=09h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71449  SL=0.71525 (7.6 pips)  TP=0.71335 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 0.71479 (equal_high, 2.5p)
  │  Liquidity below: 0.71447 (equal_low, 0.6p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 12:45:00  (verde)
  │     OHLC : O=1.34983  H=1.35051  L=1.34979  C=1.35023
  │     range=7.2 pips   corpo=56% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 73.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=09h -> London open expansion  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35023  SL=1.35101 (7.8 pips)  TP=1.34906 (11.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] GBPUSD  |  Daily bias: NEUTRAL →
  │  H4: consolidation/neutral (conf 0.70) — range 128pips ~ swing médio 113pips
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London open expansion
  │  Liquidity above: 1.35102 (high, 8.5p)
  │  Liquidity below: 1.34818 (equal_low, 19.8p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  AUDUSD SELL  ICT=14/25  Score=57.0/100
  │  ✗ LOSER   GBPUSD SELL  -- perdeu para AUDUSD SELL (ICT 14 vs 14, score 57.0 vs 54.9)
  └──

[12:56:51][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ○ GBPUSD SELL  @1.35023  SL:1.35101  TP:1.34906  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  14.2/25  ( 56.8%)  RSI 73.4
   Wick     [###########---]  15.6/20  ( 78.0%)  pavio 39%
   PinBar   [##------------]   1.8/15  ( 12.0%)  corpo 56% range  [suja]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=consolidation/neutral H1=unknown/down
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   54.9/100  (-20.1 pts vs mínimo 75)
   Pior critério: Hist 0/5  (0% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para AUDUSD SELL (ICT 14 vs 14, score 57.0 vs 54.9)
   ────────────────────────────────────────────────────────────
   [M] Momentum          57%  "RSI(9) 73.4 -> 14.2/25 pts. Gate: 70."
   [R] Rejeicao          50%  "Pavio 39% (wick 15.6), corpo 56% (pin 1.8) -> 17.4/35 pts."
   [C] Contexto          62%  "Sessao London open expansion (9.3/10), WR 30d 22% em 9T (0.0/5) -> 9.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=consolidation/neutral | H1=unknown/down | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @1.34818 = 14/25"
[12:56:51][WAR_ROOM] [GBPUSD]   cluster_decision: GBPUSD SELL preterido: perdeu para AUDUSD SELL (ICT 14 vs 14, score 57.0 vs 54.9)

-------------------------------------------------------------------

[12:56:51][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71449  SL:0.71525  TP:0.71335  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  18.0/25  ( 72.0%)  RSI 77.5
   Wick     [#########-----]  13.3/20  ( 66.5%)  pavio 33%
   PinBar   [#-------------]   1.3/15  (  8.7%)  corpo 67% range  [suja]
   Sessao   [#############-]   9.3/10  ( 93.0%)  London open expansion
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=unknown/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   57.0/100  (-18.0 pts vs mínimo 75)
   Pior critério: PinBar 1.3/15  (9% do máximo)
   → REJEITADO  —  Score 57.0 < 75 | fraco: Pin Bar 1.3/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          72%  "RSI(9) 77.5 -> 18.0/25 pts. Gate: 70."
   [R] Rejeicao          42%  "Pavio 33% (wick 13.3), corpo 67% (pin 1.3) -> 14.6/35 pts."
   [C] Contexto          69%  "Sessao London open expansion (9.3/10), WR 30d 44% em 27T (1.1/5) -> 10.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=unknown/neutral | daily_state=london_open -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71447 = 14/25"
-------------------------------------------------------------------
  Ciclo #10: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[13:02:12] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[13:02:44] POOL CLOSED — ciclo #11  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 12:45:00  (vermelha)
  │     OHLC : O=0.78793  H=0.78796  L=0.78714  C=0.78740
  │     range=8.2 pips   corpo=65% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 13.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78740  SL=0.78664 (7.6 pips)  TP=0.78854 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: London continuation
  │  Liquidity above: 0.78722 (equal_high, 0.3p)
  │  Liquidity below: 0.78717 (equal_high, 0.1p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


-------------------------------------------------------------------

[13:02:44][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78740  SL:0.78664  TP:0.78854  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 13.1
   Wick     [#########-----]  12.7/20  ( 63.5%)  pavio 32%
   PinBar   [#-------------]   1.4/15  (  9.3%)  corpo 65% range  [suja]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   65.9/100  (-9.1 pts vs mínimo 75)
   Pior critério: PinBar 1.4/15  (9% do máximo)
   → REJEITADO  —  Score 65.9 < 75 | fraco: Pin Bar 1.4/15
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 13.1 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          40%  "Pavio 32% (wick 12.7), corpo 65% (pin 1.4) -> 14.1/35 pts."
   [C] Contexto          65%  "Sessao London continuation (7.3/10), WR 30d 50% em 12T (2.5/5) -> 9.8/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=london_cont -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78722 = 17/25"
-------------------------------------------------------------------
  Ciclo #11: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[13:11:07] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=22s, total=2)

[13:11:39] POOL CLOSED — ciclo #12  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 13:00:00  (verde)
  │     OHLC : O=0.78740  H=0.78771  L=0.78696  C=0.78756
  │     range=7.5 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 59%  (min 30%)   [bot reportou 59%]
  │     [OK ] RSI(9)    : 17.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78756  SL=0.78646 (11.0 pips)  TP=0.78921 (16.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCHF  |  Daily bias: BEARISH ↓
  │  H4: unknown/up (conf 0.40) — fora dos padrões claros
  │  H1: reversal/up (conf 0.93) — BOS detectado (LH/HL)
  │  Daily Range: London continuation
  │  Liquidity above: 0.78847 (equal_low, 9.1p)
  │  Liquidity below: 0.78755 (equal_high, 0.1p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 13:00:00  (vermelha)
  │     OHLC : O=0.58532  H=0.58557  L=0.58498  C=0.58506
  │     range=5.9 pips   corpo=44% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 42%  (min 30%)   [bot reportou 42%]
  │     [OK ] RSI(9)    : 70.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58506  SL=0.58607 (10.1 pips)  TP=0.58355 (15.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London continuation
  │  Liquidity above: 0.58738 (equal_low, 22.1p)
  │  Liquidity below: 0.58398 (equal_low, 11.9p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  USDCHF BUY  ICT=17/25  Score=79.5/100
  │  ✗ LOSER   NZDUSD SELL  -- perdeu para USDCHF BUY (ICT 17 vs 14, score 79.5 vs 60.0)
  └──

[13:11:40][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ○ NZDUSD SELL  @0.58506  SL:0.58607  TP:0.58355  pavio:42%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  11.8/25  ( 47.2%)  RSI 70.9
   Wick     [############--]  16.9/20  ( 84.5%)  pavio 42%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 44% range  [aceitável]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.0/100  (-15.0 pts vs mínimo 75)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para USDCHF BUY (ICT 17 vs 14, score 79.5 vs 60.0)
   ────────────────────────────────────────────────────────────
   [M] Momentum          47%  "RSI(9) 70.9 -> 11.8/25 pts. Gate: 70."
   [R] Rejeicao          63%  "Pavio 42% (wick 16.9), corpo 44% (pin 5.0) -> 21.9/35 pts."
   [C] Contexto          82%  "Sessao London continuation (7.3/10), WR 30d 69% em 16T (5.0/5) -> 12.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.58398 = 14/25"
[13:11:40][WAR_ROOM] [NZDUSD]   cluster_decision: NZDUSD SELL preterido: perdeu para USDCHF BUY (ICT 17 vs 14, score 79.5 vs 60.0)

-------------------------------------------------------------------

[13:11:40][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF BUY  @0.78756  SL:0.78646  TP:0.78921  pavio:59%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  22.7/25  ( 90.8%)  RSI 17.4
   Wick     [##############]  20.0/20  (100.0%)  pavio 59%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 21% range  [bom]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.5/100  (+4.5 pts vs mínimo 75)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 79.5/75 -> execução (winner do cluster)
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 17.4 -> 22.7/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 59% (wick 20.0), corpo 21% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          65%  "Sessao London continuation (7.3/10), WR 30d 50% em 12T (2.5/5) -> 9.8/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=london_cont -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78847 = 17/25"
-------------------------------------------------------------------
  Ciclo #12: 1 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[13:41:13] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...
  + 1 novo(s) sinal(is) entraram no pool (t=19s, total=2)

[13:41:44] POOL CLOSED — ciclo #13  --  2 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 13:30:00  (vermelha)
  │     OHLC : O=0.71530  H=0.71576  L=0.71496  C=0.71529
  │     range=8.0 pips   corpo=1% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 57%  (min 30%)   [bot reportou 57%]
  │     [OK ] RSI(9)    : 77.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71529  SL=0.71626 (9.7 pips)  TP=0.71384 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: unknown/neutral (conf 0.40) — fora dos padrões claros
  │  Daily Range: London continuation
  │  Liquidity above: 0.71567 (equal_high, 3.8p)
  │  Liquidity below: 0.71518 (equal_low, 1.1p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-30 13:30:00  (vermelha)
  │     OHLC : O=1.36583  H=1.36594  L=1.36520  C=1.36567
  │     range=7.4 pips   corpo=22% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 64%  (min 30%)   [bot reportou 64%]
  │     [OK ] RSI(9)    : 26.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36567  SL=1.36470 (9.7 pips)  TP=1.36712 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] USDCAD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: consolidation/neutral (conf 0.70) — range 59pips ~ swing médio 43pips
  │  Daily Range: London continuation
  │  Liquidity above: 1.36671 (equal_low, 9.9p)
  │  Liquidity below: 1.36433 (low, 13.9p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


  ┌── [CLUSTER DECISION]  1 winner(s)  /  1 loser(s)
  │  ✓ WINNER  AUDUSD SELL  ICT=14/25  Score=74.9/100
  │  ✗ LOSER   USDCAD BUY  -- perdeu para AUDUSD SELL (ICT 14 vs 14, score 74.9 vs 68.3)
  └──

[13:41:45][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ○ USDCAD BUY  @1.36567  SL:1.36470  TP:1.36712  pavio:64%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  13.9/25  ( 55.6%)  RSI 26.9
   Wick     [##############]  20.0/20  (100.0%)  pavio 64%
   PinBar   [#########-----]  10.0/15  ( 66.7%)  corpo 22% range  [bom]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=consolidation/neutral
   Hist     [#########-----]   3.1/5  ( 62.0%)  WR 52%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.3/100  (-6.7 pts vs mínimo 75)
   Pior critério: RSI 13.9/25  (56% do máximo)
   → PRETERIDO_CLUSTER  —  perdeu para AUDUSD SELL (ICT 14 vs 14, score 74.9 vs 68.3)
   ────────────────────────────────────────────────────────────
   [M] Momentum          56%  "RSI(9) 26.9 -> 13.9/25 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 64% (wick 20.0), corpo 22% (pin 10.0) -> 30.0/35 pts."
   [C] Contexto          69%  "Sessao London continuation (7.3/10), WR 30d 52% em 21T (3.1/5) -> 10.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=consolidation/neutral | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity above @1.36671 = 14/25"
[13:41:45][WAR_ROOM] [USDCAD]   cluster_decision: USDCAD BUY preterido: perdeu para AUDUSD SELL (ICT 14 vs 14, score 74.9 vs 68.3)

-------------------------------------------------------------------

[13:41:45][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71529  SL:0.71626  TP:0.71384  pavio:57%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  17.5/25  ( 70.0%)  RSI 77.0
   Wick     [##############]  20.0/20  (100.0%)  pavio 57%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 1% range  [perfeito]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=unknown/neutral
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.9/100  (-0.1 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → REJEITADO  —  Score 74.9 < 75 | fraco: Histórico 1.1/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          70%  "RSI(9) 77.0 -> 17.5/25 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 57% (wick 20.0), corpo 1% (pin 15.0) -> 35.0/35 pts."
   [C] Contexto          56%  "Sessao London continuation (7.3/10), WR 30d 44% em 27T (1.1/5) -> 8.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=unknown/neutral | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71518 = 14/25"
-------------------------------------------------------------------
  Ciclo #13: 0 aprovado(s) / 1 winners / 1 preteridos cluster / 0 cliff-rejected / 2 total

[13:41:53] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[13:42:25] POOL CLOSED — ciclo #14  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 13:30:00  (verde)
  │     OHLC : O=0.58592  H=0.58638  L=0.58580  C=0.58613
  │     range=5.8 pips   corpo=36% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 80.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58613  SL=0.58688 (7.5 pips)  TP=0.58501 (11.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] NZDUSD  |  Daily bias: NEUTRAL →
  │  H4: reversal/down (conf 1.00) — BOS detectado (HH/LL)
  │  H1: unknown/down (conf 0.40) — fora dos padrões claros
  │  Daily Range: London continuation
  │  Liquidity above: 0.58738 (equal_low, 13.8p)
  │  Liquidity below: 0.58398 (equal_low, 20.2p)
  │  Alignment BUY: 14/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[13:42:25][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58613  SL:0.58688  TP:0.58501  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  20.6/25  ( 82.4%)  RSI 80.3
   Wick     [############--]  17.2/20  ( 86.0%)  pavio 43%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 36% range  [aceitável]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=reversal/down H1=unknown/down
   Hist     [##############]     5/5  (100.0%)  WR 69%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.1/100  (-5.9 pts vs mínimo 75)
   Pior critério: PinBar 5.0/15  (33% do máximo)
   → REJEITADO  —  Score 69.1 < 75 | fraco: Pin Bar 5.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          82%  "RSI(9) 80.3 -> 20.6/25 pts. Gate: 70."
   [R] Rejeicao          63%  "Pavio 43% (wick 17.2), corpo 36% (pin 5.0) -> 22.2/35 pts."
   [C] Contexto          82%  "Sessao London continuation (7.3/10), WR 30d 69% em 16T (5.0/5) -> 12.3/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=reversal/down | H1=unknown/down | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.58398 = 14/25"
-------------------------------------------------------------------
  Ciclo #14: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[14:11:16] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[14:11:48] POOL CLOSED — ciclo #15  --  1 sinal(is) processado(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-30 14:00:00  (vermelha)
  │     OHLC : O=0.71572  H=0.71605  L=0.71528  C=0.71565
  │     range=7.7 pips   corpo=9% do range
  │
  │  Gatilhos da estrategia (v6.2.0 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 78.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=11h -> London continuation  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71565  SL=0.71655 (9.0 pips)  TP=0.71430 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring
  ┌── [ICT CONTEXT] AUDUSD  |  Daily bias: NEUTRAL →
  │  H4: expansion/down (conf 0.90) — último swing 88pips vs mediana 49pips
  │  H1: reversal/up (conf 0.73) — BOS detectado (LH/HL)
  │  Daily Range: London continuation
  │  Liquidity above: 0.71647 (equal_high, 7.3p)
  │  Liquidity below: 0.71567 (equal_high, 0.7p)
  │  Alignment BUY: 20/25  |  SELL: 14/25
  └──


-------------------------------------------------------------------

[14:11:48][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71565  SL:0.71655  TP:0.71430  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  18.5/25  ( 74.0%)  RSI 78.0
   Wick     [############--]  17.1/20  ( 85.5%)  pavio 43%
   PinBar   [##############]  15.0/15  (100.0%)  corpo 9% range  [perfeito]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [########------]  14.0/25  ( 56.0%)  D1=neutral H4=expansion/down H1=reversal/up
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (27T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.0/100  (-2.0 pts vs mínimo 75)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → REJEITADO  —  Score 73.0 < 75 | fraco: Histórico 1.1/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          74%  "RSI(9) 78.0 -> 18.5/25 pts. Gate: 70."
   [R] Rejeicao          92%  "Pavio 43% (wick 17.1), corpo 9% (pin 15.0) -> 32.1/35 pts."
   [C] Contexto          56%  "Sessao London continuation (7.3/10), WR 30d 44% em 27T (1.1/5) -> 8.4/15 pts."
   [I] ICT Macro         56%  "D1 bias=neutral | H4=expansion/down | H1=reversal/up | daily_state=london_cont -> 14.0/25 pts. 12/25 — bias D1 neutro, fases sem alinhamento claro + raid liquidity below @0.71567 = 14/25"
-------------------------------------------------------------------
  Ciclo #15: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total

[14:26:23] POOL OPEN — 1 sinal(is) iniciais. Aguardando 30s para acumular correlatos...

[14:26:55] POOL CLOSED — ciclo #16  --  1 sinal(is) processado(s)
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
  │  Liquidity above: 0.78717 (equal_high, 18.8p)
  │  Liquidity below: 0.78443 (equal_high, 8.6p)
  │  Alignment BUY: 17/25  |  SELL: 20/25
  └──


-------------------------------------------------------------------

[14:26:55][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78504  SL:0.78420  TP:0.78630  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  25.0/25  (100.0%)  RSI 9.2
   Wick     [###########---]  15.3/20  ( 76.5%)  pavio 38%
   PinBar   [#####---------]   5.0/15  ( 33.3%)  corpo 43% range  [aceitável]
   Sessao   [##########----]   7.3/10  ( 73.0%)  London continuation
   ICT      [##########----]  17.0/25  ( 68.0%)  D1=bearish H4=unknown/up H1=reversal/up
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.1/100  (-3.9 pts vs mínimo 75)
   Pior critério: Hist 1.5/5  (30% do máximo)
   → REJEITADO  —  Score 71.1 < 75 | fraco: Histórico 1.5/5
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 9.2 -> 25.0/25 pts. Gate: 30."
   [R] Rejeicao          58%  "Pavio 38% (wick 15.3), corpo 43% (pin 5.0) -> 20.3/35 pts."
   [C] Contexto          59%  "Sessao London continuation (7.3/10), WR 30d 46% em 13T (1.5/5) -> 8.8/15 pts."
   [I] ICT Macro         68%  "D1 bias=bearish | H4=unknown/up | H1=reversal/up | daily_state=london_cont -> 17.0/25 pts. 15/25 — contra bias D1 mas H1 reversal alinhado (BOS recente) + raid liquidity above @0.78717 = 17/25"
-------------------------------------------------------------------
  Ciclo #16: 0 aprovado(s) / 1 winners / 0 preteridos cluster / 0 cliff-rejected / 1 total