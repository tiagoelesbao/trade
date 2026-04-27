===================================================================
  WAR ROOM v6.1.2  --  ANALISE TECNICA AGENTICA
-------------------------------------------------------------------
  Score minimo : 55/100   |   Correlacao: ATIVA   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)   [Slope/ColorReversal desativados nas Fases 1+2]
  Criterios    : RSI(35) Wick(25) PinBar(20) Sessao(15) Hist(5)  [alpha: RSI]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE (gatilhos+condicoes) -> [FASE 2] signal_analysis (score)
===================================================================
[15:19:49][WAR_ROOM]   war_room_started: War Room v6.1.2 iniciada | Score mínimo: 55/100 | 5 critérios (RSI alpha) | estratégia: Zona+Wick+RSI | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[16:26:39] ciclo #1  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 16:15:00  (verde)
  │     OHLC : O=215.14200  H=215.20500  L=215.08500  C=215.15800
  │     range=12.0 pips   corpo=13% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 47%  (min 30%)   [bot reportou 47%]
  │     [OK ] RSI(9)    : 24.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=13h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.15800  SL=215.03500 (12.3 pips)  TP=215.34250 (18.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[16:26:39][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY BUY  @215.15800  SL:215.03500  TP:215.34250  pavio:47%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  22.1/35  ( 63.1%)  RSI 24.6
   Wick     [#############-]  23.7/25  ( 94.8%)  pavio 47%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 13% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   80.8/100  (+25.8 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 80.8/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          63%  "RSI(9) 24.6 -> 22.1/35 pts. Gate: 30."
   [R] Rejeicao          97%  "Pavio 47% (wick 23.7), corpo 13% (pin 20.0) -> 43.7/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 22% em 9T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #1: 1 aprovado(s) / 1 analisado(s)

[18:26:41] ciclo #2  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 18:15:00  (verde)
  │     OHLC : O=1.17072  H=1.17154  L=1.17059  C=1.17107
  │     range=9.5 pips   corpo=37% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 86.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17107  SL=1.17204 (9.7 pips)  TP=1.16962 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[18:26:41][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD SELL  @1.17107  SL:1.17204  TP:1.16962  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 86.3
   Wick     [##############]  24.7/25  ( 98.8%)  pavio 49%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 37% range  [aceitável]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [##------------]   0.7/5  ( 14.0%)  WR 43%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   82.4/100  (+27.4 pts vs mínimo 55)
   Pior critério: Hist 0.7/5  (14% do máximo)
   → APROVADO  —  Score 82.4/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 86.3 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          70%  "Pavio 49% (wick 24.7), corpo 37% (pin 7.0) -> 31.7/45 pts."
   [C] Contexto          78%  "Sessao London+NY overlap (15.0), WR 30d 43% em 14T (0.7) -> 15.7/20 pts."
-------------------------------------------------------------------
  Ciclo #2: 1 aprovado(s) / 1 analisado(s)

[18:27:02] ciclo #3  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 18:15:00  (verde)
  │     OHLC : O=1.35039  H=1.35099  L=1.35029  C=1.35050
  │     range=7.0 pips   corpo=16% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 70%  (min 30%)   [bot reportou 70%]
  │     [OK ] RSI(9)    : 83.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35050  SL=1.35149 (9.9 pips)  TP=1.34902 (14.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[18:27:03][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35050  SL:1.35149  TP:1.34902  pavio:70%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  32.7/35  ( 93.4%)  RSI 83.2
   Wick     [##############]    25/25  (100.0%)  pavio 70%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 16% range  [bom]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   85.7/100  (+30.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          93%  "RSI(9) 83.2 -> 32.7/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 70% (wick 25.0), corpo 16% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 22% em 9T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #3: 0 aprovado(s) / 1 analisado(s)

[18:27:24] ciclo #4  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 18:15:00  (verde)
  │     OHLC : O=0.71579  H=0.71629  L=0.71576  C=0.71605
  │     range=5.3 pips   corpo=49% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 45%  (min 30%)   [bot reportou 45%]
  │     [OK ] RSI(9)    : 83.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71605  SL=0.71679 (7.4 pips)  TP=0.71494 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[18:27:24][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71605  SL:0.71679  TP:0.71494  pavio:45%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.4/35  ( 95.4%)  RSI 83.8
   Wick     [#############-]  22.6/25  ( 90.4%)  pavio 45%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 49% range  [aceitável]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.5/100  (+24.5 pts vs mínimo 55)
   Pior critério: Hist 1.5/5  (30% do máximo)
   → APROVADO  —  Score 79.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          95%  "RSI(9) 83.8 -> 33.4/35 pts. Gate: 70."
   [R] Rejeicao          66%  "Pavio 45% (wick 22.6), corpo 49% (pin 7.0) -> 29.6/45 pts."
   [C] Contexto          82%  "Sessao London+NY overlap (15.0), WR 30d 46% em 13T (1.5) -> 16.5/20 pts."
-------------------------------------------------------------------
  Ciclo #4: 1 aprovado(s) / 1 analisado(s)

[18:27:46] ciclo #5  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 18:15:00  (vermelha)
  │     OHLC : O=0.78396  H=0.78404  L=0.78330  C=0.78362
  │     range=7.4 pips   corpo=46% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 17.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=15h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78362  SL=0.78280 (8.2 pips)  TP=0.78485 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[18:27:46][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78362  SL:0.78280  TP:0.78485  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  32.3/35  ( 92.3%)  RSI 17.1
   Wick     [############--]  21.6/25  ( 86.4%)  pavio 43%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 46% range  [aceitável]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.9/100  (+20.9 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          92%  "RSI(9) 17.1 -> 32.3/35 pts. Gate: 30."
   [R] Rejeicao          64%  "Pavio 43% (wick 21.6), corpo 46% (pin 7.0) -> 28.6/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 25% em 4T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 analisado(s)

[18:56:37] ciclo #6  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 18:45:00  (verde)
  │     OHLC : O=0.86727  H=0.86750  L=0.86722  C=0.86733
  │     range=2.8 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 61%  (min 30%)   [bot reportou 61%]
  │     [OK ] RSI(9)    : 86.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=15h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86733  SL=0.86800 (6.7 pips)  TP=0.86633 (10.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[18:56:37][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP SELL  @0.86733  SL:0.86800  TP:0.86633  pavio:61%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 86.4
   Wick     [##############]    25/25  (100.0%)  pavio 61%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 21% range  [bom]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (8T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   90.5/100  (+35.5 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 90.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 86.4 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 61% (wick 25.0), corpo 21% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          88%  "Sessao London+NY overlap (15.0), WR 30d 50% em 8T (2.5) -> 17.5/20 pts."
-------------------------------------------------------------------
  Ciclo #6: 1 aprovado(s) / 1 analisado(s)

[18:56:59] ciclo #7  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 18:45:00  (vermelha)
  │     OHLC : O=215.14200  H=215.17200  L=215.11100  C=215.13700
  │     range=6.1 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 28.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=15h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.13700  SL=215.06100 (7.6 pips)  TP=215.25100 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[18:56:59][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY BUY  @215.13700  SL:215.06100  TP:215.25100  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  17.2/35  ( 49.1%)  RSI 28.4
   Wick     [############--]  21.3/25  ( 85.2%)  pavio 43%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 30%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.5/100  (+18.5 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 73.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          49%  "RSI(9) 28.4 -> 17.2/35 pts. Gate: 30."
   [R] Rejeicao          92%  "Pavio 43% (wick 21.3), corpo 8% (pin 20.0) -> 41.3/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 30% em 10T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #7: 1 aprovado(s) / 1 analisado(s)

[19:11:30] ciclo #8  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 19:00:00  (vermelha)
  │     OHLC : O=215.13700  H=215.14100  L=215.05800  C=215.08300
  │     range=8.3 pips   corpo=65% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 30%  (min 30%)   [bot reportou 30%]
  │     [OK ] RSI(9)    : 15.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=16h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.08300  SL=215.00800 (7.5 pips)  TP=215.19550 (11.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[19:11:30][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY BUY  @215.08300  SL:215.00800  TP:215.19550  pavio:30%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  33.8/35  ( 96.6%)  RSI 15.9
   Wick     [########------]  15.1/25  ( 60.4%)  pavio 30%
   PinBar   [#-------------]   2.1/20  ( 10.5%)  corpo 65% range  [suja]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 27%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   66.0/100  (+11.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 66.0/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          97%  "RSI(9) 15.9 -> 33.8/35 pts. Gate: 30."
   [R] Rejeicao          38%  "Pavio 30% (wick 15.1), corpo 65% (pin 2.1) -> 17.2/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 27% em 11T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #8: 1 aprovado(s) / 1 analisado(s)

[19:41:38] ciclo #9  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 19:30:00  (vermelha)
  │     OHLC : O=1.34911  H=1.34935  L=1.34879  C=1.34909
  │     range=5.6 pips   corpo=4% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 22.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=16h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34909  SL=1.34829 (8.0 pips)  TP=1.35029 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[19:41:38][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34909  SL:1.34829  TP:1.35029  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  25.5/35  ( 72.9%)  RSI 22.1
   Wick     [##############]    25/25  (100.0%)  pavio 54%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 4% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   85.5/100  (+30.5 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          73%  "RSI(9) 22.1 -> 25.5/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 54% (wick 25.0), corpo 4% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 22% em 9T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #9: 0 aprovado(s) / 1 analisado(s)

[19:41:59] ciclo #10  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 19:30:00  (vermelha)
  │     OHLC : O=1.36924  H=1.36936  L=1.36899  C=1.36916
  │     range=3.7 pips   corpo=22% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 79.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=16h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36916  SL=1.36986 (7.0 pips)  TP=1.36811 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[19:42:00][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD SELL  @1.36916  SL:1.36986  TP:1.36811  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.2/35  ( 80.6%)  RSI 79.9
   Wick     [#########-----]  16.2/25  ( 64.8%)  pavio 32%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 22% range  [bom]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [##############]     5/5  (100.0%)  WR 70%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   77.4/100  (+22.4 pts vs mínimo 55)
   Pior critério: Wick 16.2/25  (65% do máximo)
   → APROVADO  —  Score 77.4/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          81%  "RSI(9) 79.9 -> 28.2/35 pts. Gate: 70."
   [R] Rejeicao          65%  "Pavio 32% (wick 16.2), corpo 22% (pin 13.0) -> 29.2/45 pts."
   [C] Contexto         100%  "Sessao London+NY overlap (15.0), WR 30d 70% em 10T (5.0) -> 20.0/20 pts."
-------------------------------------------------------------------
  Ciclo #10: 1 aprovado(s) / 1 analisado(s)

[19:56:34] ciclo #11  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 19:45:00  (verde)
  │     OHLC : O=1.34909  H=1.34924  L=1.34875  C=1.34915
  │     range=4.9 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 69%  (min 30%)   [bot reportou 69%]
  │     [OK ] RSI(9)    : 18.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=16h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34915  SL=1.34825 (9.0 pips)  TP=1.35050 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[19:56:35][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34915  SL:1.34825  TP:1.35050  pavio:69%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  30.0/35  ( 85.7%)  RSI 18.7
   Wick     [##############]    25/25  (100.0%)  pavio 69%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   90.0/100  (+35.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          86%  "RSI(9) 18.7 -> 30.0/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 69% (wick 25.0), corpo 12% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          75%  "Sessao London+NY overlap (15.0), WR 30d 22% em 9T (0.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #11: 0 aprovado(s) / 1 analisado(s)

[20:06:43] ciclo #12  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 19:45:00  (verde)
  │     OHLC : O=215.09800  H=215.14800  L=215.06200  C=215.13200
  │     range=8.6 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 42%  (min 30%)   [bot reportou 42%]
  │     [OK ] RSI(9)    : 15.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.13200  SL=215.01200 (12.0 pips)  TP=215.31200 (18.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:06:43][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY BUY  @215.13200  SL:215.01200  TP:215.31200  pavio:42%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  34.1/35  ( 97.4%)  RSI 15.6
   Wick     [############--]  20.9/25  ( 83.6%)  pavio 42%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 40% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.0/100  (+17.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 72.0/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          97%  "RSI(9) 15.6 -> 34.1/35 pts. Gate: 30."
   [R] Rejeicao          62%  "Pavio 42% (wick 20.9), corpo 40% (pin 7.0) -> 27.9/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 25% em 12T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #12: 1 aprovado(s) / 1 analisado(s)

[20:26:37] ciclo #13  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 20:15:00  (vermelha)
  │     OHLC : O=1.16841  H=1.16879  L=1.16775  C=1.16827
  │     range=10.4 pips   corpo=13% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 21.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16827  SL=1.16725 (10.2 pips)  TP=1.16980 (15.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:26:37][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.16827  SL:1.16725  TP:1.16980  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  25.9/35  ( 74.0%)  RSI 21.8
   Wick     [##############]  25.0/25  (100.0%)  pavio 50%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 14% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   82.6/100  (+27.6 pts vs mínimo 55)
   Pior critério: Hist 1.7/5  (34% do máximo)
   → APROVADO  —  Score 82.6/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          74%  "RSI(9) 21.8 -> 25.9/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 50% (wick 25.0), corpo 13% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          58%  "Sessao New York (10.0), WR 30d 47% em 15T (1.7) -> 11.7/20 pts."
-------------------------------------------------------------------
  Ciclo #13: 1 aprovado(s) / 1 analisado(s)

[20:27:03] ciclo #14  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 20:15:00  (verde)
  │     OHLC : O=1.34647  H=1.34698  L=1.34585  C=1.34659
  │     range=11.3 pips   corpo=11% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 55%  (min 30%)   [bot reportou 55%]
  │     [OK ] RSI(9)    : 13.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34659  SL=1.34535 (12.4 pips)  TP=1.34845 (18.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:27:04][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34659  SL:1.34535  TP:1.34845  pavio:55%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 13.2
   Wick     [##############]    25/25  (100.0%)  pavio 55%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 11% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   90.0/100  (+35.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 13.2 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 55% (wick 25.0), corpo 11% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #14: 0 aprovado(s) / 1 analisado(s)

[20:27:21] ciclo #15  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 20:15:00  (vermelha)
  │     OHLC : O=0.71335  H=0.71377  L=0.71261  C=0.71332
  │     range=11.6 pips   corpo=3% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 61%  (min 30%)   [bot reportou 61%]
  │     [OK ] RSI(9)    : 18.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71332  SL=0.71211 (12.1 pips)  TP=0.71513 (18.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:27:21][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD BUY  @0.71332  SL:0.71211  TP:0.71513  pavio:61%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  30.7/35  ( 87.7%)  RSI 18.3
   Wick     [##############]    25/25  (100.0%)  pavio 61%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 3% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.2/100  (+33.2 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 88.2/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          88%  "RSI(9) 18.3 -> 30.7/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 61% (wick 25.0), corpo 3% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          62%  "Sessao New York (10.0), WR 30d 50% em 14T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #15: 1 aprovado(s) / 1 analisado(s)

[20:27:47] ciclo #16  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 20:15:00  (vermelha)
  │     OHLC : O=1.37077  H=1.37116  L=1.37024  C=1.37034
  │     range=9.2 pips   corpo=47% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 42%  (min 30%)   [bot reportou 42%]
  │     [OK ] RSI(9)    : 75.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.37034  SL=1.37166 (13.2 pips)  TP=1.36836 (19.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:27:48][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD SELL  @1.37034  SL:1.37166  TP:1.36836  pavio:42%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  22.0/35  ( 62.9%)  RSI 75.2
   Wick     [############--]  21.2/25  ( 84.8%)  pavio 42%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 47% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [##############]     5/5  (100.0%)  WR 70%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   65.2/100  (+10.2 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → APROVADO  —  Score 65.2/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          63%  "RSI(9) 75.2 -> 22.0/35 pts. Gate: 70."
   [R] Rejeicao          63%  "Pavio 42% (wick 21.2), corpo 47% (pin 7.0) -> 28.2/45 pts."
   [C] Contexto          75%  "Sessao New York (10.0), WR 30d 70% em 10T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #16: 1 aprovado(s) / 1 analisado(s)

[20:28:09] ciclo #17  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 20:15:00  (verde)
  │     OHLC : O=0.78630  H=0.78683  L=0.78597  C=0.78635
  │     range=8.6 pips   corpo=6% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 56%  (min 30%)   [bot reportou 56%]
  │     [OK ] RSI(9)    : 85.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78635  SL=0.78733 (9.8 pips)  TP=0.78488 (14.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:28:09][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78635  SL:0.78733  TP:0.78488  pavio:56%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 85.0
   Wick     [##############]    25/25  (100.0%)  pavio 56%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 6% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   90.0/100  (+35.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 85.0 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 56% (wick 25.0), corpo 6% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #17: 0 aprovado(s) / 1 analisado(s)

[20:28:30] ciclo #18  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 20:15:00  (verde)
  │     OHLC : O=0.58570  H=0.58605  L=0.58518  C=0.58573
  │     range=8.7 pips   corpo=3% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 60%  (min 30%)   [bot reportou 60%]
  │     [OK ] RSI(9)    : 19.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=17h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58573  SL=0.58468 (10.5 pips)  TP=0.58730 (15.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[20:28:31][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58573  SL:0.58468  TP:0.58730  pavio:60%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.3/35  ( 83.7%)  RSI 19.3
   Wick     [##############]    25/25  (100.0%)  pavio 60%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 3% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [##############]     5/5  (100.0%)  WR 64%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   89.3/100  (+34.3 pts vs mínimo 55)
   Pior critério: Sessao 10.0/15  (67% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          84%  "RSI(9) 19.3 -> 29.3/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 60% (wick 25.0), corpo 3% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          75%  "Sessao New York (10.0), WR 30d 64% em 11T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #18: 0 aprovado(s) / 1 analisado(s)

[23:26:34] ciclo #19  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 23:15:00  (verde)
  │     OHLC : O=1.16819  H=1.16849  L=1.16799  C=1.16830
  │     range=5.0 pips   corpo=22% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 40%  (min 30%)   [bot reportou 40%]
  │     [OK ] RSI(9)    : 22.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=20h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16830  SL=1.16749 (8.1 pips)  TP=1.16951 (12.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[23:26:34][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.16830  SL:1.16749  TP:1.16951  pavio:40%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  24.8/35  ( 70.9%)  RSI 22.6
   Wick     [###########---]  20.0/25  ( 80.0%)  pavio 40%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 22% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [###-----------]   0.9/5  ( 18.0%)  WR 44%  (16T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.7/100  (+13.7 pts vs mínimo 55)
   Pior critério: Hist 0.9/5  (18% do máximo)
   → APROVADO  —  Score 68.7/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          71%  "RSI(9) 22.6 -> 24.8/35 pts. Gate: 30."
   [R] Rejeicao          73%  "Pavio 40% (wick 20.0), corpo 22% (pin 13.0) -> 33.0/45 pts."
   [C] Contexto          55%  "Sessao New York (10.0), WR 30d 44% em 16T (0.9) -> 10.9/20 pts."
-------------------------------------------------------------------
  Ciclo #19: 1 aprovado(s) / 1 analisado(s)

[23:26:56] ciclo #20  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 23:15:00  (verde)
  │     OHLC : O=1.34625  H=1.34658  L=1.34610  C=1.34640
  │     range=4.8 pips   corpo=31% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 22.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=20h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34640  SL=1.34560 (8.0 pips)  TP=1.34760 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[23:26:56][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34640  SL:1.34560  TP:1.34760  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  25.0/35  ( 71.4%)  RSI 22.5
   Wick     [#########-----]  15.6/25  ( 62.4%)  pavio 31%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 31% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   57.6/100  (+2.6 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          71%  "RSI(9) 22.5 -> 25.0/35 pts. Gate: 30."
   [R] Rejeicao          50%  "Pavio 31% (wick 15.6), corpo 31% (pin 7.0) -> 22.6/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #20: 0 aprovado(s) / 1 analisado(s)

[23:27:17] ciclo #21  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 23:15:00  (vermelha)
  │     OHLC : O=0.78636  H=0.78646  L=0.78626  C=0.78633
  │     range=2.0 pips   corpo=15% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 86.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=20h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78633  SL=0.78696 (6.3 pips)  TP=0.78538 (9.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[23:27:17][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78633  SL:0.78696  TP:0.78538  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 86.7
   Wick     [##############]    25/25  (100.0%)  pavio 50%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 15% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   90.0/100  (+35.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 86.7 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 50% (wick 25.0), corpo 15% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #21: 0 aprovado(s) / 1 analisado(s)

[23:41:27] ciclo #22  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 23:30:00  (vermelha)
  │     OHLC : O=0.58532  H=0.58534  L=0.58519  C=0.58531
  │     range=1.5 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 80%  (min 30%)   [bot reportou 80%]
  │     [OK ] RSI(9)    : 26.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=20h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58531  SL=0.58469 (6.2 pips)  TP=0.58624 (9.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[23:41:27][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD BUY  @0.58531  SL:0.58469  TP:0.58624  pavio:80%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  20.3/35  ( 58.0%)  RSI 26.1
   Wick     [##############]    25/25  (100.0%)  pavio 80%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [##############]     5/5  (100.0%)  WR 64%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   80.3/100  (+25.3 pts vs mínimo 55)
   Pior critério: RSI 20.3/35  (58% do máximo)
   → APROVADO  —  Score 80.3/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          58%  "RSI(9) 26.1 -> 20.3/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 80% (wick 25.0), corpo 7% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          75%  "Sessao New York (10.0), WR 30d 64% em 11T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #22: 1 aprovado(s) / 1 analisado(s)

[23:56:23] ciclo #23  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 23:45:00  (verde)
  │     OHLC : O=1.34648  H=1.34665  L=1.34619  C=1.34661
  │     range=4.6 pips   corpo=28% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 63%  (min 30%)   [bot reportou 63%]
  │     [OK ] RSI(9)    : 26.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=20h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34661  SL=1.34569 (9.2 pips)  TP=1.34799 (13.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[23:56:24][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34661  SL:1.34569  TP:1.34799  pavio:63%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.8/35  ( 56.6%)  RSI 26.4
   Wick     [##############]    25/25  (100.0%)  pavio 63%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 28% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   67.8/100  (+12.8 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          57%  "RSI(9) 26.4 -> 19.8/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 63% (wick 25.0), corpo 28% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #23: 0 aprovado(s) / 1 analisado(s)

[23:59:13] ciclo #24  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 23:45:00  (vermelha)
  │     OHLC : O=0.78628  H=0.78646  L=0.78619  C=0.78619
  │     range=2.7 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 67%  (min 30%)   [bot reportou 67%]
  │     [OK ] RSI(9)    : 75.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=20h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78619  SL=0.78696 (7.7 pips)  TP=0.78504 (11.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[23:59:13][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78619  SL:0.78696  TP:0.78504  pavio:67%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  21.7/35  ( 62.0%)  RSI 75.0
   Wick     [##############]    25/25  (100.0%)  pavio 67%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 33% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.7/100  (+8.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          62%  "RSI(9) 75.0 -> 21.7/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 67% (wick 25.0), corpo 33% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #24: 0 aprovado(s) / 1 analisado(s)

[00:11:23] ciclo #25  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 00:00:00  (vermelha)
  │     OHLC : O=0.58522  H=0.58609  L=0.58416  C=0.58490
  │     range=19.3 pips   corpo=17% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 38%  (min 30%)   [bot reportou 38%]
  │     [OK ] RSI(9)    : 30.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=21h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58490  SL=0.58366 (12.4 pips)  TP=0.58676 (18.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[00:11:23][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD BUY  @0.58490  SL:0.58366  TP:0.58676  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.0/35  ( 42.9%)  RSI 30.0
   Wick     [###########---]  19.2/25  ( 76.8%)  pavio 38%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 17% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [#############-]   4.6/5  ( 92.0%)  WR 58%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.8/100  (+6.8 pts vs mínimo 55)
   Pior critério: RSI 15.0/35  (43% do máximo)
   → APROVADO  —  Score 61.8/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          43%  "RSI(9) 30.0 -> 15.0/35 pts. Gate: 30."
   [R] Rejeicao          72%  "Pavio 38% (wick 19.2), corpo 17% (pin 13.0) -> 32.2/45 pts."
   [C] Contexto          73%  "Sessao New York (10.0), WR 30d 58% em 12T (4.6) -> 14.6/20 pts."
-------------------------------------------------------------------
  Ciclo #25: 1 aprovado(s) / 1 analisado(s)

[00:41:36] ciclo #26  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 00:30:00  (verde)
  │     OHLC : O=214.95000  H=215.04700  L=214.90500  C=214.95300
  │     range=14.2 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 27.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=21h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=214.95300  SL=214.85500 (9.8 pips)  TP=215.10000 (14.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[00:41:37][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY BUY  @214.95300  SL:214.85500  TP:215.10000  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  18.1/35  ( 51.7%)  RSI 27.6
   Wick     [#########-----]  15.8/25  ( 63.2%)  pavio 32%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.9/100  (+8.9 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 63.9/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          52%  "RSI(9) 27.6 -> 18.1/35 pts. Gate: 30."
   [R] Rejeicao          80%  "Pavio 32% (wick 15.8), corpo 2% (pin 20.0) -> 35.8/45 pts."
   [C] Contexto          50%  "Sessao New York (10.0), WR 30d 25% em 12T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #26: 1 aprovado(s) / 1 analisado(s)

[02:26:31] ciclo #27  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 02:15:00  (vermelha)
  │     OHLC : O=0.78643  H=0.78652  L=0.78633  C=0.78634
  │     range=1.9 pips   corpo=47% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 47%  (min 30%)   [bot reportou 47%]
  │     [OK ] RSI(9)    : 78.6    (cond >= 70)
  │     [-- ] Sessao UTC : h=23h -> Fora de sessão  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78634  SL=0.78702 (6.8 pips)  TP=0.78532 (10.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[02:26:31][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78634  SL:0.78702  TP:0.78532  pavio:47%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  26.4/35  ( 75.4%)  RSI 78.6
   Wick     [#############-]  23.7/25  ( 94.8%)  pavio 47%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 47% range  [aceitável]
   Sessao   [--------------]   0.0/15  (  0.0%)  Fora de sessão
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   57.1/100  (+2.1 pts vs mínimo 55)
   Pior critério: Sessao 0.0/15  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          75%  "RSI(9) 78.6 -> 26.4/35 pts. Gate: 70."
   [R] Rejeicao          68%  "Pavio 47% (wick 23.7), corpo 47% (pin 7.0) -> 30.7/45 pts."
   [C] Contexto           0%  "Sessao Fora de sessão (0.0), WR 30d 25% em 4T (0.0) -> 0.0/20 pts."
-------------------------------------------------------------------
  Ciclo #27: 0 aprovado(s) / 1 analisado(s)