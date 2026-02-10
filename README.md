# Campaign Analytics Engine

Este projeto simula um cenário real de **CRM, campanhas de incentivo e loyalty**, utilizando **dados sintéticos intencionalmente imperfeitos**, com o objetivo de demonstrar como estruturar **pipelines de dados, integração entre múltiplas fontes, modelagem analítica, validação de qualidade e métricas confiáveis**, orientadas à **tomada de decisão de negócio**.

O foco do projeto não é apenas a construção de dashboards, mas o desenvolvimento de um **motor analítico reutilizável**, capaz de sustentar análises recorrentes, avaliação real de ROI e recomendações acionáveis.

---

## 🎯 Objetivo do Projeto

- Simular dados de CRM, transações e campanhas com **problemas reais de qualidade**
- Integrar múltiplas fontes de dados utilizando **joins controlados e auditáveis**
- Construir uma camada de **staging e modelagem analítica**
- Definir métricas claras para avaliação de campanhas
- Reduzir riscos de decisões baseadas em métricas infladas ou inconsistentes
- Demonstrar BI como **ferramenta de decisão**, não apenas de monitoramento

---

## 😖 Dores de Negócio que o Projeto Endereça

### 1. Métricas infladas por erros de integração
Em ambientes reais, campanhas aparentam bons resultados devido a:
- joins incorretos
- duplicidade de registros
- quebra de cardinalidade
- ausência de sanity checks

**Como o projeto resolve:**
- Deduplicação antes de joins  
- Validação explícita de cardinalidade  
- Uso criterioso de `INNER JOIN` e `LEFT JOIN`  
- Checagens pós-join para garantir consistência dos números  

---

### 2. Falta de clareza sobre o ROI real das campanhas
Sem baseline e incrementalidade, a empresa não consegue separar:
- crescimento natural
- efeito real da campanha
- custo efetivo do incentivo

**Como o projeto resolve:**
- Definição de baseline por cliente ou período  
- Cálculo de incrementalidade  
- Métricas de ROI orientadas à tomada de decisão  

---

### 3. Alto retrabalho em análises e dashboards
Demandas recorrentes geram:
- múltiplas queries para o mesmo conceito
- métricas diferentes com o mesmo nome
- baixa confiança nos números

**Como o projeto resolve:**
- Centralização das regras de negócio  
- Motor analítico reutilizável  
- Separação clara entre dado bruto, dado tratado e métricas  

---

### 4. BI utilizado apenas como relatório
Dashboards existem, mas não orientam decisões.

**Como o projeto resolve:**
- Dashboards conectados a métricas confiáveis  
- Visões de risco, oportunidade e quick wins  
- BI como apoio direto à decisão estratégica  

---

## 📈 Resultados Esperados

### Resultados Técnicos
- Dados confiáveis e auditáveis
- Redução de erros silenciosos em análises
- Integração consistente entre CRM, campanhas e transações
- Queries mais legíveis, versionadas e escaláveis

### Resultados de Negócio
- Entendimento claro do desempenho real das campanhas
- Melhor alocação do budget de incentivo
- Redução de desperdício financeiro
- Identificação precoce de desvios e anomalias

### Resultados Organizacionais
- Menor dependência de análises ad hoc
- Maior autonomia do time de BI
- Comunicação mais clara entre dados e áreas de negócio

---

## 🧠 Abordagem Analítica

O projeto segue uma separação clara de responsabilidades ao longo do pipeline:

### 🔹 Dados Brutos (Raw)
- Extrações diretas dos sistemas simulados
- Presença de duplicidades, inconsistências e dados faltantes
- Nenhuma regra de negócio aplicada

### 🔹 Staging
- Deduplicação de registros (ex.: CRM)
- Padronização de datas e chaves
- Validação de regras de negócio
- Preparação para integração entre fontes

### 🔹 Integração de Dados
- Joins entre CRM, transações, campanhas, ativações e premiações
- Controle explícito de cardinalidade
- Escolha criteriosa do tipo de join (`INNER` / `LEFT`)

### 🔹 Modelagem Analítica
- Organização dos dados em estruturas confiáveis
- Separação entre fatos e dimensões
- Preparação para cálculo de métricas

### 🔹 Métricas
- Baseline
- Incrementalidade
- ROI
- Indicadores acionáveis para decisão

### 🔹 Visualização
- Camada final de comunicação
- Dashboards orientados à tomada de decisão

---

## 🧪 Principais Problemas Simulados nos Dados

- Clientes duplicados no CRM
- Campos críticos ausentes (estado, segmento)
- Datas inconsistentes (atualização anterior ao cadastro)
- Duplicação de eventos de campanha
- Premiações pagas fora das regras esperadas
- Risco de métricas infladas por joins incorretos

Esses cenários refletem desafios comuns em ambientes reais de BI e Analytics.

---

## 🛠️ Stack Utilizada

- **Python**
  - Geração de dados sintéticos realistas
  - Automação de análises e validações
  - Suporte a análises exploratórias

- **SQL**
  - Staging e integração de dados
  - Joins complexos entre múltiplas fontes
  - Modelagem analítica
  - CTEs, window functions e sanity checks

- **Power BI**
  - Camada final de visualização
  - Dashboards orientados à tomada de decisão

---

## 📁 Estrutura do Repositório

```text
campaign-analytics-engine/
├── data/
│   └── raw/                      # Dados brutos simulados
├── python/
│   └── generate_data.py          # Geração de dados sintéticos
├── sql/
│   ├── 01_staging.sql            # Staging e deduplicação
│   ├── 02_quality.sql            # Relatórios de qualidade
│   ├── 03_integration.sql        # Joins e integração entre fontes
│   └── 04_metrics.sql            # Métricas (baseline, ROI, incrementalidade)
├── powerbi/
│   └── model.md                  # Modelo analítico e métricas
└── README.md

🚀 Próximos Passos

Evoluir métricas de incrementalidade com análise de cohort

Implementar alertas automatizados para anomalias

Expandir dashboards com foco em decisões executivas

Simular testes de cenário e otimização de budget

Explorar uso de IA como apoio à geração de hipóteses analíticas

📌 Observação Importante

Os dados utilizados neste projeto são totalmente sintéticos e foram criados exclusivamente para fins de estudo e demonstração técnica. Não representam dados reais de clientes ou empresas.

👤 Autoria e Contexto

Este é um projeto autoral, desenvolvido por mim de ponta a ponta como estudo técnico.

O objetivo é simular desafios reais encontrados em ambientes de BI e Analytics, incluindo integração de múltiplas fontes, tratamento de dados imperfeitos, definição de métricas e apoio à tomada de decisão.

O projeto não representa um ambiente produtivo real, mas reflete minha forma de estruturar problemas analíticos, tomar decisões técnicas e traduzir dados em valor para o negócio.