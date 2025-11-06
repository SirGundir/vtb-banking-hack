from typing import Callable

import aiohttp
import orjson
from faststream.kafka import KafkaBroker
from redis.asyncio import ConnectionPool
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from application.auth.services.access_control import AccessControl
from application.auth.services.password import PasswordService
from application.banks.services import BankService, ConnectBankService
from infrastructure.blacklist import TokenBlacklist
from infrastructure.clients import BankOpenApiInterface, HttpBankClient
from infrastructure.config.app import AppConfig
from infrastructure.config.db import PgConfig
from infrastructure.config.kafka import KafkaConfig
from infrastructure.config.redis import RedisConfig
from infrastructure.di.di_container import DIContainer
from infrastructure.repositories.banks import BankRepository
from infrastructure.repositories.users import UserRepository
from utils.event_loop import safe_get_loop


def init_redis_pool(config: RedisConfig) -> ConnectionPool:
    return ConnectionPool(
        host=config.host,
        port=config.port,
    )


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
    redis_config: RedisConfig,
    pg_config: PgConfig,
    redis_pool_factory: Callable,
    http_session_factory: Callable,
    pg_engine_factory: Callable
) -> DIContainer:
    container = DIContainer()

    # singletons
    container.register_instance(AppConfig, app_config)
    container.register_instance(RedisConfig, redis_config)
    container.register_singleton(AsyncEngine, lambda: pg_engine_factory(pg_config))
    container.register_singleton(ConnectionPool, lambda: redis_pool_factory(redis_config))
    container.register_singleton(aiohttp.ClientSession, http_session_factory)
    container.register_instance(KafkaBroker, KafkaBroker(KafkaConfig().broker_url))
    # repositories
    container.register(UserRepository)
    container.register(BankRepository)
    # caches
    container.register(TokenBlacklist)
    # etc
    container.register(BankOpenApiInterface, HttpBankClient)
    # services
    container.register(AccessControl)
    container.register(PasswordService)
    container.register(BankService)
    container.register(ConnectBankService)
    return container

