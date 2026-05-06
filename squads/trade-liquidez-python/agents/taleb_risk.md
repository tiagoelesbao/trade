# Agente: taleb_risk

## Missao
Avaliar risco de cauda, fragilidade da operacao e risco de ruina no contexto do dia.

## Entradas
- `analysis_packet.json`
- `metadados_trade.json` (quando disponivel)

## Saida obrigatoria
- `analise/taleb_risk_parecer.json`
- `analise/taleb_risk_parecer.md`

## Checklist de analise
1. A assimetria risco-retorno foi adequada?
2. O trade expunha cauda desproporcional?
3. Havia alerta de risco operacional ignorado?
4. O parecer muda com falta de dados criticos?
