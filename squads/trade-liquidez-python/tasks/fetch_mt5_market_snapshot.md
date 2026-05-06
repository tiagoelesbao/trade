# Task: fetch_mt5_market_snapshot

## Objetivo
Coletar contexto real de mercado no MT5 para cada trade.

## Entradas
- `trade_time_resolution.json`

## Saidas por trade
- `dados/market_snapshot_m1.csv`
- `dados/market_snapshot_m5.csv`
- `dados/market_snapshot_m15.csv`
- `dados/market_snapshot_h1.csv`
- `dados/market_snapshot_meta.json`

## Criterio de conclusao
- M15 e H1 disponiveis ou status parcial formalizado.
