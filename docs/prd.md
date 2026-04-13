# Trade Liquidez Python - Brownfield Enhancement PRD (Improved)

**Data:** 11 de Abril de 2026
**Autor:** @architect (Aria) - Revisão Técnica YOLO
**Status:** Aprovado para Implementação (Arquitetura Validada)

---

## 1. Introdução e Contexto do Projeto

### 1.1 Visão Geral
Integração de um motor de liquidez/trading Python (`trade-liquidez-python`) com o framework AIOX. O foco é transformar scripts isolados em um serviço orquestrado por agentes inteligentes, garantindo baixa latência e alta observabilidade.

### 1.2 Escopo do Reforço
- **Objetivos Técnicos:**
  - Reduzir overhead de inicialização do Python via suporte a Daemon.
  - Padronizar observabilidade via logs estruturados (JSONL).
  - Garantir segurança operacional via Sanity Checks pré-execução.

---

## 2. Requisitos

### 2.1 Requisitos Funcionais (FR)
- **FR1:** Monitoramento de status em tempo real via telemetria de logs.
- **FR2:** Execução de comandos parametrizados (volume, pair, strategy).
- **FR3:** Registro centralizado em `.aiox/logs/python-liquidity.jsonl`.

### 2.2 Requisitos Não-Funcionais (NFR)
- **NFR1:** Não-bloqueio do loop principal AIOX (Heartbeat < 5s).
- **NFR2:** **Timeout de Execução:** Limite máximo de 30s para chamadas síncronas; processos de longa duração devem reportar status a cada 10s.
- **NFR3:** Baixa latência: Tempo de resposta do comando inicial < 200ms após o setup do ambiente.

### 2.3 Requisitos de Compatibilidade (CR)
- **CR1:** Esquema `task-v3-schema.json`.
- **CR2:** **Sanity Check:** O motor Python deve abortar imediatamente com erro claro se variáveis críticas do `.env` estiverem ausentes.
- **CR3:** Compatibilidade estrita com Windows 11 (Ambiente de Execução).

---

## 3. Restrições Técnicas e Integração

### 3.1 Pilha Tecnológica
- **Orquestração:** AIOX (TS/Node).
- **Motor:** Python 3.x (Venv obrigatório).
- **Comunicação:** Invocação via Shell (Sidecar) com suporte a **Daemon Mode** para operações de alta frequência.

### 3.2 Estratégia de Integração
- **Logs Estruturados:** O Python deve emitir logs exclusivamente em formato **JSONL**.
- **Configuração:** Validação rigorosa de tipos no carregamento do `.env`.
- **Erro Handling:** Mapeamento de Exit Codes (ex: 0=Success, 1=ConfigError, 2=APIError, 3=RuntimeError).

---

## 4. Estrutura de Epic e Stories

### Epic 1: Integração de Motor de Liquidez Python no AIOX

#### Story 1.1: Setup e Sanity Check de Ambiente
- **Ação:** Configurar `venv`, `requirements.txt` e script de validação de `.env`.
- **IV:** O motor falha graciosamente se uma chave de API estiver faltando.

#### Story 1.2: Task Mapping e Command Dispatcher
- **Ação:** Criar tarefas `.md` que aceitam flags de timeout e modo daemon.
- **IV:** Teste de latência do comando `*ping-liquidity` < 100ms.

#### Story 1.3: Observabilidade JSONL
- **Ação:** Implementar logger JSONL no Python e coletor no AIOX.
- **IV:** O Agente QA analisa o `python-liquidity.jsonl` e extrai métricas de trade automaticamente.

---

## 5. Avaliação de Riscos (Atualizada)
- **Latência de Startup:** Mitigado via Daemon Mode opcional.
- **Drift de Dados:** Mitigado via logs estruturados JSONL para auditoria constante.
- **Vazamento de CPU:** Mitigado via timeouts rigorosos impostos pelo AIOX.
