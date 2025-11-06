CREATE TABLE kafka_accounts
(
    account_id String,
    name String,
    balance Float64,
    created_at DateTime
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'accounts',
    kafka_group_name = 'ch_accounts_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 2,
    stream_flush_interval_ms = 1000,
    kafka_max_block_size = 1000;


CREATE TABLE kafka_transactions
(
    account_id String,
    account_type String,
    nickname String,
    amount Float64,
    currency String,
    created_at DateTime
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'transactions',
    kafka_group_name = 'ch_transactions_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 2,
    stream_flush_interval_ms = 1000,
    kafka_max_block_size = 1000;


CREATE TABLE accounts
(
    account_id String,
    name String,
    balance Float64,
    created_at DateTime
)
ENGINE = ReplacingMergeTree()
ORDER BY account_id;


CREATE TABLE transactions
(
    tx_id String,
    account_id String,
    amount Float64,
    currency String,
    created_at DateTime
)
ENGINE = ReplacingMergeTree()
ORDER BY (account_id, created_at);


CREATE MATERIALIZED VIEW mv_accounts
TO accounts
AS
SELECT * FROM kafka_accounts;


CREATE MATERIALIZED VIEW mv_transactions
TO transactions
AS
SELECT * FROM kafka_transactions;


ALTER TABLE kafka_accounts MODIFY SETTING
    kafka_handle_error_mode = 'stream',
    kafka_commit_every_batch = 1,
    kafka_skip_broken_messages = 1,
    input_format_skip_unknown_fields = 1;


ALTER TABLE kafka_transactions MODIFY SETTING
    kafka_handle_error_mode = 'stream',
    kafka_commit_every_batch = 1,
    kafka_skip_broken_messages = 1,
    input_format_skip_unknown_fields = 1;