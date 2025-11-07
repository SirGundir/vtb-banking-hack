import asyncio
from dataclasses import dataclass
from typing import ClassVar, Any

from aiohttp import ClientSession, ClientError

from core.dto import UserAccountDTO, AccountBalanceDTO
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


@dataclass
class UserAccountsLoader(HttpLoader):
    endpoint: ClassVar[str] = 'accounts'

    async def get_page(self, credentials: Credentials, page=None) -> list[UserAccountDTO]:
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

    async def get_account_balance(self, account_id: str, credentials: Credentials) -> AccountBalanceDTO:
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

        print(f">>>{response=}")
        #
        # if not (accounts := response.get('data', {}).get('account')):
        #     raise DownloadError(self.endpoint, str(response))
        #
        # return [UserAccountDTO(user_id=credentials.user_id, bank_id=credentials.bank_id, **data) for data in accounts]

