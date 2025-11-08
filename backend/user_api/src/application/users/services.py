from datetime import datetime
from dataclasses import dataclass

from pydantic import UUID4

from infrastructure.repositories.users import UserStatsRepository


@dataclass
class UserStatsService:
    stats_repository: UserStatsRepository

    async def get_transactions(self, user_id: UUID4, from_dt: datetime, to_dt: datetime):
        transactions = await self.stats_repository.fetch_transactions(
            user_id=user_id,
            from_dt=from_dt.strftime('%Y-%m-%d %H:%M:%S'),
            to_dt=to_dt.strftime('%Y-%m-%d %H:%M:%S'),
        )
        print(f">>>{transactions=}")
        return transactions
