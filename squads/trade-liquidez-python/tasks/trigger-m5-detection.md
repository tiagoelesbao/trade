# Task: Detecção de Gatilho M5
id: trigger-m5-detection
agent: quant-trigger-analyst

## Objetivo
Identificar o padrão de "Violinação" e rejeição em M5 dentro das zonas validadas de H1.

## Checklist de Gatilho (Boolean)
1.  **Localização:** `Preço_Atual` está tocando ou "violinando" uma `Zona_H1_Validada`?
2.  **Violinação:** O candle atual ultrapassou a máxima/mínima da zona e está retornando?
3.  **Volume:** `Volume_Candle_Atual > Volume_Candle_Anterior`?
4.  **Anatomia:** 
    - `Pavio_Rejeição` deve ser entre **30% e 70%** do tamanho total do candle.
    - O candle atual deve ter **cor oposta** ao anterior (reversão confirmada).
5.  **Corpo:** Ignorar se o candle fechar como "Breakout" (corpo cheio rompendo a zona com pouco pavio).

## Saída para Execução
- `Preço_Entrada`: 50% do pavio de rejeição (Order Limit).
- `Preço_Stop`: Extremo do pavio + 1 tick de segurança.
- `Preço_Alvo`: Preço de abertura do candle de força anterior (Liquidez).
