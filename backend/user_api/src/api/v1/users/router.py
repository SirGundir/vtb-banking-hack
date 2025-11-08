from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.depends.auth import user_dep
from api.v1.depends.di import di_container_dep
from api.v1.users.schemas import UserSchema
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


@router.get('/me/transactions/', tags=['users'])
async def get_me_transactions(
    user: user_dep,
    stats_service: stats_service_dep,
    from_dt: datetime | None = None,
    to_dt: datetime | None = None,
):
    return await stats_service.get_transactions(user.id, from_dt=from_dt, to_dt=to_dt)
