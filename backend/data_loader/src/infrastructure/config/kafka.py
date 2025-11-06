from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaConfig(BaseSettings):
    host: str = Field(alias="KAFKA_HOST")
    port: int = Field(alias="KAFKA_PORT")

    @property
    def broker_url(self) -> str:
        return f"{self.host}:{self.port}"
