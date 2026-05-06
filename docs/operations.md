# Trade Liquidez — Operations / Runbook v6.2.0

---

## 1. Como iniciar o sistema

```
1. Executar FULL_START.bat (raiz do projeto)
   ├── Phase 1: MT5 Terminal (auto-init)
   ├── Phase 2: Next.js Dashboard → http://localhost:3000
   ├── Phase 3: Auto War Room (terminal)
   ├── Phase 4: Bot Liquidez (terminal)
   └── Phase 5: Exit War Room (terminal — Sprint 4)

2. No MetaTrader 5:
   ├── Compilar IndicadorLiquidez.mq5 (F7)
   └── Adicionar indicador em cada gráfico dos 5 pares ativos

3. Pré-requisitos:
   ├── .env com SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY
   ├── MT5 logado na corretora
   └── Schema Supabase v6.0+ aplicado (signals_liquidez, bot_heartbeats, bot_logs)
```

---

## 2. Onde olhar logs

| Localização | Conteúdo |
|-------------|----------|
| Terminal "Bot Liquidez" | Dashboard com P&L Sessão, gates de horário, cooldowns ativos, rolling log 50 eventos |
| Terminal "War Room" | FASE 1 strategy_fire + ICT context + FASE 2 scoring breakdown + cluster decision |
| Terminal "Exit War Room" | Bloco rico por posição (profit_R, ICT, status detalhado das 6 regras a-f) — Sprint 6.2 |
| `data/terminal_logs/BOT_YYYYMMDD.log` | Append-only do bot (rotação diária) |
| `data/terminal_logs/EXIT_WR_YYYYMMDD.log` | Append-only do exit war room |
| Supabase `bot_logs` | Logs estruturados com payload JSON |
| `http://localhost:3000/logs` | UI em tempo real com filtros source/level |

### Comandos úteis

```powershell
# Tail do log do bot do dia
Get-Content squads\trade-liquidez-python\data\terminal_logs\BOT_20260506.log -Wait -Tail 50

# Tail do exit war room
Get-Content squads\trade-liquidez-python\data\terminal_logs\EXIT_WR_20260506.log -Wait -Tail 50

# Cooldowns ativos agora
Get-Content squads\trade-liquidez-python\data\cooldowns.json
```

---

## 3. Config Reference (`squads/trade-liquidez-python/config.yaml`)

### Símbolos
```yaml
symbols:
  - AUDUSD
  - GBPUSD
  - USDCAD
  - USDCHF
  - NZDUSD
  # EURUSD/EURGBP pausados (Sprint 1, recomendação ICT Aula 3)
  # USDJPY/EURJPY/GBPJPY desativados por WR baixo
```

### Filtros de entrada
```yaml
zone_timeframe: "M15"
lookback_zones: 100
min_displacement_candles: 7
min_wick_pct: 0.30
rsi_period: 14            # Wilder default, alinha com MT5 (Sprint 6: 9 → 14)
rsi_overbought: 70
rsi_oversold: 30
min_candle_range_pips: 3.0  # Sprint 5: filtro de vela morta
```

### Gates de horário (Sprint 1)
```yaml
mt5_server_utc_offset: 3
entry_cutoff_hour_mt5: 22       # 19 UTC — pausa entradas após NY core
news_embargo_pause: true
news_embargo_start_utc: 13      # inclusive (13:00 UTC = 8:00 NY)
news_embargo_end_utc: 14        # exclusive (cobre 13:00-13:59)
```

### War Room
```yaml
min_confidence_score: 60        # Score mínimo para aprovação
                                # Sprint 1 subiu de 65→75; rebaixado para 60
                                # após Sprint 2 redistribuir para 6 critérios
                                # (ICT entrou com 25pts, total escalou)
cluster_pool_window_seconds: 30 # Sprint 3: pool antes de tie-breaker
cluster_pool_poll_seconds: 3
```

### Cooldown direcional (Sprint 6)
```yaml
cooldown_after_loss_enabled: true
cooldown_hours_after_loss: 4.0  # Bloqueia (sym, dir) por 4h após loss
cooldown_min_loss_pnl: -10.0    # Só ativa se loss > $10 (evita BE-stops)
```

### Risco
```yaml
lot_size: 1.0
stop_buffer_points: 50          # 5 pips
risk_reward_ratio: 1.5
breakeven_candles: 0            # DEPRECATED — BE migrou para Exit War Room
daily_max_loss: 500.0
daily_profit_target: 1000.0
```

### Exit War Room (Sprint 4)
```yaml
exit_war_room:
  enable_be_at_1R: true                    # regra a
  enable_partial_at_07R_reversal: true     # regra b
  enable_classic_be: true                  # regra c
  enable_liquidity_target_close: true      # regra d
  enable_structure_break_close: true       # regra e
  enable_time_exit_flag: true              # regra f
  monitor_interval_seconds: 10
  partial_close_pct: 0.50
  be_buffer_pips: 0.2
  time_exit_lookback_candles: 6
  time_exit_min_progress_R: 0.3
```

### Janelas de sessão ICT (Sprint 1)
```yaml
session_windows:
  asia_early:        { start: 21, end: 24, weight: 8,  label: "Asia early (post-NY)" }
  asia_judas:        { start:  0, end:  7, weight: 1,  label: "Asia continuation/Judas" }
  london_open:       { start:  7, end: 10, weight: 14, label: "London open expansion" }
  london_cont:       { start: 10, end: 13, weight: 11, label: "London continuation" }
  ny_news_embargo:   { start: 13, end: 14, weight: 0,  label: "NY 8-8:30 news embargo" }
  ny_expansion:      { start: 14, end: 15, weight: 13, label: "NY open expansion" }
  london_close:      { start: 15, end: 16, weight: 12, label: "London close reversal" }
  ny_afternoon:      { start: 16, end: 21, weight: 7,  label: "NY afternoon / end-of-day" }
```

### Identificação e execução
```yaml
magic_number: 123456
execution_mode: "market"
filling_mode: "FOK"
```

---

## 4. Troubleshoot

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| `MOTOR OFFLINE` no dashboard | Bot não envia heartbeat por >90s | Verificar terminal do bot; reiniciar `FULL_START.bat` |
| RSI no terminal divergente do chart MT5 | (resolvido v6.2.0 Sprint 5) | Confirmar `calculate_rsi` usa `ewm(alpha=1/period)` Wilder |
| Gate de horário sempre BLOCKED | `entry_cutoff_hour_mt5` ou janela embargo errada | Confirmar offset MT5 (`mt5_server_utc_offset`) bate com servidor da corretora |
| Sinais não chegam no War Room | War Room não conectado ao MT5 ou Supabase | Verificar `mt5.initialize()` e `bot_logs` por `mt5_init_failed` |
| ICT context indisponível | MT5 sem dados D1/H4/H1 (par sem histórico) | Confirmar par no Market Watch do MT5 |
| Cluster aprova trade contra-trend | ICT alignment não estava 0 mas baixo | Aumentar `min_confidence_score` no config OU rever critério ICT |
| Cooldown bloqueia trade legítimo | Janela 4h conservadora demais para volatilidade do par | Reduzir `cooldown_hours_after_loss` (testar 2-3h) |
| Indicador MQ5 não atualiza | CSV não exportado ou path errado | Confirmar `MT5_DATA_PATH` em `bot_liquidez.py` aponta para a instalação correta |
| Zonas sumindo no MT5 | Timestamps com hífen quebravam `StringToTime()` (resolvido v6.0.2) | Confirmar `_fmt_time` exporta `YYYY.MM.DD HH:MM:SS` (com pontos) |
| Trade duplicado | (resolvido v6.0) | Confirmar `idx_signals_position_id` UNIQUE no Postgres |

### Checklist diário rápido

```
[ ] FULL_START.bat rodou sem erro?
[ ] 4 terminais abertos (Bot, War Room, Exit WR, Dashboard)?
[ ] http://localhost:3000 carrega e mostra heartbeat <90s?
[ ] MT5 logado e indicador visível em pelo menos 1 par?
[ ] Supabase acessível (verificar /logs no dashboard)?
[ ] Verificar cooldowns.json — algum cooldown estourado bloqueando trade?
[ ] Conferir gate de horário no terminal do bot — está OPEN?
```

---

## 5. Operações comuns

### Pausar entradas mantendo posições abertas
```yaml
# config.yaml — set entry_cutoff baixo para bloquear novas entradas
entry_cutoff_hour_mt5: 0   # qualquer hora >= 0 bloqueia (ou seja, sempre)
```

Posições abertas continuam sob gestão do Exit War Room.

### Encerrar bot por meta diária atingida
Automático: `if pnl_session >= daily_profit_target: break`. Bot encerra com push_event "META".

### Encerrar bot por stop diário
Automático: `if pnl_session <= -daily_max_loss: break`. Bot encerra com push_event "STOP".

### Reativar par desativado
```yaml
symbols:
  - EURUSD          # reativando para teste
  - AUDUSD
  ...
```

Atenção: cooldowns por (sym, dir) só aplicam ao par específico — reativar não traz histórico.

### Ajustar feature flags do Exit War Room
```yaml
exit_war_room:
  enable_be_at_1R: false       # desabilita regra (a)
```

Atualização requer restart do `exit_war_room.py`.

### Limpar cooldowns manualmente
```powershell
# Apaga todos os cooldowns ativos
Remove-Item squads\trade-liquidez-python\data\cooldowns.json
```

### Limpar daily_state ICT
```powershell
# Estados ICT do dia (gerados automaticamente)
Remove-Item squads\trade-liquidez-python\data\daily_state_*.json
```

---

## 6. Análise pós-sessão

Pipeline LLM offline para auditar trades do dia. Detalhes em [trade-analysis.md](trade-analysis.md).

```bat
scripts\runner_analisar_trades.bat --input "squads\trade-liquidez-python\data\trades\Abril\Semana 01\2026-04-24" --mode full --verbose
```

---

## 7. Schema Supabase — setup inicial

Aplicar uma vez por instalação. SQL completo em commits anteriores ao `setup_schema_v6.sql` (deletado em v6.2.0). Tabelas requeridas:
- `signals_liquidez` (FSM)
- `bot_heartbeats` (status do motor)
- `bot_logs` (logs estruturados, com Realtime)

Índices essenciais:
```sql
CREATE UNIQUE INDEX idx_signals_position_id
  ON signals_liquidez(position_id) WHERE position_id IS NOT NULL;
CREATE INDEX idx_signals_status ON signals_liquidez(status);
CREATE INDEX idx_signals_created_at ON signals_liquidez(created_at DESC);
ALTER PUBLICATION supabase_realtime ADD TABLE bot_logs;
```

---

## 8. Deploy do dashboard

Frontend Next.js em `app/`. Vercel auto-detecta — sem `vercel.json` (intencional, removido em commit `728b4b7`).

```
Deploy automático: push para main → Vercel detecta → build app/ → deploy
```

Variáveis de ambiente no Vercel:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` (não SERVICE_ROLE — anon basta para read-only realtime)
