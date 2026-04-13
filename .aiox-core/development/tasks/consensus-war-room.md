# 🛡️ Task: Sala de Guerra Agêntica (Consenso de Trade)
**Agentes:** @analyst (Simons + Taleb)
**Objetivo:** Validar sinais técnicos do robô Python antes da execução real.

## 📋 Fluxo de Decisão
1. [ ] **Monitoramento:** Observar a tabela `signals_liquidez` por registros com `status: awaiting_consensus`.
2. [ ] **Análise Simons (Quant):** 
   - Verificar tendência no H4. Se o sinal for contra a tendência majoritária -> **Veto**.
   - Verificar RSI M15. Se estiver sobrecomprado/sobrevendido demais -> **Cuidado**.
3. [ ] **Análise Taleb (Risco):**
   - Verificar calendário econômico imediato. Notícia em < 15 min? -> **Veto**.
4. [ ] **Veredito:**
   - Consenso positivo -> Atualizar sinal para `status: approved`.
   - Consenso negativo -> Atualizar sinal para `status: rejected`.

## 🛠️ Ferramentas
- `supabase` CLI ou script Python de interface.
- `context7` para notícias em tempo real.

## 🎯 Resultado Esperado
Redução drástica de "falsos rompidos" e entradas contra a tendência macro, aumentando o Win Rate da sessão.
