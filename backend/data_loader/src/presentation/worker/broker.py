from taskiq_redis import RedisStreamBroker, RedisAsyncResultBackend

from infrastructure.config.redis import RedisConfig
from presentation.worker.tasks import download_accounts


def init_broker(config: RedisConfig) -> RedisStreamBroker:
    result_backend = RedisAsyncResultBackend(
        redis_url=config.result_backend_url,
        max_connection_pool_size=config.result_backend_pool_size
    )
    broker = RedisStreamBroker(
        url=config.broker_url,
        max_connection_pool_size=config.broker_pool_size
    ).with_result_backend(result_backend)

    broker.register_task(download_accounts, schedule=[{"cron": "*/1 * * * *", "kwargs": {'user_id': 1}}])

    return broker
