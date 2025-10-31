from fastapi import APIRouter

from api.v1.depends.auth import user_dep
from api.v1.users.schemas import UserSchema

router = APIRouter(prefix='/users')


@router.get('/me/', response_model=UserSchema, tags=['users'])
async def get_me(
    user: user_dep
):
    return user