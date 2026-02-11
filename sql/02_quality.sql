-- Checar duplicidade no RAW
SELECT
    customer_id,
    COUNT(*) AS total_registros
FROM `campaign-analytics-487115.campaign_analytics.raw_customers`
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- Checar NULL em campos críticos
SELECT
    COUNTIF(customer_id IS NULL) AS null_customer_id,
    COUNTIF(email IS NULL) AS null_email,
    COUNTIF(signup_date IS NULL) AS null_signup_date
FROM `campaign-analytics-487115.campaign_analytics.raw_customers`;
