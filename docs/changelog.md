# Changelog — Trade Liquidez

Histórico unificado v5.5 → v6.2.0. Para detalhes técnicos por sprint v6.2.0, ver [`sprints/`](sprints/).

---

## v6.2.0-ict — Sprints 1-6 (2026-04-28 → 2026-04-30)

Onda de melhorias estratégicas baseada na metodologia ICT (Inner Circle Trader). Não há breaking changes na API; mudanças são tuning + novas camadas defensivas.

### Sprint 6 — Cooldown direcional + Exit War Room logs ricos (2026-04-30)

→ [sprints/sprint-06-cooldown-logs-ricos.md](sprints/sprint-06-cooldown-logs-ricos.md)

- **NEW** `cooldown_manager.py` — bloqueio direcional pós-loss em (symbol, direction)
  - Persistência JSON em `data/cooldowns.json` (cross-process via mtime cache)
  - Defesa em camadas: bot bloqueia em `check_trigger`, War Room re-check
  - Origem: cluster USDCHF 30/04 (3 BUY losses em 2h, 4ª win após 4h) — economia teórica +$176
- **NEW** Sprint 6.2 — `evaluate_all_rules()` no Exit War Room retorna breakdown verbose
  - Dashboard rico: profit bar visual, ICT context, status individual de cada regra a-f
  - `recent_events deque` 50 → 200
  - Evento Supabase `position_evaluation` com `data.rules_breakdown` JSON completo
- **CHG** `rsi_period: 9 → 14` (Wilder default, alinha com MT5; 9 era reativo demais em vela morta)
- **NEW** Eventos: `cooldown_started`, `cooldown_active`, `position_evaluation`

### Sprint 5 — RSI Wilder + persistência local + filtros (2026-04-29)

→ [sprints/sprint-05-rsi-wilder-logs.md](sprints/sprint-05-rsi-wilder-logs.md)

- **FIX** `calculate_rsi` migrado de SMA simples → **Wilder's SMMA** (`ewm(alpha=1/period, adjust=False)`)
  - Resolve divergência de até 42 pts vs MT5 chart após vela com spike
  - Aplicado em bot_liquidez, auto_war_room, exit_war_room
- **NEW** `terminal_log_writer.py` — persistência local append-only de rolling logs
  - Path `data/terminal_logs/{BOT|EXIT_WR}_YYYYMMDD.log` (rotação diária)
  - Sobrevive a `cls` do dashboard (limpeza visual sem perder histórico)
- **NEW** `min_candle_range_pips: 3.0` — filtro de vela morta (Asia early com 1-2 pips)
- **NEW** Metadados RSI no log do trigger: `rsi_period`, `rsi_value`, `rsi_method=Wilder_SMMA`, `candle_time_mt5`, `candle_close`, `candle_range_pips`, `candle_body_ratio`
- **NEW** Eventos: `position_snapshot` (Exit WR a cada ciclo, auditoria 100%)
- **CHG** `recent_events deque` 10 → 50 (bot)
- **CHG** CSV exportado para MT5 ganhou linhas `GATE`, `SESSION`, `ICT_BIAS`, `LIQ_ABOVE/BELOW`, `POSITION`
- **FIX** 6 lugares com `print("[ERROR] ...")` direto convertidos para `logger.error()` (vai pro Supabase)

### Sprint 4 — Exit War Room (2026-04-28)

→ [sprints/sprint-04-exit-war-room.md](sprints/sprint-04-exit-war-room.md)

- **NEW** `exit_war_room.py` — 4º processo (530 linhas, loop 10s)
  - 6 regras a-f com feature flags em `config.yaml/exit_war_room`
  - Substitui `check_breakeven` legado do bot (mantido `BREAKEVEN_CANDLES=0`)
- **NEW** Detecção de structure break: BOS clássico OU trend forte (LH+LL/HH+HL)
- **NEW** Detecção de reversal candle: `body/range > 0.55` na direção contra
- **NEW** `exit_hint_<symbol>.csv` lido pelo `IndicadorLiquidez.mq5` (próxima ação prevista)
- **NEW** Eventos: `be_moved_dynamic`, `partial_closed`, `early_exit_liquidity`, `structure_break_close`, `time_exit_flagged`
- **NEW** `FULL_START.bat` ganhou 4ª janela "Exit War Room (Python)"
- **NEW** `sim_sprint4_exit.py` — audit standalone com 6 cenários (todas as regras + caso aguardar). 6/6 OK.

### Sprint 3 — War Room v2: Pool-then-Pick (2026-04-28)

→ [sprints/sprint-03-pool-then-pick.md](sprints/sprint-03-pool-then-pick.md)

- **CHG** Substituiu First-Match-Approve por Pool-then-Pick
  - Janela `cluster_pool_window_seconds: 30` com poll 3s
  - Tie-breaker direcional: `(ict_alignment, total_score, wick_pct)` desc
- **NEW** `pick_best_from_correlated()` — algoritmo greedy que escolhe winner e marca correlatos como losers
- **NEW** Verdictos: `REJEITADO_CLIFF` (ICT=0 pre-filter), `PRETERIDO_CLUSTER` (perdeu tie-breaker)
- **NEW** Evento Supabase `cluster_decision` estruturado com winner/loser
- **NEW** Card visual `[CLUSTER DECISION]` no terminal
- **NEW** `sim_sprint3_cluster.py` — audit standalone com 3 cenários (real/misto/tie-breaker)
- Por que ICT antes do score: cluster 28/04 mostrou que aprovar pelo "maior score técnico" sem ICT awareness deixa passar trades contra-trend

### Sprint 2 — ICT Context Engine (2026-04-28)

→ [sprints/sprint-02-context-engine.md](sprints/sprint-02-context-engine.md)

- **NEW** Pacote `ict/`:
  - `structure.py` — `detect_swings`, `classify_structure` (HH/HL/LH/LL, BOS), `bias_from_structure`
  - `phase_detector.py` — Aula 1 (`PhaseResult`: expansion/retracement/reversal/consolidation)
  - `liquidity_levels.py` — Aula 3 (untested + equal levels = raid targets)
  - `daily_range_algo.py` — Aula 2 (estado do dia ICT, persistência JSON)
- **NEW** `ict_context_engine.py` — orquestrador com cache TTL 5min
  - `get_context(symbol, mt5_module)` retorna closure `trade_alignment_score(BUY|SELL)` 0-25 pts
- **CHG** Scoring War Room: 5 → 6 critérios redistribuídos
  - RSI 35→25, Wick 25→20, PinBar 20→15, Sessão 15→10, **ICT 25 (NEW)**, Hist 5
- **NEW** **Gate ICT CLIFF** (única exceção autorizada para ICT virar gate)
  - Bloqueia se `alignment_score == 0/25` (trade contra D1 + H4 expansion contrária)
  - Camada 1: bot em `is_entry_blocked_by_ict_cliff` (eficiência)
  - Camada 2: war room em `analyze_signal_strength` (auditoria)
- **NEW** Card `[ICT CONTEXT]` renderizado entre FASE 1 e FASE 2 do War Room
- **CHG** 4ª opinião "ICT Macro" adicionada (com bias D1, H4/H1 phase, daily_state)
- **MEMORY** Constraint atualizada com aprovação do usuário: "macro = score-only, exceto CLIFF"

### Sprint 1 — Limpeza + 8 janelas ICT + gates de horário (2026-04-28)

→ [sprints/sprint-01-cleanup-ict.md](sprints/sprint-01-cleanup-ict.md)

- **REM** Dead code: `SLOPE_THRESHOLD_PIPS`, `USE_TREND_FILTER`, `REQUIRE_REVERSAL` (50+ linhas)
  - Eram filtros desativados desde v6.1.1 (Slope Guard operava invertido)
- **REM** Pares EURUSD e EURGBP pausados (ICT Aula 3 — instituições operam EUR intensamente)
  - 5 pares ativos: AUDUSD, GBPUSD, USDCAD, USDCHF, NZDUSD
- **NEW** Gates de horário em `is_entry_blocked_by_time()`
  - `news_embargo_pause: true` (UTC 13-14h, NY 8-8:30 release + reaction)
  - `entry_cutoff_hour_mt5: 22` (=19 UTC, end-of-day consolidation)
- **NEW** 8 janelas ICT em `session_windows` (Aula 2 — Daily Range Algorithm)
  - asia_early/asia_judas/london_open/london_cont/ny_news_embargo/ny_expansion/london_close/ny_afternoon
  - `session_score_label` reescrita ICT-aware
- **CHG** `min_confidence_score: 65 → 75` (lê do config, fim do drift de 55 hardcoded em system_logger)
- **CHG** `CORRELATED_PAIRS` ampliado: 5 → 16 entradas (USD-quote bundle completo + USD-base + cross-correlations)
- **CHG** `system_logger.MIN_CONFIDENCE_SCORE` lê do config (era 55 hardcoded)

> **Nota:** `min_confidence_score` foi posteriormente rebaixado para 60 conforme ICT (25pts) entrou no scoring e o total escalou — 75 sobre 100 puro vs 60 sobre 100 com ICT pesado é equivalente.

---

## v6.1.x — Tuning estratégico pós-call com trader (2026-04-21 a 22)

### v6.1.3 — RSI(9) + SL/Breakeven tuning (2026-04-22)

- **CHG** `rsi_period` lido do config (antes hardcoded 14); promovido a 9 (clássico, mais reativo)
- **CHG** `stop_buffer_points: 15 → 50` (5 pips absorvem sweep institucional)
- **CHG** `breakeven_candles: 7 → 0` (7 velas ejavam trades cedo demais em pullbacks)
- **REM** `slope_threshold_pips` removido do config (órfão desde v6.1.1)
- **NEW** Logs FASE 1 "Strategy Fire" antes do scoring matemático
  - `derive_strategy_context()` + `print_strategy_fire()` em `auto_war_room.py`
  - `analyze_signal_strength(signal, ctx=None)` aceita ctx pré-computado (single fetch)

### v6.1.2 — Reforma do scoring (2026-04-22)

- **CHG** Scoring 7 → 5 critérios, RSI promovido a alpha (35 pts)
  - Removidos: ~~Slope H1~~ (incoerente — bot já não usava como gate), ~~Volume~~ (não casa com mean-reversion)
- **CHG** Score mínimo 55/100 mantido

### v6.1.1 — Slope Guard e Color Reversal desativados (2026-04-21)

- **CHG** `use_trend_filter: false` — slope MA20 H1 operava INVERTIDO para estratégia contra-tendência
- **CHG** `require_color_reversal: false` — atrasava entrada para o segundo candle, perdendo ponto ótimo
- Origem: parecer técnico em `assets/analise-call-parecer-tecnico.md`

### v6.1.0 — War Room scoring 7 critérios (2026-04-21) — *substituído em v6.1.2*

- **NEW** Pin Bar (20 pts), Sessão (15 pts) adicionados ao scoring
- **NEW** Breakeven automático (`check_breakeven`) — desativado em v6.1.3
- **NEW** Logs detalhados (`signal_analysis()` no SystemLogger)
- **CHG** Score mínimo 60 → 55

---

## v6.0.x — Lifecycle Architecture (2026-04-20 a 21)

### v6.0.2 — ETL Suite + USDJPY desativado (2026-04-21)

- **NEW** Suite ETL com 4 scripts: `etl_trades`, `etl_rejections`, `etl_db_audit`, `etl_report`
- **CHG** Reorganização `/scripts/` em `legacy/` e `utils/`
- **REM** USDJPY desativado (WR 42.1%, P&L -$232.29 — JPY direcional)
- **FIX** IndicadorLiquidez.mq5: 3 bugs corrigidos
  - `InpMinBarsWidth = 60` para zonas estreitas (~15h)
  - `_fmt_time()` usa pontos (`2026.04.21`) — exigido por `StringToTime()` MQL5
  - `OBJPROP_HIDDEN = false` para labels invisíveis

### v6.0.1 — Auditoria Compliance (2026-04-21)

- **FIX** `min_wick_pct`, `rsi_overbought/oversold`, `risk_reward_ratio`, `lookback_zones` eram hardcoded
- **FIX** `use_trend_filter` flag agora é respeitada (antes era ignorada)
- **FIX** `daily_profit_target` agora é verificado (bot encerra ao atingir)

### v6.0 — Lifecycle Architecture (2026-04-20)

**Resolução de bugs críticos de v5.9.6:**
- 41.6% trades com P&L = $0 → 0%
- Duplicatas → 0% (position_id UNIQUE)

**Novidades:**
- **NEW** `trade_lifecycle_manager.py` — FSM 8 estados
  - signal_detected → awaiting_consensus → approved/rejected → filled → open → closed/error
- **NEW** `position_id` (ticket MT5) como chave única no banco
- **NEW** `sync_open_positions()` substitui `sync_with_mt5_history()` bugada
- **NEW** Cooldown via banco (substitui `session_trade_log` em memória)
- **NEW** Schema v6.0: 7 colunas novas (position_id, exit_price, approved_at, filled_at, updated_at, reject_reason, error_message)
- **NEW** Índices: `idx_signals_position_id` UNIQUE, `idx_signals_status`, `idx_signals_created_at`

---

## v5.x — Histórico anterior

| Versão | Data | Destaque |
|--------|------|----------|
| v5.9.6 | 2026-04-20 | Fix sync MT5→Supabase, zero P&L corrigido |
| v5.9.5 | 2026-04-20 | Kill-Zone fix, One-Shot persistência, race condition |
| v5.9.4 | 2026-04-16 | Source of Truth P&L, SESSION_START |
| v5.7.2 | 2026-04-15 | Backtest anual de alta fidelidade com custos operacionais realistas |
| v5.6 | 2026-04-18 | Visual Path Auditing, backtest realista |
| v5.5.1 | 2026-04-15 | Multi-pair, Slope Guard, Color Reversal — sniper finalizado |
| v5.5 | 2026-04-14 | Multi-Pair Sniper M15 com backtest de alta performance |

---

## Como contribuir com o changelog

Convenção de tags por entrada:
- **NEW** — feature/módulo novo
- **CHG** — mudança em comportamento existente
- **FIX** — correção de bug
- **REM** — remoção de código/feature

Cada sprint v6.2.0+ tem MD detalhado em `sprints/`. O changelog aqui é resumo executivo.
