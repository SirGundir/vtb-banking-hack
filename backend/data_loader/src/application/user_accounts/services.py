from dataclasses import dataclass
from datetime import datetime
from typing import AsyncGenerator

from pydantic import UUID4, BaseModel

from application.user_accounts.dto import BankDTO
from core.dto import UserDTO, UserAccountDTO, AccountBalanceDTO
from core.interfaces.data_loaders import Credentials
from infrastructure.data_loaders.accounts import UserAccountsLoader, TransactionsQueryParams
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
        return await self.accounts_loader.with_api_url(bank.api_url).get_accounts(credentials)

    async def download_balance(self, user_id: UUID4, bank_id: int, account_id: str) -> list[AccountBalanceDTO]:
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
        return await self.accounts_loader.with_api_url(bank.api_url).get_account_balances(account_id, credentials)

    async def download_transactions(
        self,
        user_id: UUID4,
        bank_id: int,
        account_id: str,
        query_params: TransactionsQueryParams | None = None
    ) -> AsyncGenerator[list[AccountBalanceDTO]]:
        query_params = query_params or TransactionsQueryParams()
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
        while True:
            resp = await self.accounts_loader.with_api_url(bank.api_url).get_account_transactions(
                account_id,
                credentials,
                query_params=query_params
            )
            yield resp.data

            if not resp.next_page:
                break

            query_params.page = resp.next_page
