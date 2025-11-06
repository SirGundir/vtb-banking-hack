from contextlib import asynccontextmanager
from typing import Callable

import aiohttp
from faststream import FastStream, ContextRepo

from infrastructure.config.db import PgConfig
from infrastructure.config.kafka import KafkaConfig
from infrastructure.di.factory import di_container_factory, init_http_session, init_pg_engine


@asynccontextmanager
async def app_lifespan(context: ContextRepo):
    di_container = di_container_factory(
        kafka_config=KafkaConfig(),
        pg_config=PgConfig(),
        http_session_factory=init_http_session,
        pg_engine_factory=init_pg_engine
    )
    context.set_global('di_container', di_container)
    http_session: aiohttp.ClientSession = di_container.resolve(aiohttp.ClientSession)
    try:
        yield
    finally:
        await http_session.close()


def init_app(broker_factory: Callable, **kwargs) -> FastStream:
    broker = broker_factory(KafkaConfig())
    return FastStream(broker, **kwargs)