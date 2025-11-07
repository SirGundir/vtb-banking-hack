from faststream.kafka import KafkaBroker

from infrastructure.config.kafka import KafkaConfig
from presentation.worker import handlers
from presentation.worker.topics import DOWNLOAD_USER_ACCOUNT_TOPIC, DOWNLOAD_USER_TRANSACTIONS_TOPIC, \
    DOWNLOAD_USER_BALANCE_TOPIC, DOWNLOAD_BANK_PRODUCTS_TOPIC


def init_broker(config: KafkaConfig) -> KafkaBroker:
    broker = KafkaBroker(config.broker_url)

    account_sub = broker.subscriber(DOWNLOAD_USER_ACCOUNT_TOPIC)
    account_sub(handlers.download_accounts)

    transactions_sub = broker.subscriber(DOWNLOAD_USER_TRANSACTIONS_TOPIC)
    transactions_sub(handlers.download_account_transactions)

    balances_sub = broker.subscriber(DOWNLOAD_USER_BALANCE_TOPIC)
    balances_sub(handlers.download_account_balance)

    products_sub = broker.subscriber(DOWNLOAD_BANK_PRODUCTS_TOPIC)
    products_sub(handlers.download_bank_products)


    # product_details_sub = broker.subscriber(DOWNLOAD_USER_BALANCE_TOPIC)



    return broker
