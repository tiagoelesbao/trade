# Plano de Estabilização de Performance e Limpeza de Dados

Este plano visa resolver a preocupação do usuário sobre a falta de trades no dia de hoje e limpar os resíduos de testes realizados para garantir a integridade das métricas do robô.

## User Review Required

> [!IMPORTANT]
> A falta de trades hoje parece estar ligada a filtros rígidos de **Volume** e **Reversão de Cor**. Vou mover esses parâmetros para o `config.yaml` para que você possa ajustá-los sem mexer no código.

## Proposed Changes

### 1. Diagnóstico e Auditoria
#### [NEW] [diagnose_today.py](file:///C:/Users/Pichau/Desktop/trade/squads/trade-liquidez-python/scripts/diagnose_today.py)
Um script que baixa os dados de hoje e imprime um relatório detalhado de cada candle, indicando qual filtro exatamente barrou a entrada (Volume, Cor ou Pavio).

### 2. Refatoração de Filtros (Flexibilidade)
#### [MODIFY] [config.yaml](file:///C:/Users/Pichau/Desktop/trade/squads/trade-liquidez-python/config.yaml)
Adição de novos parâmetros:
- `require_volume_momentum`: Se true, exige volume maior que o candle anterior.
- `require_color_reversal`: Se true, exige fechamento de cor oposta à anterior.
- `min_wick_pct`: Percentual mínimo de pavio (atualmente fixo em 0.30).
- `max_wick_pct`: Percentual máximo de pavio (atualmente fixo em 0.70).

#### [MODIFY] [bot_liquidez.py](file:///C:/Users/Pichau/Desktop/trade/squads/trade-liquidez-python/scripts/bot_liquidez.py)
Atualização da função `check_m5_trigger` para ler os novos parâmetros do `config.yaml` em vez de usar valores fixos.

### 3. Limpeza de Dados
#### [NEW] [clean_production_db.py](file:///C:/Users/Pichau/Desktop/trade/squads/trade-liquidez-python/scripts/clean_production_db.py)
Script corrigido para usar as chaves corretas do `.env` e remover todos os registros com "SIMULADO" e heartbeats de teste.

## Verification Plan

### Manual Verification
1.  **Auditoria Operacional:** Executar `python scripts/diagnose_today.py` e apresentar o relatório ao usuário para explicar o silêncio do robô hoje.
2.  **Teste de Limpeza:** Executar o script de limpeza e verificar via log se os registros foram removidos.
3.  **Teste de Configuração:** Alterar `require_volume_momentum` para `false` no config e rodar o diagnóstico novamente para ver se novos sinais seriam aceitos.
