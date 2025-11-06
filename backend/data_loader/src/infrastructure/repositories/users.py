from dataclasses import dataclass
from typing import ClassVar, Type

from infrastructure.db.base import Base
from infrastructure.db.models.users import UserModel
from infrastructure.db.repository import SQLAlchemyRepository


@dataclass
class UserRepository(SQLAlchemyRepository):
    model: ClassVar[Type[Base]] = UserModel
