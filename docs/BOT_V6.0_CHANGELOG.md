# Bot Liquidez - Changelog de Versões

**Data:** 2026-04-22
**Autor:** @dev (Dex)
**Versão Atual:** v6.1.3

> Para o histórico completo de versões (v6.0.1, v6.0.2, v6.1.0, v6.1.1, v6.1.2, v6.1.3), consulte `squads/trade-liquidez-python/CHANGELOG.md`.

---

## [v6.1.3] — 2026-04-22

### RSI período 9 promovido como default (item H do parecer)
- `config.yaml`: `rsi_period: 9` adicionado (antes 14 hardcoded)
- `bot_liquidez.py` e `auto_war_room.py`: `RSI_PERIOD = CFG.get('rsi_period', 9)`
- `calculate_rsi(series, period=None)` lê o período do config quando não especificado
- Adoção **sem teste A/B** — decisão explícita do trader (clássico, mais reativo)

### SL ajustado: `stop_buffer_points: 15 → 50`
- 1.5p era estopado por varredura típica de liquidez antes da reversão
- 5p (50 pts) absorve o sweep institucional sem afetar R/R 1:1.5

### Breakeven desativado: `breakeven_candles: 7 → 0`
- 1h45min ejetava trades a zero em pullbacks normais
- Código mantido para reativação futura

### Slope removido completamente do scoring
- `slope_threshold_pips` removido do `config.yaml` (estava órfão desde v6.1.1)
- Default `0.5` permanece em `CFG.get(...)` no código

### Logs FASE 1 (Strategy Fire)
- Novo card impresso **antes** do scoring matemático (FASE 1 → FASE 2)
- Mostra OHLC da vela, gatilhos atendidos (Wick/RSI/Sessão), plano (entry/SL/TP/RR)
- Implementado via `derive_strategy_context()` + `print_strategy_fire()` em `auto_war_room.py`
- `analyze_signal_strength(signal, ctx=None)` aceita ctx pré-computado (single fetch)

### Indicador
- `IndicadorLiquidez.mq5` versão cosmética bumped: `v6.1 → v6.1.3` (sem mudança de lógica)

---

## [v6.1.2] — 2026-04-22

### War Room scoring reformado: 7 → 5 critérios, RSI alpha

Após call com trader experiente, scoring v6.1 foi refeito:

| Critério | v6.1 | v6.1.2 |
|---|---|---|
| **RSI Extremo** | 15 pts | **35 pts (ALPHA)** |
| Wick % | 20 pts | 25 pts |
| Pin Bar | 20 pts | 20 pts |
| Sessão | 15 pts | 15 pts |
| Histórico | 5 pts | 5 pts |
| ~~Slope H1~~ | 15 pts | **REMOVIDO** |
| ~~Volume~~ | 10 pts | **REMOVIDO** |

- **RSI promovido a alpha** — tese central da estratégia (extremo na zona = reversão)
- **Slope removido** — bot já não usa como gate desde v6.1.1; manter no War Room era incoerente
- **Volume removido** — trader: "volume não casa com estratégia de reversão em zona"
- Score mínimo mantido em **55/100**
- `system_logger.py`: `SCORE_MAX`/`SCORE_LABELS`/`SCORE_KEYS_ORDER` reduzidos para 5

---

## [v6.1.1] — 2026-04-21

### Slope Guard e Color Reversal desativados (parecer técnico)

Análise técnica (`assets/analise-call-parecer-tecnico.md`) identificou dois filtros prejudicando entradas legítimas:

- **`use_trend_filter: true → false`** (item A+B): Slope MA20 H1 operava **invertido** para estratégia contra-tendência, bloqueando exatamente as melhores entradas
- **`require_color_reversal: true → false`** (item E): atrasava entrada para o segundo candle, perdendo o ponto ótimo da zona

Código mantido para reativação futura via toggles do config.

### Diretriz Fase 3 (não ativada ainda)
- MA100/200 H1 (item F do parecer): **score-only** na War Room (peso máx 20pts), **NUNCA** como gate em `check_trigger`
- Documentado em `feedback_strategy_macro_trend.md` (memory)

---

## [v6.1.0] — 2026-04-21

### War Room Scoring Redesenhado (7 critérios) — *substituído em v6.1.2*
- **Pin Bar** adicionado (20 pts): body/range ≤ 15% = rejeição perfeita
- **Sessão** adicionada (15 pts): London+NY overlap = 15; London/NY = 10; Ásia = 3
- Pesos ajustados: Wick 20, RSI 15, Slope 15, Volume 10, Histórico 5
- Score mínimo ajustado: 60 → **55** (distribuição mais criteriosa)
- `CORRELATED_PAIRS`: USDCAD↔USDCHF adicionado, USDJPY↔USDCAD removido

### Logs Detalhados (signal_analysis)
- Novo método `signal_analysis()` no SystemLogger
- Console: card completo com barra visual por critério, pts/max, %, critério mais fraco, veredicto
- Supabase: JSON estruturado em `bot_logs.data` com scores, valores brutos, opiniões

### Breakeven Automático — *desativado em v6.1.3*
- `check_breakeven()` executado após `sync_open_positions()` em cada ciclo
- Após `breakeven_candles` velas M15, move SL para entrada + 2 pts (se em lucro)
- Configuração: `breakeven_candles: 7` no config.yaml (0 = desativado)

---

## [v6.0.2] — 2026-04-21

### ETL Suite (4 scripts)
- `etl_trades.py`: stats de trades fechados (WR, R/R, expectancy, drawdown)
- `etl_rejections.py`: breakdown de sinais rejeitados por categoria
- `etl_db_audit.py`: auditoria de integridade; `--fix` corrige stuck/null
- `etl_report.py`: relatório completo JSON + Markdown para análise IA

### Reorganização /scripts
- `scripts/` — 9 arquivos de produção
- `scripts/legacy/` — 11 arquivos de backup e scripts one-time
- `scripts/utils/` — 16 ferramentas de diagnóstico e testes reutilizáveis

### USDJPY Desativado
- WR 42.1% (8/19 trades), P&L -$232.29 — comportamento JPY direcional incompatível

### IndicadorLiquidez.mq5 Fixes
- Zonas estreitas: `InpMinBarsWidth = 60` garante largura mínima ~15h
- Zonas enormes: `_fmt_time()` usa pontos (2026.04.21) para `StringToTime()` MQL5
- Labels invisíveis: `OBJPROP_HIDDEN = false` corrigido

---

## [v6.0.1] — 2026-04-21

### Auditoria Config.yaml (Compliance Fix)
- `min_wick_pct`, `rsi_overbought/oversold`, `risk_reward_ratio`, `lookback_zones` — eram hardcoded
- `use_trend_filter` — flag era ignorada; agora bloqueia se H1 indisponível
- `require_color_reversal` — flag era ignorada; agora controla corretamente
- `daily_profit_target` — nunca verificado; bot agora encerra ao atingir $500

---

## [v6.0] — 2026-04-20 — LIFECYCLE ARCHITECTURE

---

## Resumo Executivo

A versão v6.0 introduz **arquitetura de estados (lifecycle)** completa para gerenciamento de trades, eliminando bugs críticos de sincronização e proporcionando visibilidade total do fluxo desde detecção de sinal até fechamento da posição.

### Problemas Resolvidos

| Problema | v5.9.6 | v6.0 |
|----------|--------|------|
| **Trades com P&L = $0** | 41.6% (42/101 trades) | 0% |
| **Duplicatas** | Possível (sem unique key) | 0% (position_id único) |
| **Visibilidade de Estados** | Apenas "approved" e "closed" | 8 estados detalhados |
| **Sincronização MT5** | Bugada (sync_with_mt5_history) | Automática (lifecycle) |
| **Cooldown** | session_trade_log (memória) | Consulta ao banco |

---

## Arquitetura de Estados

### 8 Estados do Trade

```
signal_detected
      ↓
awaiting_consensus (opcional)
      ↓
   approved
      ↓
    filled (position_id registrado)
      ↓
     open
      ↓
    closed (P&L calculado)

    error (em caso de falha)
```

### Descrição dos Estados

| Estado | Descrição | Campos Preenchidos |
|--------|-----------|-------------------|
| `signal_detected` | Sinal técnico detectado pelo bot | symbol, type, price, sl, tp, wick_pct, magic, created_at |
| `awaiting_consensus` | Aguardando aprovação da sala de guerra | (todos acima) |
| `approved` | Aprovado para execução | + agent_opinions, approved_at |
| `rejected` | Rejeitado pela sala de guerra | + reject_reason |
| `filled` | Ordem executada no MT5 | + position_id, filled_at |
| `open` | Trade ativo (posição aberta) | (todos acima) |
| `closed` | Trade finalizado | + pnl, exit_price, closed_at |
| `error` | Erro na execução | + error_message |

---

## Mudanças Técnicas

### 1. TradeLifecycleManager

**Novo módulo:** `trade_lifecycle_manager.py`

**Métodos principais:**

```python
# Criar sinal detectado
lifecycle.create_signal(symbol, trade_type, price, sl, tp, wick_pct, magic_number)

# Aprovar sinal
lifecycle.approve_signal(signal_id, agent_opinions)

# Rejeitar sinal
lifecycle.reject_signal(signal_id, reason)

# Marcar como executado
lifecycle.mark_as_filled(signal_id, position_id)

# Marcar como posição ativa
lifecycle.mark_as_open(signal_id)

# Fechar trade com P&L
lifecycle.close_trade(position_id, pnl, exit_price)

# Marcar como erro
lifecycle.mark_as_error(signal_id, error_message)
```

### 2. Bot v6.0 - Fluxo de Execução

**Arquivo:** `bot_liquidez.py`

**Fluxo:**

```python
# 1. Detectar sinal
trigger, zone = check_trigger(...)

# 2. Criar sinal no banco (status: signal_detected)
signal = lifecycle.create_signal(
    symbol=trigger['symbol'],
    trade_type=trigger['type'],
    price=trigger['price'],
    sl=trigger['sl'],
    tp=trigger['tp'],
    wick_pct=trigger['wick_pct'],
    magic_number=MAGIC_NUMBER
)

# 3. Auto-aprovar (ou enviar para war room)
lifecycle.approve_signal(signal['id'], agent_opinions=[])

# 4. Executar ordem no MT5
exec_res = send_order(symbol, trigger)

# 5. Marcar como filled com position_id
lifecycle.mark_as_filled(signal['id'], exec_res.order)

# 6. Sincronizar posições (loop separado)
sync_open_positions()  # filled -> open -> closed
```

### 3. Sincronização Automática

**Substituiu:** `sync_with_mt5_history()` (bugada)

**Novo método:** `sync_open_positions()`

**Como funciona:**

1. Busca todos os trades com status `filled` ou `open` no banco
2. Verifica se `position_id` está aberto no MT5
3. Se aberto → marca como `open` (se estava `filled`)
4. Se não aberto → busca histórico de deals e marca como `closed` com P&L

**Vantagens:**

- ✅ Elimina duplicatas (position_id único)
- ✅ Elimina trades com P&L = $0
- ✅ Sincronização automática a cada ciclo
- ✅ P&L sempre correto (vem direto do MT5)

### 4. Cooldown Baseado em Banco

**Substituiu:** `session_trade_log` (memória, perdido em restart)

**Novo método:** `check_cooldown(symbol, current_price, pip_size)`

**Como funciona:**

```python
# Buscar trades recentes deste símbolo (últimas COOLDOWN_HOURS)
recent_trades = lifecycle.client.table("signals_liquidez")\
    .select("price, created_at")\
    .eq("symbol", symbol)\
    .gte("created_at", cutoff_time)\
    .execute()

# Verificar proximity (10 pips)
for trade in recent_trades.data:
    if abs(current_price - trade['price']) <= (PROXIMITY_PIPS * pip_size):
        return True  # Em cooldown
```

**Vantagens:**

- ✅ Persiste entre restarts
- ✅ Funciona mesmo após crash/reconexão
- ✅ Histórico completo no banco

---

## Schema v6.0

### Novas Colunas

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `position_id` | bigint | ID único da posição no MT5 (chave para evitar duplicatas) |
| `exit_price` | numeric | Preço de saída do trade |
| `approved_at` | timestamptz | Timestamp de aprovação |
| `filled_at` | timestamptz | Timestamp de execução |
| `updated_at` | timestamptz | Última atualização |
| `reject_reason` | text | Motivo da rejeição |
| `error_message` | text | Mensagem de erro |

### Índices Criados

```sql
-- Único (previne duplicatas)
CREATE UNIQUE INDEX idx_signals_position_id
ON signals_liquidez(position_id)
WHERE position_id IS NOT NULL;

-- Performance (queries por estado)
CREATE INDEX idx_signals_status ON signals_liquidez(status);

-- Performance (ordenação temporal)
CREATE INDEX idx_signals_created_at ON signals_liquidez(created_at DESC);
```

---

## Migração de Dados

**Executado:** `migrate_to_v6_lifecycle.py --migrate`

**Resultado:**

- 68 trades migrados do MT5 para Supabase
- 0 trades com P&L = $0
- 0 duplicatas
- 100% dos trades com position_id único

**Win Rate Real:** 45.1% (32W / 39L)
**P&L Total:** -$71.31

---

## Testes de Validação

**Script:** `test_bot_v6.py`

**Resultado:** ✅ **Todos os testes passaram**

| Teste | Status |
|-------|--------|
| Conexão MT5 | ✅ OK |
| Conexão Supabase | ✅ OK |
| Criação de sinal | ✅ OK |
| Transições de estado (8 estados) | ✅ OK |
| Funções do bot (get_rates, check_trigger, etc.) | ✅ OK |

---

## Backward Compatibility

### Removido (Breaking Changes)

| Item | Motivo |
|------|--------|
| `SupabaseManager.log_signal()` | Substituído por `lifecycle.create_signal()` |
| `sync_with_mt5_history()` | Substituído por `sync_open_positions()` |
| `session_trade_log` (memória) | Substituído por `check_cooldown()` (banco) |

### Mantido (Compatible)

| Item | Status |
|------|--------|
| `consumed_zones` (JSON file) | ✅ Funciona igual |
| Kill-Zone logic | ✅ Funciona igual |
| One-Shot logic | ✅ Funciona igual |
| Sniper strategy | ✅ Funciona igual |
| MT5 integration | ✅ Funciona igual |

---

## Próximos Passos

### 1. Executar Bot v6.0

```bash
cd C:\Users\Pichau\Desktop\trade\squads\trade-liquidez-python\scripts
python bot_liquidez.py
```

### 2. Monitorar Frontend

Abrir: `http://localhost:3000/historico`

**Validar:**

- ✅ Nenhum trade com P&L = $0.00
- ✅ Todos os valores batem com MT5
- ✅ Estados visíveis (signal_detected, approved, filled, open, closed)

### 3. Integrar War Room (Opcional)

**Arquivo:** `auto_war_room.py`

**Mudanças necessárias:**

```python
# Buscar sinais pendentes
pending_signals = lifecycle.get_pending_signals('awaiting_consensus')

# Aprovar sinal
lifecycle.approve_signal(signal_id, agent_opinions)

# Rejeitar sinal
lifecycle.reject_signal(signal_id, reason)
```

### 4. Atualizar Frontend (Futuro)

**Features sugeridos:**

- Filtros por estado (signal_detected, approved, filled, open, closed)
- Pipeline dashboard (quantos em cada estado)
- Badges coloridos por estado
- Timeline de transições

---

## Benefícios v6.0

| Benefício | Impacto |
|-----------|---------|
| **0 duplicatas** | position_id único |
| **0 trades zerados** | P&L sempre correto do MT5 |
| **Rastreamento completo** | 8 estados detalhados |
| **Frontend organizado** | Filtrar por cada estado |
| **Performance otimizada** | Índices criados |
| **Cooldown persistente** | Funciona após restart |
| **Sincronização automática** | Elimina bugs de sync |

---

## Arquivos Criados/Modificados

### Criados

- ✅ `trade_lifecycle_manager.py` - Gerenciador de estados
- ✅ `migrate_to_v6_lifecycle.py` - Migração de dados
- ✅ `test_bot_v6.py` - Suite de testes
- ✅ `check_schema.py` - Verificação de schema
- ✅ `setup_schema_v6.py` - Validação de schema
- ✅ `sql/setup_schema_v6.sql` - SQL para adicionar colunas
- ✅ `validate_migration.py` - Validação pós-migração
- ✅ `docs/ARQUITETURA_ESTADOS_TRADE.md` - Documentação completa
- ✅ `COMO_EXECUTAR_SQL_SUPABASE.md` - Guia passo a passo
- ✅ `RESUMO_SETUP_V6.md` - Referência rápida
- ✅ `docs/BOT_V6.0_CHANGELOG.md` - Este arquivo

### Modificados

- ✅ `bot_liquidez.py` - Integração com lifecycle (v5.9.6 → v6.0)
- ✅ Backup criado: `bot_liquidez_v5.9.6_backup.py`

---

## Suporte

**Dúvidas?** Contate @dev (Dex)

**Issues?** Verifique:

1. MT5 conectado?
2. Supabase acessível?
3. Schema v6.0 completo? (20 colunas)
4. Migração executada?

**Logs:** Monitore console do bot para mensagens `[LIFECYCLE]`

---

**Desenvolvedor:** @dev (Dex)
**Data:** 2026-04-20
**Status:** ✅ PRODUCTION READY
