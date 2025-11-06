from datetime import date

from pydantic import BaseModel, Field
from pydantic.v1 import UUID4


class UserAccountDTO(BaseModel):
    account_id: str = Field(validation_alias='accountId')
    status: str
    currency: str
    account_type: str = Field(validation_alias='accountType')
    account_sub_type: str = Field(validation_alias='accountSubType')
    opening_date: date = Field(validation_alias='openingDate')


class UserDTO(BaseModel):
    id: UUID4
    is_active: bool
    email_verified: bool
    consent_id: str