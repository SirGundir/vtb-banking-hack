from dataclasses import dataclass

from pydantic import UUID4

from application.user_accounts.dto import BankDTO
from core.dto import UserDTO, UserAccountDTO
from core.interfaces.data_loaders import Credentials
from infrastructure.data_loaders.accounts import UserAccountsLoader
from infrastructure.repositories.banks import BankRepository
from infrastructure.repositories.users import UserRepository


@dataclass
class UserAccountService:
    user_repository: UserRepository
    bank_repository: BankRepository
    accounts_loader: UserAccountsLoader

    async def download_accounts(self, user_id: UUID4, bank_id: int) -> list[UserAccountDTO]:
        bank: BankDTO = await self.bank_repository.fetch(returning_dto=BankDTO, id=bank_id)
        user: UserDTO = await self.user_repository.fetch(returning_dto=UserDTO, id=user_id)
        credentials = Credentials(
            access_token=bank.access_token,
            client_id=bank.client_id,
            consent_id=user.consents[bank_id].consent_id,
            bank_client_id=user.consents[bank_id].bank_client_id,
            user_id=user_id,
            bank_id=bank_id
        )
        return await self.accounts_loader.with_api_url(bank.api_url).get_page(credentials)

    async def download_balance(self, user_id: UUID4, bank_id: int, account_id: str):
        bank: BankDTO = await self.bank_repository.fetch(returning_dto=BankDTO, id=bank_id)
        user: UserDTO = await self.user_repository.fetch(returning_dto=UserDTO, id=user_id)
        credentials = Credentials(
            access_token=bank.access_token,
            client_id=bank.client_id,
            consent_id=user.consents[bank_id].consent_id,
            bank_client_id=user.consents[bank_id].bank_client_id,
            user_id=user_id,
            bank_id=bank_id
        )
        return await self.accounts_loader.with_api_url(bank.api_url).get_account_balance(account_id, credentials)