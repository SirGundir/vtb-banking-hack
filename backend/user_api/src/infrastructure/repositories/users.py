from dataclasses import dataclass
from typing import ClassVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models.users import UserModel
from infrastructure.db.repository import SQLAlchemyRepository


@dataclass
class UserRepository(SQLAlchemyRepository):
    session: AsyncSession

    model: ClassVar[Type[UserModel]] = UserModel
    base_filters: ClassVar[dict] = {'is_active': True}
