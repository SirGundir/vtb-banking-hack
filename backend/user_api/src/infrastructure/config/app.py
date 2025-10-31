from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    secret_key: str = Field(alias='SECRET_KEY')
    jwt_algorithm: str = 'HS256'
    jwt_access_expire_min: int = 30
    jwt_refresh_expire_min: int = 60 * 24 * 7

