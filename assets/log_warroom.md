===================================================================
  WAR ROOM v6.1.2  --  ANALISE TECNICA AGENTICA
-------------------------------------------------------------------
  Score minimo : 55/100   |   Correlacao: ATIVA   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)   [Slope/ColorReversal desativados nas Fases 1+2]
  Criterios    : RSI(35) Wick(25) PinBar(20) Sessao(15) Hist(5)  [alpha: RSI]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE (gatilhos+condicoes) -> [FASE 2] signal_analysis (score)
===================================================================
[04:08:21][WAR_ROOM]   war_room_started: War Room v6.1.2 iniciada | Score mínimo: 55/100 | 5 critérios (RSI alpha) | estratégia: Zona+Wick+RSI | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[05:41:31] ciclo #1  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 05:30:00  (verde)
  │     OHLC : O=1.17042  H=1.17064  L=1.17029  C=1.17045
  │     range=3.5 pips   corpo=9% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 37%  (min 30%)   [bot reportou 37%]
  │     [OK ] RSI(9)    : 29.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17045  SL=1.16979 (6.6 pips)  TP=1.17144 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:41:31][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.17045  SL:1.16979  TP:1.17144  pavio:37%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.1/35  ( 43.1%)  RSI 29.9
   Wick     [##########----]  18.6/25  ( 74.4%)  pavio 37%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 9% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 36%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   56.7/100  (+1.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 56.7/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          43%  "RSI(9) 29.9 -> 15.1/35 pts. Gate: 30."
   [R] Rejeicao          86%  "Pavio 37% (wick 18.6), corpo 9% (pin 20.0) -> 38.6/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 36% em 11T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #1: 1 aprovado(s) / 1 analisado(s)

[05:41:52] ciclo #2  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 05:30:00  (verde)
  │     OHLC : O=0.58981  H=0.59001  L=0.58969  C=0.58989
  │     range=3.2 pips   corpo=25% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 37%  (min 30%)   [bot reportou 37%]
  │     [OK ] RSI(9)    : 24.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58989  SL=0.58919 (7.0 pips)  TP=0.59094 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:41:52][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD BUY  @0.58989  SL:0.58919  TP:0.59094  pavio:37%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  22.8/35  ( 65.1%)  RSI 24.1
   Wick     [##########----]  18.7/25  ( 74.8%)  pavio 37%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 25% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 62%  (8T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   62.5/100  (+7.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 62.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          65%  "RSI(9) 24.1 -> 22.8/35 pts. Gate: 30."
   [R] Rejeicao          70%  "Pavio 37% (wick 18.7), corpo 25% (pin 13.0) -> 31.7/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 62% em 8T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #2: 1 aprovado(s) / 1 analisado(s)

[06:11:43] ciclo #3  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 06:00:00  (vermelha)
  │     OHLC : O=1.16970  H=1.17016  L=1.16939  C=1.16969
  │     range=7.7 pips   corpo=1% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 15.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16969  SL=1.16889 (8.0 pips)  TP=1.17089 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:11:43][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.16969  SL:1.16889  TP:1.17089  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  34.2/35  ( 97.7%)  RSI 15.6
   Wick     [###########---]  19.5/25  ( 78.0%)  pavio 39%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 1% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 33%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   76.7/100  (+21.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 76.7/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          98%  "RSI(9) 15.6 -> 34.2/35 pts. Gate: 30."
   [R] Rejeicao          88%  "Pavio 39% (wick 19.5), corpo 1% (pin 20.0) -> 39.5/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 33% em 12T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #3: 1 aprovado(s) / 1 analisado(s)

[06:12:04] ciclo #4  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 06:00:00  (verde)
  │     OHLC : O=1.36726  H=1.36744  L=1.36703  C=1.36730
  │     range=4.1 pips   corpo=10% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 34%  (min 30%)   [bot reportou 34%]
  │     [OK ] RSI(9)    : 85.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36730  SL=1.36794 (6.4 pips)  TP=1.36634 (9.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:12:05][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD SELL  @1.36730  SL:1.36794  TP:1.36634  pavio:34%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 85.2
   Wick     [##########----]  17.1/25  ( 68.4%)  pavio 34%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 10% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [############--]   4.3/5  ( 86.0%)  WR 57%  (7T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.4/100  (+24.4 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 79.4/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 85.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          82%  "Pavio 34% (wick 17.1), corpo 10% (pin 20.0) -> 37.1/45 pts."
   [C] Contexto          36%  "Sessao Ásia (3.0), WR 30d 57% em 7T (4.3) -> 7.3/20 pts."
-------------------------------------------------------------------
  Ciclo #4: 1 aprovado(s) / 1 analisado(s)

[06:26:38] ciclo #5  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 06:15:00  (verde)
  │     OHLC : O=1.34843  H=1.34861  L=1.34827  C=1.34854
  │     range=3.4 pips   corpo=32% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 47%  (min 30%)   [bot reportou 47%]
  │     [OK ] RSI(9)    : 15.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34854  SL=1.34777 (7.7 pips)  TP=1.34970 (11.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:26:39][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34854  SL:1.34777  TP:1.34970  pavio:47%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  34.3/35  ( 98.0%)  RSI 15.5
   Wick     [#############-]  23.5/25  ( 94.0%)  pavio 47%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 32% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   67.8/100  (+12.8 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          98%  "RSI(9) 15.5 -> 34.3/35 pts. Gate: 30."
   [R] Rejeicao          68%  "Pavio 47% (wick 23.5), corpo 32% (pin 7.0) -> 30.5/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 analisado(s)

[06:27:00] ciclo #6  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 06:15:00  (vermelha)
  │     OHLC : O=0.71440  H=0.71449  L=0.71380  C=0.71411
  │     range=6.9 pips   corpo=42% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 45%  (min 30%)   [bot reportou 45%]
  │     [OK ] RSI(9)    : 16.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71411  SL=0.71330 (8.1 pips)  TP=0.71532 (12.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:27:01][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD BUY  @0.71411  SL:0.71330  TP:0.71532  pavio:45%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.7/35  ( 96.3%)  RSI 16.0
   Wick     [#############-]  22.5/25  ( 90.0%)  pavio 45%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 42% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [####----------]   1.4/5  ( 28.0%)  WR 46%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   67.6/100  (+12.6 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 67.6/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          96%  "RSI(9) 16.0 -> 33.7/35 pts. Gate: 30."
   [R] Rejeicao          66%  "Pavio 45% (wick 22.5), corpo 42% (pin 7.0) -> 29.5/45 pts."
   [C] Contexto          22%  "Sessao Ásia (3.0), WR 30d 45% em 11T (1.4) -> 4.4/20 pts."
-------------------------------------------------------------------
  Ciclo #6: 1 aprovado(s) / 1 analisado(s)

[06:27:22] ciclo #7  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 06:15:00  (verde)
  │     OHLC : O=0.78560  H=0.78565  L=0.78551  C=0.78560
  │     range=1.4 pips   corpo=0% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 92.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78560  SL=0.78615 (5.5 pips)  TP=0.78478 (8.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:27:22][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78560  SL:0.78615  TP:0.78478  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 92.5
   Wick     [##########----]  17.9/25  ( 71.6%)  pavio 36%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 0% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.9/100  (+20.9 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 92.5 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 36% (wick 17.9), corpo 0% (pin 20.0) -> 37.9/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #7: 0 aprovado(s) / 1 analisado(s)

[06:27:43] ciclo #8  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 06:15:00  (vermelha)
  │     OHLC : O=0.58872  H=0.58876  L=0.58826  C=0.58847
  │     range=5.0 pips   corpo=50% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 42%  (min 30%)   [bot reportou 42%]
  │     [OK ] RSI(9)    : 10.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58847  SL=0.58776 (7.1 pips)  TP=0.58954 (10.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:27:43][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58847  SL:0.58776  TP:0.58954  pavio:42%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 10.9
   Wick     [############--]  21.0/25  ( 84.0%)  pavio 42%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 50% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [###########---]   3.9/5  ( 78.0%)  WR 56%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.9/100  (+14.9 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 10.9 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          62%  "Pavio 42% (wick 21.0), corpo 50% (pin 7.0) -> 28.0/45 pts."
   [C] Contexto          34%  "Sessao Ásia (3.0), WR 30d 56% em 9T (3.9) -> 6.9/20 pts."
-------------------------------------------------------------------
  Ciclo #8: 0 aprovado(s) / 1 analisado(s)

[06:28:05] ciclo #9  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 06:15:00  (vermelha)
  │     OHLC : O=0.86740  H=0.86747  L=0.86732  C=0.86735
  │     range=1.5 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 47%  (min 30%)   [bot reportou 47%]
  │     [OK ] RSI(9)    : 70.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86735  SL=0.86797 (6.2 pips)  TP=0.86642 (9.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:28:05][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✗ EURGBP SELL  @0.86735  SL:0.86797  TP:0.86642  pavio:47%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  16.1/35  ( 46.0%)  RSI 70.8
   Wick     [#############-]  23.3/25  ( 93.2%)  pavio 47%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 33% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   51.9/100  (-3.1 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Score 51.9 < 55 | fraco: Sessão 3.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          46%  "RSI(9) 70.8 -> 16.1/35 pts. Gate: 70."
   [R] Rejeicao          67%  "Pavio 47% (wick 23.3), corpo 33% (pin 7.0) -> 30.3/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #9: 0 aprovado(s) / 1 analisado(s)

[06:56:26] ciclo #10  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 06:45:00  (verde)
  │     OHLC : O=0.78565  H=0.78578  L=0.78558  C=0.78569
  │     range=2.0 pips   corpo=20% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 45%  (min 30%)   [bot reportou 45%]
  │     [OK ] RSI(9)    : 100.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78569  SL=0.78628 (5.9 pips)  TP=0.78480 (8.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:56:27][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78569  SL:0.78628  TP:0.78480  pavio:45%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 100.0
   Wick     [#############-]  22.5/25  ( 90.0%)  pavio 45%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 20% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.5/100  (+18.5 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 100.0 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          79%  "Pavio 45% (wick 22.5), corpo 20% (pin 13.0) -> 35.5/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #10: 0 aprovado(s) / 1 analisado(s)

[07:11:40] ciclo #11  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 07:00:00  (verde)
  │     OHLC : O=1.34852  H=1.34865  L=1.34830  C=1.34859
  │     range=3.5 pips   corpo=20% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 63%  (min 30%)   [bot reportou 63%]
  │     [OK ] RSI(9)    : 20.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34859  SL=1.34780 (7.9 pips)  TP=1.34977 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:11:40][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34859  SL:1.34780  TP:1.34977  pavio:63%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.2/35  ( 80.6%)  RSI 20.1
   Wick     [##############]    25/25  (100.0%)  pavio 63%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 20% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.2/100  (+14.2 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          81%  "RSI(9) 20.1 -> 28.2/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 63% (wick 25.0), corpo 20% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #11: 0 aprovado(s) / 1 analisado(s)

[07:12:01] ciclo #12  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 07:00:00  (vermelha)
  │     OHLC : O=0.78569  H=0.78574  L=0.78559  C=0.78562
  │     range=1.5 pips   corpo=47% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 94.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78562  SL=0.78624 (6.2 pips)  TP=0.78469 (9.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:12:02][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78562  SL:0.78624  TP:0.78469  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 94.2
   Wick     [#########-----]  16.7/25  ( 66.8%)  pavio 33%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 47% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.7/100  (+6.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 94.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          53%  "Pavio 33% (wick 16.7), corpo 47% (pin 7.0) -> 23.7/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #12: 0 aprovado(s) / 1 analisado(s)

[07:12:23] ciclo #13  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 07:00:00  (verde)
  │     OHLC : O=0.58788  H=0.58811  L=0.58758  C=0.58809
  │     range=5.3 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 57%  (min 30%)   [bot reportou 57%]
  │     [OK ] RSI(9)    : 16.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58809  SL=0.58708 (10.1 pips)  TP=0.58960 (15.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:12:23][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58809  SL:0.58708  TP:0.58960  pavio:57%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.5/35  ( 95.7%)  RSI 16.1
   Wick     [##############]    25/25  (100.0%)  pavio 57%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 40% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [###########---]   3.9/5  ( 78.0%)  WR 56%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.4/100  (+17.4 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          96%  "RSI(9) 16.1 -> 33.5/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 57% (wick 25.0), corpo 40% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          34%  "Sessao Ásia (3.0), WR 30d 56% em 9T (3.9) -> 6.9/20 pts."
-------------------------------------------------------------------
  Ciclo #13: 0 aprovado(s) / 1 analisado(s)

[08:26:32] ciclo #14  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 08:15:00  (vermelha)
  │     OHLC : O=215.26000  H=215.28400  L=215.23500  C=215.25700
  │     range=4.9 pips   corpo=6% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 70.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.25700  SL=215.33400 (7.7 pips)  TP=215.14150 (11.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[08:26:32][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY SELL  @215.25700  SL:215.33400  TP:215.14150  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.9/35  ( 45.4%)  RSI 70.7
   Wick     [##############]  24.5/25  ( 98.0%)  pavio 49%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 6% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 17%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.4/100  (+8.4 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 63.4/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 70.7 -> 15.9/35 pts. Gate: 70."
   [R] Rejeicao          99%  "Pavio 49% (wick 24.5), corpo 6% (pin 20.0) -> 44.5/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 17% em 6T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #14: 1 aprovado(s) / 1 analisado(s)

[08:47:21] ciclo #15  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 08:30:00  (verde)
  │     OHLC : O=0.71477  H=0.71505  L=0.71468  C=0.71490
  │     range=3.7 pips   corpo=35% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 41%  (min 30%)   [bot reportou 41%]
  │     [OK ] RSI(9)    : 86.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71490  SL=0.71555 (6.5 pips)  TP=0.71393 (9.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[08:47:21][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71490  SL:0.71555  TP:0.71393  pavio:41%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 86.2
   Wick     [###########---]  20.3/25  ( 81.2%)  pavio 41%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 35% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   67.8/100  (+12.8 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 67.8/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 86.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          61%  "Pavio 41% (wick 20.3), corpo 35% (pin 7.0) -> 27.3/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 12T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #15: 1 aprovado(s) / 1 analisado(s)

[09:11:35] ciclo #16  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 09:00:00  (verde)
  │     OHLC : O=0.78501  H=0.78522  L=0.78481  C=0.78513
  │     range=4.1 pips   corpo=29% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 14.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78513  SL=0.78431 (8.2 pips)  TP=0.78636 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:11:35][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78513  SL:0.78431  TP:0.78636  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 14.1
   Wick     [##############]  24.4/25  ( 97.6%)  pavio 49%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 29% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.4/100  (+20.4 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 14.1 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          83%  "Pavio 49% (wick 24.4), corpo 29% (pin 13.0) -> 37.4/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #16: 0 aprovado(s) / 1 analisado(s)

[09:11:56] ciclo #17  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 09:00:00  (vermelha)
  │     OHLC : O=0.58887  H=0.58907  L=0.58860  C=0.58867
  │     range=4.7 pips   corpo=43% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 77.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58867  SL=0.58957 (9.0 pips)  TP=0.58732 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:11:56][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD SELL  @0.58867  SL:0.58957  TP:0.58732  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  25.2/35  ( 72.0%)  RSI 77.6
   Wick     [############--]  21.3/25  ( 85.2%)  pavio 43%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 43% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [###########---]   3.9/5  ( 78.0%)  WR 56%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.4/100  (+5.4 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 60.4/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          72%  "RSI(9) 77.6 -> 25.2/35 pts. Gate: 70."
   [R] Rejeicao          63%  "Pavio 43% (wick 21.3), corpo 43% (pin 7.0) -> 28.3/45 pts."
   [C] Contexto          34%  "Sessao Ásia (3.0), WR 30d 56% em 9T (3.9) -> 6.9/20 pts."
-------------------------------------------------------------------
  Ciclo #17: 1 aprovado(s) / 1 analisado(s)

[09:12:18] ciclo #18  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 09:00:00  (verde)
  │     OHLC : O=0.86760  H=0.86787  L=0.86757  C=0.86763
  │     range=3.0 pips   corpo=10% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 80%  (min 30%)   [bot reportou 80%]
  │     [OK ] RSI(9)    : 82.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86763  SL=0.86837 (7.4 pips)  TP=0.86652 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:12:18][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP SELL  @0.86763  SL:0.86837  TP:0.86652  pavio:80%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  32.0/35  ( 91.4%)  RSI 82.8
   Wick     [##############]    25/25  (100.0%)  pavio 80%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 10% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   82.5/100  (+27.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 82.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 82.8 -> 32.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 80% (wick 25.0), corpo 10% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #18: 1 aprovado(s) / 1 analisado(s)

[09:26:33] ciclo #19  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 09:15:00  (verde)
  │     OHLC : O=0.71506  H=0.71536  L=0.71501  C=0.71514
  │     range=3.5 pips   corpo=23% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 63%  (min 30%)   [bot reportou 63%]
  │     [OK ] RSI(9)    : 75.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71514  SL=0.71586 (7.2 pips)  TP=0.71406 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:26:34][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71514  SL:0.71586  TP:0.71406  pavio:63%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  22.3/35  ( 63.7%)  RSI 75.4
   Wick     [##############]    25/25  (100.0%)  pavio 63%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 23% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   64.8/100  (+9.8 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          64%  "RSI(9) 75.4 -> 22.3/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 63% (wick 25.0), corpo 23% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          22%  "Sessao Ásia (3.0), WR 30d 46% em 13T (1.5) -> 4.5/20 pts."
-------------------------------------------------------------------
  Ciclo #19: 0 aprovado(s) / 1 analisado(s)

[09:56:38] ciclo #20  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 09:45:00  (vermelha)
  │     OHLC : O=0.78463  H=0.78467  L=0.78432  C=0.78456
  │     range=3.5 pips   corpo=20% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 69%  (min 30%)   [bot reportou 69%]
  │     [OK ] RSI(9)    : 9.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78456  SL=0.78382 (7.4 pips)  TP=0.78567 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:56:39][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78456  SL:0.78382  TP:0.78567  pavio:69%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 9.2
   Wick     [##############]    25/25  (100.0%)  pavio 69%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 20% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   76.0/100  (+21.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 9.2 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 69% (wick 25.0), corpo 20% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #20: 0 aprovado(s) / 1 analisado(s)

[09:57:00] ciclo #21  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 09:45:00  (vermelha)
  │     OHLC : O=215.41100  H=215.46400  L=215.37200  C=215.40000
  │     range=9.2 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 58%  (min 30%)   [bot reportou 58%]
  │     [OK ] RSI(9)    : 83.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.40000  SL=215.51400 (11.4 pips)  TP=215.22900 (17.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:57:00][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY SELL  @215.40000  SL:215.51400  TP:215.22900  pavio:58%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.3/35  ( 95.1%)  RSI 83.7
   Wick     [##############]    25/25  (100.0%)  pavio 58%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 14%  (7T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   81.3/100  (+26.3 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 81.3/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          95%  "RSI(9) 83.7 -> 33.3/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 58% (wick 25.0), corpo 12% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 14% em 7T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #21: 1 aprovado(s) / 1 analisado(s)

[10:11:32] ciclo #22  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 10:00:00  (verde)
  │     OHLC : O=0.78456  H=0.78473  L=0.78411  C=0.78466
  │     range=6.2 pips   corpo=16% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 73%  (min 30%)   [bot reportou 73%]
  │     [OK ] RSI(9)    : 17.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=07h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78466  SL=0.78361 (10.5 pips)  TP=0.78624 (15.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[10:11:32][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78466  SL:0.78361  TP:0.78624  pavio:73%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  32.2/35  ( 92.0%)  RSI 17.1
   Wick     [##############]    25/25  (100.0%)  pavio 73%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 16% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.2/100  (+18.2 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          92%  "RSI(9) 17.1 -> 32.2/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 73% (wick 25.0), corpo 16% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #22: 0 aprovado(s) / 1 analisado(s)

[10:11:54] ciclo #23  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 10:00:00  (verde)
  │     OHLC : O=215.40000  H=215.50500  L=215.38900  C=215.43500
  │     range=11.6 pips   corpo=30% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 60%  (min 30%)   [bot reportou 60%]
  │     [OK ] RSI(9)    : 84.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=07h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.43500  SL=215.55500 (12.0 pips)  TP=215.25500 (18.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[10:11:54][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✓ GBPJPY SELL  @215.43500  SL:215.55500  TP:215.25500  pavio:60%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  33.8/35  ( 96.6%)  RSI 84.1
   Wick     [##############]    25/25  (100.0%)  pavio 60%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 30% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 12%  (8T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.8/100  (+13.8 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 68.8/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          97%  "RSI(9) 84.1 -> 33.8/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 60% (wick 25.0), corpo 30% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 12% em 8T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #23: 1 aprovado(s) / 1 analisado(s)

[10:56:34] ciclo #24  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 10:45:00  (vermelha)
  │     OHLC : O=0.78484  H=0.78487  L=0.78436  C=0.78466
  │     range=5.1 pips   corpo=35% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 59%  (min 30%)   [bot reportou 59%]
  │     [OK ] RSI(9)    : 28.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=07h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78466  SL=0.78386 (8.0 pips)  TP=0.78586 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[10:56:34][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78466  SL:0.78386  TP:0.78586  pavio:59%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  17.3/35  ( 49.4%)  RSI 28.3
   Wick     [##############]    25/25  (100.0%)  pavio 59%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 35% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   52.3/100  (-2.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 52.3 < 55 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          49%  "RSI(9) 28.3 -> 17.3/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 59% (wick 25.0), corpo 35% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #24: 0 aprovado(s) / 1 analisado(s)

[11:26:25] ciclo #25  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 11:15:00  (vermelha)
  │     OHLC : O=1.36631  H=1.36645  L=1.36602  C=1.36617
  │     range=4.3 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 35%  (min 30%)   [bot reportou 35%]
  │     [OK ] RSI(9)    : 29.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36617  SL=1.36552 (6.5 pips)  TP=1.36714 (9.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:26:25][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD BUY  @1.36617  SL:1.36552  TP:1.36714  pavio:35%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.7/35  ( 44.9%)  RSI 29.5
   Wick     [##########----]  17.4/25  ( 69.6%)  pavio 35%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 33% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 62%  (8T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   55.1/100  (+0.1 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → APROVADO  —  Score 55.1/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 29.5 -> 15.7/35 pts. Gate: 30."
   [R] Rejeicao          54%  "Pavio 35% (wick 17.4), corpo 33% (pin 7.0) -> 24.4/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 62% em 8T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #25: 1 aprovado(s) / 1 analisado(s)

[11:26:52] ciclo #26  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 11:15:00  (vermelha)
  │     OHLC : O=0.78459  H=0.78470  L=0.78405  C=0.78428
  │     range=6.5 pips   corpo=48% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 35%  (min 30%)   [bot reportou 35%]
  │     [OK ] RSI(9)    : 22.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78428  SL=0.78355 (7.3 pips)  TP=0.78537 (10.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:26:52][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78428  SL:0.78355  TP:0.78537  pavio:35%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  25.4/35  ( 72.6%)  RSI 22.2
   Wick     [##########----]  17.7/25  ( 70.8%)  pavio 35%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 48% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.1/100  (+5.1 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          73%  "RSI(9) 22.2 -> 25.4/35 pts. Gate: 30."
   [R] Rejeicao          55%  "Pavio 35% (wick 17.7), corpo 48% (pin 7.0) -> 24.7/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #26: 0 aprovado(s) / 1 analisado(s)

[11:56:21] ciclo #27  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 11:45:00  (verde)
  │     OHLC : O=0.86644  H=0.86648  L=0.86609  C=0.86647
  │     range=3.9 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 90%  (min 30%)   [bot reportou 90%]
  │     [OK ] RSI(9)    : 19.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86647  SL=0.86559 (8.8 pips)  TP=0.86779 (13.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:56:22][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP BUY  @0.86647  SL:0.86559  TP:0.86779  pavio:90%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.2/35  ( 83.4%)  RSI 19.3
   Wick     [##############]    25/25  (100.0%)  pavio 90%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [############--]   4.3/5  ( 86.0%)  WR 57%  (7T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.5/100  (+33.5 pts vs mínimo 55)
   Pior critério: Sessao 10.0/15  (67% do máximo)
   → APROVADO  —  Score 88.5/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          83%  "RSI(9) 19.3 -> 29.2/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 90% (wick 25.0), corpo 8% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          72%  "Sessao London (10.0), WR 30d 57% em 7T (4.3) -> 14.3/20 pts."
-------------------------------------------------------------------
  Ciclo #27: 1 aprovado(s) / 1 analisado(s)

[11:56:46] ciclo #28  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPJPY SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-23 11:45:00  (verde)
  │     OHLC : O=215.59400  H=215.68800  L=215.58800  C=215.65500
  │     range=10.0 pips   corpo=61% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 70.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=215.65500  SL=215.73800 (8.3 pips)  TP=215.53050 (12.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:56:47][WAR_ROOM] [GBPJPY] ◈ signal_analysis:
   ✗ GBPJPY SELL  @215.65500  SL:215.73800  TP:215.53050  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.7/35  ( 44.9%)  RSI 70.5
   Wick     [#########-----]  16.5/25  ( 66.0%)  pavio 33%
   PinBar   [##------------]   2.3/20  ( 11.5%)  corpo 61% range  [suja]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#########-----------]   44.5/100  (-10.5 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 44.5 < 55 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 70.5 -> 15.7/35 pts. Gate: 70."
   [R] Rejeicao          42%  "Pavio 33% (wick 16.5), corpo 61% (pin 2.3) -> 18.8/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #28: 0 aprovado(s) / 1 analisado(s)

[13:26:24] ciclo #29  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 13:15:00  (vermelha)
  │     OHLC : O=0.86613  H=0.86620  L=0.86559  C=0.86565
  │     range=6.1 pips   corpo=79% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [-- ] Wick inferior: 10%  (min 30%)   [bot reportou 76%]
  │     [OK ] RSI(9)    : 18.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86613  SL=0.86534 (7.9 pips)  TP=0.86731 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:26:24][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✗ EURGBP BUY  @0.86613  SL:0.86534  TP:0.86731  pavio:76%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  30.2/35  ( 86.3%)  RSI 18.6
   Wick     [###-----------]   4.9/25  ( 19.6%)  pavio 76%
   PinBar   [#-------------]   1.3/20  (  6.5%)  corpo 79% range  [suja]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (8T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   48.9/100  (-6.1 pts vs mínimo 55)
   Pior critério: PinBar 1.3/20  (6% do máximo)
   → REJEITADO  —  Score 48.9 < 55 | fraco: Pin Bar 1.3/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          86%  "RSI(9) 18.6 -> 30.2/35 pts. Gate: 30."
   [R] Rejeicao          14%  "Pavio 10% (wick 4.9), corpo 79% (pin 1.3) -> 6.2/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 8T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #29: 0 aprovado(s) / 1 analisado(s)

[13:26:45] ciclo #30  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 13:15:00  (vermelha)
  │     OHLC : O=1.16864  H=1.16869  L=1.16813  C=1.16835
  │     range=5.6 pips   corpo=52% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 20.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16835  SL=1.16763 (7.2 pips)  TP=1.16943 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:26:46][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.16835  SL:1.16763  TP:1.16943  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  27.8/35  ( 79.4%)  RSI 20.4
   Wick     [###########---]  19.6/25  ( 78.4%)  pavio 39%
   PinBar   [##------------]   2.9/20  ( 14.5%)  corpo 52% range  [suja]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 38%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.3/100  (+5.3 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → APROVADO  —  Score 60.3/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          79%  "RSI(9) 20.4 -> 27.8/35 pts. Gate: 30."
   [R] Rejeicao          50%  "Pavio 39% (wick 19.6), corpo 52% (pin 2.9) -> 22.5/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 38% em 13T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #30: 1 aprovado(s) / 1 analisado(s)

[13:27:07] ciclo #31  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-23 13:15:00  (verde)
  │     OHLC : O=0.58738  H=0.58761  L=0.58726  C=0.58747
  │     range=3.5 pips   corpo=26% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 34%  (min 30%)   [bot reportou 34%]
  │     [OK ] RSI(9)    : 19.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58747  SL=0.58676 (7.1 pips)  TP=0.58854 (10.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:27:07][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD BUY  @0.58747  SL:0.58676  TP:0.58854  pavio:34%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.0/35  ( 82.9%)  RSI 19.5
   Wick     [##########----]  17.1/25  ( 68.4%)  pavio 34%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 26% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]   5.0/5  (100.0%)  WR 60%  (10T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.1/100  (+19.1 pts vs mínimo 55)
   Pior critério: PinBar 13.0/20  (65% do máximo)
   → APROVADO  —  Score 74.1/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          83%  "RSI(9) 19.5 -> 29.0/35 pts. Gate: 30."
   [R] Rejeicao          67%  "Pavio 34% (wick 17.1), corpo 26% (pin 13.0) -> 30.1/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 60% em 10T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #31: 1 aprovado(s) / 1 analisado(s)