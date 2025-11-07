import json
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, field_serializer
from pydantic import UUID4


class BaseModelDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserAccountDTO(BaseModelDTO):
    user_id: UUID4
    bank_id: int
    account_id: str = Field(validation_alias='accountId')
    status: str
    currency: str
    account_type: str = Field(validation_alias='accountType')
    account_sub_type: str = Field(validation_alias='accountSubType')
    opening_date: date = Field(validation_alias='openingDate')


class AccountBalanceDTO(BaseModelDTO):
    account_id: str = Field(validation_alias='accountId')
    user_id: UUID4
    bank_id: int
    currency: str
    balance_type: str = Field(validation_alias='type')
    amount: Decimal = 0
    credit_debit_indicator: str = Field(validation_alias='creditDebitIndicator')
    balance_at_datetime: datetime = Field(validation_alias='dateTime')

    @field_serializer('balance_at_datetime')
    def serialize_balance_at_datetime(self, v: datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')

    @model_validator(mode='before')
    @classmethod
    def extract_amount(cls, data: dict) -> dict:
        if amount_data := data.pop('amount', {}):
            data['amount'] = amount_data['amount']
            data['currency'] = amount_data['currency']
        return data



class ConsentDataDTO(BaseModelDTO):
    bank_client_id: str
    consent_id: str


class UserDTO(BaseModelDTO):
    id: UUID4
    is_active: bool
    email_verified: bool
    consents: dict[int, ConsentDataDTO]

    @field_validator('consents', mode='before')
    @classmethod
    def convert_to_dto(cls, value: dict[int, str | dict]):
        consents = {}
        for bank_id, data in value.items():
            if isinstance(data, str):
                data = json.loads(data)
            consents[int(bank_id)] = ConsentDataDTO(**data)
        return consents