from typing import Annotated, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from fastapi import Depends

from api.v1.depends.di import di_container_dep
from infrastructure.db.session import get_session
from infrastructure.unit_of_work import UnitOfWork
from log import get_logger

logger = get_logger(__name__)


async def get_db(di_container: di_container_dep):
    async_session = get_session(di_container.resolve(AsyncEngine))
    async with async_session() as session:
        yield session


db_session_dep = Annotated[AsyncSession, Depends(get_db)]


async def get_unit_of_work(session: db_session_dep) -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork(session) as uow:
        yield uow


unit_of_work_dep = Annotated[UnitOfWork, Depends(get_unit_of_work)]
