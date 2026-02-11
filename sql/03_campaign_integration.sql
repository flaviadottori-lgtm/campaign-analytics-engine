-- =========================================================
-- 03_campaign_integration.sql
-- Integração de campanhas + ativações + transações
-- Regras:
--  - cliente ativado participa da campanha
--  - atribuição de transação: transaction_date entre activation_date e end_date
--  - resolução de conflito: se uma transação cair em múltiplas campanhas,
--    manter a campanha com activation_date mais recente (last-touch)
-- =========================================================

-- 1) Staging de campanhas com tipagem segura
CREATE OR REPLACE VIEW `campaign-analytics-487115.campaign_analytics.stg_campaigns` AS
SELECT
  campaign_id,
  campaign_name,
  SAFE_CAST(start_date AS DATE) AS start_date,
  SAFE_CAST(end_date AS DATE) AS end_date
FROM `campaign-analytics-487115.campaign_analytics.raw_campaigns`;

-- 2) Staging de ativações com tipagem segura
CREATE OR REPLACE VIEW `campaign-analytics-487115.campaign_analytics.stg_campaign_activations` AS
SELECT
  customer_id,
  campaign_id,
  SAFE_CAST(activation_date AS DATE) AS activation_date
FROM `campaign-analytics-487115.campaign_analytics.raw_campaign_activations`;

-- 3) Integração base: 1 linha por ativação (cliente-campanha)
CREATE OR REPLACE VIEW `campaign-analytics-487115.campaign_analytics.int_campaign_activations` AS
SELECT
  a.customer_id,
  a.campaign_id,
  c.campaign_name,
  a.activation_date,
  c.start_date,
  c.end_date
FROM `campaign-analytics-487115.campaign_analytics.stg_campaign_activations` a
INNER JOIN `campaign-analytics-487115.campaign_analytics.stg_campaigns` c
  ON c.campaign_id = a.campaign_id;

-- 4) Atribuição de transações à campanha (janela activation_date -> end_date)
-- Garantia: 1 linha por transaction_id atribuído (evita dupla contagem)
CREATE OR REPLACE VIEW `campaign-analytics-487115.campaign_analytics.int_campaign_transactions` AS
SELECT * EXCEPT(rn)
FROM (
  SELECT
    ca.campaign_id,
    ca.campaign_name,
    ca.customer_id,
    ca.activation_date,
    ca.start_date,
    ca.end_date,
    t.transaction_id,
    t.transaction_date,
    t.amount,
    ROW_NUMBER() OVER (
      PARTITION BY t.transaction_id
      ORDER BY ca.activation_date DESC, ca.campaign_id
    ) AS rn
  FROM `campaign-analytics-487115.campaign_analytics.int_campaign_activations` ca
  INNER JOIN `campaign-analytics-487115.campaign_analytics.int_customer_transactions` t
    ON t.customer_id = ca.customer_id
   AND t.transaction_date BETWEEN ca.activation_date AND ca.end_date
)
WHERE rn = 1;
