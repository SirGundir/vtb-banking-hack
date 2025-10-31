from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.depends.db import db_session_dep, unit_of_work_dep
from api.v1.depends.di import di_container_dep
from application.auth.services.access_control import AccessControl
from application.auth.dto import TokenUserDTO, UserDTO
from infrastructure.di.di_container import DIContainer


def init_access_control(
    di_container: DIContainer,
    session: AsyncSession,
    user_from_db: bool = False,
    admin_only: bool = False,
):
    return di_container.resolve(
        AccessControl,
        depends={AsyncSession: session},
        options=dict(
            user_from_db=user_from_db,
            admin_only=admin_only,
        )
    )


def access_control_factory(
    user_from_db: bool = False,
    use_uow: bool = False,
    admin_only: bool = False,
):
    """Provide use_uow if you need to commit, else just session. """
    def _with_uow(
        di_container: di_container_dep,
        uow: unit_of_work_dep,
    ):
        return init_access_control(
            di_container=di_container,
            session=uow.session,
            user_from_db=user_from_db,
            admin_only=admin_only,
        )

    def _with_session(
        di_container: di_container_dep,
        session: db_session_dep,
    ):
        return init_access_control(
            di_container=di_container,
            session=session,
            user_from_db=user_from_db,
            admin_only=admin_only,
        )

    return _with_uow if use_uow else _with_session


access_control_dep = Annotated[AccessControl, Depends(access_control_factory())]


header_security = HTTPBearer(auto_error=False)
HeaderAuthorizationDeps = Annotated[
    None | HTTPAuthorizationCredentials, Depends(header_security)]


def get_auth(header_auth: HeaderAuthorizationDeps) -> str | None:
    return header_auth.credentials


auth_token_dep = Annotated[None | str, Depends(get_auth)]


async def verify_user(
    authorization: auth_token_dep,
    access_control: Annotated[
        AccessControl, Depends(access_control_factory(use_uow=False))
    ],
) -> TokenUserDTO:
    return await access_control.verify(authorization, TokenUserDTO)


async def get_user(
    authorization: auth_token_dep,
    access_control: Annotated[
        AccessControl, Depends(access_control_factory(
            use_uow=False,
            user_from_db=True)
        )
    ],
) -> UserDTO:
    return await access_control.verify(authorization, UserDTO)


token_user_dep = Annotated[TokenUserDTO, Depends(verify_user)]

user_dep = Annotated[UserDTO, Depends(get_user)]
