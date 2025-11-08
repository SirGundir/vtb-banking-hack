from dataclasses import dataclass
from typing import ClassVar, Type

from aiochclient import ChClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.dto import BaseModelDTO
from core.interfaces.repository import RepositoryInterface
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

def delete_consent(bank_id: int):
    return UserModel.consents.op('-')(str(bank_id))


@dataclass
class UserStatsRepository(RepositoryInterface):
    ch_client: ChClient

    async def fetch_transactions(self, returning_dto: Type[BaseModelDTO], **filters) -> list[BaseModelDTO]:
        user_id = filters['user_id']
        from_dt = filters.get("from_dt")
        to_dt = filters.get("to_dt")

        filter_stmt = ''
        if from_dt and to_dt:
            filter_stmt = f"AND booking_dt BETWEEN toDateTime('{from_dt}') AND toDateTime('{to_dt}')"

        elif from_dt:
            filter_stmt  = f"AND booking_dt >= toDateTime('{from_dt}')"

        elif to_dt:
            filter_stmt = f"AND booking_dt <= toDateTime('{to_dt}')"

        sql = """
            SELECT  
                user_id,
                bank_id,
                account_id,
                status,
                transaction_info,
                currency,
                amount,
                bank_transaction_code,
                booking_dt,
                value_dt
            FROM transactions FINAL
            WHERE user_id = '{user_id}'
            {filter_stmt}
            ORDER BY booking_dt DESC
        """.format(user_id=user_id, filter_stmt=filter_stmt)

        #print(f">>{sql}")
        records = await self.ch_client.fetch(sql)
        return [returning_dto(**record) for record in records]


def update_consents(bank_id: int, consent_data: ConsentData):
    return update_jsonb(
        UserModel.consents,
        {bank_id: dict(consent_data)}
    )

def delete_consent(bank_id: int):
    return UserModel.consents.op('-')(str(bank_id))