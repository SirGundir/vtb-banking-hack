from datetime import datetime, date
from dataclasses import dataclass

from pydantic import UUID4

from application.users.dto import UserTransactionsDTO
from infrastructure.repositories.users import UserStatsRepository


@dataclass
class UserStatsService:
    stats_repository: UserStatsRepository

    async def get_transactions(self, user_id: UUID4, date_from: date, date_to: date) -> list[UserTransactionsDTO]:
        transactions = await self.stats_repository.fetch_transactions(
            returning_dto=UserTransactionsDTO,
            user_id=user_id,
            from_dt=date_from.isoformat() if date_from else None,
            to_dt=date_to.isoformat() if date_to else None,
        )
        return transactions
