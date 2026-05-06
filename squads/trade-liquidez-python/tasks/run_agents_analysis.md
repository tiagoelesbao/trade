# Task: run_agents_analysis

## Objetivo
Executar pareceres dos agentes no modo `quick` ou `full`.

## Entradas
- `analysis_packet.json`
- `mode`

## Saidas
- `analise/*_parecer.json`
- `analise/*_parecer.md`
- `analise/consenso_divergencia.json`

## Criterio de conclusao
- Quorum valido conforme modo:
  - `quick`: minimo 4 de 5 agentes com status `ok|partial`
  - `full`: minimo 7 de 9 agentes com status `ok|partial`
