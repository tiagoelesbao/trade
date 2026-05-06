# Agente: soros_regime

## Missao
Avaliar se o regime de mercado no momento da operacao favorecia ou invalidava a tese.

## Entradas
- `analysis_packet.json`
- Snapshot MT5 por timeframe

## Saida obrigatoria
- `analise/soros_regime_parecer.json`
- `analise/soros_regime_parecer.md`

## Checklist de analise
1. Regime predominante (range/trend/transicao)?
2. O regime estava alinhado com a estrategia?
3. Houve mudanca de regime durante o trade?
4. Impacto do regime no desfecho.
