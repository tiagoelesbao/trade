# Funcionamento Completo - Bot Trade Liquidez v6.0

**Data:** 2026-04-22
**Versão Atual:** v6.1.3
**Arquitetura:** Source of Truth (MT5) + Lifecycle States + War Room (5 critérios, RSI alpha)

---

## Visão Geral do Sistema

O **Trade Liquidez v6.0** é um sistema de trading algorítmico que opera em **8 pares de moedas** (EURUSD, GBPUSD, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, GBPJPY) com estratégia **Sniper M15** (baixa frequência, alta precisão).

> **USDJPY desativado em v6.0.2** após análise histórica: WR 42.1% (8/19 trades), P&L -$232.29 — 82% das perdas totais. Causa: comportamento direcional do JPY incompatível com estratégia de reversão em zona.
> **EURJPY** também desativado (WR 16.7%, P&L -$85.56).

### Componentes do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│  FULL_START.bat (Orquestrador)                               │
│  ┌─────────┬────────────┬──────────────┬──────────────┐     │
│  │ Phase 1 │  Phase 2   │   Phase 3    │   Phase 4    │     │
│  │ Analyst │ Dashboard  │  War Room    │  Bot Engine  │     │
│  └─────────┴────────────┴──────────────┴──────────────┘     │
└─────────────────────────────────────────────────────────────┘
         ↓           ↓            ↓              ↓
    diagnose   localhost:3000  auto_war  bot_liquidez.py
     _today                     _room            ↓
                                  ↓         MT5 Terminal
                                  ↓              ↓
                        ┌─────────────────────────────┐
                        │   Supabase (PostgreSQL)      │
                        │   signals_liquidez table     │
                        │   20 colunas (v6.0 schema)  │
                        └─────────────────────────────┘
```

---

## FASE 1: Diagnóstico Pré-Sessão (@analyst)

**Script:** `diagnose_today.py`

**Função:** Analisar histórico do dia e ajustar config.yaml dinamicamente.

**Ações:**
- Verifica P&L do dia
- Identifica símbolos problemáticos (win rate < 30%)
- Sugere ajustes em filtros (RSI, wick_pct, slope)
- Carrega configuração Sniper

---

## FASE 2: Dashboard Next.js (Frontend)

**Porta:** 3000 (`localhost:3000`)

**Páginas:**
- `/` - Dashboard principal (visão geral)
- `/historico` - Histórico de trades com filtros
- `/performance` - Métricas de desempenho

**Sincronização:** Real-time com Supabase (PostgreSQL)

**Dados exibidos:**
- Trades em tempo real (status, P&L, símbolos)
- Gráficos de performance
- Estados do lifecycle (signal_detected, approved, filled, open, closed)

---

## FASE 3: Sala de Guerra Agêntica (War Room)

**Script:** `auto_war_room.py`

**Função:** Analisar e aprovar/rejeitar sinais detectados.

### Estado Atual (v6.1.2/v6.1.3 — IMPLEMENTADO)

A War Room executa em **2 fases** (v6.1.3):

**FASE 1 — Strategy Fire** (impressa antes do scoring): card mostrando OHLC da vela,
gatilhos atendidos (Wick/RSI/Sessão) e plano de execução (entry/SL/TP/RR).

**FASE 2 — Scoring matemático** (5 critérios, 100 pts, RSI alpha):

```python
# Busca sinais com status "awaiting_consensus"
pending = lifecycle.get_pending_signals('awaiting_consensus')

# Scoring técnico (0–100 pontos, 5 critérios — v6.1.2):
# - RSI Extremo (35pts): ALPHA — RSI(9) >= 70 (SELL) ou <= 30 (BUY).
#                         Distância vs limite: 30%/70% = 0pts; 85% = 17.5pts; >=100% = 35pts
# - Wick %      (25pts): wick_pct >= 0.50 = 25 pontos (bot já validou >=30%)
# - Pin Bar     (20pts): corpo <= 15% do range = 20 pontos
# - Sessão      (15pts): London+NY overlap (13–17h UTC) = 15 pontos
# - Histórico   ( 5pts): win rate símbolo >= 60% = 5 pontos

# Removidos em v6.1.2:
# - Slope H1 (15pts): bot já não usa como gate desde v6.1.1
# - Volume   (10pts): trader: "não casa com reversão em zona"

# Score >= 55 → APROVADO | Score < 55 → REJEITADO
lifecycle.approve_signal(signal_id, agent_opinions)
# ou
lifecycle.reject_signal(signal_id, reason)
```

**Proteções adicionais da War Room:**
- Apenas 1 aprovação por ciclo (maior score priorizado)
- Bloqueio por correlação: EURUSD↔GBPUSD, EURUSD↔USDCHF, AUDUSD↔NZDUSD
- Limpeza automática se >10 sinais acumulados

---

## FASE 4: Motor de Execução (Bot Engine)

**Script:** `bot_liquidez.py v6.0`

**Função:** Detectar sinais, executar trades, gerenciar posições.

### Ciclo Principal (Loop infinito a cada 20 segundos)

```python
while True:
    # 1. SINCRONIZAR POSIÇÕES ABERTAS
    sync_open_positions()  # filled -> open -> closed

    # 2. CALCULAR P&L DA SESSÃO
    pnl_session = get_session_pnl()  # Direto do MT5, desde SESSION_START

    # 3. VERIFICAR LIMITES FINANCEIROS
    if pnl_session <= -daily_max_loss:      # config.yaml: 350.0
        ENCERRAR BOT  # Stop diário
    if pnl_session >= daily_profit_target:  # config.yaml: 500.0
        ENCERRAR BOT  # Meta diária

    # 4. PROCESSAR CADA SÍMBOLO (8 símbolos ativos)
    trade_executed_this_cycle = False  # FLAG: 1 trade por ciclo

    for symbol in symbols:
        # 4.1 Verificar se já tem posição aberta
        if mt5.positions_get(symbol):
            continue  # Pula se já está operando

        # 4.2 Buscar dados
        df_m15 = get_rates(symbol, M15, 100)  # 100 velas M15
        zones = get_validated_zones(df_m15)   # Zonas S/R
        df_h1 = get_rates(symbol, H1, 50)     # 50 velas H1

        # 4.3 Verificar gatilho (SNIPER LOGIC)
        trigger, zone = check_trigger(
            symbol, df_m15, zones, consumed_zones, df_h1
        )

        # 4.4 Executar SE houver trigger E não executou neste ciclo
        if trigger and not trade_executed_this_cycle:
            # LIFECYCLE v6.0:

            # Criar sinal (status: signal_detected)
            signal = lifecycle.create_signal(...)

            # Auto-aprovar (ou enviar para war room)
            lifecycle.approve_signal(signal['id'])

            # Executar ordem no MT5
            exec_res = mt5.order_send(...)

            # Marcar como filled (registra position_id)
            lifecycle.mark_as_filled(signal['id'], exec_res.order)

            # Marcar flag: apenas 1 trade por ciclo
            trade_executed_this_cycle = True

            # Consumir zona (one-shot)
            consumed_zones.add(trigger['z_key'])

    # 5. SALVAR ZONAS CONSUMIDAS (persistência)
    save_consumed_zones(consumed_zones)

    # 6. AGUARDAR 20 SEGUNDOS
    time.sleep(20)
```

---

## Estratégia Sniper M15 (Lógica de Entrada)

### Função: `check_trigger()`

**Validações em Sequência (v6.1.3):**

| # | Validação | Descrição |
|---|-----------|-----------|
| 1 | **Dados suficientes** | df_m15 tem >= 15 candles |
| 2 | **Cooldown** | Não tradou este símbolo nas últimas 4h (Kill-Zone) |
| 3 | **Proximity** | Não há trade recente num raio de 10 pips |
| 4 | **RSI(9)** | >= 70 (SELL) ou <= 30 (BUY) — `rsi_period: 9` no config |
| 5 | **Wick Rejection** | Pavio >= 30% da vela total |
| 6 | **Zona Tocada** | Preço tocou zona S/R validada |
| 7 | **Zona Não Consumida** | Zona não foi usada antes (one-shot) |

**Filtros desativados em v6.1.1 (parecer técnico):**
- ~~Slope Guard MA20 H1~~: `use_trend_filter: false` — operava invertido para estratégia contra-tendência
- ~~Reversão de Cor~~: `require_color_reversal: false` — atrasava entrada no ponto ótimo

**Se TODAS as 7 condições passarem:**
- Retorna `trigger` (dict com symbol, type, price, sl, tp)
- Retorna `zone` (zona que foi tocada)
- SL = high/low do pavio ± `stop_buffer_points × point` (50 pts = 5 pips em v6.1.3)
- TP = entry ± distância_SL × `risk_reward_ratio` (1.5)

**Senão:**
- Retorna `None, None`

---

## Múltiplos Sinais Simultâneos

### SIM, o bot processa APENAS 1 TRADE POR CICLO

**Mecanismo:**

```python
trade_executed_this_cycle = False

for symbol in symbols:
    trigger = check_trigger(symbol, ...)

    if trigger and not trade_executed_this_cycle:
        # EXECUTA
        execute_trade(trigger)
        trade_executed_this_cycle = True  # BLOQUEIA demais
```

**Exemplo:**

Se em um ciclo de 20 segundos:
- EURUSD tem sinal válido
- GBPUSD tem sinal válido
- USDJPY tem sinal válido

**Resultado:**
- EURUSD é executado (primeiro na lista)
- GBPUSD é IGNORADO (flag já ativada)
- USDJPY é IGNORADO (flag já ativada)

**Por quê?**

1. **Gestão de Risco:** Evitar overtrading
2. **Capital Limitado:** $99,968 de balance
3. **Correlação:** Muitos pares correlacionados (ex: EURUSD + GBPUSD)

---

## Problema: Seleção de Melhor Sinal

**Atualmente:** Primeiro sinal válido é executado (ordem da lista de símbolos).

**Proposta:** Priorizar sinal com maior confiança.

### Critérios de Priorização (a implementar):

| Critério | Peso | Como Calcular |
|----------|------|---------------|
| **Wick %** | 30% | Maior pavio = maior rejeição = mais forte |
| **RSI Extremo** | 25% | RSI 70+ ou 30- = mais sobrecompra/venda |
| **Slope H1** | 20% | Maior inclinação = tendência mais forte |
| **Distância da Zona** | 15% | Mais próximo do centro da zona = melhor |
| **Histórico do Símbolo** | 10% | Win rate do símbolo (últimos 30 dias) |

**Score Final:**
```python
score = (wick_pct * 0.30) +
        (rsi_extreme * 0.25) +
        (slope_strength * 0.20) +
        (zone_proximity * 0.15) +
        (symbol_wr * 0.10)
```

**Sinal com maior score é executado.**

---

## Proteções Operacionais

### 1. Kill-Zone (Cooldown)

**Objetivo:** Evitar re-entrada prematura no mesmo símbolo.

**Implementação:**
```python
# Buscar trades recentes deste símbolo (últimas 4h)
recent_trades = supabase.select(...).eq("symbol", symbol).gte("created_at", cutoff_time)

# Se há trade recente dentro de 10 pips:
if abs(current_price - trade['price']) <= 10 pips:
    return None  # Bloqueado
```

**Persistência:** Banco de dados (funciona após restart)

### 2. One-Shot (Zonas Consumidas)

**Objetivo:** Não reusar zonas que falharam.

**Implementação:**
```python
consumed_zones = load_consumed_zones()  # JSON file

if z_key in consumed_zones:
    continue  # Zona já foi usada

# Após executar trade:
consumed_zones.add(z_key)
save_consumed_zones(consumed_zones)
```

**Limpeza:** Zonas expiram após 24h (auto-cleanup).

### 3. Stop Loss Diário

**Objetivo:** Proteção financeira.

**Implementação:**
```python
if pnl_session <= -daily_max_loss:   # config.yaml: $350.00
    print("STOP LOSS DIÁRIO ATINGIDO!")
    break  # Encerra bot
```

**Fonte:** P&L calculado direto do MT5 (deals history), valor lido de `config.yaml`.

### 4. Limite: 1 Trade por Ciclo

**Objetivo:** Evitar overtrading e correlação.

**Implementação:** Flag `trade_executed_this_cycle` (visto acima).

---

## Sincronização MT5 ↔ Supabase

### Função: `sync_open_positions()`

**Executada:** A cada ciclo (20 segundos).

**Lógica:**

```python
# 1. Buscar trades "filled" ou "open" no banco
active_trades = supabase.select(...).in_("status", ["filled", "open"])

# 2. Buscar posições abertas no MT5
mt5_positions = mt5.positions_get()

# 3. Para cada trade no banco:
for trade in active_trades:
    if trade['position_id'] in mt5_positions:
        # Posição ainda aberta
        if trade['status'] == 'filled':
            lifecycle.mark_as_open(trade['id'])  # filled -> open
    else:
        # Posição fechada
        check_if_closed(trade)  # Busca histórico de deals
```

### Função: `check_if_closed(trade)`

**Objetivo:** Verificar se posição foi fechada e calcular P&L.

**Lógica:**

```python
# Buscar deals desta posição
deals = mt5.history_deals_get(position=trade['position_id'])

# Encontrar deal de saída (entry == 1)
for deal in deals:
    if deal.entry == 1:  # Deal de saída
        pnl_real = deal.profit + deal.commission + deal.swap
        exit_price = deal.price

        # Atualizar banco: open -> closed
        lifecycle.close_trade(
            position_id=trade['position_id'],
            pnl=pnl_real,
            exit_price=exit_price
        )
```

**Resultado:** P&L sempre correto (vem direto do MT5).

---

## Indicador MT5 (IndicadorLiquidez.mq5)

**Objetivo:** Visualizar zonas e sinais no gráfico MT5.

**Funcionamento:**

1. Bot exporta zonas para CSV em `MQL5/Files/liquidez_data_{SYMBOL}.csv`:
   - Linha `BOT_STATUS,{pnl_sessao},{pnl_total},{n_exauridas}`
   - Até 6 zonas de RESISTÊNCIA (mais próximas ao preço, após merge de 15 pips)
   - Até 6 zonas de SUPORTE (mais próximas ao preço, após merge de 15 pips)
   - Timestamps no formato **`YYYY.MM.DD HH:MM:SS`** (pontos — exigido por `StringToTime()`)

2. Indicador lê CSV a cada 5 segundos e renderiza:
   - `OBJ_RECTANGLE` (retângulo preenchido) — zona
   - `OBJ_TREND` (linha pontilhada) — centro da zona
   - `OBJ_TEXT` (label de preço) — ancorado 1 barra fora do retângulo
   - Destaque de zonas dentro de 25 pips (cor mais intensa, texto branco)
   - Painel BOT STATUS: P&L Sessão, P&L Total, Zonas Exauridas

3. **Largura mínima garantida:** `InpMinBarsWidth = 60` barras M15 (~15h) — evita zonas invisíveis para detecções recentes.

4. **Limpeza agressiva:** Antes de redesenhar, apaga todos os objetos (sincroniza com "zonas exauridas").

**Arquivo CSV:** `C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\liquidez_data_{symbol}.csv`

**Bugs corrigidos (v6.0.2):**
- Zonas enormes → timestamp com hífens (`2026-04-20`) passado para `StringToTime()` retornava 0 → zona desde 1970. Corrigido com `_fmt_time()` no Python
- Zonas invisíveis → labels com `OBJPROP_HIDDEN = true`. Corrigido para `false`
- Zonas muito estreitas → `InpMinBarsWidth = 60` adicionado

---

## Configurações (config.yaml)

### Símbolos Operados (9)

```yaml
symbols:
  - EURUSD, GBPUSD, AUDUSD, USDCAD,
    USDCHF, NZDUSD, EURGBP, GBPJPY
  # USDJPY: DESATIVADO — WR 42.1%, P&L -$232.29
  # EURJPY: DESATIVADO — WR 16.7%, P&L -$85.56
```

### Filtros de Entrada (v6.1.3)

| Filtro | Valor | Descrição |
|--------|-------|-----------|
| `min_wick_pct` | 0.30 | Pavio >= 30% da vela |
| `rsi_period` | 9 | Período do RSI (v6.1.3 — antes hardcoded 14) |
| `rsi_overbought` | 70 | SELL se RSI(9) >= 70 |
| `rsi_oversold` | 30 | BUY se RSI(9) <= 30 |
| `use_trend_filter` | **false** | DESATIVADO em v6.1.1 (parecer técnico) |
| `require_color_reversal` | **false** | DESATIVADO em v6.1.1 (atrasava entrada) |
| ~~`slope_threshold_pips`~~ | — | REMOVIDO do config em v6.1.3; default `0.5` em `CFG.get(...)` |

### Proteções

| Proteção | Valor | Descrição |
|----------|-------|-----------|
| `cooldown_hours` | 4 | Kill-Zone: 4 horas |
| `proximity_pips` | 10 | Raio de bloqueio: 10 pips |
| `daily_max_loss` | 350.0 | Stop loss diário: $350 (sessão) |

### Gestão de Risco (v6.1.3)

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `lot_size` | 1.0 | Lote fixo por trade |
| `stop_buffer_points` | **50** | Buffer adicional no SL — 5 pips (v6.1.3: 15→50 para absorver varredura de liquidez) |
| `risk_reward_ratio` | 1.5 | TP = 1.5x SL |
| `breakeven_candles` | **0** | DESATIVADO em v6.1.3 (era 7 = 1h45min ejetava trades em pullbacks) |

---

## Lifecycle v6.0 - Estados do Trade

```
1. signal_detected      # Sinal técnico detectado
2. awaiting_consensus   # Aguardando sala de guerra (OPCIONAL)
3. approved             # Aprovado para execução
4. rejected             # Rejeitado (motivo registrado)
5. filled               # Ordem executada (position_id registrado)
6. open                 # Posição ativa no MT5
7. closed               # Trade finalizado (P&L calculado)
8. error                # Erro na execução
```

**Transições:**

```
signal_detected --(auto_war_room)--> approved
approved --(mt5.order_send)--> filled
filled --(sync_open_positions)--> open
open --(check_if_closed)--> closed
```

---

## Schema Supabase (20 colunas)

### Colunas Originais (13)

- id, symbol, type, price, sl, tp, status, pnl, magic, wick_pct, created_at, closed_at, agent_opinions

### Colunas v6.0 (7 novas)

- position_id, exit_price, approved_at, filled_at, updated_at, reject_reason, error_message

### Índices

- `idx_signals_position_id` (UNIQUE) - Previne duplicatas
- `idx_signals_status` - Performance em queries por estado
- `idx_signals_created_at` - Ordenação temporal

---

## Estatísticas Atuais (Pós-Migração v6.0)

| Métrica | Valor |
|---------|-------|
| **Total de Trades** | 71 |
| **Trades com P&L = $0** | 0 (RESOLVIDO!) |
| **Duplicatas** | 0 (RESOLVIDO!) |
| **Win Rate Real** | 45.1% (32W / 39L) |
| **P&L Total** | -$71.31 |
| **Média por Trade** | -$1.00 |

---

## Breakeven Automático (`check_breakeven()`)

> **Status v6.1.3: DESATIVADO (`breakeven_candles: 0`).** Motivo: com 7 velas (1h45min),
> trades estavam sendo ejetados a zero em pullbacks normais antes da tese consolidar.
> Código mantido para reativação futura.

Quando ativo (`breakeven_candles > 0`), executa a cada ciclo (20s), logo após `sync_open_positions()`.

**Condições para mover o SL:**
1. `breakeven_candles > 0` no `config.yaml` (feature ativa)
2. Trade em status `open` há pelo menos `breakeven_candles × 15min` desde `filled_at`
3. Preço atual favorável (trade em lucro)
4. SL ainda está do lado de risco (não foi movido antes)

**Cálculo:**
```python
# BUY:  novo SL = entry_price + 2 pontos
# SELL: novo SL = entry_price - 2 pontos
# TP: inalterado
mt5.order_send({"action": TRADE_ACTION_SLTP, "sl": breakeven_sl, "tp": pos.tp})
```

**Resultado:** trade não pode mais virar prejuízo após o tempo configurado se o preço estiver favorável. O SL fica no custo zero + 2 pontos de buffer (garante lucro mínimo mesmo que o mercado reverta para a entrada).

**Log gerado:**
```
[BOT] [EURUSD] breakeven_moved: EURUSD BUY | SL 1.08350 → 1.08502 (entrada:1.08500 | candles:8)
```

**Configuração:**
```yaml
breakeven_candles: 0   # v6.1.3: 0 = desativado (era 7 = 1h45min após abertura)
```

---

## Suite ETL (Análise e Auditoria)

Scripts Python em `/scripts/` para uso diário após sessão de trading:

### `etl_trades.py` — Análise de Trades
```bash
python etl_trades.py --session           # trades da sessão atual
python etl_trades.py --from 2026-04-21  # por data
python etl_trades.py --output csv        # exportar para planilha
```
Calcula: WR, R/R, expectancy/trade, max drawdown, curva de equity, stats por símbolo.

### `etl_rejections.py` — Análise de Rejeições
```bash
python etl_rejections.py --from 2026-04-21 --detail
python etl_rejections.py --reason trend  # filtrar por motivo
```
Breakdown por categoria: `trend_filter`, `rsi_filter`, `wick_filter`, `cooldown`, `proximity`, `reversal_filter`, `daily_limit`.

### `etl_db_audit.py` — Integridade do Banco
```bash
python etl_db_audit.py --verbose         # lista problemas
python etl_db_audit.py --fix             # corrige automaticamente
```
Verifica: trades `closed` com `pnl=NULL`, stuck open >24h, position_id duplicado, status inválido.

### `etl_report.py` — Relatório Completo para IA
```bash
python etl_report.py --session --format both
```
Gera `.json` + `.md` combinando trades, rejeições, logs e equity curve — pronto para colar em Claude/ChatGPT para análise de padrões.

---

## Respondendo Suas Perguntas

### 1. "É isso mesmo? O sistema só entra em um por vez?"

**SIM.** O bot executa **APENAS 1 TRADE POR CICLO** (20 segundos).

**Motivo:**
- Flag `trade_executed_this_cycle` bloqueia demais trades no mesmo ciclo.
- Gestão de risco: Evitar overtrading e correlação entre pares.

### 2. "E se houver vários sinais simultâneos?"

**Atualmente:** Primeiro sinal válido é executado (ordem alfabética).

**Problema:** Não há priorização por qualidade.

**Solução (a implementar):** Scoring de sinais (wick %, RSI extremo, slope, etc.).

### 3. "Como funciona a análise dos agentes?"

**Atualmente (auto_war_room.py v5.x):**
- Gera 3 opiniões fictícias (Jim Simons, Druckenmiller, Taleb)
- Aprova TODOS os sinais automaticamente
- Não há validação técnica real

**Próximo Passo (v6.0):**
- Análise técnica real (RSI, volume, tendência)
- Rejeição de sinais fracos
- Priorização por scoring
- Integração com `TradeLifecycleManager`

---

## Próximos Passos

1. ✅ **Schema v6.0** - COMPLETO
2. ✅ **Migração de Dados** - COMPLETO
3. ✅ **Bot v6.0 (Lifecycle)** - COMPLETO
4. ⏳ **War Room v6.0** - A IMPLEMENTAR AGORA
   - Análise técnica real
   - Scoring de sinais
   - Priorização quando há múltiplos
   - Integração com lifecycle

---

**Autor:** @dev (Dex)
**Data:** 2026-04-22
**Versão:** v6.1.3 (Lifecycle + War Room 5-critérios RSI alpha + RSI 9 + SL/Breakeven tuning)
