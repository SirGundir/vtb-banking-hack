from pydantic import BaseModel


class OkResponseSchema(BaseModel):
    status: str | bool = 'ok'