from dataclasses import dataclass

from pydantic.v1 import UUID4

from core.dto import UserDTO
from core.interfaces.data_loaders import Credentials
from core.interfaces.repositories import UserRepositoryInterface
from core.interfaces.users import UserAccountsLoaderInterface
from infrastructure.config.app import AppConfig


@dataclass
class UserAccountService:
    user_repository: UserRepositoryInterface
    accounts_loader: UserAccountsLoaderInterface
    config: AppConfig

    async def download_accounts(self, user_id: UUID4):
        user = await self.user_repository.fetch(returning_dto=UserDTO, id=user_id)
        credentials = Credentials(
            access_token=self.config.access_token,
            client_id=self.config.access_token,
            consent_id=user.consent_id
        )
        accounts = await self.accounts_loader.get_page(credentials)
        return account