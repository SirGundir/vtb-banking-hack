from pydantic import UUID4, BaseModel, Field


class UserSchema(BaseModel):
    id: UUID4
    email: str
    language: str
    first_name: str | None = Field(default=None, serialization_alias='firstName')
    email_verified: bool = Field(default=False, serialization_alias='emailVerified')