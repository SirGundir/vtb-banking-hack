from typing import Callable

import aiohttp
import orjson
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from infrastructure.config.app import AppConfig
from infrastructure.config.db import PgConfig
from infrastructure.config.redis import KafkaConfig
from infrastructure.di.di_container import DIContainer
from utils.event_loop import safe_get_loop


def init_http_session() -> aiohttp.ClientSession:
    loop = safe_get_loop()
    return aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            loop=loop,
            limit=5000,
            keepalive_timeout=200,
        ),
        json_serialize=lambda data: orjson.dumps(data).decode()
    )


def init_pg_engine(pg_config: PgConfig) -> AsyncEngine:
    # ToDo asyncpg Pool or external pool
    return create_async_engine(pg_config.async_dsn, poolclass=NullPool)


def di_container_factory(
    app_config: AppConfig,
    redis_config: KafkaConfig,
    pg_config: PgConfig,
    http_session_factory: Callable,
    pg_engine_factory: Callable
) -> DIContainer:
    container = DIContainer()

    # singletons
    container.register_instance(AppConfig, app_config)
    container.register_instance(KafkaConfig, redis_config)
    container.register_singleton(AsyncEngine, lambda: pg_engine_factory(pg_config))
    container.register_singleton(aiohttp.ClientSession, http_session_factory)
    # repositories
    # caches
    # etc
    # services
    return container

