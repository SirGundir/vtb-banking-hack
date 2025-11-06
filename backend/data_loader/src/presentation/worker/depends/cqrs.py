from typing import Type

from faststream import Context
from sqlalchemy.ext.asyncio import AsyncSession

from presentation.worker.depends.db import unit_of_work_dep, db_session_dep


class CQRSDependency:
    def __init__(self, resolve_cls: Type):
        self.resolve_cls = resolve_cls


class CommandDependency(CQRSDependency):

    def __call__(
        self,
        uow: unit_of_work_dep,
        di_container=Context()
    ):
        return di_container.resolve(
            self.resolve_cls,
            depends={AsyncSession: uow.session},
        )


class QueryDependency(CQRSDependency):

    def __call__(
        self,
        session: db_session_dep,
        di_container=Context()
    ):
        return di_container.resolve(
            self.resolve_cls,
            depends={AsyncSession: session},
        )