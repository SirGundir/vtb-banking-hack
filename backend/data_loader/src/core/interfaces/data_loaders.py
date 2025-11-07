from typing import Protocol, NamedTuple

from pydantic import UUID4


class Credentials(NamedTuple):
    access_token: str
    client_id: str
    consent_id: str
    bank_client_id: str
    user_id: UUID4
    bank_id: int


class LoaderInterface(Protocol):

    async def get_page(self, credentials: Credentials, page=None):
        raise NotImplementedError
