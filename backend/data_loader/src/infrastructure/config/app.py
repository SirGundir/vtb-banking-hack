from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    access_token: str = Field(alias="VBANK_ACCESS_TOKEN")
    client_id: int = Field(alias="CLIENT_ID")
