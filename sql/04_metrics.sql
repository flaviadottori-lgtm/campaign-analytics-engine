-- =========================================================
-- 04_metrics.sql
-- Camada final de métricas por campanha
-- =========================================================

CREATE OR REPLACE VIEW 
`campaign-analytics-487115.campaign_analytics.mrt_campaign_performance` AS

WITH ativacoes AS (
  SELECT
    campaign_id,
    COUNT(DISTINCT customer_id) AS total_clientes_ativados
  FROM `campaign-analytics-487115.campaign_analytics.int_campaign_activations`
  GROUP BY campaign_id
),

transacoes AS (
  SELECT
    campaign_id,
    COUNT(DISTINCT transaction_id) AS total_transacoes_atribuidas,
    COUNT(DISTINCT customer_id) AS clientes_com_compra,
    SUM(amount) AS receita_total,
    AVG(amount) AS ticket_medio
  FROM `campaign-analytics-487115.campaign_analytics.int_campaign_transactions`
  GROUP BY campaign_id
)

SELECT
  a.campaign_id,
  c.campaign_name,
  a.total_clientes_ativados,
  IFNULL(t.clientes_com_compra, 0) AS clientes_com_compra,
  SAFE_DIVIDE(IFNULL(t.clientes_com_compra, 0), a.total_clientes_ativados) AS taxa_conversao_clientes,
  IFNULL(t.total_transacoes_atribuidas, 0) AS total_transacoes_atribuidas,
  SAFE_DIVIDE(IFNULL(t.total_transacoes_atribuidas, 0), a.total_clientes_ativados) AS tx_por_ativado,
  IFNULL(t.receita_total, 0) AS receita_total,
  IFNULL(t.ticket_medio, 0) AS ticket_medio
FROM ativacoes a
LEFT JOIN transacoes t
  ON a.campaign_id = t.campaign_id
LEFT JOIN `campaign-analytics-487115.campaign_analytics.stg_campaigns` c
  ON a.campaign_id = c.campaign_id;
