# Task: pair_trade_with_warroom_logs

## Objetivo
Vincular cada trade aos eventos de aprovacao/rejeicao da War Room.

## Entradas
- `trade_catalog.json`
- `logs_index.json` (tipo warroom)

## Saidas
- `trade_warroom_links.json`

## Criterio de conclusao
- Todos os trades com tentativa de pareamento documentada e `match_confidence`.
