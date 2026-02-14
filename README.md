# 📊 Campaign Analytics Engine

Pipeline analítico completo para mensuração de performance de campanhas de marketing,
estruturado em múltiplas camadas (raw → staging → integration → metrics)
com visualização executiva em Streamlit.

O projeto simula um ambiente real de CRM + campanhas promocionais,
incluindo problemas típicos de qualidade, cardinalidade e inflação de métricas,
demonstrando como estruturar dados de forma auditável e orientada à decisão.

Stack principal: BigQuery • SQL • Python • Streamlit

---

# 🎯 Objetivo do Projeto

Simular um ambiente corporativo de Marketing Analytics estruturando:

- Pipeline com controle explícito de qualidade
- Integrações com validação de cardinalidade
- Métricas executivas auditáveis
- Comparação automática entre períodos
- Visualização executiva orientada à decisão

O foco não é apenas gerar dashboards,
mas garantir consistência numérica e governança das métricas.

---

# 🏗 Arquitetura Analítica

O projeto está organizado em quatro camadas principais:

---

## 🔹 Staging Layer

Tratamento e padronização dos dados brutos:

- Remoção de duplicidades com ROW_NUMBER()
- Normalização de datas
- Seleção do registro mais recente
- Exclusão de inconsistências temporais
- Padronização de campos críticos

---

## 🔹 Integration Layer

Integração controlada entre múltiplas fontes:

- INNER JOIN para relacionamentos obrigatórios
- LEFT JOIN para preservar base analítica
- Controle explícito de cardinalidade
- Contagem pré e pós-join
- Comparação de volumetria para evitar explosão de registros

### Técnicas aplicadas

- CTEs para modularização da lógica
- Validação de relacionamentos 1:1, 1:N e N:1
- Agregações prévias antes de joins
- Checagens com COUNT(DISTINCT)

### Riscos tratados

- Campanhas com múltiplos eventos por cliente gerando duplicidade
- Premiações associadas incorretamente
- Métricas infladas por joins N:N involuntários
- Explosão de registros após integração

---

## 🔹 Metrics Layer

Modelagem explícita de métricas executivas:

- Receita total
- Ticket médio ponderado
- Clientes ativos (soma diária)
- Baseline por período
- Receita incremental
- ROI real

### Técnicas utilizadas

- SUM() controlado
- Window functions (SUM() OVER, AVG() OVER)
- Agrupamentos consistentes
- Separação clara entre métricas técnicas e executivas

---

## 🔹 Visualization Layer (Streamlit)

Camada executiva construída em Python:

- KPIs principais no topo
- Comparação vs período anterior
- Receita ao longo do tempo
- Mix de receita por campanha
- Ranking de campanhas
- Insights automáticos
- Exportação de dados filtrados

O dashboard consome diretamente a camada de métricas (mart analítico).

---

# 📊 Dashboard Executivo

### Executive Overview
![Executive Overview](assets/01_overview.png)

### Performance
![Performance](assets/02_performance.png)

### Dados & Export
![Dados & Export](assets/03_data_export.png)

---

# ⚠️ Problemas Simulados nos Dados

O projeto inclui falhas realistas:

- Clientes duplicados no CRM
- Datas inconsistentes (update anterior ao cadastro)
- Campos críticos ausentes
- Eventos de campanha duplicados
- Premiações fora das regras
- Quebra de cardinalidade em joins
- Métricas infladas por N:N involuntário

Esses cenários refletem problemas comuns em ambientes reais de marketing e CRM.

---

# 📈 Impacto Analítico Simulado

O motor analítico permite:

- Identificar campanhas com ROI negativo real
- Detectar inflação artificial de métricas
- Reduzir desperdício de budget
- Aumentar confiança nos números
- Sustentar decisões executivas com base auditável

---

# 🛠 Stack Técnica

## Python

- Geração de dados sintéticos realistas
- Simulação de inconsistências controladas
- Construção de dashboard executivo (Streamlit)
- Comparação automática entre períodos

## SQL (BigQuery)

- CTEs para modularização
- INNER JOIN e LEFT JOIN estratégicos
- Controle de cardinalidade
- ROW_NUMBER() para deduplicação
- COUNT(DISTINCT) para auditoria
- Window functions
- Sanity checks pré e pós-integração
- Separação entre staging, integração e métricas

## Streamlit

- Layout executivo
- Filtros dinâmicos
- KPIs com variação percentual
- Visualizações interativas
- Exportação CSV

---

# 📁 Estrutura do Repositório

campaign-analytics-engine/
│
├── app.py                         # Dashboard executivo (Streamlit)
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   └── raw/                       # Dados brutos simulados
│
├── python/
│   └── generate_data.py           # Geração de dados sintéticos
│
├── sql/
│   ├── 01_staging.sql
│   ├── 02_quality.sql
│   ├── 03_integration.sql
│   └── 04_metrics.sql
│
├── assets/
<<<<<<< HEAD
│   └── dashboard_preview.png      # Print do dashboard
│
└── docs/
    └── model.md                   # Modelo analítico e métricas
```
=======
│   ├── 01_overview.png
│   ├── 02_performance.png
│   └── 03_data_export.png
│
└── docs/
    └── model.md                   # Modelo analítico e definição de métricas

---

# 🚀 Como Executar

1) Instale as dependências:

pip install -r requirements.txt

2) Configure as credenciais do BigQuery via variável de ambiente:

GOOGLE_APPLICATION_CREDENTIALS

Ou utilize:

gcloud auth application-default login

3) Execute o dashboard:

streamlit run app.py

---

# 🔐 Credenciais

Este repositório não contém credenciais.

O acesso ao BigQuery deve ser configurado via variável de ambiente
ou Application Default Credentials.
>>>>>>> 2f0ff39 (docs: update README with dashboard preview and project structure)

---

# 🚀 Roadmap de Evolução

- Implementar análise de cohort
- Criar alertas automatizados de anomalia
- Simular otimização de budget
- Incorporar análise preditiva
- Evoluir para ambiente cloud estruturado

---

# 📌 Observação

Todos os dados utilizados são sintéticos e foram criados exclusivamente
para fins educacionais e técnicos.

---

# 👤 Autoria

Projeto autoral desenvolvido de ponta a ponta como estudo aplicado de Analytics Engineering.

Reflete minha abordagem na:

- Estruturação de pipelines
- Controle de qualidade numérica
- Governança de métricas
- Tradução de dados em decisões estratégicas
