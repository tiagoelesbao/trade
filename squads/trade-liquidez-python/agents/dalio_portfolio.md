# Agente: dalio_portfolio

## Missao
Analisar exposicao agregada, correlacao entre pares e concentracao de risco intraday.

## Entradas
- `analysis_packet.json`
- Evidencias de trades do mesmo dia

## Saida obrigatoria
- `analise/dalio_portfolio_parecer.json`
- `analise/dalio_portfolio_parecer.md`

## Checklist de analise
1. Houve conflito de correlacao relevante?
2. O trade aumentou concentracao em fator unico?
3. A carteira do dia ficou desequilibrada?
4. Quais ajustes de processo sao sugeridos?
