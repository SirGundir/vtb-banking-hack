import asyncio
from typing import Callable

import aiohttp
import orjson
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from application.user_accounts.services import UserAccountService
from infrastructure.config.db import PgConfig
from infrastructure.config.kafka import KafkaConfig
from infrastructure.data_loaders.accounts import UserAccountsLoader
from infrastructure.di.di_container import DIContainer
from infrastructure.repositories.banks import BankRepository
from infrastructure.repositories.users import UserRepository
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
    kafka_config: KafkaConfig,
    pg_config: PgConfig,
    http_session_factory: Callable,
    pg_engine_factory: Callable
) -> DIContainer:
    container = DIContainer()

    # singletons
    container.register_instance(KafkaConfig, kafka_config)
    container.register_singleton(AsyncEngine, lambda: pg_engine_factory(pg_config))
    container.register_singleton(aiohttp.ClientSession, http_session_factory)
    container.register_instance(asyncio.Semaphore, asyncio.Semaphore(100))
    # repositories
    container.register(UserRepository)
    container.register(BankRepository)
    # caches
    # etc
    container.register(UserAccountsLoader)
    # services
    container.register(UserAccountService)
    return container

