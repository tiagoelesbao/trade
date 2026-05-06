# Sprint 6 — Cooldown Direcional + Exit War Room Logs Ricos

**Status**: ✅ COMPLETO (2026-04-30)
**Versão alvo**: v6.2.0-ict
**Branch**: `feature/v6.2.0-ict-context`

## Origem (forward-test 30/04 em demo)

Após segundo dia rodando v6.2.0-ict em demo (sessões 1 com score 75 e sessão 2 com score 70), foram levantadas 3 observações:

1. **3 USDCHF BUY consecutivos com loss** (09:42, 10:11, 11:36) somando -$353. A 4ª tentativa (14:26) foi WIN +$66. Cluster de losses no mesmo par+direção em 2h.
2. **Exit War Room logs pobres** — só linhas MONITOR/UNMONITOR/CLOSE, sem detalhe de PORQUÊ cada regra disparou ou não.
3. **Validação cross-check estratégia vs entradas** — confirmar se as entradas perdedoras seguiram a estratégia ou desviaram.

## Diagnóstico — Observação 3 (cross-check estratégia)

Cruzando trades do dia 30/04 com `agent_opinions` no Supabase:

| Trade | RSI | ICT D1/H1 | ICT Score | Decisão da estratégia |
|-------|-----|-----------|-----------|------------------------|
| 09:42 USDCHF BUY (-$112) | 15.5 | bearish/reversal-up | 17/25 | "tese de virada" — VÁLIDA |
| 10:11 USDCHF BUY (-$139) | 17.4 | bearish/reversal-up | 17/25 | mesma tese, VÁLIDA |
| 11:36 USDCHF BUY (-$103) | **9.2** | bearish/reversal-up | 17/25 | tese reforçada, VÁLIDA |
| **14:26 USDCHF BUY (+$66)** | 23.2 | bearish/reversal-up | 17/25 | mesma tese — **WIN** |

**Conclusão**: ICT score 17/25 representa "contra D1 bias mas H1 reversal alinhado (BOS recente)" — exatamente o que a estratégia faz (mean-reversion contra trend macro). **A edge existe** (4ª tentativa venceu), mas o **cluster de 3 losses consecutivos no mesmo par/direção** mata expectancy. **A estratégia foi seguida fielmente** — o mercado não respeitou 3x.

**Cooldown direcional pós-loss é a defesa correta** — não é falha de configuração, é mecânica de proteção pra cluster perdedor.

## Sprint 6.1 — Cooldown direcional pós-loss

### Funcionamento

- Após **loss confirmado** em (symbol, direction): bloqueia a MESMA combinação por `cooldown_hours_after_loss` horas (default **4h**)
- **Limite de severidade**: só ativa se loss ≤ `cooldown_min_loss_pnl` (default -$10) — evita ativar por BE-stops triviais
- Estado persistido em `data/cooldowns.json` (sobrevive reinício do bot)
- Defesa em camadas:
  - **Camada 1 (eficiência)**: `bot_liquidez.check_trigger` bloqueia ANTES de criar sinal — evita poluir War Room
  - **Camada 2 (auditoria)**: `auto_war_room` rejeita auto via `REJEITADO_COOLDOWN` se cache stale ou cooldown ativou no meio

### Eventos no Supabase

| Evento | Quando |
|--------|--------|
| `cooldown_started` | Loss confirmado, cooldown ativado |
| `cooldown_active` | Bot tentou disparar trigger mas foi bloqueado |
| `cooldown_expired` | Período passou, libera (implícito via re-leitura) |

### Aplicação ao cenário 30/04

```
09:42 USDCHF BUY -$111  → ativa cooldown USDCHF:BUY até 13:42
10:11 USDCHF BUY        → BLOQUEADO (cooldown ativo, 211min restantes)
11:36 USDCHF BUY        → BLOQUEADO (cooldown ativo, 126min restantes)
14:26 USDCHF BUY        → APROVADO (cooldown expirou às 13:42) → +$66 WIN
```

**P&L teórico com cooldown**: -$111 (vs -$287 real). Economia: **+$176**.

## Sprint 6.2 — Exit War Room Logs Ricos

### Antes (Sprint 4-5)

```
HISTORICO DE EVENTOS (ultimos 4/50):
  12:42:54  MONITOR    USDCHF BUY t=8431881144 entrou em monitoramento
  13:02:03  UNMONITOR  ticket=8431881144 saiu do monitoramento
```

Sem detalhe de **profit_R no fim**, **regras avaliadas**, **PORQUÊ cada regra não disparou**.

### Depois (Sprint 6.2)

**Bloco rico por posição em cada ciclo**:
```
┌── POSICAO  USDCHF BUY  ticket=8431881144  vol=1.00
│  entry=0.78793  current=0.78760  SL=0.78743  TP=0.78843
│  profit: -0.45R  (-3.3p)  risk: 5.0p  candles: 3
│  [#####|------------------------]   (-2R                 0                 +2R)
│  ICT: D1=bearish  state=london_open
│       liq above=0.78850 (5.7p)  |  liq below=0.78720 (4.0p)
│  Regras:
│    [X unmet ] regra a: profit -0.45R < 1.0R
│    [X unmet ] regra b: profit -0.45R < 0.7R
│    [X unmet ] regra c: profit -0.45R < 0.5R
│    [X unmet ] regra d: profit -0.45R <= 0
│    [X unmet ] regra e: profit -0.45R mas estrutura ICT nao quebrou
│    [X unmet ] regra f: 3c < 6c minimo
└── DECISAO: aguardando (nenhuma regra disparou)
```

### Mudanças

- `evaluate_all_rules()` retorna **breakdown completo das 6 regras** com status individual
- `print_dashboard` reescrito com bloco rico por posição (header, OHLC, profit bar visual, ICT context, status detalhado de cada regra a-f, decisão final)
- `recent_events` deque ampliado **50 → 200**
- `log_position_evaluation` envia evento `position_evaluation` ao Supabase com `data.rules_breakdown` JSON completo (auditoria 100%)
- Eventos no rolling deque marcados com `EVAL` quando profit_R cruza marco significativo (-1R, -0.5R, 0.5R, 0.7R, 1R) ou quando matched_rules muda — preserva histórico legível

### Eventos novos no Supabase

| Evento | Source | Quando |
|--------|--------|--------|
| `position_evaluation` | EXIT_WR | A cada ciclo de cada posição (com rules_breakdown JSON) — Sprint 6.2 NEW |
| `position_snapshot` | EXIT_WR | A cada ciclo (Sprint 5) |
| `cooldown_started` | BOT | Loss ativou cooldown — Sprint 6.1 NEW |
| `cooldown_active` | BOT | Trigger bloqueado por cooldown — Sprint 6.1 NEW |

## Checklist

- [x] **6.1.1** `cooldown_manager.py` criado — `CooldownManager` com persistência JSON
- [x] **6.1.2** Config: `cooldown_after_loss_enabled`, `cooldown_hours_after_loss`, `cooldown_min_loss_pnl`
- [x] **6.1.3** Bot — `is_entry_blocked_by_ict_cliff` + cooldown gate em `_gate_cliff_ok`; registra loss em `check_if_closed`
- [x] **6.1.4** War Room — pre-filter `REJEITADO_COOLDOWN` antes do CLIFF filter
- [x] **6.1.5** Dashboard do bot mostra "COOLDOWNS ATIVOS" com tempo restante
- [x] **6.2.1** `evaluate_all_rules()` retorna breakdown verbose de todas regras
- [x] **6.2.2** `print_dashboard` reescrito com bloco rico (profit bar, ICT, regras, decisão)
- [x] **6.2.3** `recent_events deque` 50 → 200
- [x] **6.2.4** `log_position_evaluation` no Supabase com rules_breakdown JSON
- [x] **6.2.5** Push event "EVAL" quando profit_R cruza marco ou matched_rules muda
- [x] **6.3** Compile validation + smoke test

## Validação executada

### Compile
```
SPRINT_6_1_COMPILE_OK
SPRINT_6_2_COMPILE_OK
  bot_liquidez.py + auto_war_room.py + exit_war_room.py
  + cooldown_manager.py + system_logger.py + ict_context_engine.py
```

### Cooldown Manager smoke test
```
Antes do loss: USDCHF BUY blocked=False
Loss registrado, libera em: 2026-05-01T00:20
Apos loss   : USDCHF BUY blocked=True  ← bloqueado
USDCHF SELL : blocked=False             ← direção oposta NÃO bloqueia
GBPUSD BUY  : blocked=False             ← par diferente NÃO bloqueia
```

### Evaluate All Rules smoke test (profit 0.6R, 4 candles)
```
   rule a [X unmet ]: profit +0.60R < 1.0R
   rule b [X unmet ]: profit +0.60R < 0.7R
   rule c [V MATCH ]: profit +0.60R + 4c + RSI 100.0   ← regra C dispara
   rule d [X unmet ]: ICT context indisponivel
   rule e [X unmet ]: profit +0.60R >= 0 (so para perdedoras)
   rule f [X unmet ]: 4c < 6c minimo
```

## Arquivos novos / modificados

| Arquivo | Operação |
|---------|----------|
| `scripts/cooldown_manager.py` | NOVO |
| `scripts/bot_liquidez.py` | + cooldown gate em check_trigger, + register_loss em check_if_closed, + dashboard mostra cooldowns ativos |
| `scripts/auto_war_room.py` | + REJEITADO_COOLDOWN pre-filter antes de CLIFF |
| `scripts/exit_war_room.py` | + evaluate_all_rules verbose, + log_position_evaluation, dashboard rico, deque 200 |
| `config.yaml` | + cooldown_after_loss_enabled, cooldown_hours_after_loss, cooldown_min_loss_pnl |
| `data/cooldowns.json` | NOVO (persistido em runtime) |

## Próximos passos sugeridos

1. **Forward-test 01/05** — observar se cooldown bloqueia clusters reais e se logs do Exit WR ficam claros
2. **Tunar `cooldown_hours_after_loss`** — começar com 4h e ajustar empiricamente (talvez 3h ou 6h melhor dependendo do par)
3. **Adicionar `cooldown_after_n_losses`** (futuro): só ativar cooldown após N losses consecutivos no par+direção (vs 1 só)
4. **Schema Supabase** (incremental, Sprint 7): colunas `ict_score`, `total_score`, `cooldown_was_active` em `signals_liquidez` para queries mais simples

## Riscos conhecidos

- **Cooldown 4h pode ser conservador demais** — se a edge existe (caso 14:26 venceu), 2-3h pode capturar mais wins. Ajustar com dados.
- **Cooldown não diferencia volatilidade** — em mercado calmo 4h é muito; em volátil pode ser pouco. Implementação atual é uniforme.
- **`position_evaluation` a cada ciclo** aumenta volume de logs no Supabase. Como já tinha `position_snapshot` (Sprint 5), agora cada ciclo gera 2 events. Free tier ainda suporta sem problema.
