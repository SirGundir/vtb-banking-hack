from faststream import Depends
from pydantic import BaseModel, UUID4

from application.user_accounts.services import UserAccountService
from presentation.worker.depends.cqrs import CommandDependency


async def download_accounts(
    user_id: UUID4,
    user_account_service: UserAccountService = Depends(CommandDependency(UserAccountService))
):
    print(f"Downloading accounts for user {user_id}")
    #accounts = await user_account_service.download_accounts()


async def download_account_transactions():
    pass
