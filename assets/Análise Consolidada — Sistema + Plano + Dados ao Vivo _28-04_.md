# Análise Consolidada — Sistema + Plano + Dados ao Vivo (28/04)

---

## 1. O que os Dados de Hoje (28/04) Revelam

Os 3 dias do plano (23–27) já eram preocupantes. Hoje ampliou e validou tudo de pior:

| Dia | Trades | WR | P&L | Sinal |
|---|---|---|---|---|
| 23 | ~30 | 73% | +$391 | ✅ |
| 24 | 9 | 80% | +$848 | ✅ |
| 25–26 | (fim de semana) | — | — | — |
| 27 | 15 | 33% | −$357 | ⚠️ |
| **28** | **11** | **9,1%** | **−$527** | **🔴 DAILY MAX LOSS HIT** |

**Janela 23–28 agregada:** 67 trades · WR 46% · +$795 — ainda positivo, mas a almofada dos 4 primeiros dias está sendo queimada em 2 dias.

### O Padrão do Plano — Confirmado em Escala Maior Hoje

Hoje 10/11 trades perderam, todos contra-tendência H1:

- **AUDUSD:** 3 BUYs perderam (02:12, 10:56, 11:30) num dia em que AUDUSD caiu o dia inteiro (0.71796 → 0.71547)
- **USDCAD:** 3 SELLs perderam (10:11, 10:57, 11:31) num dia em que USDCAD subiu (1.365 → 1.367)
- **EURUSD:** 2 BUYs perderam num dia em que EURUSD caiu (1.170 → 1.168)
- **USDCHF:** 2 SELLs perderam num dia em que USDCHF subiu

> **Único win:** AUDUSD SELL @00:12 (Asia early, com macro descendente confirmando) → +$140 — exatamente o cenário "Asia early premiada" que o plano F2 já descreve.

---

## 2. Análise dos Arquivos Core

### Pontos Fortes do Código Atual

- **`bot_liquidez.py` v6.1.5:** Lifecycle FSM bem desenhado, dedup in-memory por vela é correto, `check_breakeven` desativado mas presente para reativação fácil.
- **`auto_war_room.py` v6.1.2:** Scoring enxuto (5 critérios, 100pts), `derive_strategy_context` evita refetch, separação FASE 1 (gatilho) / FASE 2 (score) é clara.
- **`trade_lifecycle_manager.py`:** Source-of-truth no Supabase, falhas vão pro logger (não silenciam).
- **`system_logger.py`:** `signal_analysis()` grava breakdown estruturado — vai facilitar o backtest exigido pela Parte 5 do plano.

### Pontos Fracos — Confirmados pelos Dados de Hoje

#### A) Cluster de Losses no London Open (10:56–11:31)

6 trades em 35 minutos, 0 wins. Análise das rejeições:

```
40 sinais rejeitados hoje:
  22 (55%) por CORRELAÇÃO com posição já ativa
   6 (15%) por score baixo
  ...
```

O filtro de correlação está **rejeitando os depois**, não escolhendo o melhor. A `auto_war_room.py:604` ordena por score e aprova o primeiro — mas como o scoring não tem awareness de macro trend, o "melhor score" no London open hoje foi um trade contra-tendência. Os correlatos rejeitados depois (NZDUSD: 14 sinais, GBPUSD: 12 sinais) provavelmente teriam direção mais alinhada com o macro.

> **Falha estrutural além do plano:** a priorização entre correlatos é arbitrária quando o scoring é cego para direção.

#### B) GBPJPY e GBPUSD Aparecendo nas Estatísticas

- `config.yaml:9-19` desativa GBPJPY (e USDJPY, EURJPY) — mas a janela 23–28 mostra **7 trades em GBPJPY (−$62,63)**. Isso é histórico antes da desativação ou um bug de config?
- GBPUSD gerou 12 sinais hoje e 0 executados — todos rejeitados por correlação com EURUSD. GBPUSD efetivamente **nunca ganha o tie-break**.

#### C) Dead Code no `bot_liquidez.py:188-199`

Slope MA20 H1 ainda presente: `USE_TREND_FILTER` agora é sempre `False` (config), mas a lógica continua no código. Não é crítico, mas é poluição.

---

## 3. Avaliação do PLANO_ACAO_v6.2–v7.0

### O que o Plano Acerta com Solidez

**⭐⭐⭐ Diagnóstico raiz:** "cego para regime macro" + "entra no meio do caminho" + "sessão binária" — os dados de 28/04 confirmam com mais força do que os dias 23–27 que originaram o documento.

**⭐⭐⭐ Tensão A (Breakeven) bem mapeada:** a tripla condição `(3 candles + 0.5R + RSI cruzou 50)` é a forma correta de reativar BE depois do fracasso da v6.1.3.

**⭐⭐⭐ Tensão D (subdivisão de sessão) validada hoje:** trade vencedor único foi 00:12 (Asia early), e perdas catastróficas foram 10:56–11:31 (London open) — exatamente o que F2 prevê pontuar diferente.

**⭐⭐ Protocolo de validação (Parte 5)** com critério `(LOSSES filtrados / WINS filtrados) > 1,5x` é rigoroso e adequado.

**⭐⭐ Constraint da memória respeitada:** macro trend explicitamente como score-only, nunca gate (linha 21 do plano + `feedback_strategy_macro_trend.md`).

---

### Onde o Plano Subestima a Urgência

#### 🔴 Re-priorizar v6.3.0/F1 (Macro Trend Score) para v6.2.0

A sequência atual coloca Macro Trend na 3ª release (v6.3.0, semana 3). Os dados de hoje sugerem que é **a única alavanca que move os losses de 28/04**. Sem ele:

- **F1 (extension filter)** não filtra os losses de hoje — em dia de tendência forte, "K velas vermelhas" antes do gatilho de BUY **confirma** o entry no cliff. Esse filtro funciona em mercado mean-reverting, **piora** em mercado trending.
- **F2 (sessão)** só ajusta scoring marginalmente.
- **F3 (correlação ampliada)** só rejeita o 2º — sem corrigir o 1º.

**Comparativo quantitativo:**

| Filtro v6.2.0 | Trades evitados em 28/04 |
|---|---|
| F1 — extension (3 vermelhas antes de BUY) | ~2 (talvez) — mas pode aprovar mesmo |
| F2 — sessão granular | 0 — todos os losses estão em sessão "premium" |
| F3 — correlação ampliada | 1–2 (clusters 10:56) |
| **Total v6.2.0** | **~3 de 10 losses** |

| Filtro v6.3.0/F1 (macro) | Impacto |
|---|---|
| AUDUSD em downtrend → bot tentou 3 BUYs | −3 trades (−$205) evitados |
| USDCAD em uptrend → bot tentou 3 SELLs | −3 trades (−$140) evitados |
| EURUSD em downtrend → bot tentou 2 BUYs | −2 trades (−$183) evitados |
| **Total** | **~8 de 10 losses evitados** |

---

#### 🟠 Adicionar ao Plano: Tie-Breaker Direcional entre Correlatos

**Não está no plano.** Quando 3+ sinais correlatos disparam ao mesmo tempo (cluster 10:56 hoje), `auto_war_room.py:604` aprova o de maior score — mas o scoring é direcionalmente cego. Uma vez que macro trend exista no scoring (v6.3.0/F1), esse problema se resolve sozinho. **Mais um motivo para antecipar.**

#### 🟡 Tensão B (Filtro de Cor da Vela) é Menos Crítica do que Parece

O plano coloca como ⭐ baixa prioridade — concordo. Os pavios dos losses de hoje são genuínos (40–78%). O problema não é "vela errada" — é **direção errada**.

#### 🟢 v7.0.0 (ICT Liquidity) Ainda Parece Distante, mas...

**News embargo** poderia ter impacto imediato. Hoje 10:30 UTC = 7:30am NY = release de dados (frequente). O cluster 10:56–11:31 cheira a manipulação pós-news embargo. Vale considerar mover para v6.2 como **toggle simples** (calendário hardcoded de horários high-impact).

---

## 4. Riscos Não Cobertos pelo Plano

### Risco 1 — Equity Drawdown Crítico

6 dias acumulados ainda mostram +$795, mas:
- Dia 27: −$357
- Dia 28: −$527
- **Trajetória:** −$884 em 2 dias = toda a almofada em risco em 1 dia ruim a mais

> **Recomendação:** pausar bot até v6.3.0/F1 deployar. Daily max loss ($500) já protege diariamente, mas **drawdown semanal não tem ceiling** no sistema.

### Risco 2 — Backtest "Rico" pode ser Pobre Estatisticamente

O plano da Parte 5.1 propõe backtest contra logs de 5 dias (~67 trades). Em estatística de trading, **n < 200 é amostra fraca**. O critério `(LOSSES filtrados / WINS filtrados) > 1,5x` pode ser ruído estatístico.

> **Recomendação:** rodar backtest também contra logs históricos mais antigos do Supabase (se houver) ou aceitar forward-test demo de **10+ dias** antes de promover qualquer release.

### Risco 3 — Plano Não Fala em Rollback Automático

Feature flags estão lá, mas quem decide ativar rollback?

> **Sugestão:** regra automática — se **3 dias seguidos com expectancy < −$10**, killswitch e reverte a feature flag mais recente.

### Risco 4 — `breakeven_candles` Zerado Deixa Wins Virarem Losses

Nos 6 dias analisados, vários "wins" provavelmente foram trades que ficaram em +0.7R, voltaram, e fecharam negativos. Sem o BE inteligente (v6.2.1), a expectancy continua frágil.

> **Recomendação:** promover v6.2.1 para **antes** de v6.3.0 se o backtest mostrar muitos giros tardios.

---

## 5. Recomendações Concretas — Sequenciamento Revisto

### 🔴 URGENTE (esta semana)

1. **PAUSAR o bot** até deploy de macro trend
2. **Implementar v6.3.0/F1 (Macro Trend Score) PRIMEIRO** — backtest contra dias 27+28 deve mostrar 70%+ dos losses filtrados
3. **Junto, implementar v6.2.0/F3** (correlações ampliadas)

### 🟡 Semana 1–2

4. **Forward-test demo** do bundle (macro + correlations) por 5 dias
5. **v6.2.0/F2** (sessão granular) — baixo risco, deploy direto

### 🟠 Semana 2–3

6. **v6.2.0/F1** (extension filter) — **somente depois** do macro estar ativo *(sem macro, esse filtro pode piorar em trending market)*
7. **v6.2.1** (smart breakeven)

### 🟢 Semana 3–4

8. **v6.3.0/F2** (cooldown direcional)
9. **v6.4.0** (RSI exit)

---

### Ações Imediatas no Código (independente da release)

- **`auto_war_room.py:73`:** aumentar `MIN_CONFIDENCE_SCORE` de 65 para **70** enquanto macro não existe — reduz volume mas filtra mais marginais.
- **`system_logger.py:135`:** `min_score = 55` está hardcoded e desatualizado vs `MIN_CONFIDENCE_SCORE = 65` no war room. **Bug visual no log.**
- **Investigar** GBPJPY aparecendo em stats apesar de comentado em `config.yaml:18`.

---

## TL;DR

O plano está tecnicamente correto e bem fundamentado, com convergência real entre 3 fontes. Mas a **velocidade proposta (3–4 semanas até macro trend) não acompanha a deterioração observada**: 28/04 sozinho perdeu mais que 27/04, e o sistema bateu daily max loss pela primeira vez.

**Reordenar:** Macro Trend Score (v6.3.0/F1) deve ser a **PRIMEIRA** mudança, não a terceira. É a única alavanca que move 70–80% dos losses de hoje. As demais (extensão, sessão granular, breakeven) são afinamentos sobre uma base que ainda é direcionalmente cega — **corrigir a base primeiro, refinar depois**.

---

> **Próximos passos:** abrir a issue/story `v6.3.0-F1-MACRO-TREND-FIRST` ou implementar o backtest contra hoje (28/04) para quantificar exatamente quantos losses o macro filter teria evitado?