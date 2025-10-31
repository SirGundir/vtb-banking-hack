from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.auth.depends import password_command_dep, password_query_dep
from api.v1.auth.schemas import JwtTokensSchema
from api.v1.depends.auth import access_control_factory, user_dep
from api.v1.schemas import OkResponseSchema
from application.auth.services.access_control import AccessControl
from application.auth.dto import CreateUserDTO, LoginDTO, JwtTokensDTO, ChangePasswordDTO, SetPasswordDTO, \
    ResetPasswordDTO

router = APIRouter(prefix='/auth')


@router.post('/signup/', response_model=JwtTokensSchema, tags=['auth'])
async def signup(
    register_data: CreateUserDTO,
    access_control: Annotated[
        AccessControl,
        Depends(access_control_factory(
            user_from_db=True,
            use_uow=True,
        ))
    ],
):
    return await access_control.signup(register_data)


@router.post('/login/', response_model=JwtTokensSchema, tags=['auth'])
async def login(
    access_control: Annotated[
        AccessControl, Depends(access_control_factory(user_from_db=True))
    ],
    credentials: LoginDTO,
):
    return await access_control.login(credentials)



@router.post('/logout/', tags=['auth'])
async def logout(
    access_control: Annotated[
        AccessControl, Depends(access_control_factory())
    ],
    jwt_tokens: JwtTokensDTO
) -> OkResponseSchema:
    await access_control.logout(jwt_tokens)
    return OkResponseSchema()


@router.post('/change-password/', tags=['auth'], response_model=OkResponseSchema)
async def change_password(
    user: user_dep,
    password_service: password_command_dep,
    passwords: ChangePasswordDTO,
) -> OkResponseSchema:
    await password_service.change_password(user, passwords)
    return OkResponseSchema()


@router.post('/reset/start/', tags=['auth'])
async def start_reset_password(
    password_service: password_query_dep,
    reset_data: ResetPasswordDTO,
) -> OkResponseSchema:
    await password_service.request_reset_password(reset_data)
    return OkResponseSchema()


@router.post('/reset/finish/{uidb64}/{token}/', tags=['auth'])
async def reset_password(
    password_service: password_command_dep,
    uidb64: str,
    token: str,
    password_data: SetPasswordDTO,
) -> OkResponseSchema:
    await password_service.reset_password(uidb64, token, password_data)
    return OkResponseSchema()
