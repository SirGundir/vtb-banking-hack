from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class ProductIn(BaseModel):
    bank: str
    productId: str
    productType: str
    productName: str
    description: Optional[str]
    interestRate: Optional[float]
    minAmount: Optional[float]
    maxAmount: Optional[float]
    termMonths: Optional[int]

class ProductOut(BaseModel):
    product_id: str
    bank: str
    product_type: str
    product_name: str
    description: Optional[str]
    interest_rate: Optional[float]
    min_amount: Optional[float]
    max_amount: Optional[float]
    term_months: Optional[int]

    class Config:
        orm_mode = True

class BalanceItem(BaseModel):
    accountId: str
    type: Optional[str]
    dateTime: Optional[datetime]
    amount: Any

class TransactionItem(BaseModel):
    accountId: str
    transactionId: str
    amount: Any
    creditDebitIndicator: str
    status: str
    bookingDateTime: Optional[datetime]
    valueDateTime: Optional[datetime]
    transactionInformation: Optional[str]
    bankTransactionCode: Optional[dict]

class RecommendationOut(BaseModel):
    product_id: str
    score: float
    reason: Optional[str]

class FeedbackIn(BaseModel):
    product_id: str
    accepted: bool