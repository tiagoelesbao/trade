# Task: Validação de Contexto H1
id: validate-h1-context
agent: macro-context-agent

## Objetivo
Identificar e validar zonas de Suporte e Resistência no gráfico de 1 Hora (H1) que demonstrem força institucional.

## Lógica de Validação (Lookback)
1.  **Identificação de Extremidade:** Localizar topos e fundos recentes em H1.
2.  **Regra dos 7 Candles:** Uma zona só é considerada "Validada" se, após o toque nela, o preço se deslocou na direção oposta por no mínimo **7 candles** consecutivos ou predominantes.
3.  **Saída:** Lista de preços (High/Low) que representam zonas ativas para o monitoramento em M5.

## Requisitos de Dados
- Timeframe: H1
- Ativo: WIN$ (Mini Índice)
- Bibliotecas: Pandas para análise de séries temporais.
