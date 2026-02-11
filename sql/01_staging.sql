CREATE OR REPLACE VIEW 
`campaign-analytics-487115.campaign_analytics.stg_customers` AS

SELECT * EXCEPT(rn)
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY SAFE_CAST(signup_date AS DATE) DESC
        ) AS rn
    FROM `campaign-analytics-487115.campaign_analytics.raw_customers`
)
WHERE rn = 1;
