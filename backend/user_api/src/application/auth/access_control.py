from dataclasses import dataclass
from typing import Type

import jwt
from jose import ExpiredSignatureError, JWTError

from application.auth.dto import TokenUserDTO, JwtTokensDTO, CreateUserDTO, UserDTO, LoginDTO, LoginUserDTO, \
    RefreshTokenDTO
from application.auth.exceptions import AuthorizationError, ForbiddenError, CredentialsError
from application.auth.passwords import hash_password, verify_password
from application.auth.tokens import JwtTokensFactory
from core.dto import BaseModelDTO
from infrastructure.blacklist import TokenBlacklist, TokenExpire
from infrastructure.config.app import AppConfig
from infrastructure.db.exceptions import DoesNotExists
from infrastructure.db.repository import IDType
from infrastructure.log import get_logger
from infrastructure.repositories.users import UserRepository
from utils.datetime import utcnow


logger = get_logger(__name__)


@dataclass
class AccessControl:
    config: AppConfig
    user_repository: UserRepository
    blacklist: TokenBlacklist

    user_from_db: bool = False
    admin_only: bool = False

    async def _verify_jwt_token(
        self,
        jwt_token: str,
        returning_dto: Type[BaseModelDTO] | None = None,
    ) -> BaseModelDTO | IDType:
        credentials_exception = AuthorizationError(
            detail="Could not validate credentials",
        )
        access_exception = ForbiddenError()
        if not jwt_token:
            logger.error('verify_jwt_token')
            raise credentials_exception
        if await self.blacklist.has_token(jwt_token):
            raise credentials_exception

        try:
            payload = jwt.decode(
                jwt_token,
                self.config.secret_key,
                algorithms=[self.config.jwt_algorithm]
            )

            user_id = payload.get('id')
            extra_fields = {
                field: payload.get(field)
                for field in TokenUserDTO.model_fields.keys()
                if field != 'id'
            }
            if user_id is None:
                logger.error('verify_jwt_token: User id is None')
                raise credentials_exception
        except ExpiredSignatureError:
            raise credentials_exception
        except JWTError as exc:
            logger.exception(exc)
            raise credentials_exception

        if self.user_from_db:
            try:
                user = await self.user_repository.fetch(
                    returning_dto, id=user_id
                )
            except DoesNotExists as exc:
                logger.error(f'verify_jwt_token: User {user_id} not found')
                raise credentials_exception
        else:
            user = TokenUserDTO(
                id=user_id,
                **extra_fields
            )
        if self.admin_only and not user.is_admin:
            raise access_exception
        return user

    async def signup(
        self,
        user_data: CreateUserDTO,
    ) -> JwtTokensDTO:
        if await self.user_repository.check(email=user_data.email):
            raise AuthorizationError(
                detail=f"Email {user_data.email} is already used",
                status=403,
                silent=True
            )
        create_data = user_data.model_dump()
        create_data['password'] = hash_password(user_data.raw_password, self.config.secret_key)
        create_data['date_joined'] = utcnow()
        user: UserDTO = await self.user_repository.create(create_data, UserDTO)
        # ToDo send verification  email
        return JwtTokensFactory(self.config).make_jwt_tokens(user)

    async def login(
        self,
        credentials: LoginDTO
    ) -> JwtTokensDTO:
        user: LoginUserDTO = await self.user_repository.fetch(
            LoginUserDTO, email=credentials.email, is_active=True
        )
        if not verify_password(credentials.password, user.password):
            raise CredentialsError()
        if self.admin_only and not user.is_admin:
            raise ForbiddenError()
        return JwtTokensFactory(self.config).make_jwt_tokens(user)

    async def logout(self, jwt_tokens: JwtTokensDTO):
        await self._verify_jwt_token(jwt_tokens.access_token)
        await self.blacklist.add_tokens([
            TokenExpire(
                jwt_token=jwt_tokens.access_token,
                expire_min=self.config.jwt_access_expire_min
            ),
            TokenExpire(
                jwt_token=jwt_tokens.refresh_token,
                expire_min=self.config.jwt_refresh_expire_min
            ),
        ])

    async def verify(
        self,
        jwt_token: str,
        returning_dto: Type[BaseModelDTO] = None
    ) -> BaseModelDTO | IDType:
        if not jwt_token:
            raise AuthorizationError()
        return await self._verify_jwt_token(jwt_token, returning_dto)

    async def refresh_token(self, token_data: RefreshTokenDTO) -> JwtTokensDTO:
        user: TokenUserDTO = await self._verify_jwt_token(
            token_data.refresh_token, TokenUserDTO
        )
        await self.blacklist.add_token(token_data.refresh_token, self.config.jwt_refresh_expire_min)
        return JwtTokensFactory(self.config).make_jwt_tokens(user)
