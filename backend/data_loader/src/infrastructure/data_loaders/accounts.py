import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Any

from aiohttp import ClientSession, ClientError
from pydantic import BaseModel, Field

from core.dto import UserAccountDTO, AccountBalanceDTO, AccountTransactionDTO
from core.interfaces.data_loaders import Credentials
from utils.retry import retry_helper


NOT_SET_URL = 'NOT_SET_URL'


class DownloadError(Exception):
    def __init__(self, endpoint, message=''):
        super().__init__(f"Error to download data from {endpoint}, {message}")
        self.endpoint = endpoint


@dataclass
class HttpLoader:
    http_session: ClientSession
    semaphore: asyncio.Semaphore

    api_url: str = NOT_SET_URL

    def with_api_url(self, api_url: str):
        self.api_url = api_url
        return self

    @retry_helper
    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        assert self.api_url != NOT_SET_URL
        async with self.semaphore:
            async with self.http_session.request(
                method,
                f"{self.api_url}/{endpoint}",
                params=params,
                headers=headers
            ) as response:
                return await response.json()


class TransactionsQueryParams(BaseModel):
    from_dt: datetime | None = Field(serialization_alias='from_booking_date_time', default=None)
    to_dt: datetime | None = Field(serialization_alias='to_booking_date_time', default=None)
    page: int = 1
    limit: int = 100

    @property
    def as_request_params(self) -> dict:
        return self.model_dump(exclude_none=True, by_alias=True)


class PaginatedResponse(BaseModel):
    data: Any
    next_page: int | None = None


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

        if error := response.get('response'):
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

        if error := response.get('response'):
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

        if error := response.get('response'):
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

