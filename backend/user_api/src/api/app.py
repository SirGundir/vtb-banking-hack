from contextlib import asynccontextmanager
from typing import TypedDict, AsyncIterator

import aiohttp
from aiochclient import ChClient
from fastapi import HTTPException, Request, FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from redis.asyncio import ConnectionPool
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from application.auth.exceptions import PasswordValidationError, AuthorizationError, ForbiddenError, CredentialsError
from core.exceptions import ValidateDataError, ActionNotAllowedError
from infrastructure.clickhouse.http import init_clickhouse_client
from infrastructure.config.app import AppConfig
from infrastructure.config.clickhouse import ClickhouseConfig
from infrastructure.config.db import PgConfig
from infrastructure.config.redis import RedisConfig
from infrastructure.db.exceptions import AlreadyExistsError, DoesNotExists
from infrastructure.di.di_container import DIContainer
from infrastructure.di.factory import di_container_factory, init_redis_pool, init_http_session, init_pg_engine
from log import get_logger

from api.v1.auth.router import router as auth_router
from api.v1.users.router import router as users_router
from api.v1.banks.router import router as banks_router


logger = get_logger(__name__)


async def on_not_found(request, exc):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Not found.",
    )


def on_validation_error(debug: bool = False):
    async def _handler(request, exc):
        expected = exc.errors()
        received = exc.body if hasattr(exc, 'body') else 'No data'
        err_msg = 'Not validated password'
        if isinstance(exc, PasswordValidationError):
            logger.info('Not validated password')
        else:
            logger.error(err_msg)
        if debug:
            return JSONResponse(
                content=jsonable_encoder({"detail": expected, "body": received}),
                status_code=400
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request data or parameters.'
        )
    return _handler


async def on_exists_in_db(request: Request, exc: AlreadyExistsError):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Already exists. {exc.detail}',
    )


async def on_auth_error(request: Request, exc: AuthorizationError):
    if exc.silent:
        return JSONResponse(
            content=jsonable_encoder(dict(detail=exc.detail)),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.detail,
    )


async def on_forbidden_error(request: Request, exc: ForbiddenError):
    if exc.silent:
        return JSONResponse(
            content=jsonable_encoder(dict(detail=exc.detail)),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.detail,
    )


async def on_validate_data(request: Request, exc: ValidateDataError | CredentialsError | PasswordValidationError):
    if exc.silent:
        return JSONResponse(
            content=jsonable_encoder(dict(detail=exc.detail)),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=exc.detail,
    )


async def on_not_allowed(request: Request, exc: ActionNotAllowedError):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=exc.detail
    )


class State(TypedDict):
    di_container: DIContainer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    di_container = di_container_factory(
        app_config=AppConfig(),
        redis_config=RedisConfig(),
        pg_config=PgConfig(),
        ch_config=ClickhouseConfig(),
        redis_pool_factory=init_redis_pool,
        http_session_factory=init_http_session,
        pg_engine_factory=init_pg_engine,
        clickhouse_factory=init_clickhouse_client
    )
    redis_pool: ConnectionPool = di_container.resolve(ConnectionPool)
    http_session: aiohttp.ClientSession = di_container.resolve(aiohttp.ClientSession)
    ch_client: ChClient = di_container.resolve(ChClient)
    try:
        yield State(di_container=di_container)
    finally:
        await redis_pool.aclose()
        await http_session.close()
        await ch_client.close()


def init_app(
    app_lifespan,
    allow_origins: list[str],
    debug: bool = False,
) -> FastAPI:
    app = FastAPI(
        lifespan=app_lifespan,
        # openapi_url=None,
        redoc_url=None,
        # docs_url=None,
        debug=debug,
        servers=[
            {'url': 'http://localhost:8000', 'description': 'Local development server'},
        ]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    v1_router = APIRouter(prefix='/api/v1')
    v1_router.include_router(auth_router)
    v1_router.include_router(users_router)
    v1_router.include_router(banks_router)

    app.include_router(v1_router)

    app.exception_handler(RequestValidationError)(on_validation_error(debug))
    app.exception_handler(DoesNotExists)(on_not_found)
    app.exception_handler(AlreadyExistsError)(on_exists_in_db)
    app.exception_handler(AuthorizationError)(on_auth_error)
    app.exception_handler(ValidateDataError)(on_validate_data)
    app.exception_handler(CredentialsError)(on_validate_data)
    app.exception_handler(PasswordValidationError)(on_validate_data)
    app.exception_handler(ActionNotAllowedError)(on_not_allowed)

    return app
