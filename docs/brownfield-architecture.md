# Trade Liquidez — Documento de Arquitetura Brownfield v6.0

**Data:** 22 de Abril de 2026
**Versão:** 6.1.3
**Status:** Produção

---

## 1. Visão Geral da Arquitetura

O sistema é composto por quatro camadas independentes que se comunicam via Supabase (cloud) e arquivos CSV locais (MT5):

```
┌──────────────────────────────────────────────────────────┐
│  CAMADA 1: Orquestração Local                            │
│  FULL_START.bat — inicia MT5 + Next.js + War Room + Bot  │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  CAMADA 2: Motores Python                                 │
│  bot_liquidez.py          auto_war_room.py               │
│  (detecção + execução)    (análise + aprovação)          │
└──────────────────────┬───────────────────────────────────┘
                       │ REST API + Realtime
┌──────────────────────▼───────────────────────────────────┐
│  CAMADA 3: Supabase (PostgreSQL + Realtime)               │
│  signals_liquidez  │  bot_heartbeats  │  bot_logs        │
└──────────────────────┬───────────────────────────────────┘
                       │ Supabase Realtime (WebSocket)
┌──────────────────────▼───────────────────────────────────┐
│  CAMADA 4: Interfaces                                     │
│  Next.js Dashboard :3000      IndicadorLiquidez.mq5      │
│  (frontend web)               (indicador MetaTrader)     │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Componentes e Responsabilidades

### 2.1 `bot_liquidez.py` — Motor Principal

**Ciclo de execução (a cada 20s):**
1. `sync_open_positions()` — verifica posições abertas/fechadas no MT5
2. `execute_approved_signals()` — executa sinais aprovados pela War Room
3. `get_session_pnl()` + `get_account_pnl()` — calcula P&L
4. `send_heartbeat()` — upsert em `bot_heartbeats`
5. `print_dashboard()` — renderiza terminal estruturado
6. Loop por símbolo: detecta zona → check trigger → cria sinal → export CSV

**Variáveis globais (lidas do config.yaml — v6.1.3):**
```python
MAGIC_NUMBER, STOP_BUFFER, COOLDOWN_HOURS, PROXIMITY_PIPS,
MIN_WICK_PCT, RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD,
RR_RATIO, LOOKBACK_ZONES, USE_TREND_FILTER, REQUIRE_REVERSAL,
DAILY_PROFIT_TARGET, BREAKEVEN_CANDLES
# SLOPE_THRESHOLD_PIPS removido do config em v6.1.3 (default 0.5 via CFG.get)
# RSI_PERIOD adicionado em v6.1.3 (antes hardcoded 14)
```

**Algoritmo de detecção de zona (`get_validated_zones`):**
- Itera candles M15 buscando máximas/mínimas locais
- Resistência: máxima com 7 candles seguintes abaixo
- Suporte: mínima com 7 candles seguintes acima

**Algoritmo de gatilho (`check_trigger` — v6.1.3):**
- Pré-condição: cooldown limpo + zona não consumida
- SELL: preço tocou resistência + wick superior ≥ `MIN_WICK_PCT` + RSI(`RSI_PERIOD=9`) ≥ `RSI_OVERBOUGHT=70`
- BUY: inverso simétrico (RSI ≤ `RSI_OVERSOLD=30`)
- SL = high/low do pavio ± `STOP_BUFFER × point` (50 pts em v6.1.3)
- TP = entry ± distância_SL × `RR_RATIO` (1.5)
- **Filtros desativados em v6.1.1** (parecer técnico, item A+B+E):
  - `USE_TREND_FILTER = false` → slope MA20 H1 ignorado (operava invertido contra-tendência)
  - `REQUIRE_REVERSAL = false` → color reversal ignorado (atrasava entrada no ponto ótimo)
  - Se `USE_TREND_FILTER = true` (config), comportamento legado: H1 indisponível bloqueia o trade

### 2.2 `auto_war_room.py` — War Room

**Ciclo de execução (a cada 5s — v6.1.3):**
1. Busca sinais com status `awaiting_consensus` no Supabase
2. Para cada sinal: `derive_strategy_context()` → `print_strategy_fire()` (FASE 1) → `analyze_signal_strength(signal, ctx)` (FASE 2) → score 0–100
3. Ordena por score (maior primeiro)
4. Aprovação: score ≥ 55 + sem conflito de correlação → `approve_signal()`
5. Rejeição: score < 55 ou correlação → `reject_signal()`
6. Sinais não processados neste ciclo → `reject_signal("Preterido")`

**Critérios de scoring v6.1.2 — 5 critérios, RSI alpha (score mínimo: 55/100):**
| Critério | Dados | Pontos | Obs |
|---|---|---|---|
| **RSI Extremo** | MT5 M15 RSI(9) | 0–**35** | **ALPHA** — distância vs limite (70/30); 30%/70%=0pts, 85%=17.5pts, ≥100%=35 |
| Wick % | `signal.wick_pct` | 0–25 | Bot já valida ≥30%; War Room premia distância extra |
| Pin Bar | corpo/range da vela (MT5 M15) | 0–20 | corpo ≤ 15% do range |
| Sessão | `datetime.utcnow().hour` | 0–15 | London+NY overlap (13–17h UTC) |
| Histórico do símbolo | Supabase (30 dias) | 0–5 | Win rate ≥ 60% |

**Removidos em v6.1.2 (vs v6.1):**
- ~~Slope H1~~ (15pts) — bot já não usa como gate desde v6.1.1; manter no War Room era incoerente
- ~~Volume~~ (10pts) — trader: "volume não casa com estratégia de reversão em zona de liquidez"

### 2.3 `trade_lifecycle_manager.py` — FSM de Estados

**Estados:**
```python
STATES = {
    'signal_detected':    'Sinal técnico detectado',
    'awaiting_consensus': 'Aguardando aprovação da sala de guerra',
    'approved':           'Aprovado para execução',
    'rejected':           'Rejeitado pela sala de guerra',
    'filled':             'Ordem executada no MT5',
    'open':               'Trade ativo (posição aberta)',
    'closed':             'Trade finalizado',
    'error':              'Erro na execução'
}
```

**Princípio:** Sem prints. Todas as operações são silenciosas e retornam `True/False`.
Usa `lifecycle.client` (Supabase) injetado via `__init__`.

### 2.4 `system_logger.py` — Logger Centralizado

```python
logger = SystemLogger("BOT")   # ou "WAR_ROOM"
logger.info("event_slug", "mensagem", symbol="EURUSD", data={...})
logger.trade("order_executed", "...", ...)
logger.error("mt5_init_failed", "...", ...)
```

Escreve em console + tabela `bot_logs`. Se Supabase indisponível, apenas console (graceful).

### 2.5 `IndicadorLiquidez.mq5` — Indicador MT5

**Leitura do CSV** (`liquidez_data_{SYMBOL}.csv`):
```
HEADER
BOT_STATUS,{pnl_sessao},{pnl_total},{n_exauridas}
ZONE_RESISTANCE,{price},{time}
ZONE_SUPPORT,{price},{time}
SIGNAL_SELL,{price},{time}
SIGNAL_BUY,{price},{time}
```

**Renderização:**
- `OBJ_RECTANGLE` — retângulo preenchido (zona ±`InpZonePips` pips)
- `OBJ_TREND` — linha pontilhada central
- `OBJ_TEXT` — label de preço (âncora acima para resistência, abaixo para suporte)
- Zona próxima (≤ `InpNearPips` = 25): cor mais intensa + texto branco
- Painel BOT STATUS: `OBJ_RECTANGLE_LABEL` + `OBJ_LABEL`

---

## 3. Fluxo de Dados Detalhado

### 3.1 Abertura de Trade
```
bot_liquidez.py
  └─ check_trigger() → True
      └─ lifecycle.create_signal()          → INSERT signals_liquidez (signal_detected)
      └─ lifecycle.transition_to_awaiting() → UPDATE status=awaiting_consensus
      └─ consumed_zones.add(z_key)

auto_war_room.py (próximo ciclo, ≤5s)
  └─ get_pending_signals('awaiting_consensus')
  └─ analyze_signal_strength() → score
  └─ lifecycle.approve_signal(opinions)    → UPDATE status=approved

bot_liquidez.py (próximo ciclo, ≤20s)
  └─ execute_approved_signals()
      └─ mt5.order_send(request)
      └─ lifecycle.mark_as_filled(position_id) → UPDATE status=filled
```

### 3.2 Fechamento de Trade
```
bot_liquidez.py
  └─ sync_open_positions()
      └─ check_if_closed(trade)
          └─ mt5.history_deals_get(position=position_id)
          └─ exit_deal.profit + commission + swap = pnl_real
          └─ lifecycle.close_trade(position_id, pnl_real, exit_price)
              → UPDATE status=closed, pnl={pnl_real}, exit_price, closed_at
```

### 3.3 Heartbeat → Frontend
```
bot_liquidez.py (a cada ciclo)
  └─ send_heartbeat(pnl_session, pnl_total, active_zones)
      └─ Supabase UPSERT bot_heartbeats (symbol="GLOBAL")

app/app/page.tsx
  └─ setInterval(checkHeartbeat, 30_000)
      └─ SELECT FROM bot_heartbeats WHERE symbol='GLOBAL'
      └─ Se created_at > 90s atrás → "MOTOR OFFLINE"
```

---

## 4. Arquivos e Paths

### Python Scripts
```
squads/trade-liquidez-python/scripts/    ← PRODUÇÃO (9 arquivos)
├── bot_liquidez.py               # Motor principal v6.0.2
├── auto_war_room.py              # War Room v6.0
├── trade_lifecycle_manager.py    # FSM de estados
├── system_logger.py              # Logger centralizado
├── etl_trades.py                 # ETL: trades fechados
├── etl_rejections.py             # ETL: sinais rejeitados
├── etl_db_audit.py               # ETL: auditoria de integridade
├── etl_report.py                 # ETL: relatório completo (JSON+MD)
├── IndicadorLiquidez.mq5         # Indicador MT5
├── .consumed_zones.json          # Persistência de zonas exauridas
│
├── legacy/                       ← Backups e scripts one-time (11 arquivos)
│   ├── bot_liquidez_v5.9.6_backup.py
│   ├── auto_war_room_v5_backup.py
│   ├── migrate_to_v6_lifecycle.py
│   ├── setup_database.py / setup_schema_v6.py
│   ├── fix_sync_duplicates.py / fix_signal.py
│   ├── clean_db.py / clean_production_db.py
│   └── validate_migration.py / AuditorBacktest.mq5
│
└── utils/                        ← Diagnóstico e testes reutilizáveis (16 arquivos)
    ├── market_replay.py / simulate_trade.py
    ├── diagnose_today.py / diagnose_history.py
    ├── audit_full.py / audit_trade.py
    ├── check_schema.py / check_session.py
    ├── optimize_hyperparams.py
    ├── war_room_voter.py / supabase_client.py
    └── test_bot_v6.py / test_execution.py / validate_execution.py
```

### MetaTrader
```
squads/trade-liquidez-python/scripts/
└── IndicadorLiquidez.mq5         # Indicador v6.0

MT5 Data Path:
C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\
└── liquidez_data_EURUSD.csv
└── liquidez_data_GBPUSD.csv
└── ... (um CSV por símbolo)
```

### Frontend
```
app/
├── app/
│   ├── page.tsx                  # Dashboard principal
│   ├── logs/page.tsx             # Logs em tempo real
│   ├── monitor/page.tsx          # Monitor zonas H1
│   ├── historico/page.tsx        # Histórico de trades
│   └── gatilhos/page.tsx         # Lista de sinais
└── components/
    ├── dashboard-metrics.tsx     # Cards de métricas (P&L Sessão)
    └── sidebar.tsx               # Navegação (inclui Logs)
```

### Configuração
```
squads/trade-liquidez-python/
├── config.yaml                   # Todos os parâmetros operacionais
├── .env                          # SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
└── FULL_START.bat (raiz)         # Orquestrador de sessão
```

---

## 5. Supabase Schema

### `signals_liquidez`
```sql
id uuid PRIMARY KEY,
symbol text, type text, price float, sl float, tp float,
status text,  -- FSM state
wick_pct float, magic int, pnl float,
position_id bigint, exit_price float,
agent_opinions jsonb, reject_reason text, error_message text,
created_at timestamptz, approved_at timestamptz,
filled_at timestamptz, closed_at timestamptz, updated_at timestamptz
```

### `bot_heartbeats`
```sql
symbol text UNIQUE, status text,
active_zones int, pnl_today float, pnl_total float,
created_at timestamptz
```

### `bot_logs`
```sql
id bigserial PRIMARY KEY,
source text, level text, event text, message text,
symbol text, trade_id text, data jsonb,
created_at timestamptz DEFAULT now()
```
Índices: `created_at DESC`, `source`, `level`
Realtime: `ALTER PUBLICATION supabase_realtime ADD TABLE bot_logs`

---

## 6. Variáveis de Ambiente Necessárias

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

Arquivo `.env` na raiz do projeto (`C:\Users\Pichau\Desktop\trade\.env`).

---

## 7. Símbolos Operados

| Símbolo | Status | Motivo |
|---|---|---|
| EURUSD | ✅ Ativo | — |
| GBPUSD | ✅ Ativo | — |
| AUDUSD | ✅ Ativo | — |
| USDCAD | ✅ Ativo | — |
| USDCHF | ✅ Ativo | — |
| NZDUSD | ✅ Ativo | — |
| EURGBP | ✅ Ativo | — |
| GBPJPY | ✅ Ativo | — |
| USDJPY | ❌ Desativado | WR 42.1% (8/19 trades), P&L -$232.29 — JPY direcional vs estratégia de reversão |
| EURJPY | ❌ Desativado | WR 16.7% (1/6 trades), P&L -$85.56 |

---

*Arquitetura Brownfield v6.1.3 — Synkra AIOX Ecosystem*
