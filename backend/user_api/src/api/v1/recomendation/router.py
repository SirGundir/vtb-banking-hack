from fastapi import APIRouter
from typing import List
from api.v1.recomendation.schemas import ProductRecommendation
router = APIRouter(prefix='/recommend')


# Заглушка для рекомендаций
@router.post('/{client_id}', response_model=List[ProductRecommendation])
async def recommend_stub(client_id: str, top_n: int = 3, use_ml: bool = True):
    # Статические продукты
    products = [
        {
            "productId": "prod-vb-deposit-001",
            "productType": "deposit",
            "productName": 'Вклад "Надежный"',
            "description": "8.5% годовых, от 10,000₽",
            "interestRate": 8.5,
            "minAmount": 10000,
            "maxAmount": None,
            "termMonths": 12,
            "bank": "ВТБ",
            "notes": "Стандартный вклад"
        },
        {
            "productId": "prod-vb-loan-002",
            "productType": "loan",
            "productName": "Потребительский кредит",
            "description": "До 3,000,000₽, 12.9% годовых",
            "interestRate": 12.9,
            "minAmount": None,
            "maxAmount": 3000000,
            "termMonths": 36,
            "bank": "ВТБ",
            "notes": "Без залога"
        },
        {
            "productId": "prod-vb-card-003",
            "productType": "card",
            "productName": 'Карта "Свобода"',
            "description": "Дебетовая карта с кэшбэком 2%",
            "interestRate": None,
            "minAmount": None,
            "maxAmount": None,
            "termMonths": None,
            "bank": "ВТБ",
            "notes": "Кэшбэк 2% на покупки"
        },
        {
            "productId": "prod-vb-account-004",
            "productType": "account",
            "productName": 'Счёт "Универсальный"',
            "description": "Расчетный счет для физлиц",
            "interestRate": None,
            "minAmount": 0,
            "maxAmount": None,
            "termMonths": None,
            "bank": "ВТБ",
            "notes": "Без комиссии"
        }
    ]

    # Возвращаем top_n продуктов (по умолчанию 3)
    return products[:top_n]