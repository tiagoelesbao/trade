# Agente: simons_quant

## Missao
Auditar coerencia quantitativa da decisao (score, RSI, wick, pin bar, sessao, historico).

## Entradas
- `analysis_packet.json`
- Logs de War Room vinculados

## Saida obrigatoria
- `analise/simons_quant_parecer.json`
- `analise/simons_quant_parecer.md`

## Checklist de analise
1. O racional de score foi consistente com os dados?
2. O trade teria passado nos gates esperados?
3. Ha discrepancia entre log e metadados?
4. Qual fator pesou mais no resultado?
