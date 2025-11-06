from pydantic import UUID4, BaseModel, Field, computed_field

from application.auth.dto import ConsentDataDTO


class UserSchema(BaseModel):
    id: UUID4
    email: str
    language: str
    first_name: str | None = Field(default=None, serialization_alias='firstName')
    last_name: str | None = Field(default=None, serialization_alias='lastName')
    email_verified: bool = Field(default=False, serialization_alias='emailVerified')

    consents: dict[int, ConsentDataDTO] = Field(exclude=True)

    @computed_field
    @property
    def connectedBanks(self) -> list[int]:
        return list(self.consents.keys())

