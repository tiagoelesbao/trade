===================================================================
  WAR ROOM v6.1.2  --  ANALISE TECNICA AGENTICA
-------------------------------------------------------------------
  Score minimo : 55/100   |   Correlacao: ATIVA   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)   [Slope/ColorReversal desativados nas Fases 1+2]
  Criterios    : RSI(35) Wick(25) PinBar(20) Sessao(15) Hist(5)  [alpha: RSI]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE (gatilhos+condicoes) -> [FASE 2] signal_analysis (score)
===================================================================
[02:29:49][WAR_ROOM]   war_room_started: War Room v6.1.2 iniciada | Score mínimo: 55/100 | 5 critérios (RSI alpha) | estratégia: Zona+Wick+RSI | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[02:29:56] ciclo #1  --  1 sinal(is) recebido(s)
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

[02:29:57][WAR_ROOM] [USDCHF] ◈ signal_analysis:
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
  Ciclo #1: 0 aprovado(s) / 1 analisado(s)

[02:56:36] ciclo #2  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 02:45:00  (vermelha)
  │     OHLC : O=0.78625  H=0.78632  L=0.78614  C=0.78622
  │     range=1.8 pips   corpo=17% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 74.4    (cond >= 70)
  │     [-- ] Sessao UTC : h=23h -> Fora de sessão  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78622  SL=0.78682 (6.0 pips)  TP=0.78532 (9.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[02:56:37][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78622  SL:0.78682  TP:0.78532  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  20.9/35  ( 59.7%)  RSI 74.4
   Wick     [###########---]  19.4/25  ( 77.6%)  pavio 39%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 17% range  [bom]
   Sessao   [--------------]   0.0/15  (  0.0%)  Fora de sessão
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   53.3/100  (-1.7 pts vs mínimo 55)
   Pior critério: Sessao 0.0/15  (0% do máximo)
   → REJEITADO  —  Score 53.3 < 55 | fraco: Sessão 0.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          60%  "RSI(9) 74.4 -> 20.9/35 pts. Gate: 70."
   [R] Rejeicao          72%  "Pavio 39% (wick 19.4), corpo 17% (pin 13.0) -> 32.4/45 pts."
   [C] Contexto           0%  "Sessao Fora de sessão (0.0), WR 30d 25% em 4T (0.0) -> 0.0/20 pts."
-------------------------------------------------------------------
  Ciclo #2: 0 aprovado(s) / 1 analisado(s)
[06:19:22][LIFECYCLE] ✗ lifecycle_get_pending_signals(awaiting_consensus)_failed: get_pending_signals(awaiting_consensus): [WinError 10054] Foi forçado o cancelamento de uma conexão existente pelo host remoto

[06:41:42] ciclo #3  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 06:30:00  (verde)
  │     OHLC : O=1.16754  H=1.16774  L=1.16716  C=1.16761
  │     range=5.8 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 66%  (min 30%)   [bot reportou 66%]
  │     [OK ] RSI(9)    : 27.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16761  SL=1.16666 (9.5 pips)  TP=1.16904 (14.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:41:42][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.16761  SL:1.16666  TP:1.16904  pavio:66%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  18.5/35  ( 52.9%)  RSI 27.4
   Wick     [##############]    25/25  (100.0%)  pavio 66%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#-------------]   0.3/5  (  6.0%)  WR 41%  (17T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   66.8/100  (+11.8 pts vs mínimo 55)
   Pior critério: Hist 0.3/5  (6% do máximo)
   → APROVADO  —  Score 66.8/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          53%  "RSI(9) 27.4 -> 18.5/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 66% (wick 25.0), corpo 12% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          16%  "Sessao Ásia (3.0), WR 30d 41% em 17T (0.3) -> 3.3/20 pts."
-------------------------------------------------------------------
  Ciclo #3: 1 aprovado(s) / 1 analisado(s)

[06:42:04] ciclo #4  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 06:30:00  (verde)
  │     OHLC : O=0.71169  H=0.71200  L=0.71143  C=0.71187
  │     range=5.7 pips   corpo=32% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 29.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71187  SL=0.71093 (9.4 pips)  TP=0.71328 (14.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:42:04][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD BUY  @0.71187  SL:0.71093  TP:0.71328  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.7/35  ( 44.9%)  RSI 29.5
   Wick     [#############-]  22.8/25  ( 91.2%)  pavio 46%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 32% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   50.2/100  (-4.8 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Score 50.2 < 55 | fraco: Sessão 3.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 29.5 -> 15.7/35 pts. Gate: 30."
   [R] Rejeicao          66%  "Pavio 46% (wick 22.8), corpo 32% (pin 7.0) -> 29.8/45 pts."
   [C] Contexto          24%  "Sessao Ásia (3.0), WR 30d 47% em 15T (1.7) -> 4.7/20 pts."
-------------------------------------------------------------------
  Ciclo #4: 0 aprovado(s) / 1 analisado(s)

[06:42:25] ciclo #5  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 06:30:00  (vermelha)
  │     OHLC : O=0.78710  H=0.78728  L=0.78697  C=0.78705
  │     range=3.1 pips   corpo=16% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 58%  (min 30%)   [bot reportou 58%]
  │     [OK ] RSI(9)    : 73.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78705  SL=0.78778 (7.3 pips)  TP=0.78596 (10.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:42:26][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78705  SL:0.78778  TP:0.78596  pavio:58%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.5/35  ( 55.7%)  RSI 73.4
   Wick     [##############]    25/25  (100.0%)  pavio 58%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 16% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.5/100  (+5.5 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          56%  "RSI(9) 73.4 -> 19.5/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 58% (wick 25.0), corpo 16% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 analisado(s)

[07:11:28] ciclo #6  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 07:00:00  (verde)
  │     OHLC : O=1.34598  H=1.34624  L=1.34578  C=1.34613
  │     range=4.6 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 26.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34613  SL=1.34528 (8.5 pips)  TP=1.34741 (12.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:11:28][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.34613  SL:1.34528  TP:1.34741  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.4/35  ( 55.4%)  RSI 26.7
   Wick     [############--]  21.7/25  ( 86.8%)  pavio 43%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 33% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   51.1/100  (-3.9 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 51.1 < 55 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          55%  "RSI(9) 26.7 -> 19.4/35 pts. Gate: 30."
   [R] Rejeicao          64%  "Pavio 43% (wick 21.7), corpo 33% (pin 7.0) -> 28.7/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #6: 0 aprovado(s) / 1 analisado(s)

[07:11:50] ciclo #7  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 07:00:00  (verde)
  │     OHLC : O=0.71188  H=0.71227  L=0.71163  C=0.71216
  │     range=6.4 pips   corpo=44% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 28.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71216  SL=0.71113 (10.3 pips)  TP=0.71371 (15.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:11:50][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD BUY  @0.71216  SL:0.71113  TP:0.71371  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  16.7/35  ( 47.7%)  RSI 28.7
   Wick     [###########---]  19.5/25  ( 78.0%)  pavio 39%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 44% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   47.9/100  (-7.1 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Score 47.9 < 55 | fraco: Sessão 3.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          48%  "RSI(9) 28.7 -> 16.7/35 pts. Gate: 30."
   [R] Rejeicao          59%  "Pavio 39% (wick 19.5), corpo 44% (pin 7.0) -> 26.5/45 pts."
   [C] Contexto          24%  "Sessao Ásia (3.0), WR 30d 47% em 15T (1.7) -> 4.7/20 pts."
-------------------------------------------------------------------
  Ciclo #7: 0 aprovado(s) / 1 analisado(s)

[07:12:11] ciclo #8  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 07:00:00  (vermelha)
  │     OHLC : O=0.78694  H=0.78723  L=0.78680  C=0.78691
  │     range=4.3 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 67%  (min 30%)   [bot reportou 67%]
  │     [OK ] RSI(9)    : 82.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78691  SL=0.78773 (8.2 pips)  TP=0.78568 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:12:12][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78691  SL:0.78773  TP:0.78568  pavio:67%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  31.8/35  ( 90.9%)  RSI 82.6
   Wick     [##############]    25/25  (100.0%)  pavio 67%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.8/100  (+24.8 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 82.6 -> 31.8/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 67% (wick 25.0), corpo 7% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 25% em 4T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #8: 0 aprovado(s) / 1 analisado(s)

[08:41:36] ciclo #9  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 08:30:00  (verde)
  │     OHLC : O=0.71244  H=0.71291  L=0.71243  C=0.71269
  │     range=4.8 pips   corpo=52% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 85.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71269  SL=0.71341 (7.2 pips)  TP=0.71161 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[08:41:36][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71269  SL:0.71341  TP:0.71161  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 85.6
   Wick     [#############-]  22.9/25  ( 91.6%)  pavio 46%
   PinBar   [##------------]   2.9/20  ( 14.5%)  corpo 52% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   65.5/100  (+10.5 pts vs mínimo 55)
   Pior critério: PinBar 2.9/20  (14% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 85.6 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          57%  "Pavio 46% (wick 22.9), corpo 52% (pin 2.9) -> 25.8/45 pts."
   [C] Contexto          24%  "Sessao Ásia (3.0), WR 30d 47% em 15T (1.7) -> 4.7/20 pts."
-------------------------------------------------------------------
  Ciclo #9: 0 aprovado(s) / 1 analisado(s)

[08:56:29] ciclo #10  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 08:45:00  (vermelha)
  │     OHLC : O=1.34660  H=1.34671  L=1.34638  C=1.34655
  │     range=3.3 pips   corpo=15% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 73.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34655  SL=1.34721 (6.6 pips)  TP=1.34556 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[08:56:29][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.34655  SL:1.34721  TP:1.34556  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  20.1/35  ( 57.4%)  RSI 73.8
   Wick     [#########-----]  16.7/25  ( 66.8%)  pavio 33%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 15% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   52.8/100  (-2.2 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 52.8 < 55 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          57%  "RSI(9) 73.8 -> 20.1/35 pts. Gate: 70."
   [R] Rejeicao          66%  "Pavio 33% (wick 16.7), corpo 15% (pin 13.0) -> 29.7/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #10: 0 aprovado(s) / 1 analisado(s)

[08:56:50] ciclo #11  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 08:45:00  (vermelha)
  │     OHLC : O=0.71269  H=0.71283  L=0.71255  C=0.71265
  │     range=2.8 pips   corpo=14% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 81.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=05h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71265  SL=0.71333 (6.8 pips)  TP=0.71163 (10.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[08:56:51][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71265  SL:0.71333  TP:0.71163  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.6/35  ( 84.6%)  RSI 81.0
   Wick     [##############]  25.0/25  (100.0%)  pavio 50%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 14% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.3/100  (+24.3 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          85%  "RSI(9) 81.0 -> 29.6/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 50% (wick 25.0), corpo 14% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          24%  "Sessao Ásia (3.0), WR 30d 47% em 15T (1.7) -> 4.7/20 pts."
-------------------------------------------------------------------
  Ciclo #11: 0 aprovado(s) / 1 analisado(s)

[09:11:38] ciclo #12  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 09:00:00  (verde)
  │     OHLC : O=1.34655  H=1.34689  L=1.34641  C=1.34658
  │     range=4.8 pips   corpo=6% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 65%  (min 30%)   [bot reportou 65%]
  │     [OK ] RSI(9)    : 70.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34658  SL=1.34739 (8.1 pips)  TP=1.34536 (12.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:11:38][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.34658  SL:1.34739  TP:1.34536  pavio:65%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.4/35  ( 44.0%)  RSI 70.3
   Wick     [##############]    25/25  (100.0%)  pavio 65%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 6% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.4/100  (+8.4 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          44%  "RSI(9) 70.3 -> 15.4/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 65% (wick 25.0), corpo 6% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #12: 0 aprovado(s) / 1 analisado(s)

[09:11:59] ciclo #13  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 09:00:00  (vermelha)
  │     OHLC : O=0.71266  H=0.71299  L=0.71251  C=0.71252
  │     range=4.8 pips   corpo=29% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 69%  (min 30%)   [bot reportou 69%]
  │     [OK ] RSI(9)    : 73.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71252  SL=0.71349 (9.7 pips)  TP=0.71107 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:12:00][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71252  SL:0.71349  TP:0.71107  pavio:69%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.3/35  ( 55.1%)  RSI 73.2
   Wick     [##############]    25/25  (100.0%)  pavio 69%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 29% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   62.0/100  (+7.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          55%  "RSI(9) 73.2 -> 19.3/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 69% (wick 25.0), corpo 29% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          24%  "Sessao Ásia (3.0), WR 30d 47% em 15T (1.7) -> 4.7/20 pts."
-------------------------------------------------------------------
  Ciclo #13: 0 aprovado(s) / 1 analisado(s)

[10:56:22] ciclo #14  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 10:45:00  (verde)
  │     OHLC : O=1.16851  H=1.16937  L=1.16846  C=1.16908
  │     range=9.1 pips   corpo=63% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 70.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=07h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16908  SL=1.16987 (7.9 pips)  TP=1.16790 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[10:56:22][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✗ EURUSD SELL  @1.16908  SL:1.16987  TP:1.16790  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  16.0/35  ( 45.7%)  RSI 70.8
   Wick     [#########-----]  15.9/25  ( 63.6%)  pavio 32%
   PinBar   [##------------]   2.2/20  ( 11.0%)  corpo 63% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (18T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [########------------]   38.2/100  (-16.8 pts vs mínimo 55)
   Pior critério: PinBar 2.2/20  (11% do máximo)
   → REJEITADO  —  Score 38.2 < 55 | fraco: Pin Bar 2.2/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          46%  "RSI(9) 70.8 -> 16.0/35 pts. Gate: 70."
   [R] Rejeicao          40%  "Pavio 32% (wick 15.9), corpo 63% (pin 2.2) -> 18.1/45 pts."
   [C] Contexto          20%  "Sessao Ásia (3.0), WR 30d 44% em 18T (1.1) -> 4.1/20 pts."
-------------------------------------------------------------------
  Ciclo #14: 0 aprovado(s) / 1 analisado(s)

[11:41:29] ciclo #15  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 11:30:00  (vermelha)
  │     OHLC : O=0.71314  H=0.71324  L=0.71298  C=0.71301
  │     range=2.6 pips   corpo=50% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 38%  (min 30%)   [bot reportou 38%]
  │     [OK ] RSI(9)    : 71.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71301  SL=0.71374 (7.3 pips)  TP=0.71192 (10.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:41:29][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71301  SL:0.71374  TP:0.71192  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  16.9/35  ( 48.3%)  RSI 71.4
   Wick     [###########---]  19.2/25  ( 76.8%)  pavio 38%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 50% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#####---------]   1.7/5  ( 34.0%)  WR 47%  (15T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   54.8/100  (-0.2 pts vs mínimo 55)
   Pior critério: Hist 1.7/5  (34% do máximo)
   → REJEITADO  —  Score 54.8 < 55 | fraco: Histórico 1.7/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          48%  "RSI(9) 71.4 -> 16.9/35 pts. Gate: 70."
   [R] Rejeicao          58%  "Pavio 38% (wick 19.2), corpo 50% (pin 7.0) -> 26.2/45 pts."
   [C] Contexto          58%  "Sessao London (10.0), WR 30d 47% em 15T (1.7) -> 11.7/20 pts."
-------------------------------------------------------------------
  Ciclo #15: 0 aprovado(s) / 1 analisado(s)

[11:56:26] ciclo #16  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 11:45:00  (vermelha)
  │     OHLC : O=0.78648  H=0.78649  L=0.78590  C=0.78610
  │     range=5.9 pips   corpo=64% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 34%  (min 30%)   [bot reportou 34%]
  │     [OK ] RSI(9)    : 25.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78610  SL=0.78540 (7.0 pips)  TP=0.78715 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:56:27][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78610  SL:0.78540  TP:0.78715  pavio:34%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  20.8/35  ( 59.4%)  RSI 25.6
   Wick     [#########-----]  16.9/25  ( 67.6%)  pavio 34%
   PinBar   [#-------------]   2.1/20  ( 10.5%)  corpo 64% range  [suja]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   49.8/100  (-5.2 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 49.8 < 55 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          59%  "RSI(9) 25.6 -> 20.8/35 pts. Gate: 30."
   [R] Rejeicao          42%  "Pavio 34% (wick 16.9), corpo 64% (pin 2.1) -> 19.0/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #16: 0 aprovado(s) / 1 analisado(s)

[12:26:27] ciclo #17  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 12:15:00  (verde)
  │     OHLC : O=0.78619  H=0.78651  L=0.78597  C=0.78649
  │     range=5.4 pips   corpo=56% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 41%  (min 30%)   [bot reportou 41%]
  │     [OK ] RSI(9)    : 29.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=09h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78649  SL=0.78547 (10.2 pips)  TP=0.78802 (15.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[12:26:28][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78649  SL:0.78547  TP:0.78802  pavio:41%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.7/35  ( 44.9%)  RSI 29.4
   Wick     [###########---]  20.4/25  ( 81.6%)  pavio 41%
   PinBar   [##------------]   2.7/20  ( 13.5%)  corpo 56% range  [suja]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 25%  (4T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   48.8/100  (-6.2 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 48.8 < 55 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          45%  "RSI(9) 29.4 -> 15.7/35 pts. Gate: 30."
   [R] Rejeicao          51%  "Pavio 41% (wick 20.4), corpo 56% (pin 2.7) -> 23.1/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 25% em 4T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #17: 0 aprovado(s) / 1 analisado(s)

[13:26:24] ciclo #18  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-24 13:15:00  (verde)
  │     OHLC : O=0.86691  H=0.86697  L=0.86680  C=0.86696
  │     range=1.7 pips   corpo=29% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 65%  (min 30%)   [bot reportou 65%]
  │     [OK ] RSI(9)    : 26.5    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86696  SL=0.86630 (6.6 pips)  TP=0.86795 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:26:24][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP BUY  @0.86696  SL:0.86630  TP:0.86795  pavio:65%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.7/35  ( 56.3%)  RSI 26.5
   Wick     [##############]    25/25  (100.0%)  pavio 65%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 29% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.8/100  (+13.8 pts vs mínimo 55)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → APROVADO  —  Score 68.8/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          56%  "RSI(9) 26.5 -> 19.7/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 65% (wick 25.0), corpo 29% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          55%  "Sessao London (10.0), WR 30d 44% em 9T (1.1) -> 11.1/20 pts."
-------------------------------------------------------------------
  Ciclo #18: 1 aprovado(s) / 1 analisado(s)

[14:11:30] ciclo #19  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 14:00:00  (verde)
  │     OHLC : O=1.17032  H=1.17123  L=1.17019  C=1.17074
  │     range=10.4 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 47%  (min 30%)   [bot reportou 47%]
  │     [OK ] RSI(9)    : 81.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=11h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17074  SL=1.17173 (9.9 pips)  TP=1.16925 (14.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[14:11:31][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD SELL  @1.17074  SL:1.17173  TP:1.16925  pavio:47%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  30.5/35  ( 87.1%)  RSI 81.7
   Wick     [#############-]  23.6/25  ( 94.4%)  pavio 47%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 40% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [###-----------]   1.1/5  ( 22.0%)  WR 44%  (18T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.2/100  (+17.2 pts vs mínimo 55)
   Pior critério: Hist 1.1/5  (22% do máximo)
   → APROVADO  —  Score 72.2/55 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          87%  "RSI(9) 81.7 -> 30.5/35 pts. Gate: 70."
   [R] Rejeicao          68%  "Pavio 47% (wick 23.6), corpo 40% (pin 7.0) -> 30.6/45 pts."
   [C] Contexto          55%  "Sessao London (10.0), WR 30d 44% em 18T (1.1) -> 11.1/20 pts."
-------------------------------------------------------------------
  Ciclo #19: 1 aprovado(s) / 1 analisado(s)

[14:11:52] ciclo #20  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-24 14:00:00  (verde)
  │     OHLC : O=1.34920  H=1.35012  L=1.34879  C=1.34952
  │     range=13.3 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 45%  (min 30%)   [bot reportou 45%]
  │     [OK ] RSI(9)    : 90.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=11h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.34952  SL=1.35062 (11.0 pips)  TP=1.34787 (16.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[14:11:52][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.34952  SL:1.35062  TP:1.34787  pavio:45%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 90.6
   Wick     [#############-]  22.6/25  ( 90.4%)  pavio 45%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 24% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   80.6/100  (+25.6 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 90.6 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          79%  "Pavio 45% (wick 22.6), corpo 24% (pin 13.0) -> 35.6/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #20: 0 aprovado(s) / 1 analisado(s)