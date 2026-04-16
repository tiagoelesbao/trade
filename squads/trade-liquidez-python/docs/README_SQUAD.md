# 🏗️ Manual Mestre: Squad Trade-Liquidez-Python v4.1 Agêntica

Este ecossistema evoluiu para uma **Operação de Trading de Alta Fidelidade**. A estratégia de **Liquidez de Pavio** agora é totalmente autônoma, com execução imediata (Market) ou inteligente (Limit), governada por um conselho de agentes IA que reportam resultados reais e opiniões estruturadas ao Dashboard.

---

## ⚖️ 1. Arquitetura de Governança AIOX

O sistema opera em um ciclo fechado de inteligência, execução e visualização em tempo real:

1.  **Command Center (Frontend):** Monitoramento global em [trade-two-smoky.vercel.app](https://trade-two-smoky.vercel.app).
2.  **Trading Engine (Python):** Execução técnica (MARKET/LIMIT) e reporte de P&L real ao fechar ordens no MT5.
3.  **War Room (AIOX Agents):** Camada de decisão que gera opiniões (Simons, Taleb, Druckenmiller) e valida sinais via Supabase.

### 🏛️ Diagrama de Orquestração v4.1
```mermaid
graph TD
    subgraph "CAMADA CLOUD (Vercel/Supabase)"
    A[Dashboard v4.1] <-->|Real-time| B[(Supabase DB)]
    H[auto_war_room.py] <-->|Opiniões Reais| B
    end

    subgraph "CAMADA LOCAL (MetaTrader 5)"
    C[bot_liquidez.py] -->|1. Sinal / PNL Real| B
    B -->|2. Consenso/Voto| C
    C -->|3. Execução MARKET/LIMIT| D[MT5 Terminal]
    C -->|4. Sincronia Visual| E[IndicadorLiquidez.ex5]
    end

    subgraph "CICLO AUTÔNOMO"
    G[FULL_START.bat] -->|Fase 0: Limpeza| K[clean_db.py]
    G -->|Fase 1: Setup| I[@analyst - Config Otimizada]
    I -->|Setup| C
    C -->|Auto-Shutdown| J[Meta Batida / Stop atingido]
    end
```

---

## 🗺️ 2. Mapeamento do Arquipélago (Estrutura de Arquivos)

| Pasta / Arquivo | Função Principal |
|---|---|
| 📂 **Raiz do Projeto** | |
| 📄 `FULL_START.bat` | **Orquestrador v4.1.** Orquestra limpeza, diagnóstico e boot de todos os módulos. |
| 📂 **squads/trade-liquidez-python/scripts/** | |
| 📄 `bot_liquidez.py` | **Motor Mestre.** Execução dual (Market/Limit) e reporte de PNL real. |
| 📄 `auto_war_room.py` | **General de Guerra.** Gera opiniões estruturadas dos agentes IA. |
| 📄 `supabase_client.py` | **Sync de Dados.** Gerencia o ciclo de vida do sinal (Awaiting -> Closed). |
| 📄 `clean_db.py` | **Sanidade.** Limpa dados de teste para iniciar o dia com métricas zeradas. |
| 📄 `diagnose_today.py` | **Auditoria.** Explica por que o robô não entrou em trades (filtros de volume/wick). |
| 📄 `fix_signal.py` | **Utilitário.** Corrige retroativamente direção ou opiniões de sinais. |
| 📄 `config.yaml` | **Cérebro Estratégico.** Parâmetros de risco, modo de execução e metas. |

---

## 🚀 3. Motores de Performance (Avançado)

### 🧠 A. Sala de Guerra Agêntica (Real Opinions)
O robô envia o sinal e o `auto_war_room.py` gera sentimentos reais:
- **Jim Simons:** Focado em exaustão estatística e Delta.
- **Druckenmiller:** Focado em estrutura de liquidez e H1.
- **Nassim Taleb:** Focado em risco de cauda e convexidade.
- **Status VALIDADO:** Substitui o rótulo antigo "ALTA" para evitar confusão em sinais de venda.

### ⚡ B. Modos de Execução (`execution_mode`)
- **MARKET:** Execução imediata no gatilho. Ideal para mercados rápidos para não "perder o bonde".
- **LIMIT:** Aguarda um recuo (retracement) para pegar um preço melhor. Mais defensivo.

### 💰 C. Fidelidade de P&L
O sistema não usa mais estimativas. O `bot_liquidez.py` lê o histórico de `deals` do MT5 e envia o lucro/prejuízo exato (incluindo taxas e swap) para o Dashboard.

---

## 🛠️ 4. Guia de Operação Autônoma

### 🚦 Iniciando a Sessão
1.  Rode o **`FULL_START.bat`**.
2.  O sistema limpará os testes, ajustará o `config.yaml` e abrirá as 4 janelas de controle.

### 📊 Monitoramento e Endpoints
- **Painel Ao Vivo:** Visão geral com métricas de PNL real e bot status.
- **Monitor Zonas H1:** Foco na saúde técnica e Sala de Guerra ativa.
- **Histórico:** Log de todos os sinais capturados.
- **Gatilhos (Novo):** Detalhamento técnico exclusivo de ordens **executadas** e performance por trade.

---

## 🧠 5. Configuração Dinâmica (`config.yaml`)

*   `execution_mode`: Alterne entre `market` e `limit`.
*   `daily_profit_target`: Meta financeira para o auto-shutdown.
*   `use_agent_consensus`: Ativa o veto/aprovação da Sala de Guerra.

---
*Manual Mestre v4.1 Agêntica - Synkra AIOX Ecosystem*
