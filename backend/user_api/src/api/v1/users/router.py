from datetime import datetime, date
from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.depends.auth import user_dep
from api.v1.depends.di import di_container_dep
from api.v1.users.schemas import UserSchema, UserTransactionsSchema
from application.users.services import UserStatsService

router = APIRouter(prefix='/users')


def get_stats_service(di_container: di_container_dep):
    return di_container.resolve(UserStatsService)


stats_service_dep = Annotated[UserStatsService, Depends(get_stats_service)]


@router.get('/me/', response_model=UserSchema, tags=['users'])
async def get_me(
    user: user_dep
):
    return user


@router.get('/me/transactions/', tags=['users'], response_model=list[UserTransactionsSchema])
async def get_me_transactions(
    user: user_dep,
    stats_service: stats_service_dep,
    date_from: date | None = None,
    date_to: date | None = None,
    direction: str | None = None  
):
    return await stats_service.get_transactions(
        user.id, date_from=date_from, date_to=date_to, direction=direction
    )

