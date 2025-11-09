from datetime import date, datetime
from enum import Enum

from pydantic import UUID4, BaseModel, Field, computed_field

from application.auth.dto import ConsentDataDTO

class TransactionDirection(str, Enum):
    CREDIT = "Credit"
    DEBIT = "Debit"

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


class UserTransactionsSchema(BaseModel):
    user_id: UUID4 = Field(serialization_alias='userId')
    bank_id: int= Field(serialization_alias='userId')
    status: str
    currency: str
    amount: float
    booking_dt: datetime = Field(serialization_alias='bookingDt')
    value_dt: datetime = Field(serialization_alias='valueDt')
    transaction_info: str = Field(serialization_alias='transactionInfo')
    direction: TransactionDirection 
