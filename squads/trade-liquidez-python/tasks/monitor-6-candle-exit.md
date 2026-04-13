# Task: Monitoramento de Saída por Tempo (6 Candles)
id: monitor-6-candle-exit
agent: risk-controller-taleb

## Objetivo
Gerenciar o tempo de exposição do trade, limitando o risco temporal.

## Regras de Monitoramento
1.  **Início:** Disparar contador assim que a ordem é executada (filled).
2.  **Bloco 1 (Candles 1-3):** 
    - Se atingir alvo parcial ou proteção (Breakeven), ajustar stop? (A definir pelo usuário).
3.  **Bloco 2 (Candles 4-6):** 
    - Manter operação até o alvo final de liquidez.
4.  **Gatilho de Expiração:** 
    - Se o trade completar **6 candles (30 minutos em M5)** e não tiver atingido o Alvo (TP) nem o Stop (SL):
    - **Ação:** Encerra a posição IMEDIATAMENTE a mercado (`mt5.ORDER_TYPE_BUY/SELL` direto).

## Saída
- Log de encerramento por tempo vs encerramento por alvo.
