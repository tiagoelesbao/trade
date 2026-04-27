● Análise da Call — Parecer Técnico Consolidado                                                                                                                                 
                                                                                                                                                                                
  Call de ~2h com um trader experiente. Ele passou 90% do tempo validando a lógica e 10% elogiando o trabalho do robô. Abaixo o que extraí, organizado por impacto estratégico.                                                                                                                                                                                 
  ---                                                                                                                                                                             1. A Tese Central do Trader                                                                                                                                                   
                                                                                                                                                                                  ▎ "O princípio da estratégia é o RSI. Só com o RSI a gente praticamente já consegue fazer grana. Depois dele vem só o pavio (rejeição) e a zona. O resto — Pin Bar, Sessão,     ▎ Volume — ele foi o próprio robô que adicionou sozinho."                                                                                                                     
                                                                                                                                                                                
  Essa frase (aos ~01:38:00) é a chave de leitura de tudo. A estratégia dele é mais enxuta do que a nossa v6.1. O bot empilhou 7 critérios no scoring; ele quer 3.

  ---
  2. Sugestões do Trader — Mapa Completo

  🔴 CRÍTICO — Remove ou inverte (impacto estratégico alto)

  ┌─────┬───────────────────────────────────────────────────────────────────┬─────────────┬─────────────────────────────────────────────────────────────────────────────────┐   
  │  #  │                             Sugestão                              │  Timestamp  │                                  Minha leitura                                  │   
  ├─────┼───────────────────────────────────────────────────────────────────┼─────────────┼─────────────────────────────────────────────────────────────────────────────────┤   
  │     │ Slope Guard (MA20 H1) está invertido para a estratégia — ela é    │             │ Procede. O bot valida trend_slope > 0 para BUY (tendência de alta), mas o setup │   
  │ A   │ contra-tendência (reversão) e o filtro só libera trades a favor   │ 01:00–01:13 │  é "reversão em zona" — comprar no fundo de uma queda. Hoje o filtro trava      │   
  │     │ da tendência de curto prazo                                       │             │ exatamente as melhores entradas.                                                │   
  ├─────┼───────────────────────────────────────────────────────────────────┼─────────────┼─────────────────────────────────────────────────────────────────────────────────┤   
  │ B   │ Slope neutro está bloqueando — deveria liberar                    │ 01:20       │ Procede. bot_liquidez.py:219 seta trend_slope = 0 e a condição trend_slope < 0  │   
  │     │                                                                   │             │ / > 0 rejeita neutros. Lateralização é contexto ideal de reversão.              │   
  ├─────┼───────────────────────────────────────────────────────────────────┼─────────────┼─────────────────────────────────────────────────────────────────────────────────┤   
  │ C   │ Remover filtro Pin Bar ("é critério visual de trader humano")     │ 01:34–01:37 │ Parcialmente. Pin Bar é redundante com Wick %: se wick_pct ≥ 0.50 já garante    │   
  │     │                                                                   │             │ corpo ≤ 50%. Pode ficar só como bônus, não como peso de 20pts.                  │   
  ├─────┼───────────────────────────────────────────────────────────────────┼─────────────┼─────────────────────────────────────────────────────────────────────────────────┤   
  │ D   │ Remover filtro Sessão ("não faz sentido, foi o bot que            │ 01:35       │ Procede em parte. Overlap London+NY é estatística real em FX, mas 15pts é peso  │   
  │     │ adicionou")                                                       │             │ alto. Redefinir como bônus menor (5pts) ou remover.                             │   
  ├─────┼───────────────────────────────────────────────────────────────────┼─────────────┼─────────────────────────────────────────────────────────────────────────────────┤   
  │ E   │ Remover filtro Color Reversal (vela oposta)                       │ 01:22       │ Procede. Atrasa a entrada e redunda com o critério de pavio + RSI extremo.      │   
  └─────┴───────────────────────────────────────────────────────────────────┴─────────────┴─────────────────────────────────────────────────────────────────────────────────┘   

  🟡 ALTERAÇÕES ESTRATÉGICAS NOVAS (feature)

  ┌─────┬────────────────────────────────────────────────────────────┬─────────────┬────────────────────────────────────────────────────────────────────────────────────────┐   
  │  #  │                          Sugestão                          │  Timestamp  │                                      Viabilidade                                       │   
  ├─────┼────────────────────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────────────────┤   
  │ F   │ Substituir MA20 H1 por MA100 + MA200 como filtro de        │ 01:51–01:54 │ Alta. Médias longas são "universais" (mais olhadas pelo mercado). Dão contexto, não    │   
  │     │ contexto macro                                             │             │ gatilho. Usar como informação adicional ou como segundo slope.                         │   
  ├─────┼────────────────────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────────────────┤   
  │     │ Plotar RSI visualmente no gráfico com linhas horizontais   │             │ Alta, mas escopo: MQL5. Não afeta lógica Python — é evolução do IndicadorLiquidez.mq5  │   
  │ G   │ (10/20/30/70/80/90) — inspirado em vídeo ASMR que ele      │ 00:00–00:50 │ para renderizar níveis de RSI projetados no chart. Vale como feature visual para ele   │   
  │     │ citou                                                      │             │ acompanhar.                                                                            │   
  ├─────┼────────────────────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────────────────┤   
  │ H   │ Testar RSI período 9 (clássico) em vez de 14               │ 00:01,      │ Média. Diferença nos dados: período 9 é mais reativo. Fácil de A/B testar.             │   
  │     │                                                            │ 00:24       │                                                                                        │   
  ├─────┼────────────────────────────────────────────────────────────┼─────────────┼────────────────────────────────────────────────────────────────────────────────────────┤   
  │ I   │ Inverter o Slope em vez de remover (se slope subindo →     │ 01:44–01:48 │ Média-alta. Promissor: transforma o que bloqueia em feature. Precisa backtest.         │   
  │     │ vender; se subindo em excesso → sinal de exaustão)         │             │                                                                                        │   
  └─────┴────────────────────────────────────────────────────────────┴─────────────┴────────────────────────────────────────────────────────────────────────────────────────┘   

  🟢 CONFIG — Revisar valores

  ┌─────┬─────────────────────────────────┬─────────────┬──────────────────────┬────────────────────────────────────────────────────────────────────┐
  │  #  │            Parâmetro            │ Valor atual │   Sugestão trader    │                             Comentário                             │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ J   │ lookback_zones                  │ 100         │ "entre 50-100" ou 17 │ Hoje 100 = ~25h de candles. Diminuir reduz ruído de zonas antigas. │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ K   │ min_displacement_candles        │ 7           │ 4-7                  │ 7 está bom, 4 gera mais zonas (menos confiáveis).                  │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ L   │ min_wick_pct                    │ 0.30        │ OK                   │ Aprovado explicitamente.                                           │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ M   │ cooldown_hours / proximity_pips │ 4h / 10pips │ OK                   │ Aprovado: "perfeito, essa parte aí".                               │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ N   │ stop_buffer_points              │ 15          │ OK                   │ Aprovado.                                                          │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ O   │ risk_reward_ratio               │ 1.5         │ OK                   │ Aprovado implicitamente.                                           │
  ├─────┼─────────────────────────────────┼─────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ P   │ Timeframe operacional           │ M15         │ Testar M30 ou M60    │ "M5/M15 pega muito ruído" — testar TFs mais altos.                 │
  └─────┴─────────────────────────────────┴─────────────┴──────────────────────┴────────────────────────────────────────────────────────────────────┘

  ✅ APROVADOS sem mexer

  - Vela fechada (não a atual) ✓
  - Zona one-shot (cada zona gera 1 sinal) ✓
  - Zona validada por 7 velas de displacement ✓
  - Cooldown via banco + proximity ✓
  - Stop 15pts além do pavio ✓
  - TP = 1.5x SL ✓

  ---
  3. Validação Técnica das Sugestões

  Cruzando cada ponto com o código atual:

  ┌─────┬──────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────┬───────────────────────────────┐   
  │  #  │                        Onde no código                        │                              Mudança                               │             Risco             │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ A+B │ bot_liquidez.py:210-222 (check_trigger)                      │ Inverter sinal de trend_slope > 0 ou desligar use_trend_filter;    │ Baixo — é só config.yaml      │   
  │     │                                                              │ permitir neutro                                                    │                               │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ C   │ auto_war_room.py:176-179 + docs                              │ Remover pin_bar do scoring OU reduzir peso para 5pts               │ Baixo                         │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ D   │ auto_war_room.py:87-93 + auto_war_room.py:201                │ Remover session ou reduzir peso                                    │ Baixo                         │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ E   │ bot_liquidez.py:241, 263 +                                   │ require_color_reversal: false                                      │ Zero — já é toggle            │   
  │     │ config.yaml:require_color_reversal                           │                                                                    │                               │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ F   │ bot_liquidez.py:209-222 (calc_slope)                         │ Adicionar cálculo MA100 + MA200 H1/H4; novo filtro use_macro_trend │ Médio — precisa backtest      │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ G   │ squads/trade-liquidez-python/scripts/IndicadorLiquidez.mq5   │ Exportar níveis RSI para CSV + indicador desenha linhas            │ Médio — MQL5                  │   
  │     │                                                              │ horizontais                                                        │                               │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ H   │ bot_liquidez.py:153 / auto_war_room.py:72                    │ calculate_rsi(series, period=9)                                    │ Baixo — trivial               │   
  ├─────┼──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┼───────────────────────────────┤   
  │ I   │ bot_liquidez.py:214-219                                      │ Inverter lógica de slope (BUY quando slope<0)                      │ Alto — precisa backtest       │   
  │     │                                                              │                                                                    │ obrigatório                   │   
  └─────┴──────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────┴───────────────────────────────┘   

  Importante: boa parte das alterações já é toggle em config.yaml. use_trend_filter: false + require_color_reversal: false cobre A+B+E sem mudar código.

  ---
  4. Validação das Minhas Sugestões Anteriores — Ainda Válidas?

  ┌────────────────────────────────────┬─────────────────────────────────────────────────────────────┐
  │         Sugestão anterior          │                      Status após call                       │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ Timezone UTC-aware                 │ ✅ Continua crítica, independente                           │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ except: silencioso no lifecycle    │ ✅ Continua crítica                                         │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ elapsed_candles real via MT5       │ ✅ Continua                                                 │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ Atualizar strategy.md (60 → 55)    │ ⚠️ Precisa atualizar MUITO mais agora (v7.0)                │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ Centralizar scoring constants      │ ✅ Continua, melhor se feito junto com a reforma do scoring │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ War Room checar approved pendentes │ ✅ Continua                                                 │
  ├────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
  │ Remover send_order() dead code     │ ✅ Continua                                                 │
  └────────────────────────────────────┴─────────────────────────────────────────────────────────────┘

  Nenhuma foi invalidada. Algumas (scoring constants, docs) casam bem com a reforma estratégica — é uma janela natural para fazer junto.

  ---
  5. Próximos Passos — Roadmap Integrado

  Proposta em 4 fases. Cada fase é um incremento testável, não um big-bang.

  🔧 FASE 1 — Correções técnicas urgentes (2-3h)

  Coisas que não mexem em estratégia, apenas em robustez:
  1. Timezone UTC-aware nas queries de check_cooldown e histórico WR
  2. Logar falhas do TradeLifecycleManager via SystemLogger (sem mudar interface)
  3. Remover send_order() dead code
  4. Atualizar strategy.md e FUNCIONAMENTO_COMPLETO_BOT.md (60 → 55, remover menções v5.x)

  ⚙️ FASE 2 — Toggle-only (1h + observação)

  Em config.yaml, apenas:
  use_trend_filter: false        # remove slope H1 (item A+B)
  require_color_reversal: false  # remove reversão cor (item E)
  E rodar em paper trading por 2-3 dias para comparar frequência/qualidade de sinais. Zero linha de código alterada — só flipar toggles que já existem.

  🧪 FASE 3 — Refatoração v7.0 (1-2 semanas)

  Branch strategy-v7:
  1. Novo scoring enxuto (4 critérios, 100 pts): Wick 35, RSI 35, Macro Trend 20 (MA100/200), Histórico 10
  2. Adicionar MA100 + MA200 H1 (item F)
  3. Testar RSI período 9 (item H) — A/B
  4. Testar TF M30 como operacional (item P)
  5. Backtest comparativo v6.1 vs v7.0 com os trades históricos + dados sintéticos
  6. Centralizar SCORE_MAX/LABELS/MIN_SCORE em scoring_config.py

  🎨 FASE 4 — Visualização RSI no MT5 (3-5 dias)

  Evolução do IndicadorLiquidez.mq5:
  1. Bot exporta níveis de RSI (current, 30, 40, 60, 70, 80, 90) projetados no preço do chart
  2. Indicador desenha como linhas horizontais coloridas (igual ao vídeo que o trader viu)
  3. Destaque quando preço está em zona crítica (≤30 ou ≥70)

  Esta fase é visual/UX — não muda lógica de trading, mas é a primeira coisa que o trader vai abrir na próxima call com ele.

  🔬 FASE 5 — Inversão experimental do Slope (item I, opcional)

  Só depois da Fase 3 validar que a versão sem slope funciona. Se v7.0 passa nos backtests, tentar Slope invertido como +pontos de confluência (não como gate bloqueante).      
  Requer backtest dedicado.

  ---
  6. Recomendação de Priorização

  Se você me perguntasse o que fazer na segunda-feira, eu diria: Fase 1 + Fase 2 no mesmo dia. Custa 3h e já endereça os dois problemas mais críticos da call (slope invertido +
   reversão de cor atrasando entrada) sem escrever uma linha nova. Em paralelo, começar estudo técnico da Fase 4 (RSI plotado) — é a promessa visual que mais vai agradar o     
  trader na próxima call.

  Fase 3 (v7.0) deve ter backtest comparativo como gate obrigatório — não comitar sem comparar P&L expectancy com v6.1 em janela ≥ 3 meses.

● ---                       
  Resumo de 2 linhas: O trader validou a base da estratégia (zona + RSI + wick), mas quer eliminar 3 filtros que o sistema acumulou sozinho (Slope, Pin Bar, Color Reversal — o
  Slope inclusive está invertido para contra-tendência) e adicionar MA100/MA200 como contexto macro + RSI visual no chart. Dá pra testar 70% das mudanças via toggle no
  config.yaml já na segunda-feira, antes de qualquer refatoração v7.0.                                                                                                               
  Quer que eu comece pela Fase 1+2 (correções técnicas + toggles) ou prefere debater o scoring enxuto da Fase 3 antes?                                                          
