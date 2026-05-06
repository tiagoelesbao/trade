# Task: build_trade_analysis_packet

## Objetivo
Consolidar dados de cada trade em pacote unico para agentes.

## Entradas
- `trade_catalog.json`
- `trade_warroom_links.json`
- `trade_entry_links.json`
- `trade_time_resolution.json`
- `market_snapshot_meta_*.json`

## Saida
- `analysis_packet.json`

## Criterio de conclusao
- Pacote por trade com identidade, evidencias, referencias de logs e dados de mercado.
