# Trade Liquidez — PRD (Product Requirements Document) v6.0

**Data:** 22 de Abril de 2026
**Versão:** 6.1.3
**Status:** Produção

---

## 1. Visão do Produto

Sistema de trading algorítmico multi-par para forex, operando em 8 pares ativos via MetaTrader 5. Detecta zonas de liquidez institucional em M15, valida sinais através de uma War Room agêntica com scoring técnico (0–100), executa ordens aprovadas e monitora o ciclo de vida completo de cada trade via dashboard web em tempo real.

**PC de operação:** Ligado durante dias de mercado (Seg–Sex), reiniciado nos finais de semana. P&L de sessão reseta a cada reinício do bot; P&L total é acumulado histórico.

---

## 2. Objetivos

| Objetivo | Métrica |
|---|---|
| Operação autônoma | Bot roda sem intervenção manual |
| Qualidade de sinais | War Room filtra sinais com score < 55/100 (5 critérios, RSI alpha) |
| Proteção de capital | Stop diário $350, meta diária $500 |
| Observabilidade | Logs em tempo real, heartbeat 20s, dashboard ao vivo |
| Integridade de dados | P&L calculado do histórico MT5 (fonte de verdade) |

---

## 3. Requisitos Funcionais

### FR1 — Detecção de Zonas (Bot)
- Detecção de suportes e resistências M15 com lookback de 100 candles
- Confirmação: 7 candles de deslocamento após a zona
- Gatilho Sniper (v6.1.3): wick ≥ 30% + RSI(9) extremo (≥70 SELL / ≤30 BUY) em zona tocada
- Slope MA20 H1 e Color Reversal **desativados** em v6.1.1 (parecer técnico — operavam invertidos para estratégia contra-tendência)
- Todos os parâmetros configuráveis via `config.yaml` (sem hardcodes)

### FR2 — Aprovação Agêntica (War Room v6.1.2 — RSI alpha)
- Scoring **5 critérios**: RSI extremo (35 — alpha), wick% (25), pin bar (20), sessão (15), histórico (5)
- Score mínimo: **55/100** para aprovação
- **RSI Extremo (alpha):** distância em relação ao limite (70/30). 30%/70% = 0pts; 85% = 17.5pts; ≥100%/≤0% = 35pts
- **Pin Bar:** corpo ≤ 15% do range = 20 pts; corpo > 50% = penaliza (vela suja)
- **Sessão:** London+NY overlap (13–17h UTC) = 15 pts; sessão isolada = 10 pts; Ásia = 3 pts
- **Removidos em v6.1.2:** Slope H1 (incoerente com gate desativado), Volume (não casa com reversão em zona)
- Rejeição automática de pares correlacionados com posições ativas
- Aprovação de máximo 1 sinal por ciclo (maior score prioritário)
- Log **FASE 1 — Strategy Fire** (condições de mercado) impresso ANTES do scoring matemático **FASE 2** (v6.1.3)
- JSON estruturado no Supabase `bot_logs` com scores, valores brutos, opiniões dos agentes

### FR3 — Execução e Rastreamento (Bot + MT5)
- Execução via `mt5.order_send()` com `ORDER_FILLING_FOK`
- Rastreamento de posição por `position_id` (ticket MT5)
- P&L real calculado do histórico de deals MT5 no fechamento

### FR4 — Dashboard Web (Next.js)
- Painel ao vivo com P&L Sessão, P&L Total, zonas ativas
- Status do motor (online/offline) via heartbeat com timeout 90s
- Histórico de trades com filtros
- Logs em tempo real com filtro por source e level
- Supabase Realtime para atualizações sem polling

### FR5 — Indicador MetaTrader (MQ5)
- Zonas renderizadas como retângulos preenchidos com limite de 6 por lado
- Largura mínima garantida: `InpMinBarsWidth = 60` barras M15 (~15h) para zonas recentes
- Destaque de zonas dentro de 25 pips do preço atual
- Painel BOT STATUS com P&L Sessão, P&L Total, Zonas Exauridas
- Timestamps exportados no formato `YYYY.MM.DD HH:MM:SS` (exigido por `StringToTime()` do MQL5)
- Leitura de CSV gerado pelo bot (atualizado a cada ciclo de 20s)

### FR7 — Suite ETL (Análise de Operações)
- `etl_trades.py`: stats de trades fechados (WR, R/R, expectancy, drawdown), filtros por sessão/data/símbolo
- `etl_rejections.py`: sinais rejeitados com breakdown por categoria (trend_filter, rsi_filter, wick_filter, cooldown, proximity…)
- `etl_db_audit.py`: auditoria de integridade do banco; correção de stuck trades, null PNL, duplicatas
- `etl_report.py`: relatório completo JSON + Markdown para análise por IA (equity curve, por símbolo, logs de sessão)

### FR6 — Observabilidade
- `system_logger.py` escrevendo em console + Supabase `bot_logs`
- Heartbeat Supabase a cada 20s
- Dashboard terminal estruturado com rolling log de 10 eventos
- Página `/logs` no frontend com filtros e auto-scroll

---

## 4. Requisitos Não-Funcionais

| Requisito | Especificação |
|---|---|
| Latência do ciclo | 20s por iteração completa |
| Tolerância a falhas | Supabase indisponível não para o bot (graceful degradation) |
| H1 indisponível | Sem efeito em v6.1.1+ (`use_trend_filter: false` por default); se reativado, bloqueia o trade |
| Persistência | `consumed_zones.json` sobrevive a reinicializações |
| Configurabilidade | 100% dos parâmetros operacionais em `config.yaml` |
| Sem magic numbers | Nenhum valor hardcoded nos filtros de entrada (RSI period, wick, RR, etc.) |

---

## 5. Arquitetura de Estados (Trade FSM)

```
signal_detected → awaiting_consensus → approved → filled → open → closed
                                    ↘ rejected                  ↘ error
```

Gerenciado por `trade_lifecycle_manager.py` com persistência em Supabase `signals_liquidez`.

---

## 6. Proteções Operacionais

| Proteção | Implementação |
|---|---|
| Stop diário | `daily_max_loss: $350` — bot encerra sessão |
| Meta diária | `daily_profit_target: $500` — bot encerra sessão |
| Kill-Zone | 4h × 10 pips por símbolo após qualquer trade |
| One-Shot | Zona consumida imediatamente ao criar sinal |
| Anti-correlação | EURUSD+GBPUSD, EURUSD+USDCHF, AUDUSD+NZDUSD, etc. |
| 1 sinal por ciclo | Race condition eliminada |
| SL com buffer institucional | `stop_buffer_points: 50` (5 pips) — absorve varredura de liquidez típica antes da reversão (v6.1.3) |
| **Breakeven automático** | DESATIVADO em v6.1.3 (`breakeven_candles: 0`); código mantido para reativação |

---

## 7. Símbolos Operados

**8 pares ativos:** EURUSD, GBPUSD, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, GBPJPY

| Símbolo | Status | Motivo |
|---|---|---|
| USDJPY | DESATIVADO | WR 42.1% (8/19 trades), P&L -$232.29 — JPY direcional |
| EURJPY | DESATIVADO | WR 16.7% (1/6 trades), P&L -$85.56 |

---

## 8. Organização de Scripts

```
scripts/               ← produção (9 arquivos)
  bot_liquidez.py
  auto_war_room.py
  system_logger.py
  trade_lifecycle_manager.py
  IndicadorLiquidez.mq5
  etl_trades.py
  etl_rejections.py
  etl_db_audit.py
  etl_report.py

scripts/legacy/        ← backups e scripts one-time (11 arquivos)
scripts/utils/         ← diagnóstico, simulação, testes reutilizáveis (16 arquivos)
```

---

## 9. Histórico de Versões

| Versão | Data | Destaque |
|---|---|---|
| **v6.1.3** | 2026-04-22 | RSI(9) promovido como default, `stop_buffer_points` 15→50, breakeven OFF, logs FASE 1 (strategy_fire), `slope_threshold_pips` removido |
| **v6.1.2** | 2026-04-22 | Reforma do scoring: 7→5 critérios, **RSI promovido a alpha** (35pts), Slope e Volume removidos |
| **v6.1.1** | 2026-04-21 | `use_trend_filter` e `require_color_reversal` desativados (parecer técnico — operavam invertidos contra-tendência) |
| **v6.1.0** | 2026-04-21 | War Room scoring v6.1 (7 critérios, pin bar + sessão), signal_analysis logs, breakeven automático |
| **v6.0.2** | 2026-04-21 | ETL suite (4 scripts), reorganização scripts, USDJPY desativado, fixes IndicadorLiquidez.mq5 |
| **v6.0.1** | 2026-04-21 | Auditoria: todos config.yaml wired, `use_trend_filter` respeitado, `daily_profit_target` implementado |
| **v6.0** | 2026-04-21 | Lifecycle Architecture: FSM 8 estados, War Room agêntica, SystemLogger, indicador MT5 reescrito, /logs frontend |
| v5.9.6 | 2026-04-20 | Fix sync MT5→Supabase, zero P&L corrigido |
| v5.9.5 | 2026-04-20 | Kill-Zone fix, One-Shot persistência, race condition |
| v5.9.4 | 2026-04-16 | Source of Truth P&L, SESSION_START |
| v5.6 | 2026-04-18 | Visual Path Auditing, backtest realista |
| v5.5.1 | 2026-04-15 | Multi-pair, Slope Guard, Color Reversal |

---

*PRD v6.1.3 — Synkra AIOX Ecosystem*
