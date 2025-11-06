from typing import Protocol, NamedTuple


class Credentials(NamedTuple):
    access_token: str
    client_id: str
    consent_id: str


class LoaderInterface(Protocol):

    async def get_page(self, credentials: Credentials, page=None):
        raise NotImplementedError
