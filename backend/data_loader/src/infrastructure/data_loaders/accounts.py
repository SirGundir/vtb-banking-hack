from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from aiohttp import ClientError
from pydantic import BaseModel, Field

from core.dto import UserAccountDTO, AccountBalanceDTO, AccountTransactionDTO
from core.interfaces.data_loaders import Credentials
from infrastructure.data_loaders.http import HttpLoader, DownloadError, PaginatedResponse


class TransactionsQueryParams(BaseModel):
    from_dt: datetime | None = Field(serialization_alias='from_booking_date_time', default=None)
    to_dt: datetime | None = Field(serialization_alias='to_booking_date_time', default=None)
    page: int = 1
    limit: int = 100

    @property
    def as_request_params(self) -> dict:
        return self.model_dump(exclude_none=True, by_alias=True)


@dataclass
class UserAccountsLoader(HttpLoader):
    endpoint: ClassVar[str] = 'accounts'

    async def get_accounts(self, credentials: Credentials, page=None) -> list[UserAccountDTO]:
        params = dict(client_id=credentials.bank_client_id)
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'X-Consent-Id': credentials.consent_id,
            'X-Requesting-Bank': credentials.client_id
        }
        try:
            response = await self._make_request(self.endpoint, params=params, headers=headers)
        except ClientError as exc:
            raise DownloadError(self.endpoint) from exc

        if error := response.get('error'):
            raise DownloadError(self.endpoint, error)

        if not (accounts := response.get('data', {}).get('account')):
            raise DownloadError(self.endpoint, str(response))

        return [UserAccountDTO(user_id=credentials.user_id, bank_id=credentials.bank_id, **data) for data in accounts]

    async def get_account_balances(self, account_id: str, credentials: Credentials) -> list[AccountBalanceDTO]:
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'X-Consent-Id': credentials.consent_id,
            'X-Requesting-Bank': credentials.client_id
        }
        try:
            response = await self._make_request(
                f"{self.endpoint}/{account_id}/balances",
                headers=headers
            )
        except ClientError as exc:
            raise DownloadError(self.endpoint) from exc

        if error := response.get('error'):
            raise DownloadError(self.endpoint, error)

        if not (balances := response.get('data', {}).get('balance')):
            raise DownloadError(self.endpoint, str(response))

        return [
            AccountBalanceDTO(user_id=credentials.user_id, bank_id=credentials.bank_id, **data)
            for data in balances
        ]

    async def get_account_transactions(
        self,
        account_id: str,
        credentials: Credentials,
        query_params: TransactionsQueryParams
    ) -> PaginatedResponse:
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'X-Consent-Id': credentials.consent_id,
            'X-Requesting-Bank': credentials.client_id
        }
        try:
            response = await self._make_request(
                f"{self.endpoint}/{account_id}/transactions",
                headers=headers,
                params=query_params.as_request_params
            )
        except ClientError as exc:
            raise DownloadError(self.endpoint) from exc

        if error := response.get('error'):
            raise DownloadError(self.endpoint, error)

        transactions = [
            AccountTransactionDTO(user_id=credentials.user_id, bank_id=credentials.bank_id, **data)
            for data in response.get('data', {}).get('transaction')
        ]
        total_pages = response.get('meta', {}).get('totalPages', 0)
        next_page =  query_params.page + 1 if query_params.page < total_pages else None

        return PaginatedResponse(
            data=transactions, next_page=next_page
        )

