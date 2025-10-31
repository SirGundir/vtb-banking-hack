from pydantic import Field
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
