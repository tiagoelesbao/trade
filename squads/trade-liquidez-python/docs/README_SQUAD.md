# 🏗️ Manual Mestre: Squad Trade-Liquidez-Python v4.0 Agêntica

Este ecossistema evoluiu de um robô de execução para uma **Operação de Trading Autônoma**. Agora, a estratégia de **Liquidez de Pavio** é governada por um conselho de agentes IA (Simons, Taleb, Druckenmiller) que validam cada entrada em tempo real.

---

## ⚖️ 1. Arquitetura de Governança AIOX

O sistema opera em um ciclo fechado de inteligência, execução e visualização:

1.  **Command Center (Frontend):** Monitoramento global em [trade-two-smoky.vercel.app](https://trade-two-smoky.vercel.app).
2.  **Trading Engine (Python):** Execução técnica e monitoramento de P&L no MT5.
3.  **War Room (AIOX Agents):** Camada de decisão que aprova ou veta sinais via Supabase.

### 🏛️ Diagrama de Orquestração v4.0
```mermaid
graph TD
    subgraph "CAMADA CLOUD (Vercel/Supabase)"
    A[Dashboard Live] <-->|Real-time| B[(Supabase DB)]
    H[AIOX Agents - War Room] <-->|Consenso/Voto| B
    end

    subgraph "CAMADA LOCAL (MetaTrader 5)"
    C[bot_liquidez.py] -->|1. Sinais Pendentes| B
    B -->|2. Aprovação/Veto| C
    C -->|3. Execução Limit| D[MT5 Terminal]
    C -->|4. Sincronia Visual| E[IndicadorLiquidez.ex5]
    end

    subgraph "CICLO AUTÔNOMO"
    G[FULL_START.bat] -->|Abertura| I[@analyst - Config Otimizada]
    I -->|Setup| C
    C -->|Auto-Shutdown| J[Meta Batida / Stop atingido]
    end
```

---

## 🗺️ 2. Mapeamento do Arquipélago (Estrutura de Arquivos)

| Pasta / Arquivo | Função Principal |
|---|---|
| 📂 **Raiz do Projeto** | |
| 📄 `FULL_START.bat` | **Orquestrador v3.0.** Prepara a sessão com IA e liga o ecossistema. |
| 📂 **squads/trade-liquidez-python/scripts/** | |
| 📄 `bot_liquidez.py` | **Motor Mestre.** Agora com P&L diário e Consenso Agêntico. |
| 📄 `diagnose_today.py` | **Auditoria Dinâmica.** Explica por que o robô não entrou em trades. |
| 📄 `clean_production_db.py` | **Manutenção.** Limpa registros de teste e heartbeats antigos. |
| 📄 `war_room_voter.py` | **Interface de Voto.** Ferramenta dos agentes para aprovar sinais. |
| 📄 `supabase_client.py` | **Sync de Dados.** Gerencia a comunicação com a Sala de Guerra. |
| 📄 `IndicadorLiquidez.mq5` | **Ponte Visual.** Desenha zonas e sinais em tempo real no MT5. |
| 📄 `config.yaml` | **Cérebro Estratégico.** Parâmetros de risco, metas e travas de IA. |

---

## 🚀 3. Motores de Performance (Avançado)

### 🧠 A. Sala de Guerra Agêntica (AIA)
O robô não opera mais sozinho. Ao detectar um sinal, ele o envia para a "nuvem" e aguarda até 30s.
- **Aprovação:** Se o contexto macro (tendência, notícias) for favorável, os agentes aprovam.
- **Veto:** Evita entradas contra a tendência ou em momentos de notícias de alto impacto.

### 💰 B. Gestão de Meta e Auto-Shutdown
O sistema possui consciência financeira.
- **Meta Diária:** Ao atingir o lucro alvo (ex: $100), o robô encerra a sessão e se desliga.
- **Proteção de Capital:** Limite de perda (Stop Loss Diário) encerra as operações para proteger o saldo.

---

## 🛠️ 4. Guia de Operação Autônoma

### 🚦 Iniciando a Sessão
Basta executar o arquivo mestre na raiz:
1.  Rode o **`FULL_START.bat`**.
2.  O `@analyst` fará a leitura de mercado e ajustará os filtros no `config.yaml`.
3.  O Dashboard e o Robô subirão automaticamente.

### 📊 Monitoramento
Acompanhe tudo pelo endpoint de vigilância:
- [https://trade-two-smoky.vercel.app/monitor](https://trade-two-smoky.vercel.app/monitor)
- Verifique o card **SALA DE GUERRA AGÊNTICA** para ver os julgamentos da IA em tempo real.

---

## 🧠 5. Configuração Dinâmica (`config.yaml`)

Principais chaves para ajuste fino:
*   `use_agent_consensus`: Ativa/Desativa o veto da IA.
*   `daily_profit_target`: Define quando o dia "acaba" com vitória.
*   `require_volume_momentum`: Flexibiliza a entrada em mercados lentos.

---
*Manual Mestre v4.0 Agêntica - Synkra AIOX Ecosystem*
