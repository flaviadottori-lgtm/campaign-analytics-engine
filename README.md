# 📊 Campaign Analytics Engine

- Seleção do registro mais recente  
- Exclusão de inconsistências temporais  

---

## 🔹 Integration Layer

Integração controlada entre múltiplas fontes:

- `INNER JOIN` para relacionamentos obrigatórios  
- `LEFT JOIN` para preservar base analítica  
- Controle explícito de cardinalidade  
- Contagem pré e pós-join  
- Comparação de volumetria para evitar explosão de registros  

### 🧠 Técnicas aplicadas

- CTEs para modularização da lógica  
- Validação de relacionamentos 1:1, 1:N e N:1  
- Uso de agregações prévias antes de joins  
- Checagens com `COUNT(DISTINCT)`  

### ⚠️ Exemplos de riscos tratados

- Campanhas com múltiplos eventos por cliente gerando duplicidade na transação  
- Premiações associadas incorretamente a múltiplas ativações  

---

## 🔹 Metrics Layer

Modelagem explícita de métricas:

- Baseline por cliente/período  
- Receita incremental  
- ROI real  
- Custo efetivo por campanha  

### 🧮 Técnicas utilizadas

- `SUM()` controlado  
- Window functions (`SUM() OVER`, `AVG() OVER`)  
- Agrupamentos consistentes  
- Separação clara entre métricas técnicas e executivas  

---

## 🔹 Visualization Layer

Camada final implementada no Power BI:

- Modelo conectado diretamente à camada de métricas  
- Indicadores orientados à decisão  
- Foco em impacto financeiro  
- Separação entre visão executiva e visão técnica  

---

## ⚠️ Problemas Simulados nos Dados

- Clientes duplicados no CRM  
- Datas inconsistentes (update anterior ao cadastro)  
- Campos críticos ausentes  
- Eventos de campanha duplicados  
- Premiações fora das regras  
- Quebra de cardinalidade em joins  
- Métricas infladas por N:N involuntário  

Esses cenários refletem falhas comuns em ambientes reais.

---

## 📈 Impacto Simulado

O motor analítico permite:

- Identificar campanhas com ROI negativo real  
- Detectar inflação artificial de métricas  
- Reduzir desperdício de budget  
- Aumentar confiança nos números  
- Sustentar decisões executivas com base auditável  

---

# 🛠️ Stack Técnica

## 🐍 Python

- Geração de dados sintéticos realistas  
- Simulação de inconsistências controladas  
- Automação de validações  

## 🗄️ SQL

- CTEs para modularização de lógica  
- `INNER JOIN` e `LEFT JOIN` estratégicos  
- Controle de cardinalidade  
- `ROW_NUMBER()` para deduplicação  
- `COUNT(DISTINCT)` para auditoria  
- Window functions  
- `GROUP BY` estruturado  
- Sanity checks pré e pós-integração  
- Separação entre staging, integração e métricas  

## 📊 Power BI

- Modelagem conectada à camada de métricas  
- Dashboards orientados à decisão  
- Visão executiva e técnica separadas  

---

# 📁 Estrutura do Repositório

```
campaign-analytics-engine/
├── data/
│   └── raw/                      # Dados brutos simulados
├── python/
│   └── generate_data.py          # Geração de dados sintéticos
├── sql/
│   ├── 01_staging.sql            # Deduplicação e padronização
│   ├── 02_quality.sql            # Relatórios de qualidade e auditoria
│   ├── 03_integration.sql        # Integração controlada (joins e cardinalidade)
│   └── 04_metrics.sql            # Baseline, incrementalidade e ROI
├── powerbi/
│   └── model.md                  # Modelo analítico e documentação de métricas
└── README.md
```

---

# 🚀 Roadmap de Evolução

- Implementar análise de cohort para incrementalidade  
- Criar alertas automatizados para anomalias  
- Simular cenários de otimização de budget  
- Incorporar análise preditiva  
- Evoluir para ambiente cloud (BigQuery / Data Warehouse dedicado)  

---

# 📌 Observação

Todos os dados utilizados são sintéticos e foram criados exclusivamente para fins de estudo técnico.

---

# 👤 Autoria

Projeto autoral desenvolvido de ponta a ponta como estudo aplicado de Analytics Engineering.

Reflete minha abordagem na estruturação de pipelines, controle de qualidade numérica e tradução de dados em decisões estratégicas.
