from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.depends.db import unit_of_work_dep, db_session_dep
from api.v1.depends.di import di_container_dep
from application.auth.services.password import PasswordService


def get_password_command(
    uow: unit_of_work_dep,
    di_container: di_container_dep
) -> PasswordService:
    return di_container.resolve(
        PasswordService,
        depends={AsyncSession: uow.session},
    )


password_command_dep = Annotated[PasswordService, Depends(get_password_command)]


def get_password_query(
    session: db_session_dep,
    di_container: di_container_dep,
) -> PasswordService:
    return di_container.resolve(
        PasswordService,
        depends={AsyncSession: session},
    )


password_query_dep = Annotated[PasswordService, Depends(get_password_query)]