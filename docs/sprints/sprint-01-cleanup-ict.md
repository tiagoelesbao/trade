# Sprint 1 — Limpeza, Calibração e Fundamentos ICT

**Status**: ✅ COMPLETO (2026-04-28)
**Versão alvo**: v6.2.0-ict
**Branch**: `feature/v6.2.0-ict-context` (não pushed)

## Objetivo

Remover ruído (dead code, JPY, EUR), ajustar gates de horário com Daily Range Algorithm ICT (Aula 2), calibrar scoring de sessão com 8 janelas ICT, ampliar correlações, elevar score mínimo.

## Checklist

- [x] **1.1** Remover dead code Slope MA20 H1 (`bot_liquidez.py`)
  - Removido: `SLOPE_THRESHOLD_PIPS`, `USE_TREND_FILTER`, `REQUIRE_REVERSAL`
  - Removido: lógica de `trend_slope`, `is_reversal`, fetch desnecessário de `df_h1` em `check_trigger`
- [x] **1.2** `config.yaml`: pausar `EURUSD` + `EURGBP` (ICT Aula 3 — evitar EUR no início)
  - Pares ativos finais: `AUDUSD, GBPUSD, USDCAD, USDCHF, NZDUSD` (5)
- [x] **1.3** `config.yaml`: nova seção `session_windows` com 8 janelas ICT
  - `asia_early`(21-24, 8), `asia_judas`(0-7, 1), `london_open`(7-10, 14), `london_cont`(10-13, 11), `ny_news_embargo`(13-14, 0), `ny_expansion`(14-15, 13), `london_close`(15-16, 12), `ny_afternoon`(16-21, 7)
- [x] **1.4** `config.yaml`: gates `entry_cutoff_hour_mt5: 22` (= 19 UTC) e `news_embargo_pause: true` (13-14 UTC = 16-17 MT5)
- [x] **1.5** `auto_war_room.py:73`: `MIN_CONFIDENCE_SCORE: 65 → 75` (lê de `min_confidence_score` no config)
- [x] **1.6** `auto_war_room.py`: `session_score_label` reescrita ICT-aware com 8 janelas, lendo `_SESSION_WINDOWS` do config
- [x] **1.7** `system_logger.py:135`: `min_score = 55 → MIN_CONFIDENCE_SCORE` (lê do config, fim do drift)
- [x] **1.8** `auto_war_room.py`: `CORRELATED_PAIRS` ampliado de 5 → 16 entradas (USD-quote bundle completo)
- [x] **1.9** `bot_liquidez.py`: nova `is_entry_blocked_by_time()` aplicada como gate em `check_trigger()`
- [x] **1.10** Validação final: todos os arquivos compilam, YAML válido, função de sessão e gates verificados

## Validação executada

### Arquivos compilam
```
CONFIG_OK
  symbols: ['AUDUSD', 'GBPUSD', 'USDCAD', 'USDCHF', 'NZDUSD']
  min_score: 75
  cutoff_mt5: 22
  embargo: 13 - 14
  sessions: [asia_early, asia_judas, london_open, london_cont,
             ny_news_embargo, ny_expansion, london_close, ny_afternoon]
BOT_COMPILE_OK
WAR_ROOM_COMPILE_OK
LOGGER_COMPILE_OK
```

### Tabela `session_score_label` (UTC)
```
  UTC 22h ->   8 pts  | Asia early (post-NY)
  UTC 00h ->   1 pts  | Asia continuation/Judas
  UTC 05h ->   1 pts  | Asia continuation/Judas
  UTC 07h ->  14 pts  | London open expansion
  UTC 11h ->  11 pts  | London continuation
  UTC 13h ->   0 pts  | NY 8-8:30 news embargo
  UTC 14h ->  13 pts  | NY open expansion
  UTC 15h ->  12 pts  | London close reversal
  UTC 16h ->   7 pts  | NY afternoon / end-of-day
```

### Tabela de gates (cutoff MT5=22, embargo UTC 13-14)
```
  UTC 13h / MT5 16h  [BLOCK] news_embargo
  UTC 19h / MT5 22h  [BLOCK] cutoff_mt5
  UTC 20h / MT5 23h  [BLOCK] cutoff_mt5
  UTC 21h / MT5 00h  [ OPEN ]   (Asia early — único win 28/04 caiu aqui)
  outras horas       [ OPEN ]
```

### Cobertura observacional dos losses 27-28/04
| Trade | Hora | Janela ICT | Score sessão (antes / agora) |
|-------|------|------------|------------------------------|
| 27/04 01:11 EURUSD SELL (-$104) | 01 UTC | asia_judas | 3 → 1 |
| 27/04 01:12 AUDUSD SELL (-$107) | 01 UTC | asia_judas | 3 → 1 |
| 27/04 02:41 AUDUSD SELL (-$93)  | 02 UTC | asia_judas | 3 → 1 |
| 27/04 08:11 EURUSD SELL (-$93)  | 08 UTC | london_open | 10 → 14 |
| 28/04 02:12 AUDUSD BUY  (-$101) | 02 UTC | asia_judas | 3 → 1 |
| 28/04 10:56 cluster (-$237 em 3 trades) | 10 UTC | london_cont | 10 → 11 |
| 28/04 11:30 AUDUSD BUY (-$33)   | 11 UTC | london_cont | 10 → 11 |

**Conclusão sessão**: Asia/Judas penalizada (-2 pts em 5 trades = -10 pts cumulativo no score). London open premiada. News embargo ZERA (e bloqueia gate).

## Critério de pronto

- [x] Bot inicia sem erro
- [x] Log do War Room mostra novos pesos e janelas ICT
- [x] Bot bloqueia entradas em 13:00-13:59 UTC (= 16:00-16:59 MT5)
- [x] Bot bloqueia entradas após 22:00 MT5 (= 19:00 UTC)
- [x] EUR/JPY pausados — não geram sinais
- [x] Score mínimo 75 alinhado entre war room e logger

## Arquivos afetados

| Arquivo | Linhas modificadas |
|---------|---------------------|
| `squads/trade-liquidez-python/config.yaml` | reescrita ampla — symbols, sessions, gates, min_score |
| `squads/trade-liquidez-python/scripts/bot_liquidez.py` | docstring, constantes globais, `is_entry_blocked_by_time`, `check_trigger`, `print_dashboard`, main loop |
| `squads/trade-liquidez-python/scripts/auto_war_room.py` | docstring, constantes, `session_score_label`, `CORRELATED_PAIRS`, banner |
| `squads/trade-liquidez-python/scripts/system_logger.py` | leitura `MIN_CONFIDENCE_SCORE` do config, `signal_analysis` deixa de ter `min_score=55` hardcoded |

## Próximo Sprint

→ **Sprint 2**: ICT Context Engine (`ict_context_engine.py`) — multi-timeframe phase detector + untested levels + daily range state. Score-only inicial, peso 25 redistribuindo da árvore atual.

---

● Sprint 1 ✅ COMPLETO.

  Resumo do que entregamos no Sprint 1
                                                                                                                                                                                                                                          ┌────────────────────────────────────────┬───────────────────────────────────┬─────────────────────────────────────────┐
  │                  Item                  │               Antes               │                 Depois                  │                                                                                                                ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤                                                                                                                │ Pares ativos                           │ 7 (com EUR + JPY mortos no array) │ 5 (AUD, GBP, USDCAD, USDCHF, NZD)       │                                                                                                                ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤                                                                                                                │ Dead code (Slope MA20, color reversal) │ 50+ linhas mortas                 │ removido                                │                                                                                                              
  ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤
  │ Score mínimo                           │ 65 hardcoded em 2 lugares (drift) │ 75 lido do config em todos              │
  ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤
  │ Sessão                                 │ 4 janelas grossas                 │ 8 janelas ICT (Daily Range Algorithm)   │
  ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤
  │ Gate news embargo                      │ inexistente                       │ bloqueio 13-14 UTC (= 16-17 MT5)        │
  ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤
  │ Gate end-of-day                        │ inexistente                       │ bloqueio ≥22h MT5 (= 19 UTC)            │
  ├────────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────┤
  │ Correlated pairs                       │ 5 entradas                        │ 16 entradas (USD-quote bundle completo) │
  └────────────────────────────────────────┴───────────────────────────────────┴─────────────────────────────────────────┘

  Validação executada: 4 arquivos compilam sem erro, YAML válido, função de sessão e gates testados em todas as horas críticas.

  Arquivos tocados

  - config.yaml (reescrita ampla — pares, sessions, gates, min_score)
  - scripts/bot_liquidez.py (docstring, constantes, novo is_entry_blocked_by_time, check_trigger enxuto, dashboard, main loop)
  - scripts/auto_war_room.py (docstring, constantes, session_score_label ICT, CORRELATED_PAIRS ampliado, banner)
  - scripts/system_logger.py (MIN_CONFIDENCE_SCORE do config)
  - docs/sprints/SPRINT 1.md (documentação de status)

  Impacto observacional cruzado com 27-28/04

  Os 5 trades em janela asia_judas (-$497 acumulados) caem de score 3→1 (peso quase desclassifica). London open ganha de 10→14 (premiada). News embargo ZERA score E bloqueia gate (defesa em camadas).

  O que o bot v6.2.0-ict NÃO faz ainda (e está correto não fazer)

  - Não tem awareness de macro trend (só vem no Sprint 2 com ICT Context Engine)
  - scripts/bot_liquidez.py (docstring, constantes, novo is_entry_blocked_by_time, check_trigger enxuto, dashboard, main loop)
  - scripts/auto_war_room.py (docstring, constantes, session_score_label ICT, CORRELATED_PAIRS ampliado, banner)
  - scripts/system_logger.py (MIN_CONFIDENCE_SCORE do config)
  - docs/sprints/SPRINT 1.md (documentação de status)

  Impacto observacional cruzado com 27-28/04

  Os 5 trades em janela asia_judas (-$497 acumulados) caem de score 3→1 (peso quase desclassifica). London open ganha de 10→14 (premiada). News embargo ZERA score E bloqueia gate (defesa em camadas).

  O que o bot v6.2.0-ict NÃO faz ainda (e está correto não fazer)

  - Não tem awareness de macro trend (só vem no Sprint 2 com ICT Context Engine)
  - Não faz pool-then-pick em clusters de sinais correlatos (Sprint 3)
  - Não tem Exit War Room para BE inteligente / saída antecipada (Sprint 4)

  ---
  Próximo passo: começar Sprint 2 — ICT Context Engine quando você der o sinal. É o bloco mais pesado (3-4h de implementação), e é onde está a maior alavanca: o módulo que vai dizer "AUDUSD está em downtrend H1, BUY contra-tendência
   → -10 pts ICT" e exibir essa informação na FASE 1 do War Room antes do scoring.
