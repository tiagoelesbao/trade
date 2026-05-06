# Trade Liquidez — Arquitetura v6.2.0-ict

---

## 1. Visão Geral — 4 processos coordenados

O sistema runtime é composto por **4 processos paralelos** orquestrados pelo `FULL_START.bat`, comunicando-se via Supabase (PostgreSQL + Realtime) e arquivos locais.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FULL_START.bat (orquestrador)                    │
└──┬───────────────┬───────────────┬────────────────┬─────────────────┘
   │               │               │                │
   ▼               ▼               ▼                ▼
┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────────┐
│  MT5     │  │ Next.js  │  │  Bot       │  │ War Room     │
│ Terminal │  │ :3000    │  │ Liquidez   │  │ (Pool+Pick)  │
└──────────┘  └────▲─────┘  └────┬───────┘  └──────┬───────┘
                   │             │                  │
                   │           ┌─┴─────────────┐    │
                   │           │ Exit War Room │    │
                   │           │ (regras a-f)  │    │
                   │           └───────┬───────┘    │
                   │                   │            │
                   │   Supabase Realtime (WS)       │
                   ▼                                │
            ┌──────────────────────────────────────┴──────┐
            │              SUPABASE                        │
            │  signals_liquidez · bot_heartbeats · bot_logs│
            └──────────────────────────────────────────────┘
```

| Processo | Papel | Loop |
|----------|-------|------|
| **bot_liquidez.py** | Detecção (zona+wick+RSI), 4 gates de entrada, executor de ordens aprovadas, sync de posições | 20s |
| **auto_war_room.py** | Decisão Pool-then-Pick: scoring 6 critérios + tie-breaker ICT + correlação | Pool 30s + processamento |
| **exit_war_room.py** | Gestão dinâmica de saída (regras a-f), partial close, BE inteligente | 10s |
| **app/ (Next.js)** | Dashboard web em `localhost:3000` | Realtime via WebSocket |

**Indicador visual MT5:** `IndicadorLiquidez.mq5` — não é processo separado, roda dentro do MetaTrader 5. Lê CSVs exportados pelo bot e Exit War Room.

---

## 2. Pipeline de um sinal (estado-a-estado)

```
[BOT — check_trigger]
 │
 ├─ Gate 1: is_entry_blocked_by_time()       (news_embargo + cutoff)
 ├─ Gate 2: MIN_CANDLE_RANGE_PIPS ≥ 3
 ├─ Gate 3: is_entry_blocked_by_ict_cliff()  (ICT alignment == 0)
 ├─ Gate 4: cooldown_mgr.check()             (loss recente direção+símbolo)
 │
 ├─ create_signal()                         → status=signal_detected
 └─ transition_to_awaiting_consensus()      → status=awaiting_consensus
        │
        ▼
[WAR ROOM — Pool-then-Pick]
 │
 ├─ POOL OPEN (30s) — acumula correlatos
 ├─ FASE 1: derive_strategy_context() + render_context_card (ICT)
 ├─ FASE 2: analyze_signal_strength() → 6 critérios (max 100 pts)
 │
 ├─ Cooldown re-check                       → REJEITADO_COOLDOWN
 ├─ CLIFF pre-filter (ICT==0)               → REJEITADO_CLIFF
 ├─ pick_best_from_correlated()             → tie-breaker (ICT > score > wick)
 │   ├─ losers do cluster                   → PRETERIDO_CLUSTER
 │   └─ winner: gate score≥min + correlação com posições abertas
 │       ├─ falha gate                      → REJEITADO
 │       └─ aprovado                        → status=approved
        │
        ▼
[BOT — execute_approved_signals]
 │
 ├─ mt5.order_send(FOK)                     → status=filled
 └─ sync_open_positions()                   → status=open
        │
        ▼
[EXIT WAR ROOM — loop 10s]
 │
 ├─ compute_stats() — profit_R, candles_open, risk_pips
 ├─ evaluate_all_rules() — breakdown verbose das 6 regras
 ├─ evaluate_position() — primeira que matchar vence
 ├─ execute_decision() — be | partial_be | close | flag
 ├─ _write_exit_hint() → indicador MQ5
 ├─ log_position_snapshot() + log_position_evaluation() (Supabase)
        │
        ▼
[BOT — check_if_closed]
 │
 ├─ history_deals_get() → calcula PNL real do MT5
 ├─ close_trade()                           → status=closed
 └─ if pnl ≤ -$10: cooldown_mgr.register_loss(sym, type)
```

---

## 3. FSM — `trade_lifecycle_manager.py`

```
signal_detected → awaiting_consensus → approved → filled → open → closed
                                    ↘ rejected                  ↘ error
```

| Estado | Quem transiciona | Campos preenchidos |
|--------|------------------|--------------------|
| `signal_detected` | bot | symbol, type, price, sl, tp, wick_pct, magic, created_at |
| `awaiting_consensus` | bot | (idem) |
| `approved` | war_room | + agent_opinions, approved_at |
| `rejected` | war_room | + reject_reason |
| `filled` | bot | + position_id, filled_at |
| `open` | bot (sync_open_positions) | + updated_at |
| `closed` | bot (check_if_closed) | + pnl, exit_price, closed_at |
| `error` | bot | + error_message |

**Princípio:** todas as transições são silenciosas (retornam True/False). Falhas logadas via `SystemLogger("LIFECYCLE")`.

---

## 4. Componentes Python — Responsabilidades

### `bot_liquidez.py` — Detector + Executor
- `check_trigger()` aplica 4 gates em ordem (early-exit em qualquer falha)
- `get_validated_zones()` — zonas S/R por displacement de 7 candles
- `calculate_rsi()` — Wilder's SMMA (`ewm(alpha=1/period, adjust=False)`)
- `sync_open_positions()` — reconcilia banco com `mt5.positions_get()`
- `check_if_closed()` — calcula PNL real via `history_deals_get(position=...)` e ativa cooldown se loss
- `export_zones_to_mt5()` — escreve `liquidez_data_<symbol>.csv` com header rico (GATE, SESSION, ICT_BIAS, LIQ_ABOVE/BELOW, POSITION, ZONES)
- Dedup in-memory: `sent_signals: set` por (symbol, type, trigger_candle_time) — limpo periodicamente por `prune_sent_signals()`

### `auto_war_room.py` — Decisão Pool-then-Pick
- Janela de pool `cluster_pool_window_seconds: 30` com poll de 3s
- `derive_strategy_context()` — single-fetch M15+H1+ICT, alimenta FASE 1 e FASE 2
- `analyze_signal_strength()` — 6 critérios (RSI 25, Wick 20, PinBar 15, Sessão 10, ICT 25, Hist 5)
- `pick_best_from_correlated()` — greedy: itera ordenado por (ICT, score, wick), winner consome correlatos
- `CORRELATED_PAIRS` — bundle USD-quote/USD-base + cross-correlations (16 entradas)
- 4 opiniões formatadas: Momentum, Rejeição, Contexto, ICT Macro

### `exit_war_room.py` — Gestão de saída multi-condicional
- `evaluate_all_rules()` (Sprint 6.2) — breakdown verbose com status individual de cada regra
- `evaluate_position()` — primeira regra (a-f) que matchar vence
- `execute_decision()` — `_modify_position_sltp` (BE), `_close_position` (close/partial)
- Helpers: `_detect_reversal_candle`, `_detect_structure_break` (BOS clássico ou trend forte LH+LL/HH+HL)
- `_write_exit_hint()` — escreve `exit_hint_<symbol>.csv` para o indicador MQ5
- `_clear_exit_hint()` — limpa hint quando posição fecha

### `ict_context_engine.py` — Engine ICT
- Orquestra pacote `ict/`: `structure`, `phase_detector`, `liquidity_levels`, `daily_range_algo`
- `get_context(symbol, mt5_module)` retorna dict com bias D1, fases H4/H1, liquidity above/below, daily_range_state
- Closure `trade_alignment_score(BUY|SELL) → 0-25 pts` + explicação
- **Cache TTL 5min** por símbolo (compartilhado bot ↔ war_room ↔ exit_wr)
- **CLIFF (0/25)** = trade contra D1 bias + H4 expansion contrária — único caso onde ICT vira **gate** (não só score)

### `cooldown_manager.py` — Bloqueio direcional pós-loss
- Após loss > `cooldown_min_loss_pnl` (-$10), bloqueia (symbol, direction) por `cooldown_hours_after_loss` (4h)
- Persistência JSON em `data/cooldowns.json` (sobrevive reinício)
- Cache em memória via mtime — singleton-friendly cross-process
- API: `check(sym, type)`, `register_loss(sym, type)`, `cleanup_expired()`, `list_active()`

### `system_logger.py` — Logger centralizado
- Console + Supabase (`bot_logs`)
- `signal_analysis()` formata breakdown completo (6 critérios + 4 opiniões + verdito)
- Pesos `SCORE_MAX` casam com `auto_war_room.SCORE_MAX` (RSI 25, Wick 20, PinBar 15, Sessão 10, ICT 25, Hist 5)
- Timezone alinha com servidor MT5 (UTC+3 default)

### `terminal_log_writer.py` — Persistência local
- Append-only, line-buffered, rotação diária
- Path: `data/terminal_logs/{source}_YYYYMMDD.log`
- Não derruba bot se falhar (silenciador defensivo)

### `trade_lifecycle_manager.py` — FSM Supabase
- Wrapper Supabase com 8 transições
- `position_id` chave única (índice unique no Postgres)
- `cleanup_duplicates()` resolve por created_at desc

### `trade_analysis_engine.py` — Pipeline LLM offline
- **Não é runtime** — rodado manualmente pós-sessão
- Detalhes em [trade-analysis.md](trade-analysis.md)

---

## 5. Schema Supabase

### `signals_liquidez`
```sql
id            uuid PRIMARY KEY,
symbol        text,
type          text,           -- BUY | SELL
price         float,
sl            float,
tp            float,
status        text,           -- FSM state
wick_pct      float,
magic         int,
pnl           float,
position_id   bigint,         -- UNIQUE WHERE NOT NULL
exit_price    float,
agent_opinions jsonb,         -- [{Momentum}, {Rejeição}, {Contexto}, {ICT Macro}]
reject_reason text,
error_message text,
created_at    timestamptz,
approved_at   timestamptz,
filled_at     timestamptz,
closed_at     timestamptz,
updated_at    timestamptz
```

Índices: `idx_signals_position_id` (UNIQUE), `idx_signals_status`, `idx_signals_created_at DESC`.

### `bot_heartbeats`
```sql
symbol        text UNIQUE,    -- "GLOBAL"
status        text,           -- "running"
active_zones  int,            -- legacy (sempre 0 em v6.1.4+)
pnl_today     float,
pnl_total     float,
created_at    timestamptz
```
Upsert a cada 20s (`on_conflict=symbol`).

### `bot_logs`
```sql
id          bigserial PRIMARY KEY,
source      text,             -- BOT | WAR_ROOM | EXIT_WR | LIFECYCLE
level       text,             -- INFO | WARNING | ERROR | TRADE | SIGNAL
event       text,             -- slug do evento
message     text,
symbol      text,
trade_id    text,
data        jsonb,            -- payload estruturado
created_at  timestamptz DEFAULT now()
```
Índices: `created_at DESC`, `source`, `level`. Realtime publication ativada.

**Eventos principais por source:**

| Source | Eventos |
|--------|---------|
| BOT | `bot_started`, `signal_detected`, `mt5_init_failed`, `daily_stop_hit`, `daily_target_hit`, `cooldown_started`, `cooldown_active`, `ict_cliff_block`, `breakeven_failed`, `order_executed`, `trade_closed` |
| WAR_ROOM | `war_room_started`, `signal_aprovado`, `signal_rejeitado`, `signal_rejeitado_cooldown`, `signal_rejeitado_cliff`, `signal_preterido_cluster`, `cluster_decision`, `analyze_signal_failed` |
| EXIT_WR | `exit_war_room_started`, `position_snapshot`, `position_evaluation`, `be_moved_dynamic`, `partial_closed`, `early_exit_liquidity`, `structure_break_close`, `time_exit_flagged` |
| LIFECYCLE | `lifecycle_*_failed` (qualquer transição falhada) |

---

## 6. Estado Runtime Local

Diretório: `squads/trade-liquidez-python/data/`

| Arquivo | Owner | Conteúdo |
|---------|-------|----------|
| `cooldowns.json` | `cooldown_manager.py` | `{"USDCHF:BUY": "2026-04-30T13:42:00+00:00", ...}` |
| `daily_state_YYYYMMDD.json` | `ict_context_engine.daily_range_algo` | Estado do dia ICT (Asia high/low, London high/low, NY direction) |
| `terminal_logs/BOT_YYYYMMDD.log` | `terminal_log_writer.py` | Append-only rolling log do bot |
| `terminal_logs/EXIT_WR_YYYYMMDD.log` | `terminal_log_writer.py` | Append-only rolling log do exit war room |

---

## 7. Cache ICT (cross-process)

- Cada processo (bot, war_room, exit_wr) tem **cópia em memória** do cache do `ict_context_engine`
- TTL 5min por símbolo
- O cache **não é compartilhado fisicamente** (não há lock cross-process)
- Race condition tolerada: pior caso é fetch duplicado, nunca decisão errada

---

## 8. Indicador MT5 (`IndicadorLiquidez.mq5`)

**Lê CSVs gerados pelo bot:**

```
HEADER
VERSION,v6.2.0-ict
BOT_STATUS,<pnl_session>,<pnl_total>,0
GATE,<blocked 0|1>,<reason>                     # Sprint 1
SESSION,<id>,<label>,<weight_pts>               # Sprint 1
ICT_BIAS,<bias>,<h4>,<h1>,<state>,<buy>,<sell>  # Sprint 2
LIQ_ABOVE,<price>,<kind>,<dist_pips>            # Sprint 2
LIQ_BELOW,<price>,<kind>,<dist_pips>            # Sprint 2
ZONE_RESISTANCE,<price>,<time>
ZONE_SUPPORT,<price>,<time>
POSITION,<type>,<profit_R>,<candles>,<sl>,<tp>  # Sprint 4
BREAKEVEN,<price>,<type>
```

**Lê hints do Exit War Room:** `exit_hint_<symbol>.csv` com a próxima ação prevista (be/partial_be/close/flag/none + regra a-f).

**Path MT5 (Windows):**
```
C:\Users\Pichau\AppData\Roaming\MetaQuotes\Terminal\
  D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\
```

---

## 9. Configuração e Credenciais

Único arquivo de config: `squads/trade-liquidez-python/config.yaml` (referência completa em [operations.md](operations.md#config-reference)).

Credenciais em `.env` na raiz:
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

---

## 10. Frontend Next.js (`app/`)

| Rota | Função |
|------|--------|
| `/` | Dashboard principal — P&L, posições, zonas |
| `/historico` | Histórico de trades com filtro FSM |
| `/gatilhos` | Lista de sinais |
| `/logs` | Logs em tempo real (filtros source/level) |
| `/monitor` | Monitor de zonas H1 |

Realtime via Supabase WebSocket (sem polling). Heartbeat timeout de 90s indica "MOTOR OFFLINE".

Build/deploy: Vercel auto-detect a partir do `app/` (sem `vercel.json`).
