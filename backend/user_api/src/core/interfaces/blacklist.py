from typing import NamedTuple


class TokenExpire(NamedTuple):
    jwt_token: str
    expire_min: int


class BlacklistInterface:
    async def has_token(self, jwt_token: str):
        raise NotImplementedError

    async def add_token(self, jwt_token: str, expire_min: int):
        raise NotImplementedError

    async def add_tokens(self, jwt_tokens_expire: list[TokenExpire]):
        raise NotImplementedError
