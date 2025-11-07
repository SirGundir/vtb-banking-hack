import asyncio
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession
from pydantic import BaseModel

from utils.retry import retry_helper


NOT_SET_URL = 'NOT_SET_URL'


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


class DownloadError(Exception):
    def __init__(self, endpoint, message=''):
        super().__init__(f"Error to download data from {endpoint}, {message}")
        self.endpoint = endpoint


class PaginatedResponse(BaseModel):
    data: Any
    next_page: int | None = None
