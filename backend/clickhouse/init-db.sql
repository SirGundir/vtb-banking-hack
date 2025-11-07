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
    kafka_commit_every_batch = 1;


CREATE TABLE kafka_account_balances
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
    kafka_commit_every_batch = 1;

--
--CREATE TABLE kafka_transactions
--(
--    account_id String,
--    account_type String,
--    nickname String,
--    amount Float64,
--    currency String,
--    created_at DateTime
--)
--ENGINE = Kafka()
--SETTINGS
--    kafka_broker_list = 'kafka:9092',
--    kafka_topic_list = 'ch_transactions_topic',
--    kafka_group_name = 'ch_transactions_consumer',
--    kafka_format = 'JSONEachRow',
--    kafka_num_consumers = 1,
--    stream_flush_interval_ms = 500,
--    kafka_max_block_size = 1000;


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


--CREATE TABLE transactions
--(
--    tx_id String,
--    account_id String,
--    amount Float64,
--    currency String,
--    created_at DateTime
--)
--ENGINE = ReplacingMergeTree()
--ORDER BY (account_id, created_at);


CREATE MATERIALIZED VIEW mv_accounts
TO accounts
AS
SELECT * FROM kafka_accounts;


--CREATE MATERIALIZED VIEW mv_transactions
--TO transactions
--AS
--SELECT * FROM kafka_transactions;
