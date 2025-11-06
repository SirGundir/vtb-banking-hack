from faststream.kafka import KafkaBroker

from infrastructure.config.redis import KafkaConfig
from presentation.worker import handlers
from presentation.worker.topics import DOWNLOAD_USER_ACCOUNT_TOPIC, DOWNLOAD_USER_TRANSACTIONS_TOPIC


def init_broker(config: KafkaConfig) -> KafkaBroker:
    broker = KafkaBroker(config.broker_url)

    account_sub = broker.subscriber(DOWNLOAD_USER_ACCOUNT_TOPIC)
    transactions_sub = broker.subscriber(DOWNLOAD_USER_TRANSACTIONS_TOPIC)

    account_sub(handlers.download_accounts)
    transactions_sub(handlers.download_account_transactions)

    return broker
