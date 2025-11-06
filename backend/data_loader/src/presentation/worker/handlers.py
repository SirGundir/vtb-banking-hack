from faststream import Depends
from pydantic import BaseModel

from application.user_accounts.services import UserAccountService
from presentation.worker.depends.cqrs import CommandDependency


async def download_accounts(
    user_id: int,
    user_account_service: UserAccountService = Depends(CommandDependency(UserAccountService))
):
    accounts = await user_account_service.download_accounts()


async def download_account_transactions():
    pass
