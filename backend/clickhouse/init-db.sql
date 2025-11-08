CREATE TABLE kafka_accounts
(
    user_id UUID,
    bank_id Int64,
    account_id String,
    status String,
    currency String,
    account_type String,
    account_sub_type String,
    opening_date Date
)
ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'ch_accounts_topic',
    kafka_group_name = 'ch_accounts_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1,
    kafka_flush_interval_ms = 500,
    kafka_max_block_size = 1000,
    kafka_commit_every_batch = 1,
    kafka_skip_broken_messages = 1;


CREATE TABLE kafka_account_balances
(
    user_id UUID,
    bank_id Int64,
    account_id String,
    currency String,
    amount Decimal64(2),
    balance_type String,
    credit_debit_indicator String,
    balance_at_datetime DateTime
)
ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'ch_accounts_balances_topic',
    kafka_group_name = 'ch_accounts_balances_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1,
    kafka_flush_interval_ms = 500,
    kafka_max_block_size = 1000,
    kafka_commit_every_batch = 1,
    kafka_skip_broken_messages = 1;

CREATE TABLE kafka_transactions
(
    user_id UUID,
    bank_id Int64,
    account_id String,
    transaction_id String,
    status String,
    transaction_info String,
    currency String,
    amount Decimal64(2),
    bank_transaction_code String,
    booking_dt DateTime,
    value_dt DateTime
)
ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'ch_accounts_transaction_topic',
    kafka_group_name = 'ch_accounts_transactions_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1,
    stream_flush_interval_ms = 500,
    kafka_max_block_size = 1000;

CREATE TABLE kafka_bank_products
(
    bank_id Int64,
    product_id String,
    product_type String,
    product_name String,
    description Nullable(String),
    interest_rate Nullable(Decimal64(2)),
    min_amount Nullable(Decimal64(2)),
    max_amount Nullable(Decimal64(2)),
    term_months Nullable(Int64)
)
ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'ch_bank_products_topic',
    kafka_group_name = 'ch_bank_products_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1,
    stream_flush_interval_ms = 500,
    kafka_max_block_size = 1000;


CREATE TABLE accounts
(
    user_id UUID,
    bank_id Int64,
    account_id String,
    status String,
    currency String,
    account_type String,
    account_sub_type String,
    opening_date Date
)
ENGINE = ReplacingMergeTree()
ORDER BY (user_id, bank_id, account_id);


CREATE TABLE account_balances
(
    user_id UUID,
    bank_id Int64,
    account_id String,
    currency String,
    amount Decimal64(2),
    balance_type String,
    credit_debit_indicator String,
    balance_at_datetime DateTime
)
ENGINE = ReplacingMergeTree()
ORDER BY (user_id, bank_id, account_id, balance_at_datetime);


CREATE TABLE transactions
(
    user_id UUID,
    bank_id Int64,
    account_id String,
    transaction_id String,
    status String,
    transaction_info String,
    currency String,
    amount Decimal64(2),
    bank_transaction_code String,
    booking_dt DateTime,
    value_dt DateTime
)
ENGINE = ReplacingMergeTree()
ORDER BY (user_id, bank_id, account_id, transaction_id);


CREATE TABLE bank_products
(
    bank_id Int64,
    product_id String,
    product_type String,
    product_name String,
    description Nullable(String),
    interest_rate Nullable(Decimal64(2)),
    min_amount Nullable(Decimal64(2)),
    max_amount Nullable(Decimal64(2)),
    term_months Nullable(Int64)
)
ENGINE = ReplacingMergeTree()
ORDER BY (bank_id, product_id);


CREATE MATERIALIZED VIEW mv_accounts
TO accounts
AS
SELECT * FROM kafka_accounts;


CREATE MATERIALIZED VIEW mv_account_balances
TO account_balances
AS
SELECT * FROM kafka_account_balances;


CREATE MATERIALIZED VIEW mv_transactions
TO transactions
AS
SELECT * FROM kafka_transactions;


CREATE MATERIALIZED VIEW mv_bank_products
TO bank_products
AS
SELECT * FROM kafka_bank_products;