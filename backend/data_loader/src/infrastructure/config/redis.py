from pydantic import Field
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    broker_db: int = Field(alias="REDIS_BROKER_DB")
    result_backend_db: int = Field(alias="REDIS_RESULT_DB")
    broker_pool_size: int = Field(alias="REDIS_BROKER_POOL_SIZE", default=5)
    result_backend_pool_size: int = Field(alias="REDIS_RESULT_POOL_SIZE", default=5)

    @property
    def broker_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.broker_db}"

    @property
    def result_backend_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.result_backend_db}"
