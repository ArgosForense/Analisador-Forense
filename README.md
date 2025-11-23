# 🛡️ Argos Forense - Sistema de Monitoramento e Gestão de Acesso

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react)

## 📖 Sobre o Projeto

  O **Argos Forense** é uma solução SaaS voltada para a área de análise forense digital e operações de segurança (SOC). O sistema oferecerá suporte à detecção de atividades suspeitas, condução de investigações e geração de relatórios de conformidade.

  A solução foi projetada para atender empresas com múltiplos clientes, fornecendo uma interface de monitoramento interativo baseada em regras heurísticas e integração com listas de IPs maliciosos.

---
## 🏗️ Arquitetura de Software

  O projeto adota uma **Arquitetura em Camadas com Domínio Equilibrado (evitando domínio rico e anêmico)** para o backend de gestão, garantindo a separação de responsabilidades e facilitando a escalabilidade e manutenção do código. 
  O sistema é containerizado via Docker para garantir portabilidade entre ambientes (Windows, Linux, macOS).

### Estrutura de Camadas (API Gestão)
1.  **Camada de Apresentação (Controllers/Routers):** Gerencia a entrada e saída de dados (HTTP), validação de esquemas (Pydantic) e roteamento, mantendo-se livre de regras de negócio.
2.  **Camada de Modelo (Domain Layer):** As entidades (`models`) não são apenas estruturas de dados; elas encapsulam regras de negócio e comportamentos intrínsecos ao seu estado
    * (Ex.: um `Usuario` sabe como se ativar/desativar). Isso garante alta coesão e protege a integridade dos dados.
    * (Obs.: **Schemas** Definem os contratos de dados do sistema.
3.  **Camada de Serviço (Business Layer):** Responsável pela orquestração de fluxos de trabalho complexos, interação com a infraestrutura (banco de dados, e-mail) e regras que envolvem múltiplas entidades. Ela coordena as ações, mas delega a lógica de estado para os modelos.
4.  **Camada de Acesso a Dados (Repositories):** Abstrai a complexidade das consultas ao banco de dados (SQLAlchemy), fornecendo métodos limpos para que os serviços busquem e persistam as entidades.


#### Estrutura de Diretórios

```text
api_gestao/
├── 📂 app/
│   ├── 📂 models/          # Entidades com lógica de negócio (Domínio Equilibrado)
│   ├── 📂 services/        # Orquestração de fluxos e regras de aplicação
│   ├── 📂 repositories/    # Abstração de acesso ao banco de dados
│   ├── 📂 controllers/     # Lógica de controle e resposta
│   ├── 📂 api/routes/      # Definição de endpoints
│   └── 📂 schemas/         # Contratos de dados (DTOs)
```
---

## 🚀 Tecnologias Utilizadas

O projeto foi construído utilizando uma stack moderna e robusta, visando escalabilidade e facilidade de manutenção.

| Tecnologia | Categoria | Vantagem / Por que foi escolhida? |
| :--- | :--- | :--- |
| **React + Vite** | Front-end | Performance superior no desenvolvimento (Hot Reload rápido), ecossistema rico e componentização eficiente. |
| **Tailwind CSS** | Estilização | Desenvolvimento ágil de UI responsiva e moderna sem sair do HTML/JSX. |
| **FastAPI (Python)** | API Gestão | Alta performance (async), tipagem forte, validação automática (Pydantic) e documentação nativa (Swagger). |
| **Flask (Python)** | API Logs | Leveza e simplicidade para criar o proxy de comunicação com o motor de busca. |
| **Elasticsearch** | Banco de Dados (Logs) | Poderoso motor de busca e analytics, ideal para indexar e consultar grandes volumes de logs em tempo real. |
| **SQLite / SQLAlchemy** | Banco de Dados (App) | Simplicidade para gestão relacional (usuários/perfis) com ORM robusto para mapeamento de dados. |
| **Docker & Compose** | Infraestrutura | Padronização do ambiente de desenvolvimento, garantindo que "funcione na minha máquina" e na sua. |
| **Filebeat** | Coletor de Logs | Agente leve para encaminhar logs gerados para o Elasticsearch de forma eficiente. |

---

## 📂 Estrutura do Projeto (Monorepo)

O projeto está organizado em microsserviços para separar responsabilidades:

```text
argos/
├── 📂 backend/              # Diretório central dos serviços de Back-end
│   ├── 📂 api_gestao/       # API (FastAPI) para Usuários, Perfis e Auth
│   └── 📂 api_logs/         # API (Flask) para busca de Logs no Elastic
│
├── 📂 frontend/             # Aplicação React (Vite + Tailwind)
│
├── 📂 analisador/           # Script Python para detecção de anomalias
├── 📂 gerador/              # Script para gerar logs simulados (dados mockados)
├── 📂 filebeat/             # Configuração do coletor de logs
└── docker-compose.yml       # Orquestração de todos os containers
```



## Autores

| [<img src="https://avatars.githubusercontent.com/u/128331199?v=4" width=115><br><sub>Kennedy Torres</sub>](https://github.com/Kennedy-Torres) |[<img src="https://avatars.githubusercontent.com/u/111468952?v=4" width=115><br><sub>Nathalia GS</sub>](https://github.com/nathi-gs) |[<img src="https://avatars.githubusercontent.com/u/116228124?v=4" width=115><br><sub>Pedro Marques</sub>](https://github.com/phxdablio) |[<img src="https://avatars.githubusercontent.com/u/101297032?v=4" width=115><br><sub>Gustavo Horeste</sub>](https://github.com/GustavoHoreste) |[<img src="https://avatars.githubusercontent.com/u/71994927?v=4" width=115><br><sub>Matheus Vinycius</sub>](https://github.com/matheus58) |
| :---: | :---: | :---: | :---: | :---: |
