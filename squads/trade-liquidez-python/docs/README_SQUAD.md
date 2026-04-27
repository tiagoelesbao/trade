# Manual Mestre: Squad Trade-Liquidez-Python v6.0

**Versão:** 6.1.3 | **Data:** 22 de Abril de 2026 | **Status:** Produção

Sistema de trading algorítmico multi-par baseado em detecção de zonas de liquidez, aprovação agêntica via War Room e execução no MetaTrader 5. Todos os estados de trade são persistidos no Supabase e visualizados em tempo real no dashboard Next.js.

**Símbolos ativos (8):** EURUSD, GBPUSD, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, GBPJPY
*(USDJPY desativado: WR 42.1%, P&L -$232 | EURJPY desativado: WR 16.7%, P&L -$85)*

---

## 1. Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│  FULL_START.bat  (Orquestrador — inicia todos os componentes)   │
└────────────┬──────────────────────┬────────────────────────────┘
             │                      │
      ┌──────▼──────┐        ┌──────▼──────┐
      │  MetaTrader │        │  Next.js    │
      │  terminal   │        │  Dashboard  │
      │  (MT5)      │        │  :3000      │
      └──────┬──────┘        └──────▲──────┘
             │                      │ Supabase Realtime
      ┌──────▼──────────────────────┴──────────────────────────┐
      │                    SUPABASE                             │
      │  signals_liquidez  │  bot_heartbeats  │  bot_logs      │
      └────────────────────┬────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
 ┌──────▼──────┐   ┌───────▼──────┐   ┌──────▼──────┐
 │bot_liquidez │   │auto_war_room │   │IndicadorLiq │
 │  .py (Bot)  │   │  .py (WR)    │   │uidez.mq5    │
 └─────────────┘   └──────────────┘   └─────────────┘
```

### Fluxo de um Trade
```
Bot detecta zona → cria signal_detected → awaiting_consensus
War Room analisa (FASE 1: strategy_fire → FASE 2: scoring 5 critérios) → score ≥ 55 → approved
Bot executa no MT5 → filled → open
MT5 fecha posição → Bot calcula P&L → closed
```

---

## 2. Componentes (Arquivos Críticos)

### Backend Python — Core (`/scripts/`)

| Arquivo | Função |
|---|---|
| `bot_liquidez.py` | Motor principal: detecção de zonas, envio de sinais, execução de ordens aprovadas, sync de posições, heartbeat, export MT5 |
| `auto_war_room.py` | War Room: análise técnica de sinais (scoring 5 critérios), aprovação/rejeição, correlação entre pares |
| `trade_lifecycle_manager.py` | FSM de estados de trade — todas as transições Supabase |
| `system_logger.py` | Logger centralizado: console + tabela `bot_logs` |

### ETL / Análise (`/scripts/`)

| Arquivo | Função |
|---|---|
| `etl_trades.py` | Trades fechados: stats (WR, R/R, expectancy, drawdown), filtros por sessão/data/símbolo, export JSON/CSV |
| `etl_rejections.py` | Sinais rejeitados: breakdown por categoria e símbolo, top motivos |
| `etl_db_audit.py` | Auditoria de integridade do banco; flag `--fix` corrige stuck/null automaticamente |
| `etl_report.py` | Relatório completo JSON + Markdown para análise IA; combina trades, rejeições e logs |

### Scripts Auxiliares (`/scripts/utils/` e `/scripts/legacy/`)

| Pasta | Conteúdo |
|---|---|
| `utils/` | Ferramentas de diagnóstico, simulação e testes reutilizáveis (market_replay, diagnose_*, audit_*, simulate_trade, optimize_hyperparams…) |
| `legacy/` | Backups de versões anteriores, scripts de migração e setup one-time (não usar em produção) |

### MetaTrader

| Arquivo | Função |
|---|---|
| `IndicadorLiquidez.mq5` | Indicador: renderiza zonas, painel BOT STATUS, sinais de entrada/saída |

### Frontend Next.js (`app/`)

| Rota | Descrição |
|---|---|
| `/` | Painel ao vivo — zonas ativas, P&L sessão, P&L total, gatilhos recentes |
| `/monitor` | Monitor de zonas H1 |
| `/historico` | Histórico de trades |
| `/gatilhos` | Lista de sinais |
| `/logs` | Logs em tempo real (filtros: source, level) |

### Infraestrutura

| Arquivo | Função |
|---|---|
| `FULL_START.bat` | Orquestrador: inicia MT5 + Next.js + War Room + Bot |
| `config.yaml` | Configurações centralizadas (todos os filtros lidos daqui) |

---

## 3. Banco de Dados (Supabase)

### Tabela `signals_liquidez`
| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | uuid | PK |
| `symbol` | text | Par (ex: EURUSD) |
| `type` | text | BUY ou SELL |
| `price` | float | Preço de entrada |
| `sl` | float | Stop Loss |
| `tp` | float | Take Profit |
| `status` | text | Estado atual do FSM |
| `wick_pct` | float | % do pavio |
| `magic` | int | Magic number |
| `pnl` | float | P&L realizado |
| `position_id` | int | ID da posição no MT5 |
| `exit_price` | float | Preço de saída |
| `agent_opinions` | jsonb | Audit Checklist War Room (Momentum, Rejeição, Contexto) |
| `approved_at` | timestamptz | Timestamp de aprovação |
| `filled_at` | timestamptz | Timestamp de execução |
| `closed_at` | timestamptz | Timestamp de fechamento |
| `reject_reason` | text | Motivo de rejeição |
| `error_message` | text | Mensagem de erro |

### Tabela `bot_heartbeats`
| Coluna | Descrição |
|---|---|
| `symbol` | "GLOBAL" (chave única) |
| `status` | "running" |
| `active_zones` | Legacy (sempre 0 em v6.1.4+ — feature removida) |
| `pnl_today` | P&L da sessão atual |
| `pnl_total` | P&L total acumulado |
| `created_at` | Último heartbeat (upsert a cada 20s) |

### Tabela `bot_logs`
| Coluna | Descrição |
|---|---|
| `source` | "BOT" ou "WAR_ROOM" |
| `level` | "INFO", "WARNING", "ERROR", "TRADE", "SIGNAL" |
| `event` | Slug do evento |
| `message` | Mensagem legível |
| `symbol` | Par relacionado (opcional) |
| `data` | JSON com dados extras |

---

## 4. Config.yaml — Referência Completa (v6.1.3)

```yaml
# Filtros de Entrada
min_wick_pct: 0.30           # Pavio mínimo 30% da vela
rsi_period: 9                # v6.1.3: RSI período 9 (clássico, mais reativo)
rsi_overbought: 70           # RSI SELL threshold
rsi_oversold: 30             # RSI BUY threshold
use_trend_filter: false      # v6.1.1: DESATIVADO (operava invertido contra-tendência)
require_color_reversal: false # v6.1.1: DESATIVADO (atrasava entrada no ponto ótimo)
# slope_threshold_pips        # v6.1.3: REMOVIDO (default 0.5 via CFG.get no código)

# Zonas
lookback_zones: 100          # Candles M15 de lookback
min_displacement_candles: 7  # Confirmação de zona

# Proteções operacionais pós-trade — REMOVIDAS em v6.1.4
# (Kill-Zone, One-Shot de zona, trava por vela: todos removidos)

# Risco
lot_size: 1.0
stop_buffer_points: 50       # v6.1.3: 15→50 (5 pips, absorve varredura de liquidez)
risk_reward_ratio: 1.5
breakeven_candles: 0         # v6.1.3: 7→0 DESATIVADO (ejetava trades em pullbacks)
daily_max_loss: 350.0        # Bot para ao atingir
daily_profit_target: 500.0   # Bot para ao atingir

# Display / Logs
mt5_server_utc_offset: 3     # MT5 server UTC+3 (alinha logs com chart)

# Identificação
magic_number: 123456

# Execução
execution_mode: "market"
filling_mode: "FOK"
```

---

## 5. Como Iniciar o Sistema

```
1. Abrir FULL_START.bat
   └── MT5 inicia automaticamente
   └── Next.js Dashboard → http://localhost:3000
   └── War Room (terminal War Room)
   └── Bot (terminal Bot)

2. No MetaTrader:
   └── Compilar IndicadorLiquidez.mq5 (F7)
   └── Adicionar indicador em cada gráfico dos 9 pares
   └── Arquivos CSV lidos de MQL5/Files/liquidez_data_SYMBOL.csv

3. Monitoramento:
   └── http://localhost:3000           — dashboard ao vivo
   └── http://localhost:3000/logs      — logs em tempo real
   └── Terminal "Bot Liquidez"         — P&L Sessão, zonas, eventos
   └── Terminal "War Room"             — análise de sinais por score
```

---

## 6. Monitoramento e Diagnóstico

### Indicadores de Saúde
- **Dashboard online:** Painel mostra "MOTOR DE ATUALIZAÇÃO" com timestamp do último heartbeat (timeout 90s)
- **War Room:** FASE 1 imprime card de strategy_fire (OHLC + gatilhos atendidos), FASE 2 mostra score em barra visual `[####----] 46.5/100`
- **Bot terminal:** Dashboard com P&L Sessão, P&L Total, barra de stop diário, rolling log de 10 eventos, linha de filtros `RSI(9) 30/70`
- **Indicador MT5:** Painel "BOT LIQUIDEZ v6.1.4" com P&L Sessão e P&L Total (Zonas Exauridas sempre 0 em v6.1.4+)

### Erros Comuns
| Erro | Causa | Solução |
|---|---|---|
| `MOTOR OFFLINE` no frontend | Bot não enviou heartbeat por >90s | Verificar se bot está rodando, reiniciar FULL_START.bat |
| `bot_logs not found` no War Room | Tabela não criada no Supabase | Rodar SQL de criação da tabela `bot_logs` |
| Score sempre 50/100 | MT5 desconectado na War Room | War Room depende de mt5.initialize() |
| Zonas não aparecem no MT5 | CSV não gerado ou timestamp com hífens | Verificar path `MT5_DATA_PATH`; garantir que `_fmt_time()` usa pontos (`2026.04.21`) |
| Zonas com largura muito pequena | Zona detectada recentemente (t ≈ agora) | Parâmetro `InpMinBarsWidth = 60` garante mínimo de 60 barras M15 |
| Labels de zona invisíveis | `OBJPROP_HIDDEN = true` ativo | Recompilar com versão corrigida do `IndicadorLiquidez.mq5` |

---

## 7. Segurança e Limites

- Máximo 1 sinal enviado por ciclo (20s)
- Máximo 1 posição aberta simultaneamente por símbolo
- Correlação: pares correlacionados não operam simultaneamente (War Room)
- Stop diário: $350 (bot encerra sessão)
- Meta diária: $500 (bot encerra sessão)
- **Removidos em v6.1.4:** One-Shot de zonas, Kill-Zone (cooldown + proximity), trava por vela. Persistência `.consumed_zones.json` descontinuada. Motivo: privavam bons trades sem ganho estatístico comprovado.
- **Breakeven automático:** DESATIVADO em v6.1.3 (`breakeven_candles: 0`); código mantido para reativação futura
- **SL com buffer institucional:** `stop_buffer_points: 50` (5 pips) — absorve varredura de liquidez típica antes da reversão (v6.1.3)
- **Símbolos monitorados: 8** (USDJPY e EURJPY desativados por desempenho histórico negativo)

---

*Manual Mestre v6.1.3 — Synkra AIOX Ecosystem*
