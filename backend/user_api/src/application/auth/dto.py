import base64
from typing import Annotated

from jwt.utils import force_bytes
from pydantic import UUID4, EmailStr, Field, BeforeValidator, field_validator, BaseModel, model_validator

from application.auth.passwords import validate_password, generate_password
from application.language import LANGUAGES
from core.dto import BaseModelDTO
from utils.multilang import LanguageCode
from utils.strings import strip_and_lower


class TokenUserDTO(BaseModelDTO):
    id: UUID4
    is_admin: bool = False
    language: LanguageCode = 'ru'
    email_verified: bool = False
    is_active: bool | None = True


class UserDTO(TokenUserDTO):
    email: EmailStr
    banned_email: bool = False
    password: str | None = Field(exclude=True)
    first_name: str | None = None
    last_name: str | None = None

    @property
    def has_password(self):
        return bool(self.password)

    @property
    def is_email_valid(self):
        return self.email_verified

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @property
    def uidb64(self):
        return base64.b64encode(force_bytes(str(self.id))).decode()


class RefreshTokenDTO(BaseModelDTO):
    refresh_token: str


EmailStrLower = Annotated[
    EmailStr,
    BeforeValidator(strip_and_lower),
]


class LoginDTO(BaseModelDTO):
    email: EmailStrLower
    password: str


class LoginUserDTO(TokenUserDTO):
    password: str


class ChangePasswordDTO(BaseModelDTO):
    current_password: str
    new_password: str


class SetPasswordDTO(BaseModelDTO):
    password: str

    @classmethod
    @field_validator('password')
    def validate_new_password(cls, password):
        validate_password(password)
        return password


class ResetPasswordDTO(BaseModelDTO):
    email: EmailStrLower


class JwtTokensDTO(BaseModelDTO):
    access_token: str
    refresh_token: str
    frontend_slug: str | None


class CreateUserDTO(BaseModel):
    email: EmailStrLower
    raw_password: str | None = Field(default=None, validation_alias='password')
    first_name: str | None = Field(default=None, validation_alias='firstName')
    last_name: str | None = Field(default=None, validation_alias='lastName')
    language: str = 'ru'

    @model_validator(mode='after')
    def validate_raw_password(self) -> 'CreateUserDTO':
        if self.raw_password is not None:
            validate_password(self.raw_password)
        self.raw_password = self.raw_password or generate_password()
        return self

    @classmethod
    @field_validator('language')
    def check_language(cls, language: str) -> str:
        if language and LANGUAGES.validate_code(language):
            return LANGUAGES.validate_code(language)
        return language