# Relatório Executivo: Market Replay Engine (Walk-Forward)

**Ativo:** EURUSD | **Gráfico:** M5 | **Lote:** 1.0 | **Amostragem Cega:** ~7.500 candles
> Teste com isolamento absoluto (zero futuro acessível). Os parâmetros usados espelham exatamente a operação live com `config.yaml`.

## Resumo Financeiro (Validação Rigorosa)
- **Saldo Bruto Acumulado:** $193.40
- **Taxa de Acerto (Win Rate):** 47.06%
- **Total de Trades:** 17
- **Take Profits / Gains:** 8
- **Stop Loss (Cheio):** 9
- **Breakevens Acionados (0x):** 0

## Detalhamento de Entradas
| Data/Hora Entrada | Direção | Preço | PNL | Motivo de Saída | Proteção 0x ativada |
|---|---|---|---|---|---|
| 2026-03-06 13:55:00+00:00 | BUY | 1.15652 | $-13.40 | Stop Loss | Não |
| 2026-03-09 00:45:00+00:00 | BUY | 1.15331 | $10.00 | Breakeven | Sim |
| 2026-03-11 13:55:00+00:00 | BUY | 1.15976 | $-33.80 | Stop Loss | Não |
| 2026-03-12 15:45:00+00:00 | BUY | 1.15252 | $10.00 | Breakeven | Sim |
| 2026-03-16 02:50:00+00:00 | SELL | 1.14518 | $-13.40 | Stop Loss | Não |
| 2026-03-16 12:50:00+00:00 | SELL | 1.14712 | $-14.00 | Stop Loss | Não |
| 2026-03-17 11:10:00+00:00 | SELL | 1.15140 | $-18.80 | Stop Loss | Não |
| 2026-03-17 14:05:00+00:00 | SELL | 1.15153 | $-18.20 | Stop Loss | Não |
| 2026-03-19 15:50:00+00:00 | SELL | 1.14999 | $-51.20 | Stop Loss | Não |
| 2026-03-24 15:45:00+00:00 | BUY | 1.15689 | $102.00 | Take Profit | Não |
| 2026-03-25 02:50:00+00:00 | SELL | 1.16291 | $37.20 | Take Profit | Não |
| 2026-03-25 16:45:00+00:00 | BUY | 1.15781 | $74.00 | Take Profit | Não |
| 2026-03-26 08:40:00+00:00 | BUY | 1.15534 | $69.60 | Take Profit | Não |
| 2026-03-26 09:30:00+00:00 | BUY | 1.15566 | $-31.40 | Stop Loss | Não |
| 2026-03-27 12:10:00+00:00 | BUY | 1.15183 | $27.60 | Take Profit | Não |
| 2026-03-30 12:30:00+00:00 | BUY | 1.14858 | $71.20 | Take Profit | Não |
| 2026-04-10 13:50:00+00:00 | SELL | 1.17144 | $-14.00 | Stop Loss | Não |
