from pydantic import Field
from pydantic_settings import BaseSettings


class ClickhouseConfig(BaseSettings):
    host: str = Field(alias="CLICKHOUSE_HOST")
    port: int = Field(alias="CLICKHOUSE_PORT")
    user: str = Field(alias="CLICKHOUSE_USER")
    password: str = Field(alias="CLICKHOUSE_PASSWORD")
    limit: int = Field(alias="CLICKHOUSE_CONNECTION_LIMIT", default=100)
    keepalive_timeout: int = Field(alias="CLICKHOUSE_CONNECTION_TIMEOUT", default=60)

    @property
    def connection_config(self) -> dict:
        return dict(
            limit=self.limit,
            keepalive_timeout=self.keepalive_timeout
        )

    @property
    def clickhouse_params(self) -> dict:
        return dict(
            url=f"http://{self.host}:{self.port}/",
            user=self.user,
            password=self.password
        )