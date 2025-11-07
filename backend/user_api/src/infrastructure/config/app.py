from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    secret_key: str = Field(alias='SECRET_KEY')
    jwt_algorithm: str = 'HS256'
    jwt_access_expire_min: int = 30 * 60 * 24
    jwt_refresh_expire_min: int = 60 * 24 * 7
    client_id: str = Field(alias='CLIENT_ID')
    client_secret: str = Field(alias='CLIENT_SECRET')