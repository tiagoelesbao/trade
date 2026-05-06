# Trade Liquidez — PRD v6.2.0

**Status:** Produção (forward-test em demo)
**Versão:** v6.2.0-ict (Sprints 1-6 concluídos)

---

## 1. Visão do Produto

Sistema de trading algorítmico multi-par para forex que opera **mean-reversion em zonas de liquidez** com filtragem agêntica multi-camada baseada em metodologia ICT (Inner Circle Trader).

A entrada é gatilho técnico simples (zona + pavio + RSI extremo) — a sofisticação está em **camadas defensivas que decidem se o gatilho deve virar trade** (gates de horário, ICT CLIFF, cooldown direcional, scoring 6 critérios, Pool-then-Pick em clusters correlatos) e **regras dinâmicas de saída** (BE em 1R, partial em 0.7R + reversal, close cedo em liquidity raid, close imediato em structure break).

**PC de operação:** Ligado em dias de mercado (Seg-Sex). P&L de sessão reseta a cada reinício; P&L total acumula histórico.

---

## 2. Objetivos e Métricas

| Objetivo | Métrica | Estado v6.2.0 |
|----------|---------|---------------|
| Operação autônoma | Bot roda sem intervenção manual | ✅ |
| Qualidade de sinais | War Room aprova só score ≥ `min_confidence_score` (config) com ICT alignment > 0 | ✅ |
| Evitar trade contra macro | Gate ICT CLIFF (alignment 0/25) bloqueia antes de criar sinal | ✅ |
| Evitar cluster de losses | Cooldown direcional 4h após loss > $10 em (symbol, direction) | ✅ |
| Proteção de capital | Stop diário $500, meta diária $1000 | ✅ |
| Observabilidade | Logs Supabase + persistência local + heartbeat 20s | ✅ |
| Saída inteligente | 6 regras (a-f) substituem BE estático | ✅ |
| Integridade de P&L | P&L vem do `history_deals_get` MT5, não cálculo paralelo | ✅ |

---

## 3. Requisitos Funcionais

### FR1 — Detecção de Zonas (`bot_liquidez.py`)
- Lookback `lookback_zones: 100` candles M15
- Confirmação `min_displacement_candles: 7` (zona válida após 7 candles de afastamento)
- Gatilho Sniper: wick ≥ `min_wick_pct` (30%) + RSI(14) extremo (≥70 SELL / ≤30 BUY) + zona M15 tocada
- RSI calculado com **Wilder's SMMA** (alinhado com MT5 default)
- Filtro `min_candle_range_pips: 3.0` evita gatilhos em vela morta de Asia early

### FR2 — Gates de Entrada (4 camadas em `check_trigger`)
1. **Horário** — `news_embargo_pause` (UTC 13-14h) + `entry_cutoff_hour_mt5` (≥22 MT5 = 19 UTC)
2. **Range mínimo** — `min_candle_range_pips: 3.0`
3. **ICT CLIFF** — bloqueia se `trade_alignment_score == 0/25` (trade contra D1 bias + H4 expansion contrária)
4. **Cooldown direcional** — bloqueia (symbol, direction) por 4h após loss > $10

### FR3 — Decisão Agêntica (`auto_war_room.py` — Pool-then-Pick)
- Pool de 30s acumula sinais correlatos antes de decidir
- **Scoring 6 critérios (max 100 pts):**
  - RSI Extremo (25) — alpha
  - Wick % (20)
  - Pin Bar (15)
  - Sessão ICT (10)
  - **ICT Macro (25)** — closure do `ict_context_engine`
  - Histórico (5)
- **Tie-breaker:** ICT alignment > total_score > wick_pct_real
- CLIFFs (ICT=0) pré-filtrados como `REJEITADO_CLIFF`
- Correlatos do winner viram `PRETERIDO_CLUSTER`
- Aprova **1 winner por ciclo**, rejeita demais

### FR4 — Execução (`bot_liquidez.execute_approved_signals`)
- Executa via `mt5.order_send(ORDER_FILLING_FOK)`
- Lote fixo `lot_size: 1.0`
- SL = high/low do pavio ± `stop_buffer_points × point` (50 pts = 5 pips)
- TP = entry ± distância_SL × `risk_reward_ratio` (1.5)
- Rastreamento por `position_id` único (chave anti-duplicata)

### FR5 — Gestão de Saída (`exit_war_room.py` — 6 regras a-f)
| Regra | Trigger | Ação |
|-------|---------|------|
| **a** | profit ≥ 1.0R | BE imediato |
| **b** | profit ≥ 0.7R + reversal candle ICT | close 50% + BE |
| **c** | profit ≥ 0.5R + 3 candles + RSI cruzou 50 | BE clássico |
| **d** | profit > 0 + ≤3 pips de liquidity oposto | close cedo (raid completo) |
| **e** | profit < 0 + ICT structure break contra | close imediato |
| **f** | ≥ 6 candles + range < 0.3R | flag (não fecha — alerta) |

Cada regra tem feature flag em `config.yaml/exit_war_room`. Loop de 10s. Sem modificação de TP — apenas SL, volume parcial ou close.

### FR6 — Dashboard Web (Next.js)
- Painel ao vivo: P&L Sessão, P&L Total, posições ativas, zonas
- Status do motor via heartbeat (timeout 90s)
- `/historico` filtrável por estado FSM
- `/logs` em tempo real com filtros source/level
- Supabase Realtime (WebSocket, sem polling)

### FR7 — Indicador MetaTrader (`IndicadorLiquidez.mq5`)
- Lê CSV exportado pelo bot (`liquidez_data_<symbol>.csv`)
- Exibe zonas, painel BOT_STATUS (P&L, gate de horário, sessão ICT, ICT bias D1/H4/H1)
- Exibe `LIQ_ABOVE/BELOW` (próximas liquidez) e `POSITION` (posição aberta com profit_R)
- Lê `exit_hint_<symbol>.csv` do Exit War Room para mostrar próxima ação prevista

### FR8 — Observabilidade
- `system_logger.py` escreve em console + Supabase `bot_logs`
- `terminal_log_writer.py` persiste rolling logs locais em `data/terminal_logs/{BOT|EXIT_WR}_YYYYMMDD.log` (rotação diária, append-only)
- Heartbeat 20s em `bot_heartbeats`
- Eventos estruturados: `signal_detected`, `signal_aprovado`, `signal_rejeitado_*`, `position_snapshot`, `position_evaluation`, `cooldown_started`, `cooldown_active`, `cluster_decision`

### FR9 — Análise Pós-Trade Offline (`trade_analysis_engine.py`)
- Pipeline LLM separado do runtime (rodado manualmente após sessão)
- 9 agentes especializados (Huddleston ICT, Simons quant, Taleb risk, etc.)
- Gera consolidado por trade + fechamento diário
- Detalhes em [trade-analysis.md](trade-analysis.md)

---

## 4. Requisitos Não-Funcionais

| Requisito | Especificação |
|-----------|---------------|
| Latência ciclo bot | 20s |
| Latência Exit War Room | 10s |
| Latência War Room | Pool 30s + processamento ~5s |
| Cache ICT | 5min TTL por símbolo (compartilhado bot ↔ war_room ↔ exit_wr) |
| Tolerância a falhas | Supabase indisponível → console-only graceful |
| Persistência runtime | `data/cooldowns.json`, `data/daily_state_*.json`, `data/terminal_logs/*.log` |
| Configurabilidade | 100% dos parâmetros operacionais em `config.yaml` |
| Sem magic numbers | Nenhum filtro hardcoded (período RSI, wick, RR, cooldown horas, etc.) |

---

## 5. Arquitetura de Estados (FSM)

```
signal_detected → awaiting_consensus → approved → filled → open → closed
                                    ↘ rejected                  ↘ error
```

Persistido em Supabase `signals_liquidez`. Detalhes em [architecture.md](architecture.md#fsm).

---

## 6. Símbolos Operados

**5 pares ativos** (v6.2.0): AUDUSD, GBPUSD, USDCAD, USDCHF, NZDUSD

| Símbolo | Status | Motivo |
|---------|--------|--------|
| EURUSD | ⏸ Pausado v6.2.0 (Sprint 1) | ICT Aula 3 — instituições operam EUR intensamente; recomendado evitar |
| EURGBP | ⏸ Pausado v6.2.0 (Sprint 1) | Idem (cross EUR) |
| USDJPY | ❌ Desativado v6.0.2 | WR 42.1%, P&L -$232.29 (JPY direcional) |
| EURJPY | ❌ Desativado v6.1.x | WR 16.7%, P&L -$85.56 |
| GBPJPY | ❌ Desativado v6.1.x | Baixo WR |

---

## 7. Histórico de Versões

Resumo das versões atuais. Histórico completo em [changelog.md](changelog.md).

| Versão | Data | Destaque |
|--------|------|----------|
| **v6.2.0-ict (Sprint 6)** | 2026-04-30 | Cooldown direcional pós-loss + Exit War Room logs ricos |
| v6.2.0-ict (Sprint 5) | 2026-04-29 | RSI Wilder + persistência local de logs + filtro de range |
| v6.2.0-ict (Sprint 4) | 2026-04-28 | Exit War Room (4º processo, regras a-f) |
| v6.2.0-ict (Sprint 3) | 2026-04-28 | Pool-then-Pick + tie-breaker direcional ICT |
| v6.2.0-ict (Sprint 2) | 2026-04-28 | ICT Context Engine + gate CLIFF |
| v6.2.0-ict (Sprint 1) | 2026-04-28 | Limpeza dead code + 8 janelas ICT + gates de horário |
| v6.1.3 | 2026-04-22 | RSI(9) default, SL 50pts, breakeven OFF, FASE 1 logs |
| v6.0 | 2026-04-20 | Lifecycle Architecture (FSM 8 estados) |
