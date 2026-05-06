# Plano de Ação — Próxima Bateria de Incrementos (v6.2 → v7.0)

> **Documento de consolidação — 3 fontes integradas**
> Data: 2026-04-27
> Versão atual em produção: bot v6.1.5 / War Room v6.1.2 / Indicador v6.1.3
> Baseado em:
> 1. Análise quantitativa dos trades 23-27/04 (`trade anal.md`)
> 2. Calls com trader (`Trader_Analysis/Dia_24/`, `Dia_27/`)
> 3. Mentoria ICT — Aulas 1, 2 e 3 (`Trader_Lessons/`)

---

## Sumário executivo

A análise dos últimos 3 dias operacionais (23, 24 e 27 de abril) gerou +$1.211 acumulado, mas com perfil heterogêneo: **dia 27 perdeu −$455** (sessão UTC) por entradas contra-tendência forte. As três fontes de input convergem sobre **3 falhas críticas estruturais** do sistema atual:

1. **Cego para regime macro** → dia 27 perdeu 7/7 trades contra-tendência H1
2. **Entra "no meio do caminho"** → faltam N candles direcionais antes do gatilho
3. **Trata sessão como variável binária** → Asia early (100% WR) ≠ Asia continuation (0% WR)

A próxima bateria será dividida em **4 releases incrementais** (v6.2 → v7.0), com validação contra logs históricos antes de cada deploy. O maior alavanca de retorno é o **Macro Trend Score** (ICT lesson 3 + análise dia 27 + trader call 24).

**Estado de saúde atual** (3 dias):
- WR média: 55-80% (dias bons), 23-37% (dia ruim)
- R/R real: 1.45-1.89x (acima do RR configurado 1.5x — favorável)
- Expectancy: positiva nos dias 23-24, negativa dia 27
- Avg win: +$117 / Avg loss: −$80

---

## Parte 1 — Mapeamento das 3 fontes

### 1.1 Análise quantitativa (resumo)

| Métrica | Dia 23 | Dia 24 | Dia 27 (UTC) | Dia 27 (sessão MT5) |
|---------|--------|--------|--------------|---------------------|
| Aprovados WR | 30 | 9 | 13 fechados | 16 fechados |
| Win Rate | 73% mapeada | 80% | **23.1%** | 37.5% |
| P&L net | +$391 | +$848 | **−$455** | −$27 |
| Score médio | ~73 | ~74 | ~78 | — |

**Padrão crítico dia 27**: 4 SELLs em AUDUSD (uptrend) → **0/4 WR**, −$348. 3 BUYs em USDCAD (downtrend) → **0/3 WR**, −$190.

### 1.2 Trader (sumário das 2 calls)

**Call Dia 24 — pontos centrais**:
- "A gente tem que botar um filtro de quantos candles anteriores precisa pra obter uma entrada"
- "A melhor operação foi após dar 3 candles vermelhos, RSI estourado, foi onde ele deu uma compra mais do que perfeita"
- "O stop poderia ser mais curto, colado ao pavio"
- "Se ele esperasse esse candle fechar, ele teria um lucro bem maior"
- "RSI tem regiões — 70, 50 e 30. Esse mercado voltou apenas no 50%, poderia ser saída de 1º alvo"
- "Tava contra a tendência macro" (aceitou, mas reconheceu o risco)

**Call Dia 27 — pontos REINFORCED**:
- "**3 candles** no mínimo — pra ele filtrar e entrar na operação" (REPETIDO 6x)
- "Stop-loss para zero-a-zero após 2-3 candles a favor — não faz sentido perder se ficou positivo"
- "Em caso de compra, **não pode comprar vela verde**. Em caso de venda, **não pode vender vela vermelha**" (princípio do "3D")
- "RSI vai sobrecomprado, depois busca sobrevendido — saída ideal no extremo oposto"
- "Bot tá entrando quase puramente pelo RSI, falta filtros"
- "Ele pegou um pouco atrasada, nessa compra"

### 1.3 Mentoria ICT (3 aulas)

**Aula 1 — Elementos do Trade Setup**:
- 4 condições de mercado: **Expansion, Retracement, Reversal, Consolidation**
- 5 ferramentas, uma por condição:
  - **Order Blocks** ↔ Expansion (vela contrária imediatamente antes do impulso)
  - **Fair Value Gaps / Liquidity Voids** ↔ Retracement (gaps de movimentos rápidos)
  - **Liquidity Pools / Stop Runs** ↔ Reversal (varredura acima/abaixo de pivots)
  - **Equilibrium** ↔ Consolidation (50% do range)
- **Sequência obrigatória**: consolidation NUNCA vai direto pra retracement ou reversal — sempre passa por **expansion** primeiro
- **Nossa estratégia atual = Liquidity Pool / Stop Run trade** (varredura de pavio acima/abaixo de pivot M15)

**Aula 2 — Smart Money Paradigm + Daily Range Algorithm**:
- Mercado é **AI/algoritmo interbancário** — não é auction de pessoas
- **Daily Range previsível em fases**:
  - Asia consolidation
  - Judas Swing (manipulação cedo, ~midnight NY)
  - **London Open expansion** → forma high/low do dia
  - 5-8 NY: consolidation
  - **8-8:30 NY news embargo** → reversal/expansion
  - NY session: another expansion
  - **10-11 NY**: London close reversal
  - End of day: consolidation
- **News drives manipulation** — Judas Swing geralmente coincide com news embargo

**Aula 3 — Multi-timeframe + Mindset**:
- **Indicadores são inversos**: o que retail vê como sobrecomprado/sobrevendido é o que smart money usa pra raidar liquidez
- **Multi-timeframe OBRIGATÓRIA**:
  - Daily: 9-12 meses (contexto macro)
  - 4H: 3 meses (estrutura)
  - 1H: 3 semanas (direção intradiária)
  - **15M: 3-4 dias** (execução — nossa timeframe atual)
- **Equal highs/lows** = bull's eye de varredura
- **Untested recent highs/lows** = alvos prováveis
- **Time of day matters** — registrar quando high/low diário/semanal se forma

---

## Parte 2 — Matriz de convergência

| Tema | Análise quantitativa | Trader | ICT | Convergência |
|------|----------------------|--------|-----|--------------|
| **Filtro de N candles "esticados"** | Dia 27: USDCAD BUY/AUDUSD SELL pegaram início do trend | "3 candles" REPETIDO 6x | Order Block aparece após "expansion rápida" — entrar depois | ⭐⭐⭐ |
| **Macro Trend awareness** | Dia 27: 7/7 contra-tendência | "Tava contra macro" | Multi-timeframe é princípio CENTRAL ICT | ⭐⭐⭐ |
| **Sessão granular (Asia early ≠ continuation)** | Asia early 100% WR vs continuation 0% | "Horários melhores", "fechou bolsas" | Daily Range Algo: Asia consolidation, manipulação midnight, London open expansion | ⭐⭐⭐ |
| **Liquidez como alpha** | Estratégia já é mean-reversion em pavio | (concorda) | "Liquidity is the alpha" — pavios = stop runs | ⭐⭐⭐ |
| **Breakeven inteligente** | R/R real >1.5x = espaço pra proteger | "Stop a zero-a-zero após 2-3 candles favor" | (não direto) | ⭐⭐ |
| **Saída em RSI inverso (TP dinâmico)** | Avg Win cheio sugere alguns alongariam mais | "RSI vai sobrecomprado, busca sobrevendido" | (não direto, mas alinhado com cycle expansion→reversal) | ⭐⭐ |
| **Equal highs/lows como alvos** | Não considerado | Não mencionado | "Bull's eye for liquidity raids" | ⭐⭐ |
| **Untested recent highs/lows** | Não filtrado | Não mencionado | "Note recent highs that haven't been retested" | ⭐⭐ |
| **News embargo / Judas Swing** | Não considerado | Não mencionado | "8-8:30 NY news drives manipulation" | ⭐⭐ |
| **Filtro de cor da vela** | Não considerado | "Não comprar vela verde, não vender vela vermelha" | (não direto) | ⭐ |

---

## Parte 3 — Tensões a resolver com design fino

### Tensão A: Breakeven AGRESSIVO vs HISTÓRICO de ejeção precoce

| Lado | Argumento |
|------|-----------|
| Trader pede | BE após 2-3 candles a favor |
| Histórico | `breakeven_candles: 0` foi **desativado em v6.1.3** porque "BE em 1h45 estava ejetando trades a zero em pullbacks normais" |

**Resolução**: BE não pode ser **só por tempo**. Precisa **tripla condição**:
- (3 candles a favor) **AND** (preço atingiu ≥ 0.5R) **AND** (RSI cruzou 50)
- Buffer de 2-3 pips acima da entrada (não exatamente zero — proteção contra spread/wick)

### Tensão B: Filtro de cor da vela vs entrada no ponto ótimo

| Lado | Argumento |
|------|-----------|
| Trader pede | "Não comprar vela verde, não vender vela vermelha" |
| Histórico | `require_color_reversal: false` foi **desativado em v6.1.1** porque "atrasa entrada no ponto ótimo" |

**Resolução**: o que o trader quer NÃO é o `require_color_reversal` antigo (que olhava reversão entre as últimas 2 velas). É filtro DIFERENTE:
- A **vela do gatilho** (com pavio de rejeição) deve ter cor **coerente com a reversão**
- BUY (rejeição inferior): vela atual idealmente verde ou doji (não vermelha forte de continuação)
- SELL (rejeição superior): vela atual idealmente vermelha ou doji
- **Não reativar `REQUIRE_REVERSAL` antigo — implementar lógica nova**

### Tensão C: Filtro de N candles vs estratégia "sniper" early-entry

| Lado | Argumento |
|------|-----------|
| Trader pede | "Esperar 3 candles na direção esticada antes de entrar" |
| Estratégia atual | Pega gatilho na vela imediatamente após o pavio M15 fechado |

**Resolução**: Adicionar como **filtro de pré-condição** (não substituir o gatilho atual):
- BUY: ≥ N velas vermelhas das últimas K (ex: 3 de 5) **OU** displacement ≥ X pips na direção esticada
- SELL: simétrico
- Esse filtro **bloqueia** exatamente o cenário do dia 27 (AUDUSD SELL #1 pegou no início do uptrend)

### Tensão D: Sessão Asia atual vs subdivisão proposta

| Lado | Argumento |
|------|-----------|
| Sistema atual | `0 <= h < 8 → 3pts` (uniforme) |
| Análise | Asia early 100% WR, Asia continuation 0% WR (no MESMO 3pts) |
| ICT | Daily Range Algo: midnight NY = Judas Swing (manipulação), depois London Open = expansion |

**Resolução**: scoring de sessão precisa ser mais granular:
- 21-23 UTC = Asia early (post-NY close): 8 pts (premia exhaustion real)
- 23-04 UTC = Asia continuation / pre-Judas: 0-2 pts (penalidade)
- 04-07 UTC = pre-Londres: 5 pts
- 07-10 UTC = London open expansion: 12 pts
- 10-13 UTC = London continuation: 10 pts
- 13-17 UTC = London+NY overlap: **15 pts** (manter máximo)
- 17-22 UTC = NY: 8-10 pts

---

## Parte 4 — Backlog priorizado por release

### 🔴 RELEASE v6.2.0 — "Convergence Pack"

**Objetivo**: aplicar as 3 mudanças de maior convergência (3 fontes apontando), sem reescrever scoring nem estratégia. Esforço estimado: 1-2 dias dev.

#### v6.2.0/F1 — Filtro de N candles esticados ⭐⭐⭐
**Convergência**: Análise + Trader (REPETIDO 6x) + ICT (Order Block surge depois de expansion)
**Arquivo**: `bot_liquidez.py::check_trigger()` — adicionar pré-condição antes do return da tupla

```python
# Após confirmar wick + RSI + zona, antes de retornar trigger:

EXTENSION_LOOKBACK = CFG.get('extension_lookback', 5)
EXTENSION_MIN_CANDLES = CFG.get('extension_min_candles', 3)

# Slice das K velas anteriores ao gatilho (excluindo a vela do gatilho)
prev_K = df_m15.iloc[-(EXTENSION_LOOKBACK + 2):-2]  # últimas K velas fechadas antes do gatilho

if z['type'] == 'SUPPORT':  # BUY → mercado deve estar "esticado pra baixo"
    red_count = sum(1 for _, c in prev_K.iterrows() if c['close'] < c['open'])
    if red_count < EXTENSION_MIN_CANDLES:
        return None, None  # mercado ainda não foi varrido o suficiente
else:  # RESISTANCE → SELL → mercado esticado pra cima
    green_count = sum(1 for _, c in prev_K.iterrows() if c['close'] > c['open'])
    if green_count < EXTENSION_MIN_CANDLES:
        return None, None
```

**Config keys novas**:
```yaml
extension_lookback: 5        # K — quantas velas olhar pra trás
extension_min_candles: 3     # N — mínimo de velas direcionais
```

**Impacto esperado**:
- Bloqueia ~30% dos sinais atuais
- WR esperada sobe 5-10pp
- Filtra exatamente dia 27 AUDUSD SELL #1 (poucas velas verdes anteriores)

#### v6.2.0/F2 — Subdivisão da sessão (Asia early vs continuation) ⭐⭐⭐
**Convergência**: Análise (100% vs 0%) + Trader (horários) + ICT (Daily Range Algo)
**Arquivo**: `auto_war_room.py::session_score_label()`

```python
def session_score_label(hour_utc):
    """Scoring granular alinhado com Daily Range Algorithm (ICT)."""
    if 13 <= hour_utc < 17: return 15, "London+NY overlap"
    if 7  <= hour_utc < 10: return 12, "London open expansion"
    if 10 <= hour_utc < 13: return 10, "London continuation"
    if 17 <= hour_utc < 22: return 9,  "New York"
    if 21 <= hour_utc < 24: return 8,  "Asia early (post-NY)"  # NEW
    if 4  <= hour_utc < 7:  return 5,  "Pre-Londres"
    if 0  <= hour_utc < 4:  return 1,  "Asia continuation"     # NEW (antes era 3)
    return 0, "Fora de sessão"
```

**Impacto esperado**:
- Asia early ganha +5pts (premia setups validados)
- Asia continuation perde 2pts (penaliza padrão perdedor)
- Trades 04:11-05:41 dia 27 caem de score ~73 pra ~71 — pode não rejeitar isolado, mas combinado com F1 sim

**Risco**: amostra pequena (3+5 trades). Validar com mais ciclos antes de baixar threshold global.

#### v6.2.0/F3 — Ampliar `CORRELATED_PAIRS` ⭐⭐
**Convergência**: Análise (cluster perdedor 20:26-27 dia 23 e 11:11 dia 27)
**Arquivo**: `auto_war_room.py:77-83`

```python
CORRELATED_PAIRS = [
    ['EURUSD', 'GBPUSD'],
    ['EURUSD', 'USDCHF'],
    ['EURUSD', 'AUDUSD'],   # NEW — todos USD-quote movem juntos
    ['EURUSD', 'NZDUSD'],   # NEW
    ['GBPUSD', 'AUDUSD'],   # NEW
    ['GBPUSD', 'EURGBP'],
    ['AUDUSD', 'NZDUSD'],
    ['USDCAD', 'USDCHF'],
]
```

**Impacto esperado**:
- Bloqueia 2º trade do mesmo lado USD
- Dia 27 11:11 (8:11 UTC) — EURUSD SELL + AUDUSD SELL teria sido apenas 1 trade

#### Validação obrigatória pré-deploy v6.2.0

Implementar script de **backtest simulado** sobre logs War Room dos dias 23-27:

1. Ler todos os APROVADOs dos 5 logs
2. Para cada um, simular se v6.2.0 aprovaria (aplicar F1+F2+F3 nas condições registradas no log)
3. Cruzar com P&L real do Supabase
4. Métricas:
   - WR antes vs WR depois
   - Expectancy antes vs depois
   - Volume de trades (não pode cair > 50%)
   - Trades filtrados — quantos eram WIN e quantos eram LOSS

**Critério de aprovação**: ratio (LOSSES filtrados / WINS filtrados) > 1.5x

---

### 🟡 RELEASE v6.2.1 — "Smart Breakeven"

**Objetivo**: reativar breakeven, mas com tripla condição pra não repetir falha v6.1.3. Esforço: 1 dia dev.

#### v6.2.1/F1 — Breakeven condicional inteligente ⭐⭐
**Arquivo**: `bot_liquidez.py::check_breakeven()` (já existe, está desativado por config)

```python
# Reativar com regras compostas (override da função atual):

BREAKEVEN_MIN_R = CFG.get('breakeven_min_R', 0.5)
BREAKEVEN_REQUIRE_RSI_CROSS = CFG.get('breakeven_require_rsi_cross', True)

def _should_move_to_breakeven(pos, trade, df_m15, elapsed_candles):
    if elapsed_candles < BREAKEVEN_CANDLES:
        return False, "tempo insuficiente"

    entry = trade['price']
    sl = trade['sl']
    risk_pips = abs(entry - sl)
    profit_pips = (pos.price_current - entry) if trade['type'] == 'BUY' else (entry - pos.price_current)
    profit_R = profit_pips / risk_pips if risk_pips > 0 else 0

    if profit_R < BREAKEVEN_MIN_R:
        return False, f"profit {profit_R:.2f}R < {BREAKEVEN_MIN_R}R"

    if BREAKEVEN_REQUIRE_RSI_CROSS:
        rsi_now = calculate_rsi(df_m15['close']).iloc[-1]
        if trade['type'] == 'BUY' and rsi_now < 50:
            return False, f"RSI {rsi_now:.1f} ainda < 50"
        if trade['type'] == 'SELL' and rsi_now > 50:
            return False, f"RSI {rsi_now:.1f} ainda > 50"

    return True, "ok"
```

**Config keys**:
```yaml
breakeven_candles: 3         # era 0 — REATIVADO
breakeven_min_R: 0.5         # NEW — só se já tá em 0.5R de lucro
breakeven_require_rsi_cross: true  # NEW — só se RSI cruzou 50 na direção
breakeven_buffer_pips: 2     # mantém
```

**Impacto esperado**:
- Wins que viram losses por giros tardios são protegidos
- BE não dispara em pullbacks normais (porque RSI ainda não cruzou ou ainda não tem 0.5R)

**Risco**: a tripla condição pode ser muito restritiva e quase nunca disparar. Calibrar empiricamente.

---

### 🟠 RELEASE v6.3.0 — "Macro Awareness"

**Objetivo**: a alavanca de maior retorno — adicionar consciência de regime macro via MA100/200 H1 como score-only. Esforço: 3-5 dias dev.

#### v6.3.0/F1 — Macro Trend Score (MA100/MA200 H1) ⭐⭐⭐
**Convergência**: Análise (dia 27 inteiro) + Trader (call 24) + ICT (multi-timeframe é central)
**Restrição da memória**: NUNCA gate. Score-only.
**Arquivo**: `auto_war_room.py::analyze_signal_strength()`

```python
# Novo critério (peso 18 pts), redistribuir scoring total mantendo 100:

def calculate_macro_trend_score(trade_type, df_h1, current_close, point):
    """
    Score baseado no alinhamento com tendência H1 (MA100 vs MA200).
    Penaliza trades contra-tendência forte; premia a-favor.
    """
    if df_h1 is None or len(df_h1) < 200:
        return 9  # neutro se dados insuficientes (evita penalty injusta)

    ma100 = df_h1['close'].rolling(100).mean().iloc[-1]
    ma200 = df_h1['close'].rolling(200).mean().iloc[-1]

    trend_h1 = +1 if ma100 > ma200 else -1
    pip_size = point * 10
    distance_to_ma200_pips = abs(current_close - ma200) / pip_size

    if trade_type == 'BUY':
        if trend_h1 > 0:
            return 18  # a favor → premiado
        elif distance_to_ma200_pips < 30:
            return 9   # neutro perto do MA200 (zona de virada)
        else:
            return -10 # contra-tendência forte → penalty agressiva
    else:  # SELL
        if trend_h1 < 0:
            return 18
        elif distance_to_ma200_pips < 30:
            return 9
        else:
            return -10
```

**Reformatação do scoring (100 pts mantidos)**:

| Critério atual | Peso atual | Peso novo |
|----------------|------------|-----------|
| RSI | 35 | **30** |
| Wick | 25 | **20** |
| Pin Bar | 20 | **15** |
| Sessão | 15 | **12** |
| **Macro Trend** (NOVO) | — | **18** |
| Histórico | 5 | 5 |
| **Total** | 100 | 100 |

**Atualizar `SCORE_MAX`**:
```python
SCORE_MAX = {
    'rsi': 30, 'wick': 20, 'pin_bar': 15,
    'session': 12, 'macro': 18, 'history': 5
}
```

**Impacto esperado contra dia 27**:
- AUDUSD SELL @04:12 (score 73): −10 macro → 63 → REJEITADO (gate 65)
- USDCAD BUY @11:57 (score 88): −10 macro → 78 → APROVADO (mas perdeu = aceitável, alguns vão passar)
- Win rate dia 27 esperada: 40-50% (vs 23% real)

**Validação**: backtest contra dias 23-27 — não deve impactar dia 24 (regime mean-reverting); deve filtrar maior parte dos losses dia 27.

#### v6.3.0/F2 — Cooldown direcional ⭐⭐
**Convergência**: Análise (4 SELLs AUDUSD perderam em sequência dia 27)
**Arquivo**: `bot_liquidez.py` — tracking em memória

```python
# Estado em memória (não persiste entre reinícios — coerente com filosofia v6.1.5)
losses_today: dict[tuple[str, str], int] = {}  # (symbol, type) -> count
block_until: dict[tuple[str, str], datetime] = {}

def update_loss_tracking(symbol, trade_type, pnl):
    if pnl < 0:
        key = (symbol, trade_type)
        losses_today[key] = losses_today.get(key, 0) + 1
        if losses_today[key] >= 2:
            block_until[key] = datetime.now() + timedelta(hours=4)

def is_blocked(symbol, trade_type) -> bool:
    key = (symbol, trade_type)
    return key in block_until and datetime.now() < block_until[key]

# Em check_trigger antes de retornar trigger:
if is_blocked(symbol, trigger['type']):
    return None, None  # bloqueado por cooldown direcional

# Em check_if_closed após confirmar PnL:
update_loss_tracking(trade['symbol'], trade['type'], pnl_real)
```

**Config**:
```yaml
direction_cooldown_losses: 2     # após 2 losses na mesma direção/par
direction_cooldown_hours: 4      # bloqueia por 4h
```

**Impacto**: dia 27 AUDUSD SELL #3 e #4 teriam sido bloqueados.

**Risco**: pode bloquear oportunidade real de virada. Cooldown 4h é conservador — calibrar.

---

### 🟢 RELEASE v6.4.0 — "Smart Exits"

**Objetivo**: TP dinâmico baseado em RSI inverso (request explícito do trader). Esforço: 3-5 dias dev.

#### v6.4.0/F1 — Saída em RSI inverso (TP dinâmico) ⭐⭐
**Convergência**: Trader (call 24+27) + ICT (cycle expansion→reversal)
**Arquivo**: novo método em `bot_liquidez.py::check_rsi_exit()`

```python
RSI_EXIT_ENABLED = CFG.get('enable_rsi_exit', False)
RSI_EXIT_BUY_THRESHOLD = CFG.get('rsi_exit_threshold_buy', 65)
RSI_EXIT_SELL_THRESHOLD = CFG.get('rsi_exit_threshold_sell', 35)
RSI_EXIT_MIN_R = CFG.get('rsi_exit_min_R', 0.7)

def check_rsi_exit():
    """
    Fecha posição cedo se RSI atingiu zona oposta E lucro >= 0.7R.
    Captura a tese ICT de cycle expansion→reversal.
    """
    if not RSI_EXIT_ENABLED:
        return

    positions = mt5.positions_get() or []
    for pos in positions:
        if pos.magic != MAGIC_NUMBER:
            continue

        df_m15 = get_rates(pos.symbol, mt5.TIMEFRAME_M15, 30)
        rsi = calculate_rsi(df_m15['close']).iloc[-1]

        # Calcular profit em R
        risk_pips = abs(pos.price_open - pos.sl)
        is_buy = (pos.type == mt5.POSITION_TYPE_BUY)
        profit_pips = (pos.price_current - pos.price_open) if is_buy else (pos.price_open - pos.price_current)
        profit_R = profit_pips / risk_pips if risk_pips > 0 else 0

        if profit_R < RSI_EXIT_MIN_R:
            continue

        should_exit = (is_buy and rsi >= RSI_EXIT_BUY_THRESHOLD) or \
                      (not is_buy and rsi <= RSI_EXIT_SELL_THRESHOLD)

        if should_exit:
            # Fechar posição
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": mt5.ORDER_TYPE_SELL if is_buy else mt5.ORDER_TYPE_BUY,
                "magic": MAGIC_NUMBER,
                "comment": f"RSI_EXIT_{rsi:.0f}",
            }
            result = mt5.order_send(close_request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.trade("rsi_exit", f"{pos.symbol} fechado em RSI={rsi:.1f}, profit={profit_R:.2f}R")
```

**Config**:
```yaml
enable_rsi_exit: true
rsi_exit_threshold_buy: 65    # sai antes de chegar em 70
rsi_exit_threshold_sell: 35
rsi_exit_min_R: 0.7           # só sai cedo se já tem lucro razoável
```

**Impacto esperado**:
- Captura mais lucro em wins que iam direto pro TP cheio
- Evita reversões tardias que "comem" o lucro
- Pode reduzir avg_win se sair cedo demais — trade-off explícito

**Risco**: interage com TP/SL atual. Necessário backtest cuidadoso.

#### v6.4.0/F2 — Filtro de cor da vela do gatilho (princípio "3D" do trader) ⭐
**Convergência**: Trader explícito
**Arquivo**: `bot_liquidez.py::check_trigger()` — adicionar após validação de wick

```python
# Trader: "Em caso de compra, não pode comprar vela verde forte de continuação"

ENABLE_TRIGGER_COLOR_FILTER = CFG.get('enable_trigger_color_filter', False)
MAX_BODY_RATIO_OPPOSITE = CFG.get('max_body_ratio_opposite', 0.40)

if ENABLE_TRIGGER_COLOR_FILTER:
    candle_range = last['high'] - last['low']
    body = abs(last['close'] - last['open'])
    body_ratio = body / candle_range if candle_range > 0 else 1.0
    is_green = last['close'] > last['open']

    if z['type'] == 'SUPPORT':  # BUY
        # Bloquear se vela verde forte (continuação) — preferir doji ou vermelha com pavio
        if is_green and body_ratio > MAX_BODY_RATIO_OPPOSITE:
            return None, None
    else:  # SELL
        if not is_green and body_ratio > MAX_BODY_RATIO_OPPOSITE:
            return None, None
```

**Config**:
```yaml
enable_trigger_color_filter: false   # opt-in inicialmente
max_body_ratio_opposite: 0.40
```

**Impacto**: filtra velas de continuação forte que se disfarçam de pin bar. Aplicar com cuidado — pode reduzir muito o volume.

---

### 🔵 RELEASE v7.0.0 — "ICT Liquidity"

**Objetivo**: incorporar conceitos avançados ICT (untested levels, equal highs/lows, news embargo). Sprint maior, 1-2 semanas. Implementar APENAS após validar v6.2/6.3/6.4.

#### v7.0.0/F1 — Equal Highs/Lows como score bonus
- Adicionar +5pts quando o pavio do gatilho está dentro de 5 pips de **dois pivots equal recentes** (clean highs/lows)
- Modificação em `get_validated_zones()` pra detectar duplas próximas
- ICT: "double tops/bottoms = bull's eye for liquidity"

#### v7.0.0/F2 — Untested recent highs/lows
- Pivot novo (não tocado nas últimas N=20 velas) tem score maior que pivot já testado várias vezes
- Adicionar campo `times_tested` ao zone dict
- Default: pivot untested = +5pts; pivot já testado 2+ vezes = −5pts

#### v7.0.0/F3 — News embargo (NY 8-8:30 UTC = 13:00-13:30 MT5)
- Bloquear novas entradas 5min antes e 15min depois de eventos high-impact
- Requer integração com calendário econômico (FXStreet, ForexFactory API ou hardcoded)
- ICT: "Judas Swing acontece em news embargo"

#### v7.0.0/F4 — Threshold dinâmico por regime
- Em dias com range H1 > 80 pips até London open, exigir score 75+
- Em dias laterais (range < 40 pips), aceitar 60+
- `min_score_dynamic: true`

---

## Parte 5 — Protocolo de validação obrigatório

Antes de cada deploy de release:

### 5.1 Backtest contra logs históricos (23-27/04)

Implementar script `etl_backtest_signals.py`:

```python
# Pseudo-código:
# 1. Ler todos os APROVADOs dos 5 logs War Room
# 2. Reconstruir o contexto técnico (já está nos logs)
# 3. Aplicar a nova lógica (F1+F2+F3 da release atual)
# 4. Cruzar com P&L real do Supabase (já extraído)
# 5. Reportar:
#    - APROVADOS antes vs depois
#    - WINS filtrados (perda da edge)
#    - LOSSES filtrados (ganho)
#    - WR antes vs depois
#    - Expectancy antes vs depois
#    - P&L hipotético antes vs depois
```

**Critério de aprovação**:
- (LOSSES filtrados / WINS filtrados) > 1.5x
- Volume de trades não cai > 50%
- Expectancy melhora ou mantém

### 5.2 Forward test em demo

Após backtest passar:
- Rodar 3-5 dias em conta demo com a nova versão
- Comparar métricas vs baseline (semana anterior)
- Critério: WR > 50% e expectancy > 0

### 5.3 Métricas a observar SEMPRE

| Métrica | Baseline atual | Alarme se |
|---------|----------------|-----------|
| WR global | 50-60% | < 40% por 2 dias |
| Avg Win | $117 | cai > 30% |
| Avg Loss | $80 | sobe > 30% |
| R/R real | 1.5x | < 1.2x |
| Expectancy | +$15-30 | < $0 por 3 dias |
| Trades/dia | 5-15 | < 2 ou > 25 |
| Score médio aprovado | ~73 | foge > 10pts |
| WR por par | varia | algum par 0% por 5+ trades |
| WR por sessão | varia | sessão prime < 40% |

### 5.4 Rollback rápido

Cada release deve ser controlada por **feature flag no config.yaml**:
```yaml
# v6.2.0
enable_extension_filter: true
enable_session_subdivision: true
enable_extended_correlations: true

# v6.2.1
enable_smart_breakeven: false  # default OFF até validação

# v6.3.0
enable_macro_trend_score: false
enable_directional_cooldown: false
```

Permite desligar incrementos isolados sem precisar reverter código.

---

## Parte 6 — Sequência de execução recomendada

```
Semana 1 (28/04 - 04/05):
  Seg-Ter: Implementar v6.2.0 (F1+F2+F3 bundle)
  Qua: Backtest contra logs 23-27, ajustar parâmetros
  Qui-Sex: Forward test demo v6.2.0

Semana 2 (05/05 - 11/05):
  Seg: Análise resultado v6.2.0, decidir prosseguir ou ajustar
  Ter-Qua: Implementar v6.2.1 (smart breakeven), testar
  Qui-Sex: Iniciar v6.3.0 (Macro Trend Score)

Semana 3 (12/05 - 18/05):
  Seg-Ter: Finalizar v6.3.0 + validação
  Qua: Deploy v6.3.0 em produção
  Qui-Sex: Implementar v6.4.0 (RSI exit)

Semana 4 (19/05 - 25/05):
  Seg-Ter: Validação v6.4.0
  Qua-Sex: Iniciar planejamento v7.0.0 (ICT Liquidity sprint)
```

**Nota**: NÃO deployar 2 releases na mesma semana sem validação completa de cada uma. O sistema está em produção com capital real.

---

## Parte 7 — Decisões em aberto pra discussão

1. **Threshold de score após v6.3.0**: com Macro Trend pesando 18, score 65 ainda é o gate certo? Sugestão: aumentar pra 70 ou implementar threshold dinâmico.

2. **EURGBP**: análise dia 23 sugeriu suspender (3 losses score >85 em 5 trades), mas dia 27 EURGBP foi 1W/1L positivo. **Recomendação atual**: manter, observar 30 dias.

3. **Stop loss tightening**: trader sugeriu "stop colado ao pavio". Atualmente `stop_buffer_points: 50` (5 pips). Reduzir pra 30 (3 pips)? Trade-off: SL mais apertado = mais ejeções por wick microscópico.

4. **Lote dinâmico**: trader mencionou "saindo no lucro, a gente consegue entrar mais forte". Sugere lote escalado por equity? Atualmente `lot_size: 1.0` fixo. **Não priorizar agora** — adicionar variável de risco antes da estabilidade do scoring complica análise.

5. **Sumir com `JPY` permanente vs reavaliar?** Atualmente desativados por WR baixo. ICT enfatiza pares específicos por característica — talvez JPY funcione bem em horários específicos (sessão Tokyo). **Não priorizar** — focar em melhorar os 7 pares ativos primeiro.

---

## Parte 8 — Anexo: arquivos afetados por release

### v6.2.0
- `config.yaml` (3 keys novas)
- `squads/trade-liquidez-python/scripts/bot_liquidez.py` (`check_trigger`)
- `squads/trade-liquidez-python/scripts/auto_war_room.py` (`session_score_label`, `CORRELATED_PAIRS`)

### v6.2.1
- `config.yaml` (3 keys de breakeven)
- `squads/trade-liquidez-python/scripts/bot_liquidez.py` (`check_breakeven`)

### v6.3.0
- `config.yaml` (keys de macro + cooldown)
- `squads/trade-liquidez-python/scripts/auto_war_room.py` (`analyze_signal_strength`, `SCORE_MAX`)
- `squads/trade-liquidez-python/scripts/bot_liquidez.py` (estado em memória)
- `squads/trade-liquidez-python/scripts/system_logger.py` (`SCORE_MAX` atualizado pra display correto)

### v6.4.0
- `config.yaml` (keys de RSI exit + color filter)
- `squads/trade-liquidez-python/scripts/bot_liquidez.py` (nova função `check_rsi_exit`, filtro cor em `check_trigger`)

### v7.0.0
- Maior — provavelmente nova subpasta `scripts/ict/` pra módulos novos (equal_levels.py, untested_pivots.py, news_embargo.py)

---

## Parte 9 — Referências cruzadas

- **Análise quantitativa completa**: `assets/trade anal.md`
- **Trader call dia 24**: `assets/Trader_Analysis/Dia_24/README_Dia_24.md`
- **Trader call dia 27**: `assets/Trader_Analysis/Dia_27/README_Dia_27.md`
- **ICT Aula 1** (Trade Setup Elements): `assets/Trader_Lessons/Aula_1/README_Aula_1.md`
- **ICT Aula 2** (Smart Money + Daily Range Algo): `assets/Trader_Lessons/Aula_2/README_Aula_2.md`
- **ICT Aula 3** (Multi-timeframe + Mindset): `assets/Trader_Lessons/Aula_3/README_Aula_3.md`
- **Memória do operador**: `~/.claude/projects/.../memory/feedback_strategy_macro_trend.md` (regra inviolável: MA macro nunca como gate)

---

## Conclusão

A próxima bateria de incrementos é a primeira que **integra 3 fontes independentes que apontam pro mesmo lugar**: o sistema atual é tecnicamente sólido em M15 isolado, mas é **cego para regime macro e granularidade temporal**. A reforma proposta corrige isso em 4 releases incrementais sem destruir a edge atual.

**Maior alavanca**: v6.3.0 Macro Trend Score (validado por análise + trader + ICT).
**Menor risco**: v6.2.0 F2 (subdivisão de sessão — só altera scoring, não bloqueia).
**Maior controvérsia**: v6.2.1 (breakeven, com histórico de falha — exige tripla condição).

**Próximo passo recomendado**: começar implementação de v6.2.0 essa semana, com backtest obrigatório antes do deploy.

---

> _Documento gerado a partir da consolidação de análise quantitativa (3 dias operacionais), 2 calls com trader e 3 aulas da mentoria ICT. Mantido como fonte única para a roadmap v6.2 → v7.0._
