from pydantic import BaseModel

class ProductRecommendation(BaseModel):
    productId: str
    productType: str
    productName: str
    description: str
    interestRate: float | None = None
    minAmount: float | None = None
    maxAmount: float | None = None
    termMonths: int | None = None
    bank: str
    notes: str | None = None