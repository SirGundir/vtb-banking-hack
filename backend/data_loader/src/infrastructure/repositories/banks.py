from dataclasses import dataclass
from typing import ClassVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models.banks import BankModel
from infrastructure.db.repository import SQLAlchemyRepository


@dataclass
class BankRepository(SQLAlchemyRepository):
    model: ClassVar[Type[BankModel]] = BankModel
    base_filters: ClassVar[dict] = {'is_active': True}
