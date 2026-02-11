-- =========================================================
-- 03_integration.sql
-- Integração Customers (stg) + Transactions (raw/stg)
-- Com checks de cardinalidade/volumetria para evitar inflação
-- =========================================================

-- 1) (Opcional, mas recomendado) Criar staging para transactions com tipagem segura
CREATE OR REPLACE VIEW `campaign-analytics-487115.campaign_analytics.stg_transactions` AS
SELECT
  transaction_id,
  customer_id,
  SAFE_CAST(transaction_date AS DATE) AS transaction_date,
  SAFE_CAST(amount AS FLOAT64) AS amount
FROM `campaign-analytics-487115.campaign_analytics.raw_transactions`;

-- 2) View de integração: 1 linha por transação (join 1:N esperado)
CREATE OR REPLACE VIEW `campaign-analytics-487115.campaign_analytics.int_customer_transactions` AS
SELECT
  t.transaction_id,
  t.transaction_date,
  t.amount,
  c.customer_id,
  c.external_id,
  c.email,
  c.state,
  c.segment,
  SAFE_CAST(c.signup_date AS DATE) AS signup_date
FROM `campaign-analytics-487115.campaign_analytics.stg_transactions` t
LEFT JOIN `campaign-analytics-487115.campaign_analytics.stg_customers` c
  ON c.customer_id = t.customer_id;
