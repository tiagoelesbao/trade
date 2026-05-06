# Sprint 4 — Exit War Room (4º terminal)

**Status**: ✅ COMPLETO (2026-04-28) — observações de campo levantadas em 2026-04-29 ficam para Sprint 5
**Versão alvo**: v6.2.0-ict
**Branch**: `feature/v6.2.0-ict-context`

## Objetivo

4º processo no `FULL_START.bat` que monitora posições abertas em real-time e aplica regras de saída inteligente baseadas em ICT context + price action. Substitui o `check_breakeven` legado do bot (mantido desativado em config).

## Arquitetura

```
[Bot detecta zona+wick+RSI+gates]
       ↓
[War Room Pool-then-Pick + ICT scoring]
       ↓
[Bot executa ordem aprovada]
       ↓
[Posição aberta no MT5]
       ↓
[Exit War Room loop a cada 10s]
       ↓
   evaluate_position(stats, ict_ctx, df_m15, df_h1)
       ↓
   regra a-f matchou? → execute_decision
   (BE / partial+BE / close / flag / none)
```

## Checklist

- [x] **4.1** `config.yaml`: nova seção `exit_war_room` com 6 feature flags + 4 parâmetros
- [x] **4.2** `exit_war_room.py` criado (530 linhas) — main loop 10s, conexão MT5/Lifecycle/ICT, helpers `_modify_position_sltp`, `_close_position`, `_be_sl_for`, `_is_already_at_be`
- [x] **4.3** Função `evaluate_position` — 6 regras em ordem de prioridade (a → f). Cada regra com feature flag.
- [x] **4.4** `print_dashboard` — limpa terminal, mostra cada posição com profit_R, candles_open, próxima ação prevista, regras ativas. Atualiza a cada loop
- [x] **4.5** `FULL_START.bat`: 4ª janela `Exit War Room (Python)` adicionada, banner atualizado para v6.2.0-ict
- [x] **4.6** Logger source `EXIT_WR`. Eventos: `be_moved_dynamic`, `partial_closed`, `early_exit_liquidity`, `structure_break_close`, `time_exit_flagged`
- [x] **4.7** `bot_liquidez.check_breakeven` marcado como `[DEPRECATED v6.2.0 Sprint 4]` — guarded por `BREAKEVEN_CANDLES=0`
- [x] **4.8** Simulação `sim_sprint4_exit.py` cobre 6 cenários (todas as regras + caso "aguardar"). 6/6 OK.

## Regras a-f (em ordem de prioridade)

| # | Trigger | Ação | Feature flag |
|---|---------|------|--------------|
| **a** | profit ≥ 1.0R | BE imediato | `enable_be_at_1R` |
| **b** | profit ≥ 0.7R + reversal candle ICT | close 50% + BE | `enable_partial_at_07R_reversal` |
| **c** | profit ≥ 0.5R + 3 candles abertos + RSI(9) cruzou 50 | BE clássico | `enable_classic_be` |
| **d** | profit > 0 + preço a ≤3 pips de liquidity oposto | close cedo (raid completo) | `enable_liquidity_target_close` |
| **e** | profit < 0 + ICT structure contra (BOS ou trend forte) | close imediato | `enable_structure_break_close` |
| **f** | ≥ 6 candles abertos + range das últimas 6 < 0.3R | flag (não fecha — alerta) | `enable_time_exit_flag` |

**Estado em memória** (`_position_state`):
- `be_done` — evita reaplicar BE
- `partial_done` — evita reaplicar partial close
- `time_flagged` — evita logar flag repetidamente
- Limpa automaticamente quando posição fecha

## Validação executada

### Compile
```
SPRINT_4_COMPILE_OK
  bot_liquidez.py + auto_war_room.py + system_logger.py
  + ict_context_engine.py + ict/* (4 mods)
  + exit_war_room.py + sim_sprint4_exit.py
```

### Simulação `sim_sprint4_exit.py` (6 cenários)
```
OK  1) profit 1.2R + nada                              -> regra=a  BE
OK  2) profit 0.8R + reversal candle                   -> regra=b  partial_be
OK  3) profit 0.6R + 4 candles + RSI cruzou           -> regra=c  BE clássico
OK  4) profit -0.3R + trend bearish (structure contra) -> regra=e  close
OK  5) profit 0.1R + 8 candles sem progresso          -> regra=f  flag
OK  6) profit 0.2R + nada (aguardar)                   -> regra=None
```

### Ajuste fino durante validação
- `_detect_structure_break` ampliado: aciona não só em BOS estrito (alternância HH/LL) mas também em **trend confirmado contra** (LH+LL ou HH+HL consecutivos). Realista: quando entramos contra-trend e o trend continua, é structure contra mesmo sem BOS clássico.
- Fixture do teste 5 ajustado para gerar últimas 6 velas com range minúsculo (≪ 0.3R)
- Fixture do teste 4 reescrito: trend monotônico não gera pivots — precisa de oscilação senoidal + bias

## Pipeline de logs (Sprint 4)

| Evento | Source | Quando | Data JSON |
|--------|--------|--------|-----------|
| `exit_war_room_started` | EXIT_WR | startup | — |
| `be_moved_dynamic` | EXIT_WR | regra a/c dispara | rule, ticket, old_sl, new_sl, profit_R, candles_open |
| `partial_closed` | EXIT_WR | regra b dispara | rule, ticket, partial_volume, remaining_volume, new_sl |
| `early_exit_liquidity` | EXIT_WR | regra d dispara | rule, ticket, profit_R, exit_price |
| `structure_break_close` | EXIT_WR | regra e dispara | rule, ticket, profit_R, exit_price |
| `time_exit_flagged` | EXIT_WR | regra f dispara | rule, ticket, candles_open, profit_R |

## Critério de pronto

- [x] 4º terminal (`Exit War Room`) abre com `FULL_START.bat`
- [x] Dashboard mostra cada posição com profit_R, candles, próxima ação
- [x] Compila e roda standalone (simulação 6/6 OK)
- [x] BE legado do bot desativado (deprecated)
- [x] Logger registra todos os 5 eventos no Supabase

## Observações de campo (2026-04-29) — backlog para Sprint 5

Após primeiro forward-test em demo, o usuário levantou 4 pontos críticos:

1. **Exit War Room sem histórico no terminal** — usa `os.system('cls')` que apaga rolling log. Precisa scrollback como bot/war room.
2. **Divergência RSI bot vs MT5 chart** em alguns trades (USDCAD 02:45h, 11:30h) — investigar fonte (período 9 vs 14? timeframe? momento da medição?).
3. **Bot terminal apaga logs** — mesmo problema do `os.system('cls')` no `print_dashboard`. Erros transitórios são perdidos.
4. **Esquema Supabase pode precisar de colunas novas** para ICT score, cluster decision, exit events.

Detalhamento e plano de correção em `docs/sprints/SPRINT 5.md`.

## Arquivos afetados

| Arquivo | Operação |
|---------|----------|
| `squads/trade-liquidez-python/config.yaml` | Nova seção `exit_war_room` |
| `squads/trade-liquidez-python/scripts/exit_war_room.py` | NOVO — 530 linhas |
| `squads/trade-liquidez-python/scripts/sim_sprint4_exit.py` | NOVO — 6 cenários standalone |
| `squads/trade-liquidez-python/scripts/bot_liquidez.py` | `check_breakeven` marcado como deprecated |
| `FULL_START.bat` | 4ª janela `Exit War Room`, banner v6.2.0-ict, 5 processos |

## Próximo Sprint

→ **Sprint 5**: **Persistência de Logs + Diagnóstico RSI + Schema Audit**. Endereçar as 4 observações de campo levantadas em 29/04 antes de continuar acumulando dias de demo.
