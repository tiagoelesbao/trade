# RELEASE CHANGELOG — v6.2.0

**Data:** 2026-04-27
**Branch:** main
**Scope:** Mudanças acumuladas desde 2026-04-23 (não commitadas)
**Preparado por:** @devops (Gage)

---

## Resumo Executivo

Desde o último commit (`e3aae68` — 2026-04-22), o sistema passou por uma **onda massiva de refatoração e tuning estratégico**, conduzida após call com trader experiente. As mudanças cobrem:

- ✅ Tuning completo da estratégia (RSI alpha, SL, Breakeven, Slope)
- ✅ Pipeline ETL completo (4 scripts novos)
- ✅ Reorganização da estrutura de scripts (legacy/ e utils/)
- ✅ Sistema de logging centralizado (SystemLogger)
- ✅ Gestão de ciclo de vida dos trades (TradeLifecycleManager)
- ✅ War Room redesenhado (scoring 5 critérios, RSI como alpha)
- ✅ FASE 1 logs (Strategy Fire antes do scoring)
- ✅ Frontend atualizado (heartbeat, P&L Sessão, sidebar)
- ✅ FULL_START.bat com auto-inicialização MT5
- ✅ IndicadorLiquidez.mq5 com 3 bugs corrigidos
- ✅ Documentação completa (PRD, brownfield-architecture, strategy, README_SQUAD)
- ✅ Limpeza massiva (PDFs, CSVs, scripts legados, imagens)

---

## Mudanças por Categoria

### 🤖 Bot Core — `bot_liquidez.py`

| Mudança | Detalhe |
|---|---|
| `RSI_PERIOD = 9` | Período promovido a default (antes 14) — decisão do trader |
| `stop_buffer_points: 15 → 50` | 1.5p → 5p para absorver sweep de liquidez típico |
| `breakeven_candles: 7 → 0` | Desativado — ejava trades cedo demais |
| `use_trend_filter: false` | Slope Guard MA20 H1 estava invertido (contra-tendência) |
| `require_color_reversal: false` | Atrasava entrada para 2º candle desnecessariamente |
| `calculate_rsi(series, period=None)` | Lê período do config dinamicamente |
| `BREAKEVEN_CANDLES`, `RSI_OVERBOUGHT`, `RSI_OVERSOLD` | Globais do config agora usados corretamente |
| `MIN_WICK_PCT`, `RR_RATIO`, `LOOKBACK_ZONES` | Todos agora lidos do config (antes hardcoded) |
| `daily_profit_target` | Verificado — bot encerra ao atingir $500 |
| `check_breakeven()` | Nova função (code preserved, desativada via config) |
| `print_dashboard()` | Dashboard estruturado com rolling log 10 eventos |
| `send_heartbeat()` | Upsert em `bot_heartbeats` a cada ciclo (20s) |
| `export_zones_to_mt5()` | Exporta CSV com merge de zonas (threshold 15 pips) |
| `sync_open_positions()` | Substitui `sync_with_mt5_history()` bugada |
| `SESSION_START` | Timestamp de sessão ao iniciar |
| `get_session_pnl()` | P&L desde início da execução (não por data) |
| USDJPY desativado | WR 42.1%, P&L -$232.29 — incompatível com estratégia |
| 8 symbols ativos | EURUSD, GBPUSD, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, GBPJPY |

### 🧠 War Room — `auto_war_room.py`

| Mudança | Detalhe |
|---|---|
| **RSI promovido a alpha (35 pts)** | Era 15pts — agora é o critério dominante |
| Scoring reformado: 7 → 5 critérios | RSI(35) + Wick(25) + PinBar(20) + Sessão(15) + Histórico(5) |
| Slope removido do scoring | Incompatível com estratégia contra-tendência |
| Volume removido do scoring | "Não casa com reversão em zona" — trader |
| Score mínimo: 60 → 55 | Distribuição mais criteriosa |
| `RSI_PERIOD = CFG.get('rsi_period', 9)` | Mesmo período do bot |
| `derive_strategy_context(signal)` | Single fetch M15+H1 para evitar re-fetch |
| `print_strategy_fire(signal, ctx)` | Card FASE 1 antes do scoring matemático |
| `analyze_signal_strength(signal, ctx=None)` | Aceita ctx pré-computado |
| `CORRELATED_PAIRS` atualizado | USDCAD↔USDCHF adicionado, USDJPY↔USDCAD removido |
| Agentes: Momentum, Rejeição, Contexto | Substituem Jim Simons, Druckenmiller, Taleb (opiniões formatadas) |

### 📊 SystemLogger — `system_logger.py`

| Mudança | Detalhe |
|---|---|
| `signal_analysis()` | Método novo: card completo com barra visual por critério |
| `SCORE_MAX`, `SCORE_LABELS`, `SCORE_KEYS_ORDER` | Reduzidos de 7 para 5 critérios |
| Console + Supabase (`bot_logs.data`) | JSON estruturado com scores, valores brutos, opiniões |

### 🔄 TradeLifecycleManager — `trade_lifecycle_manager.py`

| Mudança | Detalhe |
|---|---|
| FSM 8 estados completo | signal_detected → awaiting_consensus → approved/rejected → filled → open → closed/error |
| `create_signal()`, `approve_signal()`, `reject_signal()` | Lifecycle completo |
| `mark_as_filled()`, `mark_as_open()`, `close_trade()` | Transições de estado |
| `position_id` único | Elimina duplicatas |
| Cooldown via banco | Persiste entre restarts |

### 📦 ETL Suite (4 scripts novos)

| Script | Função |
|---|---|
| `etl_trades.py` | Stats de trades fechados (WR, R/R, expectancy, drawdown) |
| `etl_rejections.py` | Breakdown de sinais rejeitados por categoria |
| `etl_db_audit.py` | Auditoria de integridade com `--fix` |
| `etl_report.py` | Relatório completo JSON + Markdown para IA |

### 🗂️ Reorganização `/scripts`

| Estrutura | Conteúdo |
|---|---|
| `/scripts/` | 9 arquivos de produção |
| `/scripts/legacy/` | 11 arquivos (backups v5.x, scripts one-time) |
| `/scripts/utils/` | 16 ferramentas de diagnóstico e testes |

### 🖥️ Frontend — `app/`

| Arquivo | Mudança |
|---|---|
| `app/page.tsx` | Heartbeat com timeout 90s, exibe "X min atrás" |
| `dashboard-metrics.tsx` | "Lucro Hoje" → "P&L Sessão (MT5)" |
| `sidebar.tsx` | Item "Logs" adicionado na navegação |

### ⚙️ Infraestrutura

| Item | Mudança |
|---|---|
| `FULL_START.bat` | Auto-inicialização MT5, `chcp 65001`, delays entre processos |
| `config.yaml` | Todos os parâmetros agora corretamente consumidos pelo bot |
| `IndicadorLiquidez.mq5` | 3 bugs corrigidos (zonas estreitas, timestamps, labels invisíveis) |
| `setup_schema_v6.sql` | Schema v6.0 com 7 novas colunas + 3 índices |

### 🗑️ Arquivos Removidos (Limpeza)

- 8 imagens de assets (PNGs)
- 4 PDFs (brownfield, PRD, relatórios)
- 2 CSVs de dados (EURUSDH1.csv, ml_dataset.csv)
- 15+ scripts legados (diagnose_*, audit_*, clean_*, setup_*, simulate_*)
- AuditorBacktest.mq5
- Arquivos de tasks obsoletos (monitor-6-candle-exit, send-order-limit, etc.)
- Agentes v5.x (execution-manager, macro-context-agent, quant-trigger-analyst, risk-controller-taleb)

### 📄 Documentação Atualizada

| Doc | Status |
|---|---|
| `docs/BOT_V6.0_CHANGELOG.md` | Criado — histórico completo v6.0 → v6.1.3 |
| `docs/FUNCIONAMENTO_COMPLETO_BOT.md` | Criado — referência técnica operacional |
| `docs/brownfield-architecture.md` | Expandido massivamente (+332 linhas) |
| `docs/prd.md` | Atualizado (+180 linhas) |
| `squads/trade-liquidez-python/CHANGELOG.md` | Histórico v5.5.1 → v6.1.3 |
| `squads/trade-liquidez-python/docs/strategy.md` | Atualizado (+230 linhas) |
| `squads/trade-liquidez-python/docs/README_SQUAD.md` | Expandido (+276 linhas) |
| `assets/repport_call.md` | Call com trader experiente — parecer técnico completo |
| `assets/analise-call-parecer-tecnico.md` | Análise técnica dos itens A-P do parecer |
| `assets/log_warroom_session*.md` | 4 sessões de war room logadas |

---

## Versão Sugerida: `v6.2.0`

**Justificativa MINOR** (não MAJOR):
- Não há breaking changes na API/interface externa
- Mudanças são tuning estratégico + infraestrutura
- Lifecycle já existia (v6.0) — este release é maturação
- ETL suite é additive (não quebra nada existente)

> Se preferir `v6.1.4` por ser continuação da linha 6.1.x, também é válido.
> Se considerar a ETL suite + reorganização estrutural uma mudança maior, `v6.2.0` é mais adequado.

---

## Mensagem de Commit Sugerida

```
feat(trading): v6.2.0 — RSI alpha tuning, ETL suite, war room reform, infra cleanup

- RSI(9) como default, SL 50pts, breakeven off, slope/color-reversal off
- War room: 5 critérios (RSI alpha 35pts), FASE 1 Strategy Fire logs
- ETL suite: etl_trades, etl_rejections, etl_db_audit, etl_report
- TradeLifecycleManager + SystemLogger maduros
- Scripts reorganizados: legacy/ e utils/ separados
- Frontend: P&L Sessão, heartbeat 90s, sidebar Logs
- FULL_START.bat com auto-MT5
- IndicadorLiquidez.mq5: 3 bugs corrigidos
- Limpeza massiva: PDFs, CSVs, 15+ scripts legados, imagens
- Docs: BOT_V6.0_CHANGELOG, FUNCIONAMENTO_COMPLETO, strategy, PRD atualizados
```

---

**Preparado por:** @devops (Gage) — deployando com confiança 🚀
