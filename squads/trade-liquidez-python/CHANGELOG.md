# CHANGELOG - Trade Liquidez Python

---

## [v6.1.3] - 2026-04-22 - RSI(9) ALPHA + SL/BREAKEVEN TUNING

### RSI período 9 promovido como default (item H do parecer técnico)

`config.yaml` agora expõe `rsi_period: 9` (antes hardcoded 14). Adoção feita
**sem teste A/B** — decisão explícita do trader: período 9 é o clássico,
mais reativo, melhor para entrar nos extremos da zona.

- `bot_liquidez.py`: `RSI_PERIOD = CFG.get('rsi_period', 9)`; `calculate_rsi(series, period=None)` usa o config.
- `auto_war_room.py`: mesma constante, scoring de RSI lê o período do config.
- Banner do bot e dashboard exibem `RSI(9) 30/70`.

### Ajuste de SL — `stop_buffer_points: 15 → 50` (1.5p → 5p)

Análise de 3 trades em 2026-04-22 mostrou entradas no ponto ótimo (topo/fundo
da varredura) sendo estopadas por 1–2 pips antes da reversão. Buffer subiu
para 50 pts (5 pips) para absorver a varredura típica de liquidez antes da
reversão consolidar. Risco-recompensa permanece 1:1.5.

### Breakeven desativado por padrão — `breakeven_candles: 7 → 0`

Com 7 velas (1h45min), trades estavam sendo ejetados a zero em pullbacks
normais antes da tese consolidar. Setado para `0` (desativado). Código da
feature mantido para reativação futura.

### Slope removido completamente do scoring (continuação da v6.1.1)

`slope_threshold_pips` removido do `config.yaml` — estava abandonado desde
v6.1.1 quando `use_trend_filter` foi setado para `false`. Default `0.5`
permanece em `CFG.get(...)` no código para reativação segura no futuro.

### Logs FASE 1 (Strategy Fire) na War Room

Novo card impresso **antes** do scoring matemático, mostrando as condições
de mercado que dispararam o sinal:

```
┌── [FASE 1] STRATEGY FIRE  |  EURUSD SELL  |  zona: RESISTÊNCIA
│  Vela M15 fechada @ HH:MM (vermelha)
│     OHLC : O=1.08540 H=1.08580 L=1.08490 C=1.08510
│     range=9.0 pips  corpo=33% do range
│  Gatilhos da estrategia (v6.1.2 — Zona+Wick+RSI):
│     [OK] Wick superior: 78%  (min 30%)
│     [OK] RSI(9)       : 87.3  (limite >= 70)
│     [OK] Sessao UTC   : 14h -> London+NY overlap
│  Plano: entry=1.08510 SL=1.08580 TP=1.08405  RR=1:1.5
└── decisao: gatilhos ATENDIDOS -> [FASE 2] scoring
```

Implementado via `derive_strategy_context(signal)` (single fetch M15+H1)
e `print_strategy_fire(signal, ctx)`. `analyze_signal_strength` aceita o
ctx pré-computado para evitar re-fetch.

### Arquivos Modificados
- `config.yaml` — `rsi_period: 9` adicionado, `slope_threshold_pips` removido, `stop_buffer_points: 50`, `breakeven_candles: 0`
- `scripts/bot_liquidez.py` — `RSI_PERIOD` global, `calculate_rsi(period=None)`, dashboard atualizado
- `scripts/auto_war_room.py` — `RSI_PERIOD` global, `derive_strategy_context()`, `print_strategy_fire()`
- `scripts/IndicadorLiquidez.mq5` — bump cosmético `v6.1 → v6.1.3` no painel/header

---

## [v6.1.2] - 2026-04-22 - WAR ROOM SCORING REFORM (5 critérios, RSI alpha)

### Reforma do scoring após call com trader experiente

Scoring v6.1 (7 critérios) foi reformado para **5 critérios** com **RSI promovido
a alpha** (35 pts — peso máximo). Slope e Volume **removidos**. Score mínimo
mantido em **55/100**.

| Critério | v6.1 | v6.1.2 | Justificativa |
|---|---|---|---|
| **RSI Extremo** | 15 pts | **35 pts** | **ALPHA** — tese central da estratégia |
| Wick % | 20 pts | 25 pts | Premia distância extra além do mínimo de 30% |
| Pin Bar | 20 pts | 20 pts | Mantido — corpo ≤ 15% do range |
| Sessão | 15 pts | 15 pts | London+NY overlap (13–17h UTC) |
| Histórico | 5 pts | 5 pts | Poucos dados locais — peso baixo |
| ~~Slope H1~~ | 15 pts | **REMOVIDO** | Bot já não usa como gate desde v6.1.1 |
| ~~Volume~~ | 10 pts | **REMOVIDO** | Trader: "volume não casa com reversão em zona" |

**RSI Extremo (alpha):** distância em relação ao limite (70/30). RSI 30%/70% = 0pts;
RSI 85% = 17.5pts; RSI ≥100% (SELL) ou ≤0% (BUY) = 35pts.

### Arquivos Modificados
- `scripts/auto_war_room.py` — `analyze_signal_strength()` com 5 critérios, RSI 35 pts
- `scripts/system_logger.py` — `SCORE_MAX`/`SCORE_LABELS`/`SCORE_KEYS_ORDER` reduzidos para 5

---

## [v6.1.1] - 2026-04-21 - DESATIVAÇÃO SLOPE + COLOR REVERSAL (parecer técnico)

### Filtros desativados após call com trader experiente

Análise técnica do parecer (`assets/analise-call-parecer-tecnico.md`)
identificou dois filtros prejudicando entradas legítimas:

**A+B. Slope Guard MA20 H1 (`use_trend_filter: true → false`):**
- Filtro operava **invertido** para estratégia contra-tendência
- Bloqueava exatamente as melhores entradas (reversão em zona)
- Decisão: filtro desligado por padrão; código preservado para reativação

**E. Color Reversal (`require_color_reversal: true → false`):**
- Exigia que a vela atual tivesse cor oposta à anterior
- Atrasava entrada para o segundo candle, perdendo o ponto ótimo
- Em zona, a primeira vela com wick + RSI extremo já é o sinal

### Diretriz arquitetural Fase 3

MA100/200 H1 (item F do parecer) será adicionada **exclusivamente como
pontuação** na War Room (peso máx 20pts), **NUNCA** como gate em
`bot_liquidez.check_trigger()`. Usar como gate repetiria o erro do Slope
Guard. Documentado em `feedback_strategy_macro_trend.md`.

### Arquivos Modificados
- `config.yaml` — `use_trend_filter: false`, `require_color_reversal: false` com comentários explicativos

---

## [v6.1.0] - 2026-04-21 - WAR ROOM REDESIGN + LOGS DETALHADOS + BREAKEVEN

### War Room v6.1 — Scoring Redesenhado (7 critérios)

Scoring anterior penalizava critérios que o bot **já validou** como mínimo antes de enviar o sinal.
Nova distribuição de pesos foca em critérios que o bot não verifica:

| Critério | v6.0 | v6.1 | Obs |
|---|---|---|---|
| Wick % | 30 pts | 20 pts | Bot já valida ≥30% |
| **Pin Bar** | — | 20 pts | **NOVO**: corpo/range da vela (rejeição limpa vs vela suja) |
| RSI Extremo | 25 pts | 15 pts | Bot já filtra; War Room premia distância extra |
| Slope H1 | 20 pts | 15 pts | Bot já valida direção; War Room premia força |
| **Sessão** | — | 15 pts | **NOVO**: London+NY overlap=15, sessão isolada=10, Ásia=3 |
| Volume | 15 pts | 10 pts | Reduzido |
| Histórico | 10 pts | 5 pts | Poucos dados locais = dado frágil |

Score mínimo ajustado de 60 → **55** (scoring mais criterioso distribui melhor).

### SystemLogger — `signal_analysis()` — Logs Completos

Novo método `signal_analysis()` no `SystemLogger` substitui os `logger.warning/info` simples:

**Console** imprime card completo por sinal:
```
[WAR_ROOM] [EURUSD] ◈ signal_analysis:
   ✗ EURUSD SELL  @1.08500  SL:1.08560  TP:1.08410  pavio:45%
   ───────────────────────────────────────────────────────────
   Wick    [##############]   18.0/20  (90.0%)  pavio 45%
   PinBar  [####################]  20.0/20  (100%)  corpo 6% range [perfeito]
   RSI     [###-----------]    4.5/15  (30.0%)  RSI 67.0
   Slope   [######--------]    7.5/15  (50.0%)  -1.20 pip/vela H1
   Sessao  [##############]   15.0/15  (100%)   London+NY overlap
   Volume  [#####---------]    5.0/10  (50.0%)  1.25x média
   Hist    [##########----]    4.0/ 5  (80.0%)  WR 56% (9T/30d)
   ───────────────────────────────────────────────────────────
   TOTAL   [################----]  74.0/100  (+19.0 pts vs mínimo 55)
   → APROVADO — Score 74.0/55 → execução
   [JS] Jim Simons   18%  "RSI 67.0. Nível aceitável, sem amplitude."
   [SD] Druckenmiller 84%  "Pavio 45%, corpo 6%. Pin bar perfeito..."
   [NT] Nassim Taleb  34%  "WR 56% (9T, 30d). Sessão: London+NY overlap..."
```

**Supabase** (`bot_logs.data`) grava JSON estruturado completo: verdict, total_score, scores por critério, valores brutos (RSI, slope_pips, volume_ratio, symbol_wr, sessão), opiniões dos agentes.

### Breakeven Automático

Nova função `check_breakeven()` executada a cada ciclo de 20s após `sync_open_positions()`.

**Lógica:**
1. Para cada posição aberta com `magic == MAGIC_NUMBER`
2. Verifica se `filled_at` + `breakeven_candles × 15min` já passou
3. Se trade está em lucro E SL ainda está do lado de risco → move SL para `entry + 2 pts` (BUY) ou `entry - 2 pts` (SELL) via `TRADE_ACTION_SLTP`
4. TP permanece intacto
5. Log registrado em `bot_logs` com SL antigo, novo SL, candles abertos

**Configuração em `config.yaml`:**
```yaml
breakeven_candles: 7   # 0 = desativado | 7 = após 1h45min em M15
```

Condições de segurança:
- Trade deve estar **em lucro** no momento da verificação (não move se preço voltou)
- SL que já foi movido para breakeven não é modificado novamente
- `retcode` verificado — falhas logadas como WARNING

### Arquivos Modificados
- `scripts/auto_war_room.py` — scoring v6.1 (7 critérios), score mínimo 55
- `scripts/system_logger.py` — novo método `signal_analysis()` com breakdown completo
- `scripts/bot_liquidez.py` — `check_breakeven()`, global `BREAKEVEN_CANDLES`, chamada no loop

---

## [v6.0.2] - 2026-04-21 - ETL SUITE + ORGANIZAÇÃO + INDICADOR FIXES

### Suite de Scripts ETL

Quatro scripts Python para análise e auditoria diária das operações:

| Script | Função |
|---|---|
| `etl_trades.py` | Trades fechados com stats completos (WR, R/R, expectancy, max DD), filtros por sessão/data/símbolo, export JSON/CSV |
| `etl_rejections.py` | Sinais rejeitados com breakdown por categoria (trend_filter, rsi_filter, wick_filter, cooldown, proximity…), top motivos, por símbolo |
| `etl_db_audit.py` | Auditoria de integridade: closed c/ pnl=NULL, pnl=0 suspeito, stuck open >24h, position_id duplicado, status inválido; `--fix` aplica correções |
| `etl_report.py` | Relatório completo (JSON + Markdown) pronto para colar em IA: equity curve, stats por símbolo, rejeições categorizadas, logs de sessão |

Uso rápido:
```bash
python etl_report.py --session --format both   # relatório da sessão atual
python etl_db_audit.py --verbose               # integridade do banco
python etl_rejections.py --from 2026-04-21 --detail
python etl_trades.py --output csv
```

### Reorganização de `/scripts`

Estrutura limpa para manutenção:
- **`/scripts/`** — apenas 9 arquivos de produção (bot + ETL + indicador)
- **`/scripts/legacy/`** — 11 arquivos: backups v5.x, scripts de setup/migração one-time, scripts de limpeza
- **`/scripts/utils/`** — 16 arquivos: market_replay, simulate_trade, diagnose_*, audit_*, check_*, optimize_hyperparams, war_room_voter, etc.

### Desativação de USDJPY

Análise do histórico de trades revelou:
- **USDJPY:** WR 42.1% (8/19 trades), P&L **-$232.29** — 82% das perdas totais
- **EURJPY:** WR 16.7% (1/6 trades), P&L **-$85.56** (já estava desativado)

Causa raiz do USDJPY: overtrading em 2026-04-20 por flags de filtro ignoradas (corrigido em v6.0.1) + incompatibilidade do comportamento do JPY com estratégia de reversão em zona.

`config.yaml` atualizado:
```yaml
# - USDJPY  # DESATIVADO: WR 42.1% (8/19), P&L -$232.29 | JPY tendência forte vs estratégia reversão
# - EURJPY  # DESATIVADO: WR 16.7% (1/6), P&L -$85.56
```

**Símbolos ativos: 8** (EURUSD, GBPUSD, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, GBPJPY)

### Fixes do IndicadorLiquidez.mq5

- **Zonas estreitas corrigidas:** `InpMinBarsWidth = 60` garante largura mínima de 60 barras M15 (~15h) — zonas recentes não apareciam porque tinham largura quase zero
- **Zonas enormes corrigidas:** Bug de timestamp — Python exportava `"2026-04-20"` (hífens) mas `StringToTime()` do MQL5 requer `"2026.04.20"` (pontos). Sem conversão, `t=0` → retângulo desde 1970. Corrigido com `_fmt_time()` no Python
- **Labels invisíveis corrigidas:** `OBJPROP_HIDDEN = true` estava ativo em `OBJ_TEXT`. Corrigido para `false`; label posicionado 1 barra fora do retângulo (`TimeCurrent() + 15*60`)
- **`InpZonePips = 10`** (era 8) — zona com raio de 10 pips
- **Painel:** "Hoje:" → "Sessão:" (alinhado com P&L de sessão)

### Arquivos Criados/Modificados
- Criados: `scripts/etl_trades.py`, `scripts/etl_rejections.py`, `scripts/etl_db_audit.py`, `scripts/etl_report.py`
- Criados: `scripts/legacy/` (11 arquivos movidos), `scripts/utils/` (16 arquivos movidos)
- Modificados: `config.yaml` (USDJPY desativado), `scripts/IndicadorLiquidez.mq5` (3 bugs corrigidos)

---

## [v6.0.1] - 2026-04-21 - CONFIG AUDIT (Compliance Fix)

### Auditoria completa de config.yaml vs código

**Problema identificado:** Parâmetros críticos do `config.yaml` não estavam sendo lidos pelo bot —
valores eram hardcoded. Flags `use_trend_filter` e `require_color_reversal` eram silenciosamente ignoradas,
causando entradas indevidas (ex: USDJPY com H1 neutro/sem dados).

### Fixes Aplicados

- **`min_wick_pct`** — era hardcoded `0.3`, agora lê `CFG['min_wick_pct']` via `MIN_WICK_PCT`
- **`rsi_overbought / rsi_oversold`** — eram hardcoded `60/40`, agora lêem config via `RSI_OVERBOUGHT / RSI_OVERSOLD`
- **`use_trend_filter`** — flag era **ignorada**; agora: se `true`, H1 indisponível **bloqueia** o trade; `trend_slope < 0` obrigatório para SELL, `trend_slope > 0` para BUY (antes `<= 0` e `>= 0` deixavam neutro passar)
- **`require_color_reversal`** — flag era **ignorada**; agora controla se a reversão de cor é exigida
- **`risk_reward_ratio`** — era hardcoded `*1.5`; agora usa `RR_RATIO = CFG['risk_reward_ratio']` com cálculo correto baseado na distância real ao SL
- **`lookback_zones`** — era hardcoded `100`; agora usa `LOOKBACK_ZONES = CFG['lookback_zones']`
- **`daily_profit_target`** — nunca era verificado; bot agora encerra ao atingir `$500` de lucro na sessão

### Variáveis Globais Adicionadas
```python
MIN_WICK_PCT, RSI_OVERBOUGHT, RSI_OVERSOLD, RR_RATIO,
LOOKBACK_ZONES, USE_TREND_FILTER, REQUIRE_REVERSAL, DAILY_PROFIT_TARGET
```

### Arquivos Modificados
- `bot_liquidez.py`

---

## [v6.0] - 2026-04-21 - LIFECYCLE ARCHITECTURE

### Mudança Arquitetural Completa

Reescrita total para arquitetura de estados de trade. Cada operação passa por um FSM de 8 estados
gerenciado pelo `TradeLifecycleManager` com persistência no Supabase.

### Novos Arquivos

#### `trade_lifecycle_manager.py`
- FSM com 8 estados: `signal_detected → awaiting_consensus → approved/rejected → filled → open → closed/error`
- Gerencia todas as transições de estado via Supabase `signals_liquidez`
- Sem prints — operações silenciosas; erros suprimidos com retorno `True/False`
- Métodos: `create_signal`, `transition_to_awaiting_consensus`, `approve_signal`, `reject_signal`,
  `mark_as_filled`, `mark_as_open`, `close_trade`, `mark_as_error`, `get_pending_signals`, `cleanup_duplicates`

#### `system_logger.py`
- Logger centralizado para console + tabela Supabase `bot_logs`
- Sources: `BOT`, `WAR_ROOM`
- Levels: `INFO`, `WARNING`, `ERROR`, `TRADE`, `SIGNAL`
- Graceful: se Supabase indisponível, apenas loga no console

### Bot Liquidez (`bot_liquidez.py`) — Reescrito

**Fluxo de execução:**
1. Bot detecta sinal → `create_signal()` → `transition_to_awaiting_consensus()`
2. War Room analisa → `approve_signal()` ou `reject_signal()`
3. Bot executa aprovados → `mark_as_filled()` → `mark_as_open()`
4. Posição fechada pelo MT5 → `close_trade()` com P&L real

**Novas funções:**
- `SESSION_START = datetime.now()` — timestamp de sessão ao iniciar
- `get_session_pnl()` — P&L desde o início desta execução do bot (não mais por data)
- `print_dashboard()` — dashboard estruturado com rolling log de 10 eventos
- `send_heartbeat()` — upsert na tabela `bot_heartbeats` a cada ciclo (20s)
- `export_zones_to_mt5()` — exporta CSV com merge de zonas (threshold 15 pips), ordenação por proximidade, limite 6 por lado, linha `BOT_STATUS`
- `_merge_zone_list()` — helper de merge de zonas próximas

### Auto War Room (`auto_war_room.py`) — Reescrito

- `MAGIC_NUMBER` lido de `config.yaml` (antes hardcoded `123456`)
- Sistema de scoring 5 critérios (0–100): wick% (30pts), RSI extremo (25pts), slope H1 (20pts), volume (15pts), histórico do símbolo (10pts)
- Score mínimo: 60/100 para aprovação
- Detecção de correlação entre pares (`CORRELATED_PAIRS`)
- Bug de loop de rejeição corrigido via `processed_ids = set()`
- Aprovação de apenas 1 sinal por ciclo (mais alto score)
- Agentes analíticos: Jim Simons, Druckenmiller, Nassim Taleb (opiniões salvas em `agent_opinions`)

### Indicador MetaTrader (`IndicadorLiquidez.mq5`) — Reescrito v6.0

- Zonas renderizadas como: `OBJ_RECTANGLE` (preenchido) + `OBJ_TREND` (linha pontilhada) + `OBJ_TEXT` (label de preço)
- Destaque de zona próxima: zonas dentro de 25 pips recebem cor mais viva e texto branco
- Limite máximo: 6 zonas por lado
- Painel BOT STATUS: lê linha `BOT_STATUS,pnl_sessao,pnl_total,exauridas` do CSV
- Painel mostra: "BOT LIQUIDEZ v6.0", P&L Sessão, P&L Total, Zonas Exauridas
- `OnChartEvent` para redesenho automático ao redimensionar gráfico
- Timer de 5s para atualização periódica

### Frontend

- `app/app/page.tsx` — heartbeat com timeout 90s, exibe "X min atrás"
- `app/app/logs/page.tsx` — **nova página** de logs em tempo real via Supabase Realtime
- `app/components/sidebar.tsx` — item "Logs" adicionado na navegação
- `app/components/dashboard-metrics.tsx` — "Lucro Hoje" → "P&L Sessão (MT5)"

### FULL_START.bat

- Auto-inicialização do MetaTrader 5 (`[0/3]`, verifica dois caminhos comuns)
- `chcp 65001` para suporte a UTF-8
- Delays entre processos (`timeout /t 2`)

### Supabase Schema

Tabela `signals_liquidez` — 7 colunas adicionadas:
`position_id`, `exit_price`, `approved_at`, `filled_at`, `updated_at`, `reject_reason`, `error_message`, `agent_opinions`

Tabela `bot_logs` — nova:
`id, source, level, event, message, symbol, trade_id, data, created_at`

---

## [v5.9.6] - 2026-04-20 - SYNC-FIX

### Fix
- Corrigido sync MT5 → Supabase (trades com P&L = $0)
- `position_id` como chave única (elimina duplicatas)
- Script `fix_sync_duplicates.py` para corrigir histórico

---

## [v5.9.5] - 2026-04-20 - PATCHED

### Fixes
- Kill-Zone: usa candle fechado `iloc[-2]`
- One-Shot: persistência de `consumed_zones` via JSON
- Race condition: 1 trade por ciclo
- EURJPY desativado (Win Rate 7.7%)

---

## [v5.9.4] - 2026-04-16 - ULTRA-SYNC

### Features
- Source of Truth (P&L do histórico MT5)
- SESSION_START timestamp
- Auto-healing sync

---

## [v5.6] - 2026-04-18 - Auditor Edition

### Features
- Visual Path Auditing (AuditorBacktest.mq5)
- Realistic Engine (market_replay.py)
- Absolute Session Tracking

---

## [v5.5.1] - 2026-04-15

### Features
- Multi-pair (10 símbolos)
- Slope Guard H1
- Color Reversal confirmation
