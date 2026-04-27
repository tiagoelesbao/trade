# Documento Estratégico: Sniper v6.0 (Lifecycle Architecture)

**Data:** 21 de Abril de 2026
**Versão:** 6.0.1
**Status:** Produção

---

## 1. Filosofia de Operação

O sistema opera como um **Algoritmo de Seleção M15** — baixa frequência, alta precisão. A estratégia detecta zonas de liquidez onde capital institucional rejeitou o preço, aguarda confirmação técnica de reversão e envia o sinal para aprovação pela War Room antes de executar.

### Princípios Fundamentais
1. **Gatilho Institucional (M15):** Decisões baseadas no fechamento de velas de 15 minutos, filtrando ruído de timeframes menores.
2. **Aprovação Agêntica:** Nenhuma ordem é enviada sem passar pelo scoring da War Room (mín. 55/100).
3. **One-Shot por Zona:** Cada zona de liquidez é consumida após um único uso — sem re-entradas no mesmo nível.
4. **Config como Lei:** Todos os filtros vêm exclusivamente do `config.yaml`; nenhum valor hardcoded no código.

---

## 2. Pipeline de Execução (FSM 8 Estados)

```
[BOT detecta]          [WAR ROOM analisa]       [BOT executa]
signal_detected  →  awaiting_consensus  →  approved  →  filled  →  open  →  closed
                                       ↘  rejected                        ↘  error
```

### Descrição dos Estados
| Estado | Responsável | Descrição |
|---|---|---|
| `signal_detected` | Bot | Sinal técnico identificado, registro criado no Supabase |
| `awaiting_consensus` | Bot | Aguardando análise da War Room |
| `approved` | War Room | Score ≥ 55/100, sem conflito de correlação |
| `rejected` | War Room | Score < 55/100 ou correlação ativa |
| `filled` | Bot | Ordem executada no MT5, `position_id` registrado |
| `open` | Bot | Posição ativa monitorada |
| `closed` | Bot | P&L real calculado do histórico MT5 |
| `error` | Bot | Falha na execução registrada |

---

## 3. Filtros de Entrada (todos lidos do config.yaml)

### A. Detecção de Zona (M15)
- **Lookback:** `lookback_zones: 100` candles (~25h de mercado)
- **Confirmação:** `min_displacement_candles: 7` — zona só é válida após 7 candles de afastamento (105 min)
- **Tipo:** Resistências (máximas locais) e Suportes (mínimas locais)

### B. Gatilho de Entrada
| Filtro | Parâmetro config | Condição SELL | Condição BUY |
|---|---|---|---|
| Wick Rejection | `min_wick_pct: 0.30` | Pavio superior ≥ 30% da vela | Pavio inferior ≥ 30% da vela |
| RSI Guard | `rsi_period: 9` / `rsi_overbought: 70` / `rsi_oversold: 30` | RSI ≥ 70 (sobrecomprado) | RSI ≤ 30 (sobrevendido) |
| Slope Guard H1 | `use_trend_filter: false` (v6.1.1) — `slope_threshold_pips` removido do config em v6.1.3 | MA20 H1 descendente (< -0.5 pip/vela) | MA20 H1 ascendente (> +0.5 pip/vela) |
| Color Reversal | `require_color_reversal: false` (v6.1.1) | Vela anterior vermelha, atual verde oposto | Vela anterior verde, atual vermelha oposto |

**Comportamento crítico do `use_trend_filter`:**
- Se `true` e H1 não carregou dados → trade **bloqueado** (não assume neutro)
- Se `false` (default v6.1.1) → filtro de slope ignorado completamente — operação pura reversão em zona

**Nota v6.1.1 (2026-04-21):** Após call de revisão com trader experiente, `use_trend_filter` e `require_color_reversal` foram desativados. Motivos:
- Slope Guard operava invertido para estratégia contra-tendência (bloqueava exatamente as melhores entradas)
- Color Reversal atrasava entrada no ponto ótimo da zona

**Diretriz arquitetural v7.0 (Fase 3) — MA100/200:**
- **MA100 + MA200 H1** (macro trend) serão adicionadas **exclusivamente como pontuação** na War Room (peso máx 20pts). **Nunca** como gate no `check_trigger`. Usar como gate repetiria o erro do Slope Guard anterior, já que a estratégia é contra-tendência em zona.
- Status em 2026-04-22: **pendente** — escopo de Fase 3.

**RSI período 9 — ADOTADO em v6.1.3 (2026-04-22):**
- Config key: `rsi_period: 9` (antes: hardcoded 14 em `calculate_rsi`).
- Promovido como default **sem teste A/B** — decisão explícita do usuário baseada no item H do parecer técnico (trader: "período 9 é o clássico, mais reativo").
- `calculate_rsi(series, period=None)` em `bot_liquidez.py` e `auto_war_room.py` lê o valor do config.

### C. Scoring da War Room (v6.1.2 — 5 critérios, máx. 100 pts, RSI alpha)

Reforma de scoring aplicada em 2026-04-22 após call com trader experiente.
**RSI promovido a alpha** (tese central da estratégia); **Slope e Volume removidos**
(Slope repetia o erro do gate do bot; Volume não casa com reversão em zona).

| Critério | Pts | Condição máxima | Obs |
|---|---|---|---|
| **RSI Extremo** | **35** | RSI ≥ 100 (SELL) ou ≤ 0 (BUY) | **ALPHA** — 30% → 0pts, 85 → 17.5, 100 → 35 |
| Wick % | 25 | wick_pct ≥ 0.50 | Bot valida ≥30%; War Room premia distância extra |
| Pin Bar | 20 | corpo ≤ 15% do range | Bot não verifica tamanho do corpo |
| Sessão | 15 | London+NY overlap (13–17h UTC) | Bot não verifica horário |
| Histórico | 5 | Win rate ≥ 60% (30 dias) | Poucos dados locais — peso baixo |

Score mínimo para aprovação: **55/100** (mantém ~55% do máximo)

**Removidos da v6.1.2:**
- `Slope H1` (15pts) — bot já não usa como gate desde v6.1.1. Manter no War Room era incoerente.
- `Volume` (10pts) — trader: "volume não casa com estratégia de reversão em zona de liquidez."

---

## 4. Travas de Segurança

### Kill-Zone de Proximidade
- **Raio:** `proximity_pips: 10` — bloqueia novo trade se houve um a menos de 10 pips
- **Janela:** `cooldown_hours: 4` — período de bloqueio após trade

### Breakeven Automático

**Status v6.1.3 (2026-04-22): DESATIVADO (`breakeven_candles: 0`).**
Motivo: com o valor anterior (7 velas = 1h45), trades estavam sendo ejetados a zero
em pullbacks normais antes da tese consolidar. Mantido o código da feature para
reativação futura.

Quando ativo (`breakeven_candles > 0`), após N velas M15 desde a abertura o bot move
o SL para o preço de entrada + 2 pontos de buffer (custo zero). Condições:
- Trade deve estar em **lucro** no momento da verificação
- SL ainda deve estar do lado de risco (não modifica duas vezes)
- TP permanece intacto
- Implementado via `TRADE_ACTION_SLTP` — modificação direta no servidor da corretora

```yaml
breakeven_candles: 0   # 0 = desativado (default v6.1.3) | 7 = 1h45min após abertura
```

### One-Shot (Consumo de Zona)
- Zona marcada como `consumed_zones` na abertura do sinal (não na execução)
- Persistida em `.consumed_zones.json` — sobrevive a reinicializações
- Expira após 24 horas automaticamente

### Correlação entre Pares (War Room)
Pares correlacionados não podem ter posições simultâneas:
- EURUSD ↔ GBPUSD (correlação positiva alta)
- EURUSD ↔ USDCHF (correlação negativa alta)
- GBPUSD ↔ EURGBP
- AUDUSD ↔ NZDUSD
- USDCAD ↔ USDJPY *(USDJPY desativado — par removido da operação)*

### Limite de 1 Sinal por Ciclo
- Bot envia apenas 1 sinal a cada ciclo de 20s para evitar race conditions

---

## 5. Gestão Financeira (config.yaml)

| Parâmetro | Valor | Comportamento |
|---|---|---|
| `lot_size` | 1.0 | Lote fixo por operação |
| `stop_buffer_points` | 50 | Pontos adicionais além da mínima/máxima do pavio (v6.1.3: 15 → 50 para absorver varredura de liquidez) |
| `risk_reward_ratio` | 1.5 | TP = distância_SL × 1.5 |
| `daily_max_loss` | $350 | Bot para (sessão encerrada) |
| `daily_profit_target` | $500 | Bot para (meta atingida) |
| `filling_mode` | FOK | Fill or Kill — cancela se preço mudou |

---

## 6. P&L de Sessão

- `SESSION_START = datetime.now()` capturado no boot do bot
- `get_session_pnl()` — soma todos os deals MT5 desde `SESSION_START`
- P&L Sessão reseta a cada reinício do bot (não usa data/meia-noite)
- P&L Total = histórico completo da conta desde 2020

---

## 7. Exportação para MetaTrader (Indicador)

A cada ciclo, o bot gera `liquidez_data_{SYMBOL}.csv` em `MQL5/Files/` com:
1. Linha `BOT_STATUS,{pnl_sessao},{pnl_total},{n_exauridas}`
2. Até 6 zonas de RESISTÊNCIA (mais próximas ao preço atual, após merge de 15 pips)
3. Até 6 zonas de SUPORTE (mais próximas ao preço atual, após merge de 15 pips)

O indicador `IndicadorLiquidez.mq5` lê este CSV a cada 5s e renderiza:
- Retângulos preenchidos (zonas)
- Linha pontilhada central
- Label de preço (anchorado acima para resistência, abaixo para suporte)
- Destaque de zonas dentro de 25 pips (cor mais intensa)
- Painel BOT STATUS no canto superior esquerdo

---

## 8. Símbolos Operados

**8 pares ativos** (reduzido de 9 após análise de desempenho histórico):

```yaml
symbols:
  - EURUSD
  - GBPUSD
  - AUDUSD
  - USDCAD
  - USDCHF
  - NZDUSD
  - EURGBP
  - GBPJPY
  # USDJPY: DESATIVADO — WR 42.1% (8/19 trades), P&L -$232.29 | JPY comportamento direcional
  # EURJPY: DESATIVADO — WR 16.7% (1/6 trades), P&L -$85.56
```

**Critério de desativação:** Símbolo com mais de 6 trades e WR < 45% + P&L negativo é candidato a desativação.

---

## 9. Suite ETL (Análise Diária)

Scripts Python para extração e análise das operações — executar após a sessão ou para diagnóstico:

| Script | Comando exemplo |
|---|---|
| `etl_trades.py` | `python etl_trades.py --session --detail` |
| `etl_rejections.py` | `python etl_rejections.py --from 2026-04-21 --reason trend` |
| `etl_db_audit.py` | `python etl_db_audit.py --fix --verbose` |
| `etl_report.py` | `python etl_report.py --session --format both` |

O `etl_report.py` gera `.json` pronto para colar em IA para análise de padrões e geração de insights.

---

*Documento Estratégico v6.0.2 — Synkra AIOX Ecosystem*
