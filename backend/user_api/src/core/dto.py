from pydantic import BaseModel, ConfigDict


class BaseModelDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
