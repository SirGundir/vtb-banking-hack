from core.interfaces.blacklist import TokenExpire, BlacklistInterface
from infrastructure.cache.base import BaseAsyncCache


class TokenBlacklist(BlacklistInterface, BaseAsyncCache):

    def _get_key(self, token: str) -> str:
        return f'token_blacklist_{token}'

    async def has_token(self, jwt_token: str):
        async with self.get_connection() as conn:
            return bool(await conn.get(self._get_key(jwt_token)))

    async def add_token(self, jwt_token: str, expire_min: int):
        async with self.get_connection() as conn:
            await conn.set(self._get_key(jwt_token), jwt_token, ex=expire_min * 60)

    async def add_tokens(self, jwt_tokens_expire: list[TokenExpire]):
        async with self.get_connection() as conn:
            async with conn.pipeline() as pipe:
                for token_exp in jwt_tokens_expire:
                    await pipe.set(
                        self._get_key(token_exp.jwt_token),
                        token_exp.jwt_token,
                        ex=token_exp.expire_min * 60
                    )
                await pipe.execute()