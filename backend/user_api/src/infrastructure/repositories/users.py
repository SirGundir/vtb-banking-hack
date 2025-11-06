from dataclasses import dataclass
from typing import ClassVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models.users import UserModel, ConsentData
from infrastructure.db.repository import SQLAlchemyRepository
from infrastructure.db.utils import update_jsonb


@dataclass
class UserRepository(SQLAlchemyRepository):
    session: AsyncSession

    model: ClassVar[Type[UserModel]] = UserModel
    base_filters: ClassVar[dict] = {'is_active': True}


def update_consents(bank_id: int, consent_data: ConsentData):
    return update_jsonb(
        UserModel.consents,
        {bank_id: dict(consent_data)}
    )
