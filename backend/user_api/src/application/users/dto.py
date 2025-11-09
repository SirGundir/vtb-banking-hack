from datetime import datetime
from decimal import Decimal

from pydantic import UUID4

from core.dto import BaseModelDTO
from enum import Enum

class TransactionDirection(str, Enum):
    CREDIT = "Credit"
    DEBIT = "Debit"

class UserTransactionsDTO(BaseModelDTO):
    user_id: UUID4
    bank_id: int
    status: str
    currency: str
    amount: Decimal
    booking_dt: datetime
    value_dt: datetime
    transaction_info: str
    direction: TransactionDirection
