===================================================================
  WAR ROOM v6.1.2  --  ANALISE TECNICA AGENTICA
-------------------------------------------------------------------
  Score minimo : 65/100   |   Correlacao: ATIVA   |   Max sinais: 10
  Estrategia   : Zona + Wick + RSI(9)   [Slope/ColorReversal desativados nas Fases 1+2]
  Criterios    : RSI(35) Wick(25) PinBar(20) Sessao(15) Hist(5)  [alpha: RSI]
  Timezone logs: MT5 server (UTC+03:00) — casa com o chart
  Pipeline log : [FASE 1] STRATEGY FIRE (gatilhos+condicoes) -> [FASE 2] signal_analysis (score)
===================================================================
[23:57:17][WAR_ROOM]   war_room_started: War Room v6.1.2 iniciada | Score mínimo: 65/100 | 5 critérios (RSI alpha) | estratégia: Zona+Wick+RSI | TZ=UTC+3
  MT5 conectado. Aguardando sinais do bot...


[00:11:38] ciclo #1  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 00:00:00  (verde)
  │     OHLC : O=1.16935  H=1.17003  L=1.16852  C=1.16985
  │     range=15.1 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 55%  (min 30%)   [bot reportou 55%]
  │     [OK ] RSI(9)    : 20.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=21h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.16985  SL=1.16802 (18.3 pips)  TP=1.17260 (27.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[00:11:39][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.16985  SL:1.16802  TP:1.17260  pavio:55%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.3/35  ( 80.9%)  RSI 20.0
   Wick     [##############]    25/25  (100.0%)  pavio 55%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 33% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [#-------------]   0.5/5  ( 10.0%)  WR 42%  (19T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.8/100  (+15.8 pts vs mínimo 55)
   Pior critério: Hist 0.5/5  (10% do máximo)
   → APROVADO  —  Score 70.8/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          81%  "RSI(9) 20.0 -> 28.3/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 55% (wick 25.0), corpo 33% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          52%  "Sessao New York (10.0), WR 30d 42% em 19T (0.5) -> 10.5/20 pts."
-------------------------------------------------------------------
  Ciclo #1: 1 aprovado(s) / 1 analisado(s)

[00:12:00] ciclo #2  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 00:00:00  (vermelha)
  │     OHLC : O=0.58672  H=0.58706  L=0.58554  C=0.58635
  │     range=15.2 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 53%  (min 30%)   [bot reportou 53%]
  │     [OK ] RSI(9)    : 11.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=21h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58635  SL=0.58504 (13.1 pips)  TP=0.58832 (19.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[00:12:00][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD BUY  @0.58635  SL:0.58504  TP:0.58832  pavio:53%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 11.6
   Wick     [##############]    25/25  (100.0%)  pavio 53%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 24% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [##############]     5/5  (100.0%)  WR 62%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.0/100  (+33.0 pts vs mínimo 55)
   Pior critério: PinBar 13.0/20  (65% do máximo)
   → APROVADO  —  Score 88.0/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 11.6 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 53% (wick 25.0), corpo 24% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          75%  "Sessao New York (10.0), WR 30d 62% em 13T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #2: 1 aprovado(s) / 1 analisado(s)

[00:26:34] ciclo #3  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 00:15:00  (vermelha)
  │     OHLC : O=0.71332  H=0.71361  L=0.71314  C=0.71331
  │     range=4.7 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 3.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=21h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71331  SL=0.71264 (6.7 pips)  TP=0.71431 (10.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[00:26:35][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD BUY  @0.71331  SL:0.71264  TP:0.71431  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 3.3
   Wick     [##########----]  18.1/25  ( 72.4%)  pavio 36%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [#########-----]   3.2/5  ( 64.0%)  WR 53%  (17T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   86.3/100  (+31.3 pts vs mínimo 55)
   Pior critério: Hist 3.2/5  (64% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 3.3 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          85%  "Pavio 36% (wick 18.1), corpo 2% (pin 20.0) -> 38.1/45 pts."
   [C] Contexto          66%  "Sessao New York (10.0), WR 30d 53% em 17T (3.2) -> 13.2/20 pts."
-------------------------------------------------------------------
  Ciclo #3: 0 aprovado(s) / 1 analisado(s)

[00:26:56] ciclo #4  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 00:15:00  (vermelha)
  │     OHLC : O=1.36770  H=1.36778  L=1.36760  C=1.36763
  │     range=1.8 pips   corpo=39% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 44%  (min 30%)   [bot reportou 44%]
  │     [OK ] RSI(9)    : 87.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=21h -> New York  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36763  SL=1.36828 (6.5 pips)  TP=1.36666 (9.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[00:26:56][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD SELL  @1.36763  SL:1.36828  TP:1.36666  pavio:44%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 87.7
   Wick     [############--]  22.2/25  ( 88.8%)  pavio 44%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 39% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  New York
   Hist     [##############]     5/5  (100.0%)  WR 73%  (11T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.2/100  (+24.2 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → APROVADO  —  Score 79.2/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 87.7 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          65%  "Pavio 44% (wick 22.2), corpo 39% (pin 7.0) -> 29.2/45 pts."
   [C] Contexto          75%  "Sessao New York (10.0), WR 30d 73% em 11T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #4: 1 aprovado(s) / 1 analisado(s)

[02:26:22] ciclo #5  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 02:15:00  (vermelha)
  │     OHLC : O=1.35158  H=1.35178  L=1.35138  C=1.35139
  │     range=4.0 pips   corpo=48% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 72.4    (cond >= 70)
  │     [-- ] Sessao UTC : h=23h -> Fora de sessão  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35139  SL=1.35228 (8.9 pips)  TP=1.35005 (13.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[02:26:23][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35139  SL:1.35228  TP:1.35005  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  18.2/35  ( 52.0%)  RSI 72.4
   Wick     [##############]    25/25  (100.0%)  pavio 50%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 48% range  [aceitável]
   Sessao   [--------------]   0.0/15  (  0.0%)  Fora de sessão
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   50.2/100  (-4.8 pts vs mínimo 55)
   Pior critério: Sessao 0.0/15  (0% do máximo)
   → REJEITADO  —  Score 50.2 < 65 | fraco: Sessão 0.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          52%  "RSI(9) 72.4 -> 18.2/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 50% (wick 25.0), corpo 48% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto           0%  "Sessao Fora de sessão (0.0), WR 30d 22% em 9T (0.0) -> 0.0/20 pts."
-------------------------------------------------------------------
  Ciclo #5: 0 aprovado(s) / 1 analisado(s)

[02:26:44] ciclo #6  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 02:15:00  (vermelha)
  │     OHLC : O=0.71445  H=0.71463  L=0.71434  C=0.71434
  │     range=2.9 pips   corpo=38% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 62%  (min 30%)   [bot reportou 62%]
  │     [OK ] RSI(9)    : 85.4    (cond >= 70)
  │     [-- ] Sessao UTC : h=23h -> Fora de sessão  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71434  SL=0.71513 (7.9 pips)  TP=0.71315 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[02:26:44][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71434  SL:0.71513  TP:0.71315  pavio:62%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 85.4
   Wick     [##############]    25/25  (100.0%)  pavio 62%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 38% range  [aceitável]
   Sessao   [--------------]   0.0/15  (  0.0%)  Fora de sessão
   Hist     [#########-----]   3.2/5  ( 64.0%)  WR 53%  (17T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.2/100  (+15.2 pts vs mínimo 55)
   Pior critério: Sessao 0.0/15  (0% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 85.4 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 62% (wick 25.0), corpo 38% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          16%  "Sessao Fora de sessão (0.0), WR 30d 53% em 17T (3.2) -> 3.2/20 pts."
-------------------------------------------------------------------
  Ciclo #6: 0 aprovado(s) / 1 analisado(s)

[02:41:39] ciclo #7  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 02:30:00  (vermelha)
  │     OHLC : O=0.71434  H=0.71439  L=0.71424  C=0.71433
  │     range=1.5 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 85.4    (cond >= 70)
  │     [-- ] Sessao UTC : h=23h -> Fora de sessão  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71433  SL=0.71489 (5.6 pips)  TP=0.71349 (8.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[02:41:39][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✗ AUDUSD SELL  @0.71433  SL:0.71489  TP:0.71349  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 85.4
   Wick     [#########-----]  16.7/25  ( 66.8%)  pavio 33%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [--------------]   0.0/15  (  0.0%)  Fora de sessão
   Hist     [#########-----]   3.2/5  ( 64.0%)  WR 53%  (17T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.9/100  (+19.9 pts vs mínimo 55)
   Pior critério: Sessao 0.0/15  (0% do máximo)
   → REJEITADO  —  Correlação com NZDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 85.4 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          82%  "Pavio 33% (wick 16.7), corpo 7% (pin 20.0) -> 36.7/45 pts."
   [C] Contexto          16%  "Sessao Fora de sessão (0.0), WR 30d 53% em 17T (3.2) -> 3.2/20 pts."
-------------------------------------------------------------------
  Ciclo #7: 0 aprovado(s) / 1 analisado(s)

[03:26:36] ciclo #8  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 03:15:00  (verde)
  │     OHLC : O=0.86642  H=0.86650  L=0.86639  C=0.86645
  │     range=1.1 pips   corpo=27% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 45%  (min 30%)   [bot reportou 45%]
  │     [OK ] RSI(9)    : 80.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=00h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86645  SL=0.86700 (5.5 pips)  TP=0.86563 (8.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[03:26:36][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP SELL  @0.86645  SL:0.86700  TP:0.86563  pavio:45%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.1/35  ( 83.1%)  RSI 80.6
   Wick     [#############-]  22.7/25  ( 90.8%)  pavio 45%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 27% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.3/100  (+15.3 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 70.3/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          83%  "RSI(9) 80.6 -> 29.1/35 pts. Gate: 70."
   [R] Rejeicao          79%  "Pavio 45% (wick 22.7), corpo 27% (pin 13.0) -> 35.7/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 12T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #8: 1 aprovado(s) / 1 analisado(s)

[04:11:34] ciclo #9  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:00:00  (verde)
  │     OHLC : O=1.17159  H=1.17267  L=1.17155  C=1.17197
  │     range=11.2 pips   corpo=34% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 63%  (min 30%)   [bot reportou 63%]
  │     [OK ] RSI(9)    : 84.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17197  SL=1.17317 (12.0 pips)  TP=1.17017 (18.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:11:35][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD SELL  @1.17197  SL:1.17317  TP:1.17017  pavio:63%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.7/35  ( 96.3%)  RSI 84.0
   Wick     [##############]    25/25  (100.0%)  pavio 63%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 34% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [###-----------]   1.2/5  ( 24.0%)  WR 45%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.9/100  (+14.9 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 69.9/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          96%  "RSI(9) 84.0 -> 33.7/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 63% (wick 25.0), corpo 34% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          21%  "Sessao Ásia (3.0), WR 30d 45% em 20T (1.2) -> 4.2/20 pts."
-------------------------------------------------------------------
  Ciclo #9: 1 aprovado(s) / 1 analisado(s)

[04:11:56] ciclo #10  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:00:00  (verde)
  │     OHLC : O=1.35213  H=1.35342  L=1.35213  C=1.35279
  │     range=12.9 pips   corpo=51% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 84.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35279  SL=1.35392 (11.3 pips)  TP=1.35109 (17.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:11:56][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35279  SL:1.35392  TP:1.35109  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  34.9/35  ( 99.7%)  RSI 84.9
   Wick     [##############]  24.4/25  ( 97.6%)  pavio 49%
   PinBar   [##------------]   2.9/20  ( 14.5%)  corpo 51% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   65.2/100  (+10.2 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 84.9 -> 34.9/35 pts. Gate: 70."
   [R] Rejeicao          61%  "Pavio 49% (wick 24.4), corpo 51% (pin 2.9) -> 27.3/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #10: 0 aprovado(s) / 1 analisado(s)

[04:12:17] ciclo #11  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:00:00  (verde)
  │     OHLC : O=0.71571  H=0.71682  L=0.71571  C=0.71612
  │     range=11.1 pips   corpo=37% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 63%  (min 30%)   [bot reportou 63%]
  │     [OK ] RSI(9)    : 88.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71612  SL=0.71732 (12.0 pips)  TP=0.71432 (18.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:12:18][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71612  SL:0.71732  TP:0.71432  pavio:63%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 88.2
   Wick     [##############]    25/25  (100.0%)  pavio 63%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 37% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#########-----]   3.2/5  ( 64.0%)  WR 53%  (17T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.2/100  (+18.2 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 73.2/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 88.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 63% (wick 25.0), corpo 37% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          31%  "Sessao Ásia (3.0), WR 30d 53% em 17T (3.2) -> 6.2/20 pts."
-------------------------------------------------------------------
  Ciclo #11: 1 aprovado(s) / 1 analisado(s)

[04:12:39] ciclo #12  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 04:00:00  (vermelha)
  │     OHLC : O=1.36698  H=1.36698  L=1.36625  C=1.36674
  │     range=7.3 pips   corpo=33% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 67%  (min 30%)   [bot reportou 67%]
  │     [OK ] RSI(9)    : 10.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36674  SL=1.36575 (9.9 pips)  TP=1.36823 (14.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:12:39][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD BUY  @1.36674  SL:1.36575  TP:1.36823  pavio:67%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 10.8
   Wick     [##############]    25/25  (100.0%)  pavio 67%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 33% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 75%  (12T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.0/100  (+20.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 75.0/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 10.8 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 67% (wick 25.0), corpo 33% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 75% em 12T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #12: 1 aprovado(s) / 1 analisado(s)

[04:13:00] ciclo #13  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 04:00:00  (vermelha)
  │     OHLC : O=0.78569  H=0.78569  L=0.78472  C=0.78533
  │     range=9.7 pips   corpo=37% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 63%  (min 30%)   [bot reportou 63%]
  │     [OK ] RSI(9)    : 20.8    (cond <= 30)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78533  SL=0.78422 (11.1 pips)  TP=0.78699 (16.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:13:01][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78533  SL:0.78422  TP:0.78699  pavio:63%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  27.2/35  ( 77.7%)  RSI 20.8
   Wick     [##############]    25/25  (100.0%)  pavio 63%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 37% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   64.7/100  (+9.7 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Score 64.7 < 65 | fraco: Sessão 3.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          78%  "RSI(9) 20.8 -> 27.2/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 63% (wick 25.0), corpo 37% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #13: 0 aprovado(s) / 1 analisado(s)

[04:13:22] ciclo #14  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:00:00  (verde)
  │     OHLC : O=0.58819  H=0.58895  L=0.58819  C=0.58848
  │     range=7.6 pips   corpo=38% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 62%  (min 30%)   [bot reportou 62%]
  │     [OK ] RSI(9)    : 90.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58848  SL=0.58945 (9.7 pips)  TP=0.58703 (14.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:13:22][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58848  SL:0.58945  TP:0.58703  pavio:62%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 90.2
   Wick     [##############]    25/25  (100.0%)  pavio 62%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 38% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.0/100  (+20.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 90.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 62% (wick 25.0), corpo 38% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #14: 0 aprovado(s) / 1 analisado(s)

[04:26:28] ciclo #15  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:15:00  (verde)
  │     OHLC : O=1.35278  H=1.35343  L=1.35276  C=1.35311
  │     range=6.7 pips   corpo=49% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 48%  (min 30%)   [bot reportou 48%]
  │     [OK ] RSI(9)    : 86.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35311  SL=1.35393 (8.2 pips)  TP=1.35188 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:26:29][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35311  SL:1.35393  TP:1.35188  pavio:48%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 86.3
   Wick     [#############-]  23.9/25  ( 95.6%)  pavio 48%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 49% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   68.9/100  (+13.9 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 86.3 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          69%  "Pavio 48% (wick 23.9), corpo 49% (pin 7.0) -> 30.9/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #15: 0 aprovado(s) / 1 analisado(s)

[04:26:50] ciclo #16  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 04:15:00  (vermelha)
  │     OHLC : O=0.78533  H=0.78541  L=0.78497  C=0.78525
  │     range=4.4 pips   corpo=18% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 64%  (min 30%)   [bot reportou 64%]
  │     [OK ] RSI(9)    : 19.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78525  SL=0.78447 (7.8 pips)  TP=0.78642 (11.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:26:50][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78525  SL:0.78447  TP:0.78642  pavio:64%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.7/35  ( 82.0%)  RSI 19.7
   Wick     [##############]    25/25  (100.0%)  pavio 64%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 18% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.2/100  (+17.2 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          82%  "RSI(9) 19.7 -> 28.7/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 64% (wick 25.0), corpo 18% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #16: 0 aprovado(s) / 1 analisado(s)

[04:27:11] ciclo #17  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:15:00  (verde)
  │     OHLC : O=0.58848  H=0.58890  L=0.58827  C=0.58851
  │     range=6.3 pips   corpo=5% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 62%  (min 30%)   [bot reportou 62%]
  │     [OK ] RSI(9)    : 95.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58851  SL=0.58940 (8.9 pips)  TP=0.58718 (13.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:27:12][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58851  SL:0.58940  TP:0.58718  pavio:62%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 95.8
   Wick     [##############]    25/25  (100.0%)  pavio 62%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 5% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.0/100  (+33.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 95.8 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 62% (wick 25.0), corpo 5% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #17: 0 aprovado(s) / 1 analisado(s)

[04:56:29] ciclo #18  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:45:00  (verde)
  │     OHLC : O=1.35322  H=1.35370  L=1.35309  C=1.35340
  │     range=6.1 pips   corpo=30% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 97.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35340  SL=1.35420 (8.0 pips)  TP=1.35220 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:56:30][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35340  SL:1.35420  TP:1.35220  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 97.7
   Wick     [##############]  24.6/25  ( 98.4%)  pavio 49%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 30% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.6/100  (+20.6 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 97.7 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 49% (wick 24.6), corpo 30% (pin 13.0) -> 37.6/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #18: 0 aprovado(s) / 1 analisado(s)

[04:56:51] ciclo #19  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 04:45:00  (vermelha)
  │     OHLC : O=0.78513  H=0.78515  L=0.78477  C=0.78496
  │     range=3.8 pips   corpo=45% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 0.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78496  SL=0.78427 (6.9 pips)  TP=0.78599 (10.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:56:52][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78496  SL:0.78427  TP:0.78599  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 0.0
   Wick     [##############]    25/25  (100.0%)  pavio 50%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 45% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.5/100  (+17.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 0.0 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 50% (wick 25.0), corpo 45% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #19: 0 aprovado(s) / 1 analisado(s)

[04:57:13] ciclo #20  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 04:45:00  (verde)
  │     OHLC : O=0.58881  H=0.58909  L=0.58868  C=0.58887
  │     range=4.1 pips   corpo=15% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 100.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=01h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58887  SL=0.58959 (7.2 pips)  TP=0.58779 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[04:57:13][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58887  SL:0.58959  TP:0.58779  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 100.0
   Wick     [##############]    25/25  (100.0%)  pavio 54%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 15% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.0/100  (+33.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 100.0 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 54% (wick 25.0), corpo 15% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #20: 0 aprovado(s) / 1 analisado(s)

[05:11:38] ciclo #21  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 05:00:00  (verde)
  │     OHLC : O=0.78496  H=0.78519  L=0.78480  C=0.78504
  │     range=3.9 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 41%  (min 30%)   [bot reportou 41%]
  │     [OK ] RSI(9)    : 5.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78504  SL=0.78430 (7.4 pips)  TP=0.78615 (11.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:11:38][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78504  SL:0.78430  TP:0.78615  pavio:41%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 5.1
   Wick     [###########---]  20.5/25  ( 82.0%)  pavio 41%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 20% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.0/100  (+19.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 5.1 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          74%  "Pavio 41% (wick 20.5), corpo 21% (pin 13.0) -> 33.5/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #21: 0 aprovado(s) / 1 analisado(s)

[05:26:27] ciclo #22  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 05:15:00  (verde)
  │     OHLC : O=1.35327  H=1.35363  L=1.35315  C=1.35328
  │     range=4.8 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 73%  (min 30%)   [bot reportou 73%]
  │     [OK ] RSI(9)    : 93.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35328  SL=1.35413 (8.5 pips)  TP=1.35201 (12.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:26:28][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35328  SL:1.35413  TP:1.35201  pavio:73%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 93.7
   Wick     [##############]    25/25  (100.0%)  pavio 73%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   83.0/100  (+28.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 93.7 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 73% (wick 25.0), corpo 2% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #22: 0 aprovado(s) / 1 analisado(s)

[05:26:49] ciclo #23  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 05:15:00  (vermelha)
  │     OHLC : O=0.78504  H=0.78507  L=0.78482  C=0.78501
  │     range=2.5 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 76%  (min 30%)   [bot reportou 76%]
  │     [OK ] RSI(9)    : 6.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78501  SL=0.78432 (6.9 pips)  TP=0.78604 (10.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:26:49][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78501  SL:0.78432  TP:0.78604  pavio:76%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 6.3
   Wick     [##############]    25/25  (100.0%)  pavio 76%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   85.5/100  (+30.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 6.3 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 76% (wick 25.0), corpo 12% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #23: 0 aprovado(s) / 1 analisado(s)

[05:27:10] ciclo #24  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 05:15:00  (vermelha)
  │     OHLC : O=0.58882  H=0.58896  L=0.58869  C=0.58878
  │     range=2.7 pips   corpo=15% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 52%  (min 30%)   [bot reportou 52%]
  │     [OK ] RSI(9)    : 94.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58878  SL=0.58946 (6.8 pips)  TP=0.58776 (10.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:27:11][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58878  SL:0.58946  TP:0.58776  pavio:52%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 94.4
   Wick     [##############]    25/25  (100.0%)  pavio 52%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 15% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.0/100  (+33.0 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 94.4 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 52% (wick 25.0), corpo 15% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #24: 0 aprovado(s) / 1 analisado(s)

[05:41:43] ciclo #25  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 05:30:00  (verde)
  │     OHLC : O=0.71690  H=0.71747  L=0.71688  C=0.71704
  │     range=5.9 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 73%  (min 30%)   [bot reportou 73%]
  │     [OK ] RSI(9)    : 96.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71704  SL=0.71797 (9.3 pips)  TP=0.71565 (13.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:41:44][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71704  SL:0.71797  TP:0.71565  pavio:73%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 96.8
   Wick     [##############]    25/25  (100.0%)  pavio 73%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 24% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (18T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   78.5/100  (+23.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 78.5/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 96.8 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 73% (wick 25.0), corpo 24% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 18T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #25: 1 aprovado(s) / 1 analisado(s)

[05:42:05] ciclo #26  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 05:30:00  (vermelha)
  │     OHLC : O=0.78501  H=0.78504  L=0.78478  C=0.78491
  │     range=2.6 pips   corpo=38% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 5.9    (cond <= 30)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78491  SL=0.78428 (6.3 pips)  TP=0.78585 (9.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:42:06][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78491  SL:0.78428  TP:0.78585  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 5.9
   Wick     [##############]    25/25  (100.0%)  pavio 50%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 38% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.5/100  (+17.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 5.9 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 50% (wick 25.0), corpo 38% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #26: 0 aprovado(s) / 1 analisado(s)

[05:42:27] ciclo #27  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 05:30:00  (verde)
  │     OHLC : O=0.58878  H=0.58926  L=0.58878  C=0.58903
  │     range=4.8 pips   corpo=52% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 48%  (min 30%)   [bot reportou 48%]
  │     [OK ] RSI(9)    : 95.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58903  SL=0.58976 (7.3 pips)  TP=0.58794 (10.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:42:27][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58903  SL:0.58976  TP:0.58794  pavio:48%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 95.0
   Wick     [#############-]  24.0/25  ( 96.0%)  pavio 48%
   PinBar   [##------------]   2.9/20  ( 14.5%)  corpo 52% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   69.9/100  (+14.9 pts vs mínimo 55)
   Pior critério: PinBar 2.9/20  (14% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 95.0 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          60%  "Pavio 48% (wick 24.0), corpo 52% (pin 2.9) -> 26.9/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #27: 0 aprovado(s) / 1 analisado(s)

[05:56:34] ciclo #28  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 05:45:00  (verde)
  │     OHLC : O=1.35372  H=1.35401  L=1.35370  C=1.35383
  │     range=3.1 pips   corpo=35% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 58%  (min 30%)   [bot reportou 58%]
  │     [OK ] RSI(9)    : 94.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35383  SL=1.35451 (6.8 pips)  TP=1.35281 (10.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:56:34][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35383  SL:1.35451  TP:1.35281  pavio:58%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 94.3
   Wick     [##############]    25/25  (100.0%)  pavio 58%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 36% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   70.0/100  (+15.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 94.3 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 58% (wick 25.0), corpo 35% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #28: 0 aprovado(s) / 1 analisado(s)

[05:56:56] ciclo #29  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 05:45:00  (vermelha)
  │     OHLC : O=0.78491  H=0.78494  L=0.78468  C=0.78482
  │     range=2.6 pips   corpo=35% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 6.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78482  SL=0.78418 (6.4 pips)  TP=0.78578 (9.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:56:56][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78482  SL:0.78418  TP:0.78578  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 6.1
   Wick     [##############]    25/25  (100.0%)  pavio 54%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 35% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.5/100  (+17.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 6.1 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          71%  "Pavio 54% (wick 25.0), corpo 35% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #29: 0 aprovado(s) / 1 analisado(s)

[05:57:17] ciclo #30  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 05:45:00  (verde)
  │     OHLC : O=0.58903  H=0.58926  L=0.58900  C=0.58917
  │     range=2.6 pips   corpo=54% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 35%  (min 30%)   [bot reportou 35%]
  │     [OK ] RSI(9)    : 94.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=02h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58917  SL=0.58976 (5.9 pips)  TP=0.58828 (8.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[05:57:17][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58917  SL:0.58976  TP:0.58828  pavio:35%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 94.2
   Wick     [##########----]  17.3/25  ( 69.2%)  pavio 35%
   PinBar   [##------------]   2.8/20  ( 14.0%)  corpo 54% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.1/100  (+8.1 pts vs mínimo 55)
   Pior critério: PinBar 2.8/20  (14% do máximo)
   → REJEITADO  —  Score 63.1 < 65 | fraco: Pin Bar 2.8/20
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 94.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          45%  "Pavio 35% (wick 17.3), corpo 54% (pin 2.8) -> 20.1/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #30: 0 aprovado(s) / 1 analisado(s)

[06:11:27] ciclo #31  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 06:00:00  (vermelha)
  │     OHLC : O=0.78482  H=0.78483  L=0.78455  C=0.78465
  │     range=2.8 pips   corpo=61% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 6.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78465  SL=0.78405 (6.0 pips)  TP=0.78555 (9.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:11:28][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78465  SL:0.78405  TP:0.78555  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 6.7
   Wick     [##########----]  17.9/25  ( 71.6%)  pavio 36%
   PinBar   [##------------]   2.4/20  ( 12.0%)  corpo 61% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.8/100  (+5.8 pts vs mínimo 55)
   Pior critério: PinBar 2.4/20  (12% do máximo)
   → REJEITADO  —  Score 60.8 < 65 | fraco: Pin Bar 2.4/20
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 6.7 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          45%  "Pavio 36% (wick 17.9), corpo 61% (pin 2.4) -> 20.3/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #31: 0 aprovado(s) / 1 analisado(s)

[06:26:34] ciclo #32  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 06:15:00  (verde)
  │     OHLC : O=1.35437  H=1.35446  L=1.35422  C=1.35437
  │     range=2.4 pips   corpo=0% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 37%  (min 30%)   [bot reportou 37%]
  │     [OK ] RSI(9)    : 92.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35437  SL=1.35496 (5.9 pips)  TP=1.35349 (8.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:26:34][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35437  SL:1.35496  TP:1.35349  pavio:37%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 92.9
   Wick     [##########----]  18.7/25  ( 74.8%)  pavio 37%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 0% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   76.7/100  (+21.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 92.9 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 37% (wick 18.7), corpo 0% (pin 20.0) -> 38.7/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #32: 0 aprovado(s) / 1 analisado(s)

[06:26:55] ciclo #33  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 06:15:00  (verde)
  │     OHLC : O=0.78465  H=0.78470  L=0.78458  C=0.78466
  │     range=1.2 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 58%  (min 30%)   [bot reportou 58%]
  │     [OK ] RSI(9)    : 10.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78466  SL=0.78408 (5.8 pips)  TP=0.78553 (8.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:26:56][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78466  SL:0.78408  TP:0.78553  pavio:58%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 10.6
   Wick     [##############]    25/25  (100.0%)  pavio 58%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   85.5/100  (+30.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 10.6 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 58% (wick 25.0), corpo 8% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #33: 0 aprovado(s) / 1 analisado(s)

[06:27:12] ciclo #34  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 06:15:00  (vermelha)
  │     OHLC : O=0.58934  H=0.58940  L=0.58922  C=0.58924
  │     range=1.8 pips   corpo=56% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 83.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58924  SL=0.58990 (6.6 pips)  TP=0.58825 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:27:12][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.58924  SL:0.58990  TP:0.58825  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  32.8/35  ( 93.7%)  RSI 83.3
   Wick     [#########-----]  16.7/25  ( 66.8%)  pavio 33%
   PinBar   [##------------]   2.7/20  ( 13.5%)  corpo 56% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   60.2/100  (+5.2 pts vs mínimo 55)
   Pior critério: PinBar 2.7/20  (14% do máximo)
   → REJEITADO  —  Score 60.2 < 65 | fraco: Pin Bar 2.7/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          94%  "RSI(9) 83.3 -> 32.8/35 pts. Gate: 70."
   [R] Rejeicao          43%  "Pavio 33% (wick 16.7), corpo 56% (pin 2.7) -> 19.4/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #34: 0 aprovado(s) / 1 analisado(s)

[06:56:36] ciclo #35  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 06:45:00  (vermelha)
  │     OHLC : O=1.35467  H=1.35484  L=1.35440  C=1.35441
  │     range=4.4 pips   corpo=59% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 80.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35441  SL=1.35534 (9.3 pips)  TP=1.35302 (13.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:56:36][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35441  SL:1.35534  TP:1.35302  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.6/35  ( 81.7%)  RSI 80.2
   Wick     [###########---]  19.3/25  ( 77.2%)  pavio 39%
   PinBar   [##------------]   2.5/20  ( 12.5%)  corpo 59% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   53.4/100  (-1.6 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 53.4 < 65 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          82%  "RSI(9) 80.2 -> 28.6/35 pts. Gate: 70."
   [R] Rejeicao          48%  "Pavio 39% (wick 19.3), corpo 59% (pin 2.5) -> 21.8/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #35: 0 aprovado(s) / 1 analisado(s)

[06:56:57] ciclo #36  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 06:45:00  (verde)
  │     OHLC : O=0.78445  H=0.78462  L=0.78437  C=0.78462
  │     range=2.5 pips   corpo=68% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 25.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=03h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78462  SL=0.78387 (7.5 pips)  TP=0.78574 (11.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[06:56:58][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78462  SL:0.78387  TP:0.78574  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  21.3/35  ( 60.9%)  RSI 25.2
   Wick     [#########-----]  16.0/25  ( 64.0%)  pavio 32%
   PinBar   [#-------------]   1.9/20  (  9.5%)  corpo 68% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#########-----------]   44.7/100  (-10.3 pts vs mínimo 55)
   Pior critério: PinBar 1.9/20  (10% do máximo)
   → REJEITADO  —  Score 44.7 < 65 | fraco: Pin Bar 1.9/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          61%  "RSI(9) 25.2 -> 21.3/35 pts. Gate: 30."
   [R] Rejeicao          40%  "Pavio 32% (wick 16.0), corpo 68% (pin 1.9) -> 17.9/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #36: 0 aprovado(s) / 1 analisado(s)

[07:11:33] ciclo #37  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 07:00:00  (vermelha)
  │     OHLC : O=0.78462  H=0.78467  L=0.78455  C=0.78459
  │     range=1.2 pips   corpo=25% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 33%  (min 30%)   [bot reportou 33%]
  │     [OK ] RSI(9)    : 29.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78459  SL=0.78405 (5.4 pips)  TP=0.78540 (8.1 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:11:33][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78459  SL:0.78405  TP:0.78540  pavio:33%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  16.0/35  ( 45.7%)  RSI 29.2
   Wick     [#########-----]  16.7/25  ( 66.8%)  pavio 33%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 25% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   51.2/100  (-3.8 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Score 51.2 < 65 | fraco: Sessão 3.0/15
   ────────────────────────────────────────────────────────────
   [M] Momentum          46%  "RSI(9) 29.2 -> 16.0/35 pts. Gate: 30."
   [R] Rejeicao          66%  "Pavio 33% (wick 16.7), corpo 25% (pin 13.0) -> 29.7/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #37: 0 aprovado(s) / 1 analisado(s)

[07:41:40] ciclo #38  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 07:30:00  (vermelha)
  │     OHLC : O=1.17305  H=1.17315  L=1.17286  C=1.17299
  │     range=2.9 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 34%  (min 30%)   [bot reportou 34%]
  │     [OK ] RSI(9)    : 73.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17299  SL=1.17365 (6.6 pips)  TP=1.17200 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:41:41][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✗ EURUSD SELL  @1.17299  SL:1.17365  TP:1.17200  pavio:34%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  19.1/35  ( 54.6%)  RSI 73.0
   Wick     [##########----]  17.2/25  ( 68.8%)  pavio 34%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 21% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##------------]   0.7/5  ( 14.0%)  WR 43%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   53.0/100  (-2.0 pts vs mínimo 55)
   Pior critério: Hist 0.7/5  (14% do máximo)
   → REJEITADO  —  Score 53.0 < 65 | fraco: Histórico 0.7/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          55%  "RSI(9) 73.0 -> 19.1/35 pts. Gate: 70."
   [R] Rejeicao          67%  "Pavio 34% (wick 17.2), corpo 21% (pin 13.0) -> 30.2/45 pts."
   [C] Contexto          18%  "Sessao Ásia (3.0), WR 30d 43% em 21T (0.7) -> 3.7/20 pts."
-------------------------------------------------------------------
  Ciclo #38: 0 aprovado(s) / 1 analisado(s)

[07:42:02] ciclo #39  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 07:30:00  (vermelha)
  │     OHLC : O=1.35449  H=1.35461  L=1.35440  C=1.35447
  │     range=2.1 pips   corpo=10% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 57%  (min 30%)   [bot reportou 57%]
  │     [OK ] RSI(9)    : 80.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35447  SL=1.35511 (6.4 pips)  TP=1.35351 (9.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:42:02][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35447  SL:1.35511  TP:1.35351  pavio:57%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.6/35  ( 81.7%)  RSI 80.2
   Wick     [##############]    25/25  (100.0%)  pavio 57%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 10% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   76.6/100  (+21.6 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          82%  "RSI(9) 80.2 -> 28.6/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 57% (wick 25.0), corpo 10% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #39: 0 aprovado(s) / 1 analisado(s)

[07:42:18] ciclo #40  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 07:30:00  (verde)
  │     OHLC : O=0.78443  H=0.78453  L=0.78434  C=0.78444
  │     range=1.9 pips   corpo=5% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 47%  (min 30%)   [bot reportou 47%]
  │     [OK ] RSI(9)    : 20.0    (cond <= 30)
  │     [OK ] Sessao UTC : h=04h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78444  SL=0.78384 (6.0 pips)  TP=0.78534 (9.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[07:42:19][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78444  SL:0.78384  TP:0.78534  pavio:47%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.3/35  ( 80.9%)  RSI 20.0
   Wick     [#############-]  23.7/25  ( 94.8%)  pavio 47%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 5% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   77.5/100  (+22.5 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com USDCAD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          81%  "RSI(9) 20.0 -> 28.3/35 pts. Gate: 30."
   [R] Rejeicao          97%  "Pavio 47% (wick 23.7), corpo 5% (pin 20.0) -> 43.7/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #40: 0 aprovado(s) / 1 analisado(s)

[08:41:25] ciclo #41  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 08:30:00  (vermelha)
  │     OHLC : O=0.58864  H=0.58867  L=0.58826  C=0.58842
  │     range=4.1 pips   corpo=54% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 39%  (min 30%)   [bot reportou 39%]
  │     [OK ] RSI(9)    : 24.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=05h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58842  SL=0.58776 (6.6 pips)  TP=0.58941 (9.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[08:41:26][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58842  SL:0.58776  TP:0.58941  pavio:39%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  22.9/35  ( 65.4%)  RSI 24.1
   Wick     [###########---]  19.5/25  ( 78.0%)  pavio 39%
   PinBar   [##------------]   2.8/20  ( 14.0%)  corpo 54% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   53.2/100  (-1.8 pts vs mínimo 55)
   Pior critério: PinBar 2.8/20  (14% do máximo)
   → REJEITADO  —  Score 53.2 < 65 | fraco: Pin Bar 2.8/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          65%  "RSI(9) 24.1 -> 22.9/35 pts. Gate: 30."
   [R] Rejeicao          50%  "Pavio 39% (wick 19.5), corpo 54% (pin 2.8) -> 22.3/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #41: 0 aprovado(s) / 1 analisado(s)

[09:11:29] ciclo #42  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:00:00  (vermelha)
  │     OHLC : O=1.17223  H=1.17229  L=1.17175  C=1.17192
  │     range=5.4 pips   corpo=57% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 17.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17192  SL=1.17125 (6.7 pips)  TP=1.17292 (10.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:11:29][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✗ EURUSD BUY  @1.17192  SL:1.17125  TP:1.17292  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  31.9/35  ( 91.1%)  RSI 17.3
   Wick     [#########-----]  15.7/25  ( 62.8%)  pavio 31%
   PinBar   [##------------]   2.6/20  ( 13.0%)  corpo 57% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##------------]   0.7/5  ( 14.0%)  WR 43%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   53.9/100  (-1.1 pts vs mínimo 55)
   Pior critério: PinBar 2.6/20  (13% do máximo)
   → REJEITADO  —  Score 53.9 < 65 | fraco: Pin Bar 2.6/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 17.3 -> 31.9/35 pts. Gate: 30."
   [R] Rejeicao          41%  "Pavio 31% (wick 15.7), corpo 57% (pin 2.6) -> 18.3/45 pts."
   [C] Contexto          18%  "Sessao Ásia (3.0), WR 30d 43% em 21T (0.7) -> 3.7/20 pts."
-------------------------------------------------------------------
  Ciclo #42: 0 aprovado(s) / 1 analisado(s)

[09:11:50] ciclo #43  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:00:00  (vermelha)
  │     OHLC : O=1.35331  H=1.35332  L=1.35251  C=1.35277
  │     range=8.1 pips   corpo=67% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 13.4    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35277  SL=1.35201 (7.6 pips)  TP=1.35391 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:11:51][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.35277  SL:1.35201  TP:1.35391  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 13.4
   Wick     [#########-----]  16.0/25  ( 64.0%)  pavio 32%
   PinBar   [#-------------]   2.0/20  ( 10.0%)  corpo 67% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   56.0/100  (+1.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 56.0 < 65 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 13.4 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          40%  "Pavio 32% (wick 16.0), corpo 67% (pin 2.0) -> 18.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #43: 0 aprovado(s) / 1 analisado(s)

[09:12:12] ciclo #44  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:00:00  (vermelha)
  │     OHLC : O=0.58835  H=0.58838  L=0.58787  C=0.58823
  │     range=5.1 pips   corpo=24% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 71%  (min 30%)   [bot reportou 71%]
  │     [OK ] RSI(9)    : 16.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58823  SL=0.58737 (8.6 pips)  TP=0.58952 (12.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:12:12][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58823  SL:0.58737  TP:0.58952  pavio:71%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.4/35  ( 95.4%)  RSI 16.2
   Wick     [##############]    25/25  (100.0%)  pavio 71%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 24% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.4/100  (+24.4 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          95%  "RSI(9) 16.2 -> 33.4/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 71% (wick 25.0), corpo 24% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #44: 0 aprovado(s) / 1 analisado(s)

[09:26:37] ciclo #45  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:15:00  (vermelha)
  │     OHLC : O=1.17192  H=1.17211  L=1.17165  C=1.17188
  │     range=4.6 pips   corpo=9% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 17.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17188  SL=1.17115 (7.3 pips)  TP=1.17297 (10.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:26:37][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD BUY  @1.17188  SL:1.17115  TP:1.17297  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  31.9/35  ( 91.1%)  RSI 17.3
   Wick     [##############]    25/25  (100.0%)  pavio 50%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 9% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##------------]   0.7/5  ( 14.0%)  WR 43%  (21T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   80.6/100  (+25.6 pts vs mínimo 55)
   Pior critério: Hist 0.7/5  (14% do máximo)
   → APROVADO  —  Score 80.6/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          91%  "RSI(9) 17.3 -> 31.9/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 50% (wick 25.0), corpo 9% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          18%  "Sessao Ásia (3.0), WR 30d 43% em 21T (0.7) -> 3.7/20 pts."
-------------------------------------------------------------------
  Ciclo #45: 1 aprovado(s) / 1 analisado(s)

[09:27:04] ciclo #46  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:15:00  (vermelha)
  │     OHLC : O=1.35277  H=1.35281  L=1.35242  C=1.35271
  │     range=3.9 pips   corpo=15% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 74%  (min 30%)   [bot reportou 74%]
  │     [OK ] RSI(9)    : 13.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35271  SL=1.35192 (7.9 pips)  TP=1.35390 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:27:04][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.35271  SL:1.35192  TP:1.35390  pavio:74%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 13.7
   Wick     [##############]    25/25  (100.0%)  pavio 74%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 15% range  [bom]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   76.0/100  (+21.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURGBP (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 13.7 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 74% (wick 25.0), corpo 15% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #46: 0 aprovado(s) / 1 analisado(s)

[09:27:20] ciclo #47  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 09:15:00  (verde)
  │     OHLC : O=0.78546  H=0.78567  L=0.78546  C=0.78559
  │     range=2.1 pips   corpo=62% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 38%  (min 30%)   [bot reportou 38%]
  │     [OK ] RSI(9)    : 84.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78559  SL=0.78617 (5.8 pips)  TP=0.78472 (8.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:27:20][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78559  SL:0.78617  TP:0.78472  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  34.6/35  ( 98.9%)  RSI 84.7
   Wick     [###########---]  19.0/25  ( 76.0%)  pavio 38%
   PinBar   [##------------]   2.3/20  ( 11.5%)  corpo 62% range  [suja]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.4/100  (+6.4 pts vs mínimo 55)
   Pior critério: PinBar 2.3/20  (12% do máximo)
   → REJEITADO  —  Score 61.4 < 65 | fraco: Pin Bar 2.3/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          99%  "RSI(9) 84.7 -> 34.6/35 pts. Gate: 70."
   [R] Rejeicao          47%  "Pavio 38% (wick 19.0), corpo 62% (pin 2.3) -> 21.3/45 pts."
   [C] Contexto          28%  "Sessao Ásia (3.0), WR 30d 50% em 6T (2.5) -> 5.5/20 pts."
-------------------------------------------------------------------
  Ciclo #47: 0 aprovado(s) / 1 analisado(s)

[09:27:41] ciclo #48  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:15:00  (vermelha)
  │     OHLC : O=0.58823  H=0.58834  L=0.58808  C=0.58821
  │     range=2.6 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 50%  (min 30%)   [bot reportou 50%]
  │     [OK ] RSI(9)    : 17.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.58821  SL=0.58758 (6.3 pips)  TP=0.58915 (9.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:27:42][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD BUY  @0.58821  SL:0.58758  TP:0.58915  pavio:50%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  31.3/35  ( 89.4%)  RSI 17.7
   Wick     [##############]    25/25  (100.0%)  pavio 50%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   84.3/100  (+29.3 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          89%  "RSI(9) 17.7 -> 31.3/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 50% (wick 25.0), corpo 8% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 64% em 14T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #48: 0 aprovado(s) / 1 analisado(s)

[09:41:30] ciclo #49  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 09:30:00  (verde)
  │     OHLC : O=1.35271  H=1.35332  L=1.35243  C=1.35311
  │     range=8.9 pips   corpo=45% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 21.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=06h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35311  SL=1.35193 (11.8 pips)  TP=1.35488 (17.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[09:41:30][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD BUY  @1.35311  SL:1.35193  TP:1.35488  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  26.7/35  ( 76.3%)  RSI 21.3
   Wick     [#########-----]  15.7/25  ( 62.8%)  pavio 31%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 45% range  [aceitável]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##########----------]   52.4/100  (-2.6 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 52.4 < 65 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          76%  "RSI(9) 21.3 -> 26.7/35 pts. Gate: 30."
   [R] Rejeicao          50%  "Pavio 31% (wick 15.7), corpo 45% (pin 7.0) -> 22.7/45 pts."
   [C] Contexto          15%  "Sessao Ásia (3.0), WR 30d 22% em 9T (0.0) -> 3.0/20 pts."
-------------------------------------------------------------------
  Ciclo #49: 0 aprovado(s) / 1 analisado(s)

[10:41:33] ciclo #50  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 10:30:00  (vermelha)
  │     OHLC : O=1.36478  H=1.36493  L=1.36452  C=1.36473
  │     range=4.1 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 51%  (min 30%)   [bot reportou 51%]
  │     [OK ] RSI(9)    : 22.6    (cond <= 30)
  │     [OK ] Sessao UTC : h=07h -> Ásia  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36473  SL=1.36402 (7.1 pips)  TP=1.36579 (10.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[10:41:33][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD BUY  @1.36473  SL:1.36402  TP:1.36579  pavio:51%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  24.8/35  ( 70.9%)  RSI 22.6
   Wick     [##############]    25/25  (100.0%)  pavio 51%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [###-----------]   3.0/15  ( 20.0%)  Ásia
   Hist     [##############]     5/5  (100.0%)  WR 69%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   77.8/100  (+22.8 pts vs mínimo 55)
   Pior critério: Sessao 3.0/15  (20% do máximo)
   → APROVADO  —  Score 77.8/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          71%  "RSI(9) 22.6 -> 24.8/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 51% (wick 25.0), corpo 12% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          40%  "Sessao Ásia (3.0), WR 30d 69% em 13T (5.0) -> 8.0/20 pts."
-------------------------------------------------------------------
  Ciclo #50: 1 aprovado(s) / 1 analisado(s)

[11:11:21] ciclo #51  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:00:00  (vermelha)
  │     OHLC : O=1.17438  H=1.17475  L=1.17395  C=1.17435
  │     range=8.0 pips   corpo=4% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 79.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.17435  SL=1.17525 (9.0 pips)  TP=1.17300 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:11:21][WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✓ EURUSD SELL  @1.17435  SL:1.17525  TP:1.17300  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  27.4/35  ( 78.3%)  RSI 79.3
   Wick     [#############-]  23.1/25  ( 92.4%)  pavio 46%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 4% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [####----------]   1.4/5  ( 28.0%)  WR 46%  (22T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   81.9/100  (+26.9 pts vs mínimo 55)
   Pior critério: Hist 1.4/5  (28% do máximo)
   → APROVADO  —  Score 81.9/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          78%  "RSI(9) 79.3 -> 27.4/35 pts. Gate: 70."
   [R] Rejeicao          96%  "Pavio 46% (wick 23.1), corpo 4% (pin 20.0) -> 43.1/45 pts."
   [C] Contexto          57%  "Sessao London (10.0), WR 30d 45% em 22T (1.4) -> 11.4/20 pts."
-------------------------------------------------------------------
  Ciclo #51: 1 aprovado(s) / 1 analisado(s)

[11:11:48] ciclo #52  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:00:00  (verde)
  │     OHLC : O=0.71768  H=0.71824  L=0.71737  C=0.71784
  │     range=8.7 pips   corpo=18% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 46%  (min 30%)   [bot reportou 46%]
  │     [OK ] RSI(9)    : 77.8    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71784  SL=0.71874 (9.0 pips)  TP=0.71649 (13.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:11:48][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71784  SL:0.71874  TP:0.71649  pavio:46%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  25.4/35  ( 72.6%)  RSI 77.8
   Wick     [#############-]  23.0/25  ( 92.0%)  pavio 46%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 18% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#####---------]   1.8/5  ( 36.0%)  WR 47%  (19T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   73.2/100  (+18.2 pts vs mínimo 55)
   Pior critério: Hist 1.8/5  (36% do máximo)
   → APROVADO  —  Score 73.2/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          73%  "RSI(9) 77.8 -> 25.4/35 pts. Gate: 70."
   [R] Rejeicao          80%  "Pavio 46% (wick 23.0), corpo 18% (pin 13.0) -> 36.0/45 pts."
   [C] Contexto          59%  "Sessao London (10.0), WR 30d 47% em 19T (1.8) -> 11.8/20 pts."
-------------------------------------------------------------------
  Ciclo #52: 1 aprovado(s) / 1 analisado(s)

[11:12:09] ciclo #53  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:00:00  (verde)
  │     OHLC : O=0.58978  H=0.59044  L=0.58963  C=0.59015
  │     range=8.1 pips   corpo=46% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 91.7    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.59015  SL=0.59094 (7.9 pips)  TP=0.58896 (11.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:12:09][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.59015  SL:0.59094  TP:0.58896  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 91.7
   Wick     [##########----]  17.9/25  ( 71.6%)  pavio 36%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 46% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   74.9/100  (+19.9 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 91.7 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          55%  "Pavio 36% (wick 17.9), corpo 46% (pin 7.0) -> 24.9/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 64% em 14T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #53: 0 aprovado(s) / 1 analisado(s)

[11:12:31] ciclo #54  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:00:00  (vermelha)
  │     OHLC : O=0.86699  H=0.86710  L=0.86683  C=0.86696
  │     range=2.7 pips   corpo=11% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 41%  (min 30%)   [bot reportou 41%]
  │     [OK ] RSI(9)    : 74.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86696  SL=0.86760 (6.4 pips)  TP=0.86600 (9.6 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:12:31][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP SELL  @0.86696  SL:0.86760  TP:0.86600  pavio:41%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  21.0/35  ( 60.0%)  RSI 74.5
   Wick     [###########---]  20.4/25  ( 81.6%)  pavio 41%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 11% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   72.9/100  (+17.9 pts vs mínimo 55)
   Pior critério: Hist 1.5/5  (30% do máximo)
   → APROVADO  —  Score 72.9/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          60%  "RSI(9) 74.5 -> 21.0/35 pts. Gate: 70."
   [R] Rejeicao          90%  "Pavio 41% (wick 20.4), corpo 11% (pin 20.0) -> 40.4/45 pts."
   [C] Contexto          57%  "Sessao London (10.0), WR 30d 46% em 13T (1.5) -> 11.5/20 pts."
-------------------------------------------------------------------
  Ciclo #54: 1 aprovado(s) / 1 analisado(s)

[11:26:40] ciclo #55  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 11:15:00  (vermelha)
  │     OHLC : O=0.78430  H=0.78441  L=0.78399  C=0.78412
  │     range=4.2 pips   corpo=43% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 31%  (min 30%)   [bot reportou 31%]
  │     [OK ] RSI(9)    : 23.2    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78412  SL=0.78349 (6.3 pips)  TP=0.78507 (9.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:26:41][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78412  SL:0.78349  TP:0.78507  pavio:31%
   ────────────────────────────────────────────────────────────
   RSI      [##########----]  24.1/35  ( 68.9%)  RSI 23.2
   Wick     [#########-----]  15.5/25  ( 62.0%)  pavio 31%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 43% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   59.1/100  (+4.1 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → REJEITADO  —  Score 59.1 < 65 | fraco: Pin Bar 7.0/20
   ────────────────────────────────────────────────────────────
   [M] Momentum          69%  "RSI(9) 23.2 -> 24.1/35 pts. Gate: 30."
   [R] Rejeicao          50%  "Pavio 31% (wick 15.5), corpo 43% (pin 7.0) -> 22.5/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 6T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #55: 0 aprovado(s) / 1 analisado(s)

[11:56:28] ciclo #56  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:45:00  (verde)
  │     OHLC : O=1.35510  H=1.35574  L=1.35510  C=1.35539
  │     range=6.4 pips   corpo=45% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 55%  (min 30%)   [bot reportou 55%]
  │     [OK ] RSI(9)    : 80.5    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35539  SL=1.35624 (8.5 pips)  TP=1.35411 (12.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:56:28][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35539  SL:1.35624  TP:1.35411  pavio:55%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.0/35  ( 82.9%)  RSI 80.5
   Wick     [##############]    25/25  (100.0%)  pavio 55%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 45% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   71.0/100  (+16.0 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          83%  "RSI(9) 80.5 -> 29.0/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 55% (wick 25.0), corpo 45% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #56: 0 aprovado(s) / 1 analisado(s)

[11:56:51] ciclo #57  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  AUDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:45:00  (verde)
  │     OHLC : O=0.71844  H=0.71898  L=0.71844  C=0.71879
  │     range=5.4 pips   corpo=65% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 35%  (min 30%)   [bot reportou 35%]
  │     [OK ] RSI(9)    : 99.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.71879  SL=0.71948 (6.9 pips)  TP=0.71776 (10.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:56:52][WAR_ROOM] [AUDUSD] ◈ signal_analysis:
   ✓ AUDUSD SELL  @0.71879  SL:0.71948  TP:0.71776  pavio:35%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 99.3
   Wick     [##########----]  17.6/25  ( 70.4%)  pavio 35%
   PinBar   [#-------------]   2.1/20  ( 10.5%)  corpo 65% range  [suja]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [###-----------]   1.2/5  ( 24.0%)  WR 45%  (20T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   65.9/100  (+10.9 pts vs mínimo 55)
   Pior critério: PinBar 2.1/20  (11% do máximo)
   → APROVADO  —  Score 65.9/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 99.3 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          44%  "Pavio 35% (wick 17.6), corpo 65% (pin 2.1) -> 19.7/45 pts."
   [C] Contexto          56%  "Sessao London (10.0), WR 30d 45% em 20T (1.2) -> 11.2/20 pts."
-------------------------------------------------------------------
  Ciclo #57: 1 aprovado(s) / 1 analisado(s)

[11:57:13] ciclo #58  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCAD BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 11:45:00  (verde)
  │     OHLC : O=1.36157  H=1.36171  L=1.36108  C=1.36168
  │     range=6.3 pips   corpo=17% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 78%  (min 30%)   [bot reportou 78%]
  │     [OK ] RSI(9)    : 2.3    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.36168  SL=1.36058 (11.0 pips)  TP=1.36333 (16.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:57:14][WAR_ROOM] [USDCAD] ◈ signal_analysis:
   ✓ USDCAD BUY  @1.36168  SL:1.36058  TP:1.36333  pavio:78%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 2.3
   Wick     [##############]    25/25  (100.0%)  pavio 78%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 18% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.0/100  (+33.0 pts vs mínimo 55)
   Pior critério: PinBar 13.0/20  (65% do máximo)
   → APROVADO  —  Score 88.0/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 2.3 -> 35.0/35 pts. Gate: 30."
   [R] Rejeicao          84%  "Pavio 78% (wick 25.0), corpo 17% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 64% em 14T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #58: 1 aprovado(s) / 1 analisado(s)

[11:57:36] ciclo #59  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 11:45:00  (vermelha)
  │     OHLC : O=0.78373  H=0.78379  L=0.78337  C=0.78356
  │     range=4.2 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 45%  (min 30%)   [bot reportou 45%]
  │     [OK ] RSI(9)    : 16.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78356  SL=0.78287 (6.9 pips)  TP=0.78459 (10.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:57:36][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78356  SL:0.78287  TP:0.78459  pavio:45%
   ────────────────────────────────────────────────────────────
   RSI      [#############-]  33.5/35  ( 95.7%)  RSI 16.1
   Wick     [#############-]  22.6/25  ( 90.4%)  pavio 45%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 40% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.6/100  (+20.6 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          96%  "RSI(9) 16.1 -> 33.5/35 pts. Gate: 30."
   [R] Rejeicao          66%  "Pavio 45% (wick 22.6), corpo 40% (pin 7.0) -> 29.6/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 6T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #59: 0 aprovado(s) / 1 analisado(s)

[11:57:57] ciclo #60  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:45:00  (verde)
  │     OHLC : O=0.59092  H=0.59135  L=0.59092  C=0.59109
  │     range=4.3 pips   corpo=40% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 60%  (min 30%)   [bot reportou 60%]
  │     [OK ] RSI(9)    : 100.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.59109  SL=0.59185 (7.6 pips)  TP=0.58995 (11.4 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:57:57][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.59109  SL:0.59185  TP:0.58995  pavio:60%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 100.0
   Wick     [##############]    25/25  (100.0%)  pavio 60%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 40% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   82.0/100  (+27.0 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 100.0 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          71%  "Pavio 60% (wick 25.0), corpo 40% (pin 7.0) -> 32.0/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 64% em 14T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #60: 0 aprovado(s) / 1 analisado(s)

[11:58:18] ciclo #61  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 11:45:00  (verde)
  │     OHLC : O=0.86672  H=0.86683  L=0.86667  C=0.86676
  │     range=1.6 pips   corpo=25% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 44%  (min 30%)   [bot reportou 44%]
  │     [OK ] RSI(9)    : 70.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=08h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86676  SL=0.86733 (5.7 pips)  TP=0.86591 (8.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[11:58:19][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✗ EURGBP SELL  @0.86676  SL:0.86733  TP:0.86591  pavio:44%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.0/35  ( 42.9%)  RSI 70.0
   Wick     [############--]  21.9/25  ( 87.6%)  pavio 44%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 25% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [############--------]   61.4/100  (+6.4 pts vs mínimo 55)
   Pior critério: Hist 1.5/5  (30% do máximo)
   → REJEITADO  —  Score 61.4 < 65 | fraco: Histórico 1.5/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          43%  "RSI(9) 70.0 -> 15.0/35 pts. Gate: 70."
   [R] Rejeicao          78%  "Pavio 44% (wick 21.9), corpo 25% (pin 13.0) -> 34.9/45 pts."
   [C] Contexto          57%  "Sessao London (10.0), WR 30d 46% em 13T (1.5) -> 11.5/20 pts."
-------------------------------------------------------------------
  Ciclo #61: 0 aprovado(s) / 1 analisado(s)

[12:41:32] ciclo #62  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 12:30:00  (verde)
  │     OHLC : O=0.78381  H=0.78403  L=0.78360  C=0.78390
  │     range=4.3 pips   corpo=21% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 49%  (min 30%)   [bot reportou 49%]
  │     [OK ] RSI(9)    : 24.7    (cond <= 30)
  │     [OK ] Sessao UTC : h=09h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78390  SL=0.78310 (8.0 pips)  TP=0.78510 (12.0 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[12:41:33][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF BUY  @0.78390  SL:0.78310  TP:0.78510  pavio:49%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  22.1/35  ( 63.1%)  RSI 24.7
   Wick     [##############]  24.4/25  ( 97.6%)  pavio 49%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 21% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   72.0/100  (+17.0 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          63%  "RSI(9) 24.7 -> 22.1/35 pts. Gate: 30."
   [R] Rejeicao          83%  "Pavio 49% (wick 24.4), corpo 21% (pin 13.0) -> 37.4/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 6T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #62: 0 aprovado(s) / 1 analisado(s)

[12:41:54] ciclo #63  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 12:30:00  (vermelha)
  │     OHLC : O=0.59109  H=0.59118  L=0.59093  C=0.59098
  │     range=2.5 pips   corpo=44% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 36%  (min 30%)   [bot reportou 36%]
  │     [OK ] RSI(9)    : 86.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=09h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.59098  SL=0.59168 (7.0 pips)  TP=0.58993 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[12:41:55][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.59098  SL:0.59168  TP:0.58993  pavio:36%
   ────────────────────────────────────────────────────────────
   RSI      [##############]  35.0/35  (100.0%)  RSI 86.2
   Wick     [##########----]  18.0/25  ( 72.0%)  pavio 36%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 44% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###############-----]   75.0/100  (+20.0 pts vs mínimo 55)
   Pior critério: PinBar 7.0/20  (35% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum         100%  "RSI(9) 86.2 -> 35.0/35 pts. Gate: 70."
   [R] Rejeicao          56%  "Pavio 36% (wick 18.0), corpo 44% (pin 7.0) -> 25.0/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 64% em 14T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #63: 0 aprovado(s) / 1 analisado(s)

[13:11:34] ciclo #64  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 13:00:00  (verde)
  │     OHLC : O=1.35503  H=1.35552  L=1.35489  C=1.35517
  │     range=6.3 pips   corpo=22% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 56%  (min 30%)   [bot reportou 56%]
  │     [OK ] RSI(9)    : 70.2    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35517  SL=1.35602 (8.5 pips)  TP=1.35390 (12.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:11:35][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35517  SL:1.35602  TP:1.35390  pavio:56%
   ────────────────────────────────────────────────────────────
   RSI      [######--------]  15.3/35  ( 43.7%)  RSI 70.2
   Wick     [##############]    25/25  (100.0%)  pavio 56%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 22% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.3/100  (+8.3 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 63.3 < 65 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          44%  "RSI(9) 70.2 -> 15.3/35 pts. Gate: 70."
   [R] Rejeicao          84%  "Pavio 56% (wick 25.0), corpo 22% (pin 13.0) -> 38.0/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #64: 0 aprovado(s) / 1 analisado(s)

[13:11:56] ciclo #65  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 13:00:00  (verde)
  │     OHLC : O=0.59094  H=0.59118  L=0.59090  C=0.59096
  │     range=2.8 pips   corpo=7% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 79%  (min 30%)   [bot reportou 79%]
  │     [OK ] RSI(9)    : 80.3    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.59096  SL=0.59168 (7.2 pips)  TP=0.58988 (10.8 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:11:57][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✗ NZDUSD SELL  @0.59096  SL:0.59168  TP:0.58988  pavio:79%
   ────────────────────────────────────────────────────────────
   RSI      [###########---]  28.7/35  ( 82.0%)  RSI 80.3
   Wick     [##############]    25/25  (100.0%)  pavio 79%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 7% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##################--]   88.7/100  (+33.7 pts vs mínimo 55)
   Pior critério: Sessao 10.0/15  (67% do máximo)
   → REJEITADO  —  Correlação com AUDUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          82%  "RSI(9) 80.3 -> 28.7/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 79% (wick 25.0), corpo 7% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 64% em 14T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #65: 0 aprovado(s) / 1 analisado(s)

[13:41:38] ciclo #66  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 13:30:00  (verde)
  │     OHLC : O=1.35560  H=1.35583  L=1.35540  C=1.35565
  │     range=4.3 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 42%  (min 30%)   [bot reportou 42%]
  │     [OK ] RSI(9)    : 71.4    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35565  SL=1.35633 (6.8 pips)  TP=1.35463 (10.2 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:41:38][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35565  SL:1.35633  TP:1.35463  pavio:42%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  16.8/35  ( 48.0%)  RSI 71.4
   Wick     [############--]  20.9/25  ( 83.6%)  pavio 42%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [##############------]   67.7/100  (+12.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          48%  "RSI(9) 71.4 -> 16.8/35 pts. Gate: 70."
   [R] Rejeicao          91%  "Pavio 42% (wick 20.9), corpo 12% (pin 20.0) -> 40.9/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #66: 0 aprovado(s) / 1 analisado(s)

[13:41:59] ciclo #67  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP BUY  |  zona: SUPORTE (rejeição inferior)
  │  Vela M15 fechada @ 2026-04-27 13:30:00  (verde)
  │     OHLC : O=0.86620  H=0.86631  L=0.86607  C=0.86622
  │     range=2.4 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick inferior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 19.1    (cond <= 30)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86622  SL=0.86557 (6.5 pips)  TP=0.86719 (9.7 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:42:00][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP BUY  @0.86622  SL:0.86557  TP:0.86719  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  29.5/35  ( 84.3%)  RSI 19.1
   Wick     [##############]    25/25  (100.0%)  pavio 54%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [####----------]   1.5/5  ( 30.0%)  WR 46%  (13T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   86.0/100  (+31.0 pts vs mínimo 55)
   Pior critério: Hist 1.5/5  (30% do máximo)
   → APROVADO  —  Score 86.0/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          84%  "RSI(9) 19.1 -> 29.5/35 pts. Gate: 30."
   [R] Rejeicao         100%  "Pavio 54% (wick 25.0), corpo 8% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          57%  "Sessao London (10.0), WR 30d 46% em 13T (1.5) -> 11.5/20 pts."
-------------------------------------------------------------------
  Ciclo #67: 1 aprovado(s) / 1 analisado(s)

[13:56:30] ciclo #68  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 13:45:00  (verde)
  │     OHLC : O=1.35565  H=1.35632  L=1.35555  C=1.35600
  │     range=7.7 pips   corpo=45% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 42%  (min 30%)   [bot reportou 42%]
  │     [OK ] RSI(9)    : 73.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=10h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35600  SL=1.35682 (8.2 pips)  TP=1.35477 (12.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[13:56:31][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35600  SL:1.35682  TP:1.35477  pavio:42%
   ────────────────────────────────────────────────────────────
   RSI      [########------]  18.9/35  ( 54.0%)  RSI 73.0
   Wick     [############--]  20.8/25  ( 83.2%)  pavio 42%
   PinBar   [#####---------]   7.0/20  ( 35.0%)  corpo 46% range  [aceitável]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [###########---------]   56.7/100  (+1.7 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 56.7 < 65 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          54%  "RSI(9) 73.0 -> 18.9/35 pts. Gate: 70."
   [R] Rejeicao          62%  "Pavio 42% (wick 20.8), corpo 45% (pin 7.0) -> 27.8/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #68: 0 aprovado(s) / 1 analisado(s)

[14:26:30] ciclo #69  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 14:15:00  (verde)
  │     OHLC : O=0.78443  H=0.78458  L=0.78421  C=0.78446
  │     range=3.7 pips   corpo=8% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 32%  (min 30%)   [bot reportou 32%]
  │     [OK ] RSI(9)    : 82.1    (cond >= 70)
  │     [OK ] Sessao UTC : h=11h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78446  SL=0.78508 (6.2 pips)  TP=0.78353 (9.3 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[14:26:30][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78446  SL:0.78508  TP:0.78353  pavio:32%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  31.2/35  ( 89.1%)  RSI 82.1
   Wick     [#########-----]  16.2/25  ( 64.8%)  pavio 32%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 8% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   79.9/100  (+24.9 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          89%  "RSI(9) 82.1 -> 31.2/35 pts. Gate: 70."
   [R] Rejeicao          80%  "Pavio 32% (wick 16.2), corpo 8% (pin 20.0) -> 36.2/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 6T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #69: 0 aprovado(s) / 1 analisado(s)

[14:56:30] ciclo #70  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  USDCHF SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 14:45:00  (vermelha)
  │     OHLC : O=0.78483  H=0.78498  L=0.78458  C=0.78478
  │     range=4.0 pips   corpo=12% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 38%  (min 30%)   [bot reportou 38%]
  │     [OK ] RSI(9)    : 81.9    (cond >= 70)
  │     [OK ] Sessao UTC : h=11h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.78478  SL=0.78548 (7.0 pips)  TP=0.78373 (10.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[14:56:31][WAR_ROOM] [USDCHF] ◈ signal_analysis:
   ✗ USDCHF SELL  @0.78478  SL:0.78548  TP:0.78373  pavio:38%
   ────────────────────────────────────────────────────────────
   RSI      [############--]  30.8/35  ( 88.0%)  RSI 81.9
   Wick     [###########---]  18.8/25  ( 75.2%)  pavio 38%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 12% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (6T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [################----]   82.1/100  (+27.1 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → REJEITADO  —  Correlação com EURUSD (posição ativa)
   ────────────────────────────────────────────────────────────
   [M] Momentum          88%  "RSI(9) 81.9 -> 30.8/35 pts. Gate: 70."
   [R] Rejeicao          86%  "Pavio 38% (wick 18.8), corpo 12% (pin 20.0) -> 38.8/45 pts."
   [C] Contexto          62%  "Sessao London (10.0), WR 30d 50% em 6T (2.5) -> 12.5/20 pts."
-------------------------------------------------------------------
  Ciclo #70: 0 aprovado(s) / 1 analisado(s)

[15:26:38] ciclo #71  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  GBPUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 15:15:00  (vermelha)
  │     OHLC : O=1.35708  H=1.35758  L=1.35642  C=1.35682
  │     range=11.6 pips   corpo=22% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 43%  (min 30%)   [bot reportou 43%]
  │     [OK ] RSI(9)    : 72.6    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=1.35682  SL=1.35808 (12.6 pips)  TP=1.35493 (18.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:26:38][WAR_ROOM] [GBPUSD] ◈ signal_analysis:
   ✗ GBPUSD SELL  @1.35682  SL:1.35808  TP:1.35493  pavio:43%
   ────────────────────────────────────────────────────────────
   RSI      [#######-------]  18.5/35  ( 52.9%)  RSI 72.6
   Wick     [############--]  21.6/25  ( 86.4%)  pavio 43%
   PinBar   [#########-----]  13.0/20  ( 65.0%)  corpo 22% range  [bom]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [--------------]     0/5  (  0.0%)  WR 22%  (9T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#############-------]   63.1/100  (+8.1 pts vs mínimo 55)
   Pior critério: Hist 0/5  (0% do máximo)
   → REJEITADO  —  Score 63.1 < 65 | fraco: Histórico 0.0/5
   ────────────────────────────────────────────────────────────
   [M] Momentum          53%  "RSI(9) 72.6 -> 18.5/35 pts. Gate: 70."
   [R] Rejeicao          77%  "Pavio 43% (wick 21.6), corpo 22% (pin 13.0) -> 34.6/45 pts."
   [C] Contexto          50%  "Sessao London (10.0), WR 30d 22% em 9T (0.0) -> 10.0/20 pts."
-------------------------------------------------------------------
  Ciclo #71: 0 aprovado(s) / 1 analisado(s)

[15:27:00] ciclo #72  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  NZDUSD SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 15:15:00  (verde)
  │     OHLC : O=0.59188  H=0.59216  L=0.59166  C=0.59189
  │     range=5.0 pips   corpo=2% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 54%  (min 30%)   [bot reportou 54%]
  │     [OK ] RSI(9)    : 76.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=12h -> London  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.59189  SL=0.59266 (7.7 pips)  TP=0.59074 (11.5 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[15:27:00][WAR_ROOM] [NZDUSD] ◈ signal_analysis:
   ✓ NZDUSD SELL  @0.59189  SL:0.59266  TP:0.59074  pavio:54%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  23.0/35  ( 65.7%)  RSI 76.0
   Wick     [##############]    25/25  (100.0%)  pavio 54%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 2% range  [perfeito]
   Sessao   [#########-----]  10.0/15  ( 66.7%)  London
   Hist     [##############]     5/5  (100.0%)  WR 64%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   83.0/100  (+28.0 pts vs mínimo 55)
   Pior critério: RSI 23.0/35  (66% do máximo)
   → APROVADO  —  Score 83.0/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          66%  "RSI(9) 76.0 -> 23.0/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 54% (wick 25.0), corpo 2% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          75%  "Sessao London (10.0), WR 30d 64% em 14T (5.0) -> 15.0/20 pts."
-------------------------------------------------------------------
  Ciclo #72: 1 aprovado(s) / 1 analisado(s)

[16:11:36] ciclo #73  --  1 sinal(is) recebido(s)
-------------------------------------------------------------------

  ┌── [FASE 1] STRATEGY FIRE  |  EURGBP SELL  |  zona: RESISTÊNCIA (rejeição superior)
  │  Vela M15 fechada @ 2026-04-27 16:00:00  (verde)
  │     OHLC : O=0.86682  H=0.86761  L=0.86666  C=0.86685
  │     range=9.5 pips   corpo=3% do range
  │
  │  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
  │     [OK ] Wick superior: 80%  (min 30%)   [bot reportou 80%]
  │     [OK ] RSI(9)    : 75.0    (cond >= 70)
  │     [OK ] Sessao UTC : h=13h -> London+NY overlap  (contexto)
  │
  │  Plano de trade enviado:
  │     entry=0.86685  SL=0.86811 (12.6 pips)  TP=0.86496 (18.9 pips)  RR=1.50
  └── decisao: gatilhos ATENDIDOS -> sinal enviado a War Room para [FASE 2] scoring


-------------------------------------------------------------------

[16:11:37][WAR_ROOM] [EURGBP] ◈ signal_analysis:
   ✓ EURGBP SELL  @0.86685  SL:0.86811  TP:0.86496  pavio:80%
   ────────────────────────────────────────────────────────────
   RSI      [#########-----]  21.7/35  ( 62.0%)  RSI 75.0
   Wick     [##############]    25/25  (100.0%)  pavio 80%
   PinBar   [##############]  20.0/20  (100.0%)  corpo 3% range  [perfeito]
   Sessao   [##############]  15.0/15  (100.0%)  London+NY overlap
   Hist     [#######-------]   2.5/5  ( 50.0%)  WR 50%  (14T / 30d)
   ────────────────────────────────────────────────────────────
   TOTAL   [#################---]   84.2/100  (+29.2 pts vs mínimo 55)
   Pior critério: Hist 2.5/5  (50% do máximo)
   → APROVADO  —  Score 84.2/65 → execução
   ────────────────────────────────────────────────────────────
   [M] Momentum          62%  "RSI(9) 75.0 -> 21.7/35 pts. Gate: 70."
   [R] Rejeicao         100%  "Pavio 80% (wick 25.0), corpo 3% (pin 20.0) -> 45.0/45 pts."
   [C] Contexto          88%  "Sessao London+NY overlap (15.0), WR 30d 50% em 14T (2.5) -> 17.5/20 pts."
-------------------------------------------------------------------
  Ciclo #73: 1 aprovado(s) / 1 analisado(s)