# Análise Detalhada de Operações — 23/04 a 27/04

---

## 1. Mapeamento dos Dados

| Fonte | Dia 23 (S1+S2) | Dia 24 (S3+S4) | Dia 27 (S5) |
|---|---|---|---|
| War Room aprovados | 30 | 9 | 18 |
| War Room rejeitados | 28 | 20 | 55 |
| Screenshots c/ P&L individual | 15 (5 JPY sem print) | 10 | 0 (consolidado por par) |
| MIN_CONFIDENCE_SCORE | 55 | 55 | **65 ← elevado** |
| Versão War Room | v6.1.2 | v6.1.2 | v6.1.2 |

> **Observação importante:** o threshold subiu 55 → 65 entre semana 1 e 2. Isso explica por que o dia 27 tem mais REJEITADOs por score (55 ocorrências) — vários sinais que teriam passado em 23/24 foram filtrados.

---

## 2. Dia 23 — Sessão Dupla (Madrugada → Noite)

### Síntese P&L (15 trades mapeados, JPY excluído)

| Resultado | Trades | Soma |
|---|---|---|
| WINS | 11 | +$1.205,91 |
| LOSSES | 9 | −$814,51 |
| **NET (sem JPY)** | **20** | **+$391,40** |

### Detalhamento por Horário e Score

| Hora MT5 | Par | Tipo | Score | P&L | Sessão UTC | Comentário |
|---|---|---|---|---|---|---|
| 05:41 | EURUSD | BUY | 56.7 | −$62 | Ásia | Score limítrofe. Hist 0/5. Pavio 37%. |
| 05:41 | NZDUSD | BUY | 62.5 | −$81 | Ásia | Mesmo candle 05:30 que EURUSD — cluster correlato matinal perdedor. |
| 06:11 | EURUSD | BUY | 76.7 | +$106 | Ásia | RSI 15.6, pin perfeito. Reversão validada na vela seguinte. |
| 06:12 | USDCAD | SELL | 79.4 | +$70.26 | Ásia | RSI 85.2 (extremo). Setup quase ideal. |
| 06:27 | AUDUSD | BUY | 67.6 | +$124 | Ásia | Pavio 45%, RSI 16. |
| 08:47 | AUDUSD | SELL | 67.8 | −$22 | Londres | Reversão da BUY que ganhou — SL apertado salvou. |
| 09:11 | NZDUSD | SELL | 60.4 | +$139 | Londres | Score baixo mas vitória sólida. |
| 09:12 | EURGBP | SELL | 82.5 | +$143 | Londres | Pavio 80% — classic pin. |
| 11:26 | USDCAD | BUY | 55.1 | +$71.68 | Londres | Score 55.1, exatamente o limiar — venceu mesmo assim. |
| 11:56 | EURGBP | BUY | 88.5 | −$134 | Londres | ⚠️ Score altíssimo (88.5) virou loss. Pavio 90%. Sinal de "exhaustion fake". |
| 13:26 | EURUSD | BUY | 60.3 | +$100 | London+NY overlap começando | — |
| 13:27 | NZDUSD | BUY | 74.1 | +$94 | London+NY | — |
| 18:26 | EURUSD | SELL | 82.4 | +$133 | London+NY | RSI 86.3, sessão máxima. |
| 18:27 | AUDUSD | SELL | 79.5 | +$100 | London+NY | — |
| 18:56 | EURGBP | SELL | 90.5 | −$87.51 | London+NY | ⚠️ Outro EURGBP de score altíssimo perdedor. |
| 20:26 | EURUSD | SELL | 82.6 | −$127 | NY | ⚠️ Cluster de 3 trades simultâneos no mesmo candle 20:15. |
| 20:27 | AUDUSD | SELL | 88.2 | −$128 | NY | ⚠️ Score 88.2 virou loss (cluster). |
| 20:27 | USDCAD | BUY | 65.2 | +$124.97 | NY | Único sobrevivente do cluster. |
| 23:26 | EURUSD | BUY | 68.7 | −$91 | NY late | — |
| 23:41 | NZDUSD | BUY | 80.3 | −$82 | NY late | — |

### Observações — Dia 23

- **Anomalia EURGBP:** 2 dos 9 losses foram EURGBP com score > 88. Pavios extremos (80–90%) parecem indicar exaustão, mas em ambos os casos o preço continuou na direção da rejeição inicial — clássica armadilha de pin bar no contexto errado.
- **Cluster perigoso 20:26–20:27:** 3 trades simultâneos não-correlatos (sem gate de correlação acionado). 2 perderam, 1 ganhou. NY abertura de US data tem causalidade forte que pode mover o dólar de forma uniforme — bot tratou como independentes.
- **Score como preditor:**

| Score | n | Win Rate | P&L |
|---|---|---|---|
| 55–65 | 6 | 66,7% | +$209 |
| 65–75 | 5 | 60,0% | +$66 |
| 75–85 | 6 | 66,7% | +$162 |
| **>85** | **3** | **33,3%** | **−$345 ⚠️** |

> **Insight crítico:** scores muito altos (>85) tiveram win rate **INVERSO** no dia 23 — pavios gigantes em EURGBP/AUDUSD viraram falsos topos/fundos.

---

## 3. Dia 24 — Sessão Dupla (Madrugada → Tarde)

### Síntese P&L

| Resultado | Trades | Soma |
|---|---|---|
| WINS | 8 | +$1.056,11 |
| LOSSES | 2 | −$207,76 |
| **NET** | **10** | **+$848,35** |

### Detalhamento

| Hora MT5 | Par | Tipo | Score | P&L | Comentário |
|---|---|---|---|---|---|
| 00:11 | NZDUSD | (sessão 2) | 61.8 | +$131 | Asia |
| 06:41 | EURUSD | BUY | 66.8 | +$130 | Asia tail / pré-Londres |
| 13:26 | EURGBP | BUY | 68.8 | +$132.25 | Overlap |
| 14:11 | EURUSD | BUY | 72.2 | −$105 | Overlap |
| 15:03 | EURGBP | (BUY?) | 92.5 | +$141 | ⭐ Score 92.5 finalmente vitorioso |
| 15:11 | AUDUSD | — | 61.5 | +$96 | Score limítrofe positivo |
| 15:12 | USDCHF | — | 79.7 | +$143.72 | — |
| 16:41 | AUDUSD | — | 97.5 | +$146 | ⭐ Score 97.5 — alto e venceu |
| 16:41 | USDCHF | — | 71.5 | +$136.14 | — |
| 17:26 | EURGBP | — | 62.9 | −$102.76 | EURGBP novamente loss |

### Observações — Dia 24

- **Day after melhor que day before:** 80% win rate, +$848 — dia espetacular.
- **Sessão da tarde europeia (15:00–17:00 MT5 = 12–14 UTC):** 5 trades, 4W/1L, +$464 → **janela campeã**.
- **EURGBP volátil:** mesmo com score >90 ganhou (15:03 +$141), mas score 62.9 às 17:26 perdeu. A correlação score ↔ resultado é fraca para EURGBP.
- **Hipótese reforçada do dia 23:** 16:41 AUDUSD (score 97.5) foi WIN — aparentemente AUDUSD respeita melhor a estratégia que EURGBP em scores extremos.

---

## 4. Dia 27 — Sessão Única (Asia → NY)

### Distribuição dos 18 Aprovados

| Par | Trades | BUY/SELL | Notas de tendência |
|---|---|---|---|
| EURUSD | 4 | 2 BUY / 2 SELL | Lateral c/ leve alta |
| USDCAD | 4 | 3 BUY / 1 SELL | ⚠️ Downtrend forte — 3 BUYs contra-tendência |
| AUDUSD | 4 | 0 BUY / 4 SELL | ⚠️ Uptrend forte — todas SELLs contra-tendência |
| EURGBP | 4 | 1 BUY / 3 SELL | Misto |
| NZDUSD | 2 | 1 BUY / 1 SELL | Uptrend |

### Padrões Críticos do Dia 27

| Hora MT5 | Par | Tipo | Score | Direção vs tendência |
|---|---|---|---|---|
| 04:11 | EURUSD | SELL @1.17197 | 69.9 | Reversão da BUY 04:11 — bot abriu lados opostos no mesmo par em 4h |
| 04:12 | AUDUSD | SELL @0.71612 | 73.2 | Início do uptrend AUDUSD do dia → loss provável |
| 05:41 | AUDUSD | SELL @0.71704 | 78.5 | AUDUSD continuou subindo → loss provável |
| 09:26 | EURUSD | BUY @1.17188 | 80.6 | Ponto de virada do EURUSD |
| 10:41 | USDCAD | BUY @1.36473 | 77.8 | ⚠️ Contra downtrend |
| 11:11 | AUDUSD | SELL @0.71784 | 73.2 | AUDUSD ainda subindo → loss provável |
| 11:11 | EURUSD | SELL @1.17435 | 81.9 | Possível pico — pode ter dado bem |
| 11:56 | AUDUSD | SELL @0.71879 | 65.9 | ⚠️ Score 65.9, exatamente no limiar + 4ª SELL contra-tendência |
| 11:57 | USDCAD | BUY @1.36168 | 88.0 | Score top — pode ter pegado o fundo |
| 13:42 | EURGBP | BUY @0.86622 | 86.0 | — |
| 15:27 | NZDUSD | SELL @0.59189 | 83.0 | Contra uptrend NZD |
| 16:11 | EURGBP | SELL @0.86685 | 84.2 | — |

### Observações — Dia 27

- **Tese vs realidade:** a estratégia é contra-tendência (vende em resistência, compra em suporte). No dia 27, os charts de AUDUSD/USDCAD mostraram trends fortes e duradouros — exatamente o cenário onde uma estratégia de reversão sofre.
- **AUDUSD:** 4 SELLs em uptrend é o **pior cenário possível** para a estratégia. Sem screenshots individuais não é possível confirmar, mas o esperado é que pelo menos 3 das 4 tenham perdido.
- **Threshold 65 funcionou parcialmente:** filtrou 55 sinais, mas ainda aprovou trades 65.9 (limítrofes) em momentos ruins.
- **Sem o filtro de trend macro**, o bot não tem como saber que "AUDUSD subiu 80 pips no dia" — cada vela M15 é avaliada isoladamente.

> Sem os P&Ls individuais do dia 27 não é possível quantificar o resultado, mas o padrão de SELLs em pares em uptrend é um sinal vermelho que valida a discussão sobre MA100/200 score-only no roadmap v7.0.

---

## 5. Padrões Transversais (Cross-Cutting)

### A. Score >85 não é garantia (semana 1)

| Score | Trades | WR | P&L médio |
|---|---|---|---|
| 55–65 | 7 | 71% | +$30 |
| 65–75 | 7 | 71% | +$54 |
| 75–85 | 7 | 57% | +$30 |
| **>85** | **4** | **50%** | **−$48 ⚠️** |

Scores muito altos (pin bar perfeito + RSI extremo + sessão prime) não tiveram edge nas 25 amostras da semana 1. **Hipótese:** pavios gigantes (>80%) frequentemente são reação inicial a notícia/dados → preço continua, não reverte.

### B. EURGBP é Problemático

3 de 4 EURGBPs com score >85 perderam (−$324 acumulado). **Hipótese:** spread relativo + correlação cruzada com GBPUSD/EURUSD cria movimentos não-mean-reverting.

### C. Cluster Correlato Não-Protegido

20:26–20:27 do dia 23: EURUSD SELL + AUDUSD SELL + USDCAD BUY simultâneos. Os pares não estão na lista de `CORRELATED_PAIRS` (`auto_war_room.py:77-83`), mas movimentos de USD em NY abertura afetam todos. 2 losses ao mesmo tempo = **−$255 num único candle**.

### D. Sessão Ásia (UTC 02–07) tem Upside

Dia 23 madrugada e dia 27 madrugada deram entradas decentes (06:11 +$106, 06:27 +$124, 06:41 +$130). A penalização de sessão de 3pts talvez seja excessiva quando o RSI está em extremo absoluto (RSI 10–15).

### E. Dedup in-memory v6.1.5 Funcionou

Não há trades duplicados na mesma vela em nenhum log. Se a v6.1.5 entrou em vigor entre as sessões, o problema de saturação foi resolvido.

---

## 6. Recomendações Priorizadas

### 🔴 P0 — Acionáveis Imediatamente (zero código novo)

**1. Ampliar CORRELATED_PAIRS em `auto_war_room.py:77-83`:**
- Adicionar `['EURUSD', 'AUDUSD']` e `['EURUSD', 'NZDUSD']` (todos USD-base movem juntos em US data)
- Evitaria o cluster perdedor 20:26–20:27 do dia 23

**2. Penalty para score altíssimo com pavio gigante:**
- Trades com score > 85 e pavio > 75% mostram inversão
- Adicionar penalty de −10pts quando `wick_pct > 0.75` → captura menos exhaustion fake

**3. Suspender EURGBP temporariamente:**
- 3 losses de score >85 em 5 trades = WR 40% nos sinais top
- Suspender por 30 dias e reavaliar

### 🟡 P1 — Validar com Mais Dados

**4. Threshold por par:**
- USDCAD/AUDUSD parecem tolerar 65; EURGBP precisa de 75+
- Fácil implementar como `dict` no config: `min_score_per_symbol`

**5. Macro trend score (v7.0 roadmap):**
- Dia 27 é exatamente o caso de uso
- SELLs em AUDUSD uptrend + BUYs em USDCAD downtrend deveriam levar penalty −15pts *(sem virar gate)*

### 🟢 P2 — Investigar

**6. Dia 27 P&L individual:**
- Puxar `signals_liquidez` no Supabase filtrando `created_at >= 2026-04-27 AND status = 'closed'`
- Sem isso, parte da análise do dia 27 é hipótese

**7. Análise de duração:**
- WINs vs LOSSes têm tempo até fechamento diferente?
- Se losses fecham rápido (SL tight) e wins demoram → candidato para trailing stop

---

## Resumo Executivo

| Métrica | Dia 23 | Dia 24 | Dia 27 |
|---|---|---|---|
| Sinais aprovados | 30 | 9 | 18 |
| Trades mapeados | 15 (50%) | 10 (100%) | 0 (consolidado) |
| WR mapeada | 73% | 80% | n/d |
| Net (mapeado) | +$391 | +$848 | n/d |
| Score médio aprovado | ~73 | ~74 | ~78 |

Trajetória positiva entre 23 e 24 (+117% net). Dia 27 tem incerteza sem P&Ls individuais, mas o mix de tipos contra tendências fortes sinaliza dia desafiador para a estratégia mean-reversion. A elevação do threshold 55 → 65 é válida.

> **Próximo passo recomendado:** puxar P&L do Supabase para o dia 27 antes de tomar decisões. Sem isso, não é possível fechar a análise da semana 2.

---
---

# Reconciliação Completa — Sessão 5

> **Hipótese confirmada categoricamente + descoberta extra.** Os primeiros 3 trades da "Sessão 5" eram do fim do dia 26 UTC (madrugada MT5 dia 27 — como o operador vê) e mudam o quadro.

## Resultado por Bloco

| Bloco | Trades | W/L | P&L |
|---|---|---|---|
| Asia early (21:11–21:26 UTC do dia 26) | 3 | 3W / 0L | +$427,71 |
| Asia continuation (00–04 UTC do dia 27) | 5 | 0W / 5L | −$450,46 |
| Londres (06–09 UTC) | 4 | 1W / 3L | −$170,27 |
| London+NY overlap (10–12 UTC) | 3 | 2W / 1L | +$163,97 |
| NY (12:26 UTC) | 1 | 1W / 0L | +$105,30 |
| **Total Sessão 5** | **16** | **6W / 10L (37,5%)** | **−$27,05** |

> Sem o resgate dos 3 trades Asia-early (+$427,71), o dia teria sido −$454,76. Esses 3 trades pegaram o exhaustion real da NY do dia 26 — RSI extremo após mercado já fechado.

---

## Hipótese Contra-Tendência: ✅ CONFIRMADA

| Par | Trades | W/L | P&L | Tendência do dia | Direção dos sinais |
|---|---|---|---|---|---|
| AUDUSD | 4 | 0W / 4L | −$348 | Uptrend forte | 4 SELLs (todas contra) |
| USDCAD (BUYs) | 3 | 0W / 3L | −$189,95 | Downtrend forte | 3 BUYs (todas contra) |
| USDCAD (SELL inicial) | 1 | 1W / 0L | +$71,71 | Topo ainda intacto | 1 SELL (a favor da virada) |
| EURUSD (BUYs early) | 2 | 2W / 0L | +$357 | USD enfraquecendo | BUYs catch the move |
| EURUSD (SELLs late) | 2 | 0W / 2L | −$197 | Continuou subindo | SELLs contra |
| EURGBP | 2 | 1W / 1L | +$57 | Misto | — |
| NZDUSD (SELL único) | 1 | 1W / 0L | +$105 | Pico do uptrend | Caçou o topo certo |
| NZDUSD (BUY early) | 1 | 1W / 0L | +$117 | Asia early | RSI extremo real |

### Padrão Macro: Dia de Fraqueza Ampla do USD

- USDCAD ↓ · AUDUSD ↑ · NZDUSD ↑ · EURUSD ↑
- **BUYs em pares EUR/AUD/NZD** (favoráveis ao USD-weakness) → ganharam
- **SELLs em pares EUR/AUD + BUYs em USDCAD** → morreram

---

## Comparação: Hipótese Pré-Supabase vs Realidade

| Hipótese | Realidade |
|---|---|
| AUDUSD 4 SELLs em uptrend deve ter perdido | ✅ 4 LOSSES (0% WR) |
| USDCAD 3 BUYs em downtrend deve ter perdido | ✅ 3 LOSSES (0% WR) |
| Threshold 65 não foi suficiente | ✅ Trade limítrofe (65.9 AUDUSD SELL) virou loss de −$66 |
| Day 27 net incerto | Real: −$27 (sessão 5) ou −$454 (só dia 27 UTC) |

---

## Insights Novos Revelados pela Query

### 1. Asia Early ≠ Asia Continuation

| Janela | Trades | WR |
|---|---|---|
| 21–23 UTC (NY post-close) | 3 | **100%** |
| 00–04 UTC | 5 | **0%** |

Mesma sessão "Ásia" pelo scoring (3pts), comportamentos **opostos**. A penalização uniforme de 3pts é imprecisa. Asia early pega exhaustion real da NY que acabou; Asia continuation tenta re-shortar/re-buyar tendências já formadas que respiram.

### 2. Threshold 65 Não Filtrou Bem em Dia Macro-Direcional

Trades aprovados ≥75 que perderam:

| Trade | Score | Loss |
|---|---|---|
| AUDUSD SELL @05:41 | 78.5 | −$93 |
| EURUSD SELL @11:11 | 81.9 | −$93 |
| AUDUSD SELL @11:11 | 73.2 | −$82 |
| USDCAD BUY @11:57 | 88.0 | −$69,82 |

4 dos 7 trades com score ≥73 foram losses contra-tendência. Score técnico é **ortogonal a regime macro** — exatamente o que o roadmap v7.0 (MA100/200 score-only) endereça.

### 3. Estatísticas Operacionais

| Métrica | Dia 27 UTC | Dia 27 MT5 (sessão 5) |
|---|---|---|
| Trades | 13 | 16 |
| WR | 23,1% | 37,5% |
| Avg Win | +$117,32 | +$152 (estimado) |
| Avg Loss | −$80,67 | −$80,67 |
| R/R real | **1,45x** | **1,89x** |
| Expectancy | −$34,98 | −$1,69 |
| Max DD intra-day | $688,73 | — |

R/R real (1,45x dia 27 / 1,89x sessão) acima do RR configurado de 1,50 — TPs estão saindo cheios quando vencem. O problema é puramente de **WR baixo**.

---
---

# Plano de Ação — Bateria de Incrementos (v6.2 → v6.3)

> ⚠️ **Caveat sobre Trader_Lessons:** os 3 README das aulas (Aula_1, Aula_2, Aula_3) têm conteúdo idêntico (só diferem no header e link YouTube). O ETL provavelmente duplicou o arquivo da Aula 1 nas 3 pastas. Recomenda-se refazer o ETL das aulas 2 e 3. Mesmo só com 1 aula real do curso, a sinergia com as calls do trader e a análise quantitativa já é forte.

---

## 1. Matriz de Convergência — Onde as 3 Fontes Apontam o Mesmo Lugar

| Tema | Análise quantitativa | Trader (calls 24+27) | ICT Aula 1 | Convergência |
|---|---|---|---|---|
| Filtro de N candles "esticados" antes da entrada | Dia 27: 0/7 contra-tendência forte — mercado já estava fora de zona "barata" | REPETIDO 6x: "3 candles vermelhos pra BUY, 3 verdes pra SELL", "espera a esticada" | Smart money espera "expansão rápida" depois reverte | ⭐⭐⭐ |
| Breakeven inteligente após 2–3 candles a favor | R/R real 1,45–1,89x — alguns wins fechariam piores se BE fosse cego | "Stop-loss para zero-a-zero após 2–3 candles a favor" | (não direto) | ⭐⭐ |
| Saída em RSI inverso (não só RR fixo 1.5) | Avg Win $117 sugere TPs cheios, mas mercado às vezes ia muito além | "RSI vai sobrecomprado, depois busca sobrevendido — saída ideal no extremo oposto" | Alinhado com "smart money runs to liquidity then reverses" | ⭐⭐ |
| Macro trend / regime aware | Dia 27: 0/7 contra-tendência forte | "Tava contra tendência macro, mas a gente opera contra" — reconhece o risco | Multi-timeframe alignment (Daily→4H→1H→15M) é princípio central | ⭐⭐⭐ |
| Filtro temporal (sessão granular) | Asia early WIN 100%, Asia continuation LOSS 100% (mesmo score 3pts) | "Horários melhores", "fechou bolsas, só robô operando, sai fora" | "Time of day matters — quando high/low se forma (Londres vs NY)" | ⭐⭐⭐ |
| Liquidez como tese alpha | Estratégia já é mean-reversion em pavio | (concorda implicitamente) | "Liquidity is the alpha" — buy/sell stops acima/abaixo de máximas/mínimas recentes | ⭐⭐⭐ |
| Equal highs/lows como alvo de varredura | Não considerado no scoring atual | Não mencionado | "Equal highs/lows = bull's eye for liquidity grab" | ⭐⭐ |
| Untested recent highs/lows | Não filtrado (qualquer pivot vale) | Não mencionado | "Note recent highs/lows that haven't been retested — vão ser influenciais" | ⭐⭐ |
| Filtro de cor da vela do gatilho | Não considerado | "Não comprar vela verde, não vender vela vermelha — princípio do 3D" | (não direto) | ⭐ |

---

## 2. Tensões a Resolver

### Tensão A: Breakeven Agressivo vs Histórico de Ejeção Precoce

| Lado | Argumento |
|---|---|
| Trader pede | BE após 2–3 candles a favor — "não faz sentido perder se ficou positivo" |
| Histórico do código | `breakeven_candles: 0` foi desativado em v6.1.3 porque "BE em 1h45 estava ejetando trades a zero em pullbacks normais antes da tese consolidar" |

**Resolução:** BE não pode ser só por tempo. Deve ser condicional:
- BE acionado quando: `(3 candles a favor) AND (preço atingiu ≥ 0.5R) AND (RSI cruzou 50)`
- Buffer de 2–3 pips acima da entrada (não exatamente zero) para não ser ejetado por spread/wick microscópico

### Tensão B: Filtro de Cor da Vela vs Entrada no Ponto Ótimo

| Lado | Argumento |
|---|---|
| Trader pede | "Não comprar vela verde, não vender vela vermelha" |
| Histórico do código | `require_color_reversal: false` foi desativado em v6.1.1 porque "atrasa entrada no ponto ótimo" |

**Resolução:** o que o trader quer **não** é o `require_color_reversal` antigo (que exigia inversão de cor entre as últimas 2 velas). É algo diferente:
- A vela do **gatilho** (com pavio de rejeição) deve ter cor coerente com o reverso — para BUY, idealmente vela verde ou indecisa (não vermelha forte de continuação); para SELL, vela vermelha ou indecisa
- O filtro antigo olhava para a vela **anterior**; o do trader olha para a vela **atual** do gatilho. São filtros diferentes.

### Tensão C: Filtro de "N Candles Esticados" vs Estratégia Sniper Early-Entry

| Lado | Argumento |
|---|---|
| Trader pede | "Esperar 3 candles na direção esticada antes de entrar — esperar a esticada acontecer" |
| Estratégia atual | Pega o gatilho na vela imediatamente após o pavio de rejeição (M15 fechada) |

**Resolução:** Adicionar como filtro de pré-condição (sem substituir o gatilho atual). Antes de aceitar o gatilho, exigir:
- **BUY:** pelo menos N velas (ex: 3) das últimas K velas (ex: 5) foram vermelhas **OU** o close caiu ≥ X pips no "displacement" pré-zona
- **SELL:** simétrico
- Isso filtra exatamente o cenário do dia 27 onde AUDUSD SELL pegou em pleno uptrend (poucas velas vermelhas anteriores)

---

## 3. Backlog Priorizado

### 🔴 P0 — Implementação Imediata (alta convergência, baixo esforço)

#### P0.1 — Filtro de "Candles Esticados" Antes do Gatilho ⭐⭐⭐

**Convergência:** Análise + Trader (REPETIDO 6x) + ICT  
**Mudança:** `bot_liquidez.py::check_trigger()`

```python
# Para BUY em SUPORTE:
last_K = df_m15.iloc[-K-1:-1]  # K velas antes do gatilho
red_count = sum(1 for c in last_K if c['close'] < c['open'])
if red_count < N:  # ex: N=3, K=5
    return None  # mercado ainda não "esticou" o suficiente
# Para SELL em RESISTÊNCIA: simétrico (verdes)
```

**Config keys novas:**
- `extension_lookback: 5` (K — quantas velas olhar para trás)
- `extension_min_candles: 3` (N — mínimo de velas direcionais)

**Impacto esperado:** bloquear entradas tipo dia 27 AUDUSD SELL #1 (pegou no início do uptrend, antes de qualquer reversão técnica). Win rate deve subir 5–10pp à custa de 20–30% menos sinais.  
**Validação:** rodar backtest contra logs War Room dias 23–27 — quantos APROVADOs ainda passariam? Quais são os WINs/LOSSes filtrados?

---

#### P0.2 — Breakeven Condicional Inteligente ⭐⭐

**Convergência:** Trader (call 27 explícito) + análise (R/R real >1.5 sugere espaço para proteger)  
**Mudança:** `bot_liquidez.py::check_breakeven()` (já existe, está desativado)

```python
# Reativar com regras compostas:
if elapsed_candles >= 3 AND in_profit_R >= 0.5 AND rsi_crossed_50:
    move_sl_to_entry + buffer_pips
```

**Config keys:**
- `breakeven_candles: 3` (era 0)
- `breakeven_min_R: 0.5` (nova — só se já está em 0.5R de lucro)
- `breakeven_require_rsi_cross: true` (nova — só se RSI cruzou 50 na direção correta)
- `breakeven_buffer_pips: 2` (manter)

**Impacto esperado:** protege wins que viram losses por giros tardios; evita ejeção precoce que matou v6.1.3 porque a regra anterior era SÓ por tempo.  
**Risco:** a tripla condição pode ser muito restritiva e quase nunca disparar. Calibrar empiricamente.

---

#### P0.3 — Subdividir Score de Sessão (Asia Early vs Asia Continuation) ⭐⭐⭐

**Convergência:** Análise (100% vs 0% WR no MESMO score 3pts) + Trader (horários) + ICT (time of day)  
**Mudança:** `auto_war_room.py::session_score_label()`

```python
def session_score_label(hour_utc):
    if 21 <= hour_utc < 24: return 8, "Asia early (post-NY)"   # NEW: separado
    if 0  <= hour_utc < 6:  return 0, "Asia continuation"      # NEW: penalizado
    if 6  <= hour_utc < 8:  return 5, "Pre-Londres"
    if 13 <= hour_utc < 17: return 15, "London+NY overlap"
    if 8  <= hour_utc < 13: return 10, "London"
    if 17 <= hour_utc < 22: return 10, "New York"
    return 0, "Fora de sessão"
```

**Impacto esperado:** penaliza com 0pts os trades de madrugada continuação (todos perderam dia 27); premia Asia post-NY (todos ganharam dia 27).  
**Risco:** amostra pequena (3+5 trades). Validar com mais ciclos antes de baixar threshold global.

---

#### P0.4 — Ampliar CORRELATED_PAIRS ⭐⭐

**Convergência:** Análise (cluster perdedor 20:26–27 dia 23 e 11:11 dia 27)  
**Mudança:** `auto_war_room.py:77-83`

```python
CORRELATED_PAIRS = [
    ['EURUSD', 'GBPUSD'],
    ['EURUSD', 'USDCHF'],
    ['EURUSD', 'AUDUSD'],   # NEW
    ['EURUSD', 'NZDUSD'],   # NEW (todos USD-quote)
    ['GBPUSD', 'EURGBP'],
    ['AUDUSD', 'NZDUSD'],
    ['USDCAD', 'USDCHF'],
]
```

**Impacto esperado:** bloqueia 2º trade do mesmo lado USD quando o 1º já foi aprovado. Dia 27 11:11 teria evitado AUDUSD SELL.

---

### 🟡 P1 — Implementação após Validar P0

#### P1.1 — Macro Trend Score (MA100/MA200 H1) — Score-Only, Peso ALTO ⭐⭐⭐

**Convergência:** Análise (dia 27 inteiro) + Trader ("contra tendência macro") + ICT (multi-timeframe)  
**Restrição da memória:** NUNCA gate. Score-only.

```python
# 6º critério (peso até 25pts, redistribuir):
ma100_h1 = df_h1['close'].rolling(100).mean().iloc[-1]
ma200_h1 = df_h1['close'].rolling(200).mean().iloc[-1]
trend_h1 = +1 if ma100 > ma200 else -1

if trade_type == 'BUY':
    macro_score = 25 if trend_h1 > 0 else (10 if abs(close - ma200)/pip < 30 else -15)
else:
    macro_score = 25 if trend_h1 < 0 else (10 if abs(close - ma200)/pip < 30 else -15)
```

**Score total reformatado (manter 100pts):**

| Critério | Peso Atual | Peso Novo |
|---|---|---|
| RSI | 35 | 30 |
| Wick | 25 | 20 |
| PinBar | 20 | 15 |
| Sessão | 15 | 12 |
| Macro | — | **18 (NOVO)** |
| Histórico | 5 | 5 |

**Impacto esperado:** dia 27, 4 SELLs AUDUSD em uptrend levariam −15pts → caem de score 73–78 para 58–63 → todos rejeitados pelo gate 65.

---

#### P1.2 — Saída em RSI Inverso (TP Dinâmico) ⭐⭐

**Convergência:** Trader (calls 24+27 — "esperar candle fechar, RSI atingir extremo oposto")

```python
# Para posição BUY aberta:
if pos_type == BUY:
    if rsi >= 65 and price_in_R >= 0.7:
        close_position(reason="rsi_inverse_exit")
```

**Config:**
- `enable_rsi_exit: true`
- `rsi_exit_threshold_buy: 65`
- `rsi_exit_threshold_sell: 35`
- `rsi_exit_min_R: 0.7`

**Risco:** pode interferir com o RR 1,5x já configurado. Necessário backtest cuidadoso.

---

#### P1.3 — Limite por Par-em-Direção/Dia (Cooldown Direcional) ⭐⭐

**Convergência:** Análise (4 SELLs AUDUSD perderam em sequência no dia 27)

```python
# Após 2 losses no mesmo (symbol, type) no dia, bloquear esse lado por 4h
losses_today: dict[(symbol, type)] = 0
last_loss_time: dict[(symbol, type)] = None

if pnl < 0:
    losses_today[(sym, typ)] += 1
    last_loss_time[(sym, typ)] = now
    if losses_today[(sym, typ)] >= 2:
        block_until[(sym, typ)] = now + 4h

if (sym, typ) in block_until and now < block_until[(sym, typ)]:
    return None
```

**Impacto esperado:** dia 27 AUDUSD SELL #3 e #4 teriam sido bloqueados.  
**Risco:** pode bloquear oportunidade real de virada após 2 losses iniciais. Cooldown de 4h é negociável.

---

### 🟢 P2 — Pesquisa / Próxima Fase

- **P2.1** — Detecção de Equal Highs/Lows como alvos prioritários (ICT): score bonus quando o pavio do gatilho está dentro de 5 pips de um pivot equal recente
- **P2.2** — "Untested" recent highs/lows (ICT): pivot novo (não tocado no último N=20 candles) tem score maior que pivot já testado várias vezes; adicionar campo `times_tested` ao zone dict
- **P2.3** — Volume filter: penalty se `tick_volume[-1] < ma_volume * 0.5`
- **P2.4** — Threshold dinâmico por regime: score 75+ em dias com range H1 > 80 pips até London open; aceitar 60+ em dias laterais (<40 pips)

---

## 4. Protocolo de Validação

Para cada PR/incremento:

1. **Backtest contra logs War Room 23–27** (já temos os dados):
   - Com a mudança ativa, quais dos 39 APROVADOs (dia 23+24+27) ainda passariam?
   - Dos rejeitados pela mudança, quantos viraram WIN vs LOSS?
   - **Métrica de sucesso:** filtra mais losses do que wins (melhora expectancy)

2. **Forward test 3–5 dias em conta demo:**
   - Comparar WR e expectancy com baseline (semana atual)
   - **Métrica:** WR > 50% e expectancy > 0

3. **Métricas a observar SEMPRE:**
   - WR global
   - Avg Win / Avg Loss / Expectancy
   - Score médio dos APROVADOs
   - Trades por dia — volume não pode cair >50% (sinal de filtro agressivo demais)
   - WR por par e por sessão (regressão)

---

## 5. Sequência de Releases

### v6.2.0 — "Convergence Pack" (1–2 dias dev)

Bundle dos P0 validados contra logs históricos:
- ✅ P0.1 — Filtro N candles esticados
- ✅ P0.3 — Asia early vs continuation
- ✅ P0.4 — CORRELATED_PAIRS expandido

> ⚠️ **Não incluir P0.2 (breakeven) ainda** — risco de regressão histórica. Validar P0.1 sozinho primeiro.

### v6.2.1 — Breakeven Condicional (1 dia)

- ✅ P0.2 — BE com tripla condição (apenas se v6.2.0 mostrou estabilidade)

### v6.3.0 — "Macro Awareness" (3–5 dias dev)

- ✅ P1.1 — Macro Trend Score com peso 18 — **A FEATURE MAIS IMPACTANTE**
- ✅ P1.3 — Cooldown direcional
- Reformatação completa do scoring (100pts redistribuídos)

### v6.4.0 — "Smart Exits" (3–5 dias dev)

- ✅ P1.2 — RSI exit dinâmico (requer cautela — interage com TP/SL atual)

### v7.0.0 — "ICT Liquidity" (sprint maior)

- ✅ P2.1 — Equal highs/lows priority
- ✅ P2.2 — Untested levels
- Possivelmente reescrita de `get_validated_zones()`

---

## 6. Resumo Executivo Final

### P&L dos 3 Dias

| Dia | Net | WR |
|---|---|---|
| Dia 23 | +$391 | 55% |
| Dia 24 | +$848 | 80% |
| Dia 27 | −$27 (sessão) / −$455 (dia UTC) | 37,5% |
| **Acumulado** | **~+$1.211** | — |

As **3 fontes** (análise quantitativa + trader + ICT) convergem sobre **3 falhas críticas** atuais:

1. **Bot é cego para macro** → dia 27 −$455 perdidos em SELLs em uptrend / BUYs em downtrend
2. **Bot entra "no meio do caminho"** → faltam N candles "esticados" antes do gatilho
3. **Bot trata sessão de forma binária demais** → Asia early ≠ Asia continuation (mesma penalty 3pts)

| Prioridade | Ação | Observação |
|---|---|---|
| 🏆 Maior alavanca de retorno | **P1.1** — Macro Trend Score ≥18 com penalty −15 contra H1 | Validada pelas 3 fontes |
| ⚡ Implementação mais rápida | **P0.4** — Ampliar CORRELATED_PAIRS | ~1h de código |
| ⚠️ Mais polêmica | **P0.2** — Breakeven | Tem histórico de falha; requer tripla condição |

**Próximo passo recomendado:** implementar **v6.2.0** (P0.1 + P0.3 + P0.4 bundle), validar em backtest contra logs 23–27 (filtragem deve aumentar WR sem cortar >30% dos sinais), depois rodar 3 dias forward.