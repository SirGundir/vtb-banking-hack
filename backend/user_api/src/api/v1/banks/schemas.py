from pydantic import BaseModel, Field, model_validator, field_validator


class BankSchema(BaseModel):
    id: int
    name: str
