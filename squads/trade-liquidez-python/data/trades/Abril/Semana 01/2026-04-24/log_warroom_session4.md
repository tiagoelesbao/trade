===================================================================
  WAR ROOM v6.1.2  --  ANALISE TECNICA AGENTICA
-------------------------------------------------------------------
  Score minimo : 55/100   |   Correlacao: ATIVA   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)   [Slope/ColorReversal desativados nas Fases 1+2]
  Criterios    : RSI(35) Wick(25) PinBar(20) Sessao(15) Hist(5)  [alpha: RSI]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE (gatilhos+condicoes) -> [FASE 2] signal_analysis (score)
===================================================================
[15:03:14][WAR_ROOM]   war_room_started: War Room v6.1.2 iniciada | Score mínimo: 55/100 | 5 critérios (RSI alpha) | estratégia: Zona+Wick+RSI | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[15:03:21] ciclo #1  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 14:45:00  (vermelha)
  │     OHLC : O=0.86806  H=0.86826  L=0.86802  C=0.86804
  │     range=2.4 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 83%  (min 30%)   [bot reportou 83%]
  │     [OK ] RSI(9)    : 96.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86804  SL=0.86876 (7.2 pips)  TP=0.86696 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:03:21][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP SELL  @0.86804  SL:0.86876  TP:0.86696  pavio:83%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 96.3
   Wick     [##############]    25/25  (100.0%)  pavio 83%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   92.5/100  (+37.5 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 92.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 96.3 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 83% (wick 25.0), corpo 8% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 10T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #1: 1 aprovado(s) / 1 analisado(s)

[15:11:17] ciclo #2  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 15:00:00  (verde)
  │     OHLC : O=1.34949  H=1.34989  L=1.34915  C=1.34964
  │     range=7.4 pips   corpo=20% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 34%  (min 30%)   [bot reportou 34%]
  │     [OK ] RSI(9)    : 70.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34964  SL=1.35039 (7.5 pips)  TP=1.34851 (11.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:11:17][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.34964  SL:1.35039  TP:1.34851  pavio:34%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.9/35  ( 45.4%)  RSI 70.7
   Wick     [#########-----]  16.9/25  ( 67.6%)  pavio 34%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 20% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   55.8/100  (+0.8 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 70.7 -> 15.9/35 pts. Gate: 70."
   [R] Rejeicao          66%  "Pavio 34% (wick 16.9), corpo 20% (pin 13.0) -> 29.9/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #2: 0 aprovado(s) / 1 analisado(s)

[15:11:38] ciclo #3  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 15:00:00  (verde)
  │     OHLC : O=0.71440  H=0.71473  L=0.71431  C=0.71453
  │     range=4.2 pips   corpo=31% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 48%  (min 30%)   [bot reportou 48%]
  │     [OK ] RSI(9)    : 73.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71453  SL=0.71523 (7.0 pips)  TP=0.71348 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:11:39][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71453  SL:0.71523  TP:0.71348  pavio:48%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.0/35  ( 54.3%)  RSI 73.0
   Wick     [#############-]  23.8/25  ( 95.2%)  pavio 48%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 31% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.5/100  (+6.5 pts vs mínimo 55)
   Pior critério: Hist 1.7/5  (34% do máximo)
   → APROVADO  —  Score 61.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          54%  "RSI(9) 73.0 -> 19.0/35 pts. Gate: 70."
   [R] Rejeicao          68%  "Pavio 48% (wick 23.8), corpo 31% (pin 7.0) -> 30.8/45 pts."
   [C] Contexto          58%  "Sessao London (10.0), WR 30d 47% em 15T (1.7) -> 11.7/20 pts."
-------------------------------------------------------------------
  Ciclo #3: 1 aprovado(s) / 1 analisado(s)

[15:12:00] ciclo #4  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 15:00:00  (vermelha)
  │     OHLC : O=0.78530  H=0.78545  L=0.78492  C=0.78515
  │     range=5.3 pips   corpo=28% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 14.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78515  SL=0.78442 (7.3 pips)  TP=0.78625 (11.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:12:00][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF BUY  @0.78515  SL:0.78442  TP:0.78625  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 14.8
   Wick     [############--]  21.7/25  ( 86.8%)  pavio 43%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 28% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.7/100  (+24.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 79.7/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 14.8 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          77%  "Pavio 43% (wick 21.7), corpo 28% (pin 13.0) -> 34.7/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #4: 1 aprovado(s) / 1 analisado(s)

[15:12:27] ciclo #5  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 15:00:00  (verde)
  │     OHLC : O=0.58732  H=0.58768  L=0.58732  C=0.58746
  │     range=3.6 pips   corpo=39% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 61%  (min 30%)   [bot reportou 61%]
  │     [OK ] RSI(9)    : 82.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58746  SL=0.58818 (7.2 pips)  TP=0.58638 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:12:27][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58746  SL:0.58818  TP:0.58638  pavio:61%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  31.8/35  ( 90.9%)  RSI 82.6
   Wick     [##############]    25/25  (100.0%)  pavio 61%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 39% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 62%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   78.8/100  (+23.8 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 82.6 -> 31.8/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 61% (wick 25.0), corpo 39% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 62% em 13T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 analisado(s)

[16:41:34] ciclo #6  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 16:30:00  (verde)
  │     OHLC : O=0.71305  H=0.71337  L=0.71256  C=0.71308
  │     range=8.1 pips   corpo=4% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 60%  (min 30%)   [bot reportou 60%]
  │     [OK ] RSI(9)    : 8.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=13h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71308  SL=0.71206 (10.2 pips)  TP=0.71461 (15.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[16:41:35][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD BUY  @0.71308  SL:0.71206  TP:0.71461  pavio:60%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 8.3
   Wick     [##############]    25/25  (100.0%)  pavio 60%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 4% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [####################]   97.5/100  (+42.5 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 97.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 8.3 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 60% (wick 25.0), corpo 4% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          88%  "Sessao London+NY overlap (15.0), WR 30d 50% em 16T (2.5) -> 17.5/20 pts."
-------------------------------------------------------------------
  Ciclo #6: 1 aprovado(s) / 1 analisado(s)

[16:41:56] ciclo #7  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 16:30:00  (verde)
  │     OHLC : O=0.78671  H=0.78744  L=0.78653  C=0.78715
  │     range=9.1 pips   corpo=48% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 84.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=13h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78715  SL=0.78794 (7.9 pips)  TP=0.78597 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[16:41:56][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✓ USDCHF SELL  @0.78715  SL:0.78794  TP:0.78597  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.6/35  ( 96.0%)  RSI 84.0
   Wick     [#########-----]  15.9/25  ( 63.6%)  pavio 32%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 48% range  [aceitável]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 40%  (5T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.5/100  (+16.5 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 71.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          96%  "RSI(9) 84.0 -> 33.6/35 pts. Gate: 70."
   [R] Rejeicao          51%  "Pavio 32% (wick 15.9), corpo 48% (pin 7.0) -> 22.9/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 40% em 5T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #7: 1 aprovado(s) / 1 analisado(s)

[16:42:17] ciclo #8  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 16:30:00  (vermelha)
  │     OHLC : O=0.58647  H=0.58662  L=0.58614  C=0.58645
  │     range=4.8 pips   corpo=4% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 65%  (min 30%)   [bot reportou 65%]
  │     [OK ] RSI(9)    : 15.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=13h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58645  SL=0.58564 (8.1 pips)  TP=0.58766 (12.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[16:42:17][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58645  SL:0.58564  TP:0.58766  pavio:65%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  34.7/35  ( 99.1%)  RSI 15.3
   Wick     [##############]    25/25  (100.0%)  pavio 65%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 4% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [##############]     5/5  (100.0%)  WR 62%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [####################]   99.7/100  (+44.7 pts vs mínimo 55)
   Pior critério: RSI 34.7/35  (99% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          99%  "RSI(9) 15.3 -> 34.7/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 65% (wick 25.0), corpo 4% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto         100%  "Sessao London+NY overlap (15.0), WR 30d 62% em 13T (5.0) -> 20.0/20 pts."
-------------------------------------------------------------------
  Ciclo #8: 0 aprovado(s) / 1 analisado(s)

[17:26:32] ciclo #9  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 17:15:00  (vermelha)
  │     OHLC : O=0.86725  H=0.86730  L=0.86684  C=0.86704
  │     range=4.6 pips   corpo=46% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 29.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=14h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86704  SL=0.86634 (7.0 pips)  TP=0.86809 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[17:26:33][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP BUY  @0.86704  SL:0.86634  TP:0.86809  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.6/35  ( 44.6%)  RSI 29.5
   Wick     [############--]  21.7/25  ( 86.8%)  pavio 43%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 46% range  [aceitável]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [##########----]   3.6/5  ( 72.0%)  WR 54%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   62.9/100  (+7.9 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → APROVADO  —  Score 62.9/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 29.5 -> 15.6/35 pts. Gate: 30."
   [R] Rejeicao          64%  "Pavio 43% (wick 21.7), corpo 46% (pin 7.0) -> 28.7/45 pts."
   [C] Contexto          93%  "Sessao London+NY overlap (15.0), WR 30d 55% em 11T (3.6) -> 18.6/20 pts."
-------------------------------------------------------------------
  Ciclo #9: 1 aprovado(s) / 1 analisado(s)