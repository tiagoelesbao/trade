# Trade Liquidez — Estratégia v6.2.0-ict

---

## 1. Filosofia

**Mean-reversion em zonas de liquidez institucional**, com filtragem multi-camada baseada em metodologia ICT (Inner Circle Trader).

A entrada é simples (zona + pavio + RSI extremo). A sofisticação está nos **gates defensivos** que decidem se o gatilho deve virar trade, e nas **regras dinâmicas de saída** que substituem o BE estático tradicional.

### Princípios

1. **Gatilho M15** — decisões em fechamento de velas de 15min, filtrando ruído de timeframes menores.
2. **Defesa em camadas** — bot bloqueia primeiro (eficiência), War Room bloqueia depois (auditoria), Exit War Room ajusta saída (gestão de risco).
3. **ICT como contexto, não como gate (exceto CLIFF)** — score 0-25 pts compõe o total. Bloqueio só ocorre no caso catastrófico (alignment 0/25).
4. **Config como lei** — todos os filtros lidos de `config.yaml`. Nada hardcoded.
5. **Sem invenção** — toda regra documentada veio de observação empírica (cluster 28/04, RSI Wilder vs SMA divergente, USDCHF cluster 30/04).

---

## 2. Detecção de Zona (`get_validated_zones`)

| Parâmetro | Valor |
|-----------|-------|
| Timeframe | M15 |
| Lookback | 100 candles |
| Confirmação | 7 candles de afastamento |
| Tipo | Resistência (max local) e Suporte (min local) |

Resistência: máxima com 7 candles seguintes abaixo. Suporte: simétrico.

---

## 3. Gatilho de Entrada — `check_trigger`

Sequência de gates (early-exit em qualquer falha):

### Gate 1 — Horário (`is_entry_blocked_by_time`)

| Condição | Bloqueio |
|----------|----------|
| `news_embargo_pause: true` E UTC ∈ [13, 14) | News embargo (NY 8:00-8:59 release + reaction) |
| Hora MT5 ≥ `entry_cutoff_hour_mt5` (22) | End-of-day cutoff (= 19 UTC, ICT end-of-day consolidation) |

Posições já abertas continuam sob gestão do Exit War Room.

### Gate 2 — Range mínimo da vela

```yaml
min_candle_range_pips: 3.0
```

Bloqueia gatilhos em vela morta de Asia early (range < 3 pips) onde RSI fica errático — qualquer micro-movimento vira "extremo".

### Gate 3 — ICT CLIFF (`is_entry_blocked_by_ict_cliff`)

Bloqueia se `trade_alignment_score(BUY|SELL) == 0/25`. Caso CLIFF é específico:
**trade contra daily bias D1 + H4 em expansion contrária forte** = entrar contra "willingness to reveal pricing model" (Aula 1 ICT). Mesmo princípio do "don't catch a falling knife".

> Memória atualizada: macro/ICT em geral é **score-only**, mas o CLIFF é a única exceção autorizada para virar gate. Indicadores simples (MA100/200, slopes) seguem proibidos como gate.

### Gate 4 — Cooldown direcional

Bloqueia (symbol, direction) por `cooldown_hours_after_loss` (4h) após loss > `cooldown_min_loss_pnl` (-$10).

Origem: cluster USDCHF 30/04 — 3 BUYs consecutivos com loss em 2h, 4ª tentativa (após 4h) foi WIN. Cooldown teria evitado 3 losses (-$353) e capturado o win (+$66) = economia de **+$176**.

### Gatilho técnico (após gates)

| Filtro | Condição SELL | Condição BUY |
|--------|---------------|--------------|
| Wick Rejection | Pavio superior ≥ `min_wick_pct` (30%) | Pavio inferior ≥ 30% |
| RSI Guard | RSI(14) ≥ `rsi_overbought` (70) | RSI(14) ≤ `rsi_oversold` (30) |
| Zona Tocada | Preço tocou resistência M15 | Preço tocou suporte M15 |

**RSI calculado com Wilder's SMMA** (`ewm(alpha=1/14, adjust=False)`) — alinhado com MT5 default. Antes (até v6.2.0 Sprint 5) usava SMA simples, causando divergência de 20-40pts vs chart após spike.

### Plano de trade

```
SL  = high/low_pavio ± stop_buffer_points × point   (50 pts = 5 pips)
TP  = entry ± distância_SL × risk_reward_ratio       (1.5)
```

---

## 4. Decisão Agêntica — Scoring War Room

### 4.1 Pool-then-Pick (Sprint 3)

Quando War Room detecta sinais pendentes, **abre janela de 30s** com poll de 3s. Sinais correlatos que chegam durante a janela entram no mesmo pool.

**Por quê:** cluster 28/04 10:56 UTC tinha 3 sinais correlatos (AUDUSD/EURUSD/USDCAD) que chegavam separados por 20-40s. First-Match-Approve aprovava o primeiro arbitrariamente; Pool-then-Pick aplica tie-breaker informado.

### 4.2 Scoring (6 critérios, max 100 pts)

| Critério | Peso | Cálculo |
|----------|------|---------|
| **RSI Extremo** | 25 | Distância vs limite. RSI 70/30 → 11; 80/20 → 20; 85+/15- → 25 |
| **Wick %** | 20 | 30% → 12 pts; 50%+ → 20 pts |
| **Pin Bar** | 15 | corpo ≤15% range → 15; 30% → 10; 50% → 5; >50% penaliza |
| **Sessão ICT** | 10 | London open (14pts→10 escalado), NY open (13→8.7), London cont (11→7.3), Asia early (8→5.3), end-of-day (7→4.7), Asia/Judas (1→0.7), embargo (0) |
| **ICT Macro** | 25 | Closure do `ict_context_engine.trade_alignment_score`. 0=CLIFF; 25=a-favor + H4 expansion alinhada |
| **Histórico** | 5 | WR 30 dias do símbolo: 40% → 0; 60% → 5 |

### 4.3 Tie-breaker (cluster decision)

Ordenação: `(ict_alignment, total_score, wick_pct_real)` desc.

Greedy: itera do melhor pro pior.
- Item livre → vira **winner**
- Correlatos restantes → marcados como **PRETERIDO_CLUSTER** com motivo (`perdeu para X (ICT N vs M, score X.X vs Y.Y)`)

**Por que ICT antes do score:** cluster 28/04 mostrou que aprovar pelo "maior score técnico" sem ICT awareness deixa passar trades contra-trend macro.

### 4.4 Verdictos possíveis

| Verdito | Quando |
|---------|--------|
| `APROVADO` | Score ≥ `min_confidence_score`, ICT > 0, sem correlação com posições abertas, winner do cluster |
| `REJEITADO_COOLDOWN` | Cooldown ativo (defesa em 2ª camada) |
| `REJEITADO_CLIFF` | ICT alignment == 0/25 |
| `PRETERIDO_CLUSTER` | Perdeu tie-breaker para correlato com ICT/score melhor |
| `REJEITADO` | Score < min OU correlação com posição aberta no MT5 |

Aprova **1 winner por ciclo**.

---

## 5. Execução

```yaml
lot_size: 1.0
stop_buffer_points: 50    # 5 pips, absorve sweep institucional típico
risk_reward_ratio: 1.5    # TP = 1.5x SL
filling_mode: FOK         # Fill-or-Kill, cancela se preço mudou
```

Rastreamento por `position_id` (ticket MT5) — chave única anti-duplicata.

---

## 6. Gestão de Saída — Exit War Room (regras a-f)

Loop a cada `monitor_interval_seconds: 10`. Cada regra tem feature flag em `config.yaml/exit_war_room`. Primeira regra que matchar vence (ordem de prioridade):

| Regra | Trigger | Ação | Flag |
|-------|---------|------|------|
| **a** | profit ≥ 1.0R | BE imediato | `enable_be_at_1R` |
| **b** | profit ≥ 0.7R + reversal candle ICT | close 50% + BE | `enable_partial_at_07R_reversal` |
| **c** | profit ≥ 0.5R + 3 candles + RSI cruzou 50 | BE clássico | `enable_classic_be` |
| **d** | profit > 0 + ≤3 pips de liquidity oposto | close cedo (raid completo) | `enable_liquidity_target_close` |
| **e** | profit < 0 + ICT structure contra (BOS ou trend forte) | close imediato | `enable_structure_break_close` |
| **f** | ≥ 6 candles + range das últimas 6 < 0.3R | flag (não fecha — alerta) | `enable_time_exit_flag` |

### Detecção de reversal candle (regra b)

Vela fechada com `body/range > 0.55` na direção contra ao trade (bearish forte para BUY, bullish forte para SELL).

### Detecção de structure break (regra e)

Aciona em DOIS casos:
1. **BOS estrito** — alternância HH/LL ou LH/HL na direção contra
2. **Trend confirmado** — LH+LL (bearish) ou HH+HL (bullish) consecutivos contra o trade

Detalhe: quando entramos contra-trend e o trend continua, é "structure contra" mesmo sem alternância de BOS clássico.

### Não modifica TP

Exit War Room **só altera SL** (via `TRADE_ACTION_SLTP`), volume parcial (via `TRADE_ACTION_DEAL`) ou força close. TP permanece intacto.

### Buffer no BE

```yaml
be_buffer_pips: 0.2   # 2 pontos acima/abaixo da entrada (proteção spread)
```

---

## 7. Símbolos Operados — Critério de seleção

**5 ativos:** AUDUSD, GBPUSD, USDCAD, USDCHF, NZDUSD.

**Critério de desativação histórica:**
- WR < 45% + P&L negativo após 6+ trades
- Comportamento direcional incompatível com mean-reversion (ex: JPY)
- Recomendação ICT (Aula 3) — EUR pausado por instituições operarem intensamente

### Correlações ativas (16 entradas)

USD-quote bundle (movem juntos quando USD mexe):
- AUDUSD ↔ NZDUSD ↔ GBPUSD

USD-base bundle (par fortalece/fraqueja contra USD na mesma direção):
- USDCAD ↔ USDCHF

Cross-correlations (commodities + risk-on):
- AUDUSD/NZDUSD ↔ USDCAD/USDCHF (risk-on)
- GBPUSD ↔ USDCAD/USDCHF
- EUR* (mantidos no array para reativação futura)

---

## 8. Janelas de Sessão ICT (Aula 2 — Daily Range Algorithm)

Em UTC, com pesos absolutos (max 14) que o War Room re-escala para 0-10 pts:

| Janela | UTC | Peso | Comportamento |
|--------|-----|------|---------------|
| `asia_early` | 21-24 | 8 | Exhaustion após NY close |
| `asia_judas` | 00-07 | 1 | Manipulação pré-London (penalizada) |
| `london_open` | 07-10 | **14** | Prime time (forma high/low do dia) |
| `london_cont` | 10-13 | 11 | Follow-through London |
| `ny_news_embargo` | 13-14 | **0** | Bloqueado como gate |
| `ny_expansion` | 14-15 | 13 | NY abre expansion |
| `london_close` | 15-16 | 12 | London close reversal |
| `ny_afternoon` | 16-21 | 7 | End-of-day consolidation (fraco) |

**Cobertura empírica (losses 27-28/04):**
- 5 trades em Asia/Judas → score 1 (quase desclassifica)
- News embargo zera score E bloqueia gate (defesa em camadas)
- London open premiada (14)

---

## 9. Defesa em camadas — Resumo

| Camada | Onde | Quando dispara |
|--------|------|----------------|
| **Bot — gate horário** | `is_entry_blocked_by_time` | News embargo / cutoff (UTC 13-14, MT5 ≥22) |
| **Bot — gate range** | `min_candle_range_pips` | Vela morta de Asia early |
| **Bot — gate ICT CLIFF** | `is_entry_blocked_by_ict_cliff` | ICT alignment 0/25 |
| **Bot — gate cooldown** | `cooldown_mgr.check` | (Sym, Dir) com loss recente |
| **War Room — re-check cooldown** | `auto_war_room.cooldown_items` | Cache stale ou cooldown ativou no meio |
| **War Room — CLIFF rejection** | `cliff_items` | Score ICT == 0 (defesa em 2ª camada) |
| **War Room — cluster tie-breaker** | `pick_best_from_correlated` | Cluster correlato — escolhe melhor ICT |
| **War Room — score gate** | `score < min_confidence_score` | Qualidade técnica insuficiente |
| **War Room — correlation gate** | `check_correlation_conflict` | Posição aberta correlata no MT5 |
| **Exit War Room — close imediato** | regra (e) | Loss + structure break ICT contra |
| **Exit War Room — close cedo** | regra (d) | Profit + liquidity raid completo |
| **Exit War Room — BE auto** | regras (a/b/c) | Profit ≥ 1R / ≥ 0.7R+rev / ≥ 0.5R+RSI |

---

## 10. Métricas de risco financeiro

| Limite | Valor | Ação |
|--------|-------|------|
| `daily_max_loss` | $500 | Bot encerra sessão |
| `daily_profit_target` | $1000 | Bot encerra sessão |

P&L de sessão é calculado direto do MT5 `history_deals_get` desde `SESSION_START` (timestamp de boot do bot).
