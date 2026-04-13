# 📈 Task: Preparação de Sessão Quantitativa
**Agente:** @analyst (Simons / Druckenmiller)
**Objetivo:** Analisar o mercado de ontem e ajustar o `config.yaml` para a sessão de hoje.

## 📋 Checklist de Abertura
1. [ ] **Auditoria de Ontem:** Executar `python squads/trade-liquidez-python/scripts/diagnose_today.py` com o contexto de ontem.
2. [ ] **Volatilidade:** Verificar se o mercado está em tendência forte ou lateral.
   - Tendência Forte -> Exigir `require_color_reversal: true`.
   - Lateralização -> Pode relaxar filtros de volume.
3. [ ] **Configuração Dinâmica:** Atualizar o `config.yaml` com os novos parâmetros.
4. [ ] **Log de Plano:** Gerar `docs/sessions/daily-plan-YYYY-MM-DD.md`.

## 🛠️ Scripts Relacionados
- `squads/trade-liquidez-python/scripts/diagnose_today.py`
- `squads/trade-liquidez-python/config.yaml`

## 🎯 Resultado Esperado
O sistema deve iniciar a sessão com o `config.yaml` otimizado para o cenário atual, maximizando as chances de bater a meta de lucro de $100 definida no config.
