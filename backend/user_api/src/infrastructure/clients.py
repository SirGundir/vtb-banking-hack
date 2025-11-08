from dataclasses import dataclass
from typing import Any, NamedTuple

from aiohttp import ClientSession, ClientError
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_exponential
from websockets import Protocol


class ConsentRequest(NamedTuple):
    bank_client_id: str
    client_id: str
    client_secret: str
    access_token: str


class BankAuthError(Exception):
    """Error to get access token"""


class GetConsentError(Exception):
    """Error to get consent"""


NOT_SET_URL = 'NOT_SET_URL'


class BankOpenApiInterface(Protocol):
    api_url: str = NOT_SET_URL

    def with_api_url(self, api_url: str):
        self.api_url = api_url
        return self

    async def get_bank_token(self, client_id: str, client_secret: str) -> str:
        raise NotImplementedError

    async def create_consent(self, request: ConsentRequest):
        raise NotImplementedError

    async def get_consent_status(self):
        raise NotImplementedError

    async def delete_consent(self, consent_id: str):
        raise NotImplementedError


retry_helper = retry(
    retry=retry_if_exception_type(ClientError),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=3),
    reraise=True
)


@dataclass
class HttpBankClient(BankOpenApiInterface):
    http_session: ClientSession

    @retry_helper
    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        **kwargs
    ) -> Any:
        assert self.api_url != NOT_SET_URL
        async with self.http_session.request(
            method,
            f"{self.api_url}/{endpoint}",
            params=params,
            headers=headers,
            **kwargs
        ) as response:
            return await response.json()

    async def get_bank_token(self, client_id: str, client_secret: str) -> str:
        params = {
            'client_id': client_id,
            'client_secret': client_secret
        }
        try:
            data = await self._make_request('auth/bank-token', method='POST', params=params)
        except ClientError as exc:
            raise BankAuthError() from exc

        if not (access_token := data.get('access_token')):
            raise BankAuthError(f"No token {data}")

        return data

    async def create_consent(self, request: ConsentRequest) -> str:
        headers = {
            'Authorization': f"Bearer {request.access_token}",
            'X-Requesting-Bank': request.client_id
        }
        payload = {
          "client_id": request.bank_client_id,
          "permissions": ["ReadAccountsDetail", "ReadBalances", "ReadTransactionsDetail"],
          "reason": "Агрегация счетов для HackAPI",
          "requesting_bank": request.client_id,
          "requesting_bank_name": "Team 221 App"
        }
        try:
            data = await self._make_request(
                'account-consents/request',
                method='POST',
                headers=headers,
                json=payload
            )
        except ClientError as exc:
            raise GetConsentError(f"Cant create consent") from exc

        if data.get('status') != 'approved':
            raise GetConsentError(str(data))

        return data.get('consent_id')

    async def delete_consent(self, consent_id: str):
        try:
            await self._make_request(
                f'account-consents/{consent_id}',
                method='DELETE',
            )
        except ClientError as exc:
            raise GetConsentError(f"Cant delete {consent_id=}") from exc
