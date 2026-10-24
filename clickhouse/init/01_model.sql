CREATE TABLE IF NOT EXISTS ed_store_bd.dim_users
(
    user_id       UInt32,
    name          String,
    city          LowCardinality(String),
    segment       Enum8('new' = 1, 'regular' = 2, 'vip' = 3),
    registered_at DateTime
)
ENGINE = MergeTree
ORDER BY user_id;

CREATE TABLE IF NOT EXISTS ed_store_bd.dim_products
(
    product_id UInt32,
    name       String,
    category   LowCardinality(String),
    base_price Decimal(10, 2)
)
ENGINE = MergeTree
ORDER BY product_id;

CREATE TABLE IF NOT EXISTS ed_store_bd.fact_order_items
(
    order_id       UUID,
    order_ts       DateTime,
    user_id        UInt32,
    product_id     UInt32,
    quantity       UInt16,
    price          Decimal(10, 2),
    discount       Decimal(4, 3),
    amount         Decimal(12, 2) MATERIALIZED price * quantity,
    payment_method Enum8('card' = 1, 'cash' = 2, 'sbp' = 3, 'credit' = 4),
    status         Enum8('paid' = 1, 'cancelled' = 2)
)
ENGINE = MergeTree
PARTITION BY toDate(order_ts)
ORDER BY (order_ts, user_id, product_id);