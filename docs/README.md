# Trade — Documentação

Sistema de trading algorítmico multi-par para forex. Detecta zonas de liquidez em M15, valida sinais via War Room agêntica com contexto ICT, executa no MetaTrader 5 e gerencia saída dinâmica em real-time.

**Versão atual:** v6.2.0-ict (Sprints 1-6)
**Pares ativos:** AUDUSD, GBPUSD, USDCAD, USDCHF, NZDUSD
**Status:** Produção (forward-test em demo)

---

## Mapa da documentação

| Doc | Responde |
|-----|----------|
| [prd.md](prd.md) | **O quê e por quê** — visão do produto, requisitos funcionais, métricas de sucesso |
| [architecture.md](architecture.md) | **Como está montado** — 4 processos, FSM de estados, schema Supabase, paths de dados |
| [strategy.md](strategy.md) | **Qual a tese** — gatilhos de entrada, gates ICT, scoring War Room, regras de saída a-f |
| [operations.md](operations.md) | **Como rodo / debugo** — FULL_START, config reference, troubleshoot, onde olhar logs |
| [changelog.md](changelog.md) | **O que mudou** — histórico v5.5 → v6.2.0 |
| [trade-analysis.md](trade-analysis.md) | **Pipeline LLM pós-trade** — analise multiagente offline (não-runtime) |
| [sprints/](sprints/) | Detalhes técnicos por sprint (1-6) |

---

## Quick start

```bash
# Iniciar todo o sistema (4 processos)
FULL_START.bat

# Acessar dashboard
http://localhost:3000

# Ver logs em tempo real
http://localhost:3000/logs
```

Para troubleshoot, configuração e detalhes operacionais → [operations.md](operations.md).

---

## Estrutura do projeto

```
trade/
├── app/                                    # Frontend Next.js (dashboard)
├── docs/                                   # Esta documentação
├── squads/trade-liquidez-python/           # Squad de trading
│   ├── config.yaml                         # Configuração canônica
│   ├── scripts/                            # Motores Python + indicador MT5
│   │   ├── bot_liquidez.py                 # Detector + executor
│   │   ├── auto_war_room.py                # Decisão (Pool-then-Pick)
│   │   ├── exit_war_room.py                # Gestão de saída (regras a-f)
│   │   ├── ict_context_engine.py           # Engine ICT multi-timeframe
│   │   ├── cooldown_manager.py             # Cooldown direcional pós-loss
│   │   ├── ict/                            # Submódulos ICT
│   │   └── IndicadorLiquidez.mq5           # Indicador visual MT5
│   └── data/                               # Estado runtime (cooldowns, daily_state)
├── FULL_START.bat                          # Orquestrador (inicia 4 processos)
└── .env                                    # SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
```
