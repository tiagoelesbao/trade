# Task: Envio de Ordem Limitada
id: send-order-limit
agent: execution-manager

## Objetivo
Executar a entrada técnica via API MetaTrader 5 usando ordens pendentes.

## Lógica de Execução
1.  **Conexão:** Verificar se `mt5.initialize()` está ativo.
2.  **Tipo de Ordem:** 
    - Se venda: `mt5.ORDER_TYPE_SELL_LIMIT`
    - Se compra: `mt5.ORDER_TYPE_BUY_LIMIT`
3.  **Parâmetros:**
    - `price`: Calculado no 50% do pavio.
    - `sl`: Stop Loss no extremo do pavio.
    - `tp`: Take Profit no alvo de liquidez.
    - `magic`: Identificador único do robô.
    - `comment`: "Candle-a-Candle Liquidez".

## Tratamento de Erros
- Se a ordem não for preenchida em até X segundos (opcional), cancelar? (Seguir regra de 6 candles).
- Validar se há margem disponível antes do envio.
