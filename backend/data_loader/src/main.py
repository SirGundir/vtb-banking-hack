import asyncio

from broker_instance import broker
from infrastructure.config.redis import RedisConfig
from presentation.worker.broker import init_broker
from presentation.worker.tasks import download_accounts


async def main():
    await broker.startup()


if __name__ == "__main__":
    asyncio.run(main())
