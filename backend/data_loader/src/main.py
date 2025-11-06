import asyncio

from app_instance import broker
from infrastructure.config.redis import KafkaConfig
from presentation.worker.broker import init_broker
from presentation.worker.handlers import download_accounts


async def main():
    await broker.startup()


if __name__ == "__main__":
    asyncio.run(main())
