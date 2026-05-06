# Sprint 2 — ICT Context Engine (Macro Awareness)

**Status**: ✅ COMPLETO (2026-04-28)
**Versão alvo**: v6.2.0-ict
**Branch**: `feature/v6.2.0-ict-context`

## Objetivo

Construir módulo de análise multi-timeframe baseado nas Aulas 1+2+3 do método ICT, integrar como 6º critério de scoring no War Room (peso 25), e estabelecer **gate ICT CLIFF** (defesa em camadas: bot + war room) para o cenário catastrófico de trade contra D1 bias + H4 expansion contrária.

## Arquitetura entregue

```
squads/trade-liquidez-python/scripts/
├── ict/
│   ├── __init__.py
│   ├── structure.py            # detect_swings, classify_structure (HH/HL/LH/LL, BOS)
│   ├── phase_detector.py       # Aula 1 — expansion/retracement/reversal/consolidation
│   ├── liquidity_levels.py     # Aula 3 — untested + equal levels (raid targets)
│   └── daily_range_algo.py     # Aula 2 — estado do dia (Asia/Judas/London/NY)
└── ict_context_engine.py       # Orquestrador + cache 5min + alignment scorer
```

## Checklist

- [x] **2.1** `ict/structure.py` — `detect_swings(df, depth=5)` com strength em pips, `classify_structure(pivots)` com BOS detection, `bias_from_structure`
- [x] **2.2** `ict/phase_detector.py` — `classify_phase(df)` retornando `PhaseResult(phase, direction, confidence, note)`. Heurísticas: BOS → reversal; range pequeno → consolidation; swing >1.3x mediana → expansion; retração 30-65% → retracement
- [x] **2.3** `ict/liquidity_levels.py` — `find_untested_levels`, `find_equal_levels` (double tops/bottoms), `next_levels(price)` retornando above/below mais próximos
- [x] **2.4** `ict/daily_range_algo.py` — `get_current_phase(now_utc)` mapeando em 8 fases ICT, `DailyState` dataclass + persistência JSON `data/daily_state_YYYYMMDD.json`, `cleanup_old_states(days_to_keep=7)`
- [x] **2.5** `ict_context_engine.py` — `get_context(symbol, mt5_module)` orquestra fetch D1+H4+H1+M15, monta dict completo, cache TTL 300s, `_build_alignment_scorer` retorna closure `(score_fn, explain_fn)` 0-25 pts
- [x] **2.6** `auto_war_room.py` — 6º critério ICT (25 pts), redistribuição RSI 35→25, Wick 25→20, PinBar 20→15, Sessão 15→10, ICT 25 NEW, Hist 5. 4ª opinião "ICT Macro". `print_signal_card` mostra detalhe `D1=... H4=... H1=...`
- [x] **2.6b** `bot_liquidez.py` — `is_entry_blocked_by_ict_cliff(symbol, trade_type)` aplicado em `check_trigger` ANTES de retornar gatilho. Bloqueia se `ict_score == 0`. Cache compartilhado com War Room (5min TTL no engine)
- [x] **2.7** `auto_war_room.print_strategy_fire` — card `[ICT CONTEXT]` com bias D1, phases H4/H1, liquidity above/below, alignment BUY vs SELL renderizado entre FASE 1 e FASE 2
- [x] **2.7b** **CLIFF rejection no War Room** — `analyze_signal_strength`: se `scores['ict'] == 0` → `REJEITADO_CLIFF` independente do total. Não passa pra checagem de score nem correlação
- [x] **2.8** Validação: 9 arquivos compilam, teste sintético com trend bullish detectado (bias=bullish, BUY=25/25, SELL=0/25 cliff)

## Mudança de regra de memória — IMPORTANTE

A constraint original `feedback_strategy_macro_trend.md` ("macro nunca pode ser gate, só score") **foi atualizada** com aprovação explícita do usuário no Sprint 2:

- **Score-only continua como default** (0-25 pts compõem o total normal)
- **Gate é permitido apenas no caso CLIFF** (ict_score = 0/25)
- **Gate NÃO é permitido para indicadores simples** (MAs, slopes) — reservado a análise estrutural ICT multi-timeframe

Justificativa ICT (Aula 1): expansion = "willingness to reveal pricing model" — entrar contra expansion forte é cliff, mesmo princípio do "don't catch a falling knife".

## Pesos do scoring v6.2.0 (Sprint 2)

| Critério | Sprint 1 | Sprint 2 | Δ |
|----------|---------:|---------:|---:|
| RSI Extremo | 35 | **25** | -10 |
| Wick % | 25 | **20** | -5 |
| Pin Bar | 20 | **15** | -5 |
| Sessão (ICT janelas) | 15 | **10** | -5 |
| **ICT Macro** | — | **25** | +25 |
| Histórico | 5 | 5 | 0 |
| **Total** | 100 | **100** | 0 |

Score mínimo: **75/100** (mantido do Sprint 1).

## Faixas do `trade_alignment_score` (0-25 pts)

| Cenário | Pontos | Comportamento |
|---------|-------:|---------------|
| A-favor D1 + H4 expansion na direção | **25** | Trade ideal ICT |
| A-favor D1 + H4 retracement (pullback) | **22** | Pullback em trend — ICT favorito |
| A-favor D1, fases mistas | **18** | Bom |
| A-favor D1 + H4 consolidation | **16** | Range, baixa convicção |
| Bias D1 neutro + H1 reversal alinhado | **18** | Setup local em mercado lateral |
| Bias D1 neutro + H1 expansion alinhado | **16** | OK |
| Bias D1 neutro, sem alinhamento | **12** | Score neutro (default fallback) |
| Contra D1 + H1 reversal alinhado (BOS) | **15** | Tese de virada |
| Contra D1 + consolidation | **10** | Aceitável |
| Contra D1 + retracement contrária | **5** | Fraco |
| **Contra D1 + H4 expansion contrária** | **0** | **CLIFF — gate** |

Bonus liquidity (±2 pts dentro do max 25):
- +2 se trade vai em direção a liquidity level próximo (≤30 pips, raid target)
- −2 se liquidity contrária a ≤15 pips (vai bater logo)

## Validação executada

### Compile
```
ALL_COMPILE_OK
  bot_liquidez.py
  auto_war_room.py
  system_logger.py
  ict_context_engine.py
  ict/__init__.py + structure.py + phase_detector.py + liquidity_levels.py + daily_range_algo.py
```

### Teste funcional sintético (trend bullish 100 candles)
```
Test 1: detect_swings -> 5 pivots detectados
Test 2: bias = bullish (correto, trend de alta)
Test 3: phase = consolidation/neutral (com noise alto, esperado)
Test 4: untested=2, equals=0
Test 5: current daily phase = asia_early (UTC=22)
Test 6: BUY a-favor D1 bullish + H4 expansion up: 25/25
        SELL contra trend: 0/25 (CLIFF — bloqueado)
```

### Defesa em camadas
| Camada | Local | Quando dispara |
|--------|-------|----------------|
| 1ª (eficiência) | Bot `check_trigger` | Cliff detectado antes de criar sinal — não polui War Room |
| 2ª (auditoria) | War Room `analyze_signal_strength` | Se cache stale ou bot não checou — REJEITADO_CLIFF logado |

## Cobertura observacional dos losses 27-28/04 (estimada)

| Trade | Cenário esperado ICT | Score ICT estimado |
|-------|---------------------|-------------------:|
| 28/04 02:12 AUDUSD BUY (-$101) | downtrend D1, BUY contra | 0-5 (provável CLIFF) |
| 28/04 10:56 AUDUSD BUY (-$71)  | downtrend D1, H1 expansion contra | 0 (CLIFF) |
| 28/04 11:30 AUDUSD BUY (-$33)  | downtrend D1, H1 expansion contra | 0 (CLIFF) |
| 28/04 10:11 USDCAD SELL (-$42) | uptrend D1, SELL contra | 0-5 |
| 28/04 06:11 EURUSD BUY (-$88)  | downtrend D1, BUY contra | 0-5 |
| 28/04 00:12 AUDUSD SELL (+$140)| Asia early, exhaustion real | 18-22 (a-favor) |

**Conclusão estimada**: 8-9 dos 10 losses de 28/04 teriam recebido ICT ≤ 5pts; pelo menos 4-5 teriam disparado CLIFF (bloqueio total). O único win do dia teria recebido pontuação alta. **Validação real só com forward-test demo nos próximos dias.**

## Critério de pronto

- [x] War Room imprime card `[ICT CONTEXT]` antes do scoring com bias/phase/levels
- [x] Cada trade recebe 0-25 pts ICT no scoring
- [x] CLIFF (0/25) bloqueia em duas camadas (bot + war room)
- [x] Cache 5min compartilhado entre bot e war room (mesmo `_CACHE` global no `ict_context_engine`)
- [x] Memória de constraint atualizada (`feedback_strategy_macro_trend.md`)

## Arquivos afetados

| Arquivo | Operação |
|---------|----------|
| `scripts/ict/__init__.py` | NOVO |
| `scripts/ict/structure.py` | NOVO |
| `scripts/ict/phase_detector.py` | NOVO |
| `scripts/ict/liquidity_levels.py` | NOVO |
| `scripts/ict/daily_range_algo.py` | NOVO |
| `scripts/ict_context_engine.py` | NOVO |
| `scripts/bot_liquidez.py` | adicionado import + `is_entry_blocked_by_ict_cliff` + uso em `check_trigger` |
| `scripts/auto_war_room.py` | adicionado import + critério ICT em `analyze_signal_strength` + 4ª opinion + REJEITADO_CLIFF + card no `print_strategy_fire` |
| `scripts/system_logger.py` | SCORE_MAX/SCORE_LABELS atualizados (6 critérios) + detalhe `ict` |
| `data/` | criado (futuro home dos `daily_state_*.json`) |

## Próximo Sprint

→ **Sprint 3**: War Room v2 com Pool-then-Pick + Tie-breaker direcional. Janela de 30s pra acumular sinais correlatos antes de aprovar; vencedor é o de maior `(ict_alignment, score)`. Resolve o problema do cluster 10:56 UTC de 28/04 onde "primeiro a chegar" ganhou arbitrariamente.

---

● Sprint 2 ✅ COMPLETO.                       

  Resumo do que entregamos
                                                                                                                                                                                                                        Pacote ict/ (4 módulos novos)
                                                                                                                                                                                                                      
  ┌─────────────────────┬──────────────────────────────────────────────────────────────────────────────────────┐
  │       Módulo        │                                        Função                                        │                                                                                                        ├─────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤                                                                                                        │ structure.py        │ detect_swings, classify_structure (HH/HL/LH/LL + BOS), bias_from_structure           │                                                                                                        ├─────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤                                                                                                        │ phase_detector.py   │ classify_phase retornando expansion/retracement/reversal/consolidation por timeframe │                                                                                                      
  ├─────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ liquidity_levels.py │ find_untested_levels, find_equal_levels, next_levels (raid targets ICT Aula 3)       │
  ├─────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ daily_range_algo.py │ Estado do dia ICT (Aula 2) com persistência JSON, cleanup_old_states                 │
  └─────────────────────┴──────────────────────────────────────────────────────────────────────────────────────┘

  Orquestrador ict_context_engine.py

  - get_context(symbol) — fetch D1/H4/H1, monta contexto consolidado
  - Cache 5min compartilhado entre bot e war room
  - _build_alignment_scorer — closure que entrega 0-25 pts por trade type
  - render_context_card — desenha card ASCII para FASE 1

  Integração

  ┌───────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────┐
  │              Componente               │                                     Mudança                                     │
  ├───────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
  │ auto_war_room.analyze_signal_strength │ 6º critério ICT (25 pts), redistribuição de pesos, 4ª opinion "ICT Macro"       │
  ├───────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
  │ auto_war_room decisão                 │ REJEITADO_CLIFF se ict_score == 0 (independente do total)                       │
  ├───────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
  │ auto_war_room.print_strategy_fire     │ Card [ICT CONTEXT] com bias/phases/liquidity entre FASE 1 e FASE 2              │
  ├───────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
  │ bot_liquidez.check_trigger            │ Gate is_entry_blocked_by_ict_cliff ANTES de retornar gatilho (defesa em camada) │
  ├───────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
  │ system_logger.SCORE_MAX/LABELS        │ 6 critérios alinhados com war room                                              │
  └───────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────┘

  Mudança de regra documentada
  Mudança de regra documentada

  Memória feedback_strategy_macro_trend.md atualizada: ICT é score-only por padrão, gate só em CLIFF (alignment 0/25 = trade contra D1 + H4 expansion contrária). Reservado a análise estrutural ICT — não vale para  
  indicadores simples (MAs/slopes).

  Validação

  - 9 arquivos compilam sem erro
  - Teste sintético com trend bullish: bias detectado corretamente, BUY a-favor = 25/25, SELL contra-trend = 0/25 (CLIFF)
  - Defesa em camadas: bot bloqueia primeiro (não cria sinal), war room rejeita se cache stale

  Cobertura estimada para 28/04

  8-9 dos 10 losses teriam ICT ≤ 5pts; 4-5 teriam disparado CLIFF (bloqueio completo). Validação real só com forward-test em demo (próximos dias).

  ---
  Próximo passo: Sprint 3 — War Room v2 com Pool-then-Pick + Tie-breaker direcional. Resolve o cluster 10:56 UTC de 28/04 onde "primeiro a chegar" ganhou arbitrariamente — agora a janela de 30s acumula correlatos e
   escolhe o de maior (ict_alignment, score) antes de aprovar.

  Quer que eu siga direto pro Sprint 3 ou prefere primeiro fazer um smoke run em demo do bot v6.2.0-ict (3 terminais: bot + war room + dashboard) pra ver os logs ICT aparecerem ao vivo?
  