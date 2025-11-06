import asyncio
from dataclasses import dataclass
from typing import ClassVar, Any

from aiohttp import ClientSession

from core.dto import UserAccountDTO
from core.interfaces.data_loaders import Credentials
from core.interfaces.users import UserAccountsLoaderInterface
from utils.retry import retry_helper


@dataclass
class HttpLoader:
    http_session: ClientSession
    semaphore: asyncio.Semaphore

    api_url: str

    @retry_helper
    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        async with self.semaphore:
            async with self.http_session.request(
                method,
                f"{self.api_url}/{endpoint}",
                params=params,
                headers=headers
            ) as response:
                return await response.json()


@dataclass
class UserAccountsLoader(UserAccountsLoaderInterface, HttpLoader):
    api_url: str
    endpoint: ClassVar[str] = 'accounts'

    async def get_page(self, credentials: Credentials, page=None) -> list[UserAccountDTO]:
        params = dict(client_id=credentials.client_id)
        headers = {
            'Authorization': f"Bearer {credentials.access_token}",
            'x-consent-id': credentials.consent_id
        }
        data_list = await self._make_request(self.endpoint, params=params, headers=headers)
        return [UserAccountDTO(**data) for data in data_list]
