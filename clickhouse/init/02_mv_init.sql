CREATE TABLE IF NOT EXISTS ed_store_bd.agg_sales_by_minute
(
    minute   DateTime,
    category LowCardinality(String),
    city     LowCardinality(String),
    orders   AggregateFunction(uniq, UUID),
    items    SimpleAggregateFunction(sum, UInt64),
    revenue  SimpleAggregateFunction(sum, Decimal(38, 2))
)
ENGINE = AggregatingMergeTree
PARTITION BY toDate(minute)
ORDER BY (minute, category, city);

CREATE MATERIALIZED VIEW IF NOT EXISTS ed_store_bd.mv_sales_by_minute
TO ed_store_bd.agg_sales_by_minute
AS
SELECT
    toStartOfMinute(f.order_ts)  AS minute,
    p.category                   AS category,
    u.city                       AS city,
    uniqState(f.order_id)        AS orders,
    sum(f.quantity)              AS items,
    sum(f.amount)                AS revenue
FROM ed_store_bd.fact_order_items AS f
LEFT JOIN ed_store_bd.dim_products AS p ON p.product_id = f.product_id
LEFT JOIN ed_store_bd.dim_users    AS u ON u.user_id    = f.user_id
WHERE f.status = 'paid'
GROUP BY minute, category, city;

CREATE VIEW IF NOT EXISTS ed_store_bd.v_sales_by_minute AS
SELECT
    minute,
    category,
    city,
    uniqMerge(orders) AS orders,
    sum(items)        AS items,
    sum(revenue)      AS revenue
FROM ed_store_bd.agg_sales_by_minute
GROUP BY minute, category, city;