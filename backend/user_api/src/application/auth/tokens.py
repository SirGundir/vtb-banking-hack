from dataclasses import dataclass
from datetime import timedelta, datetime

from jose import jwt

from application.auth.dto import UserDTO, TokenUserDTO, JwtTokensDTO
from infrastructure.config.app import AppConfig
from utils.datetime import utcnow


@dataclass
class JwtTokensFactory:
    config: AppConfig

    def _make_token(
        self,
        payload: dict,
        expire: datetime,
        salt: str | None = None
    ) -> str:
        salt = salt or self.config.secret_key
        payload['exp'] = expire
        return jwt.encode(
            payload,
            salt,
            algorithm=self.config.jwt_algorithm
        )

    def make_jwt_tokens(
        self,
        user: UserDTO | TokenUserDTO,
        salt: str | None = None,
    ) -> JwtTokensDTO:
        include = TokenUserDTO.model_fields.keys()
        access_token_expires = timedelta(minutes=self.config.jwt_access_expire_min)
        access_expire = utcnow() + access_token_expires
        refresh_token_expires = timedelta(minutes=self.config.jwt_refresh_expire_min)
        refresh_expire = utcnow() + refresh_token_expires
        return JwtTokensDTO(
            accessToken=self._make_token(
                user.model_dump(mode='json', include=include),
                access_expire,
                salt
            ),
            refreshToken=self._make_token(
                user.model_dump(mode='json', include=include),
                refresh_expire,
                salt
            )
        )