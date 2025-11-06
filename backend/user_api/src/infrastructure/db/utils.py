import json
from typing import Callable, cast

from sqlalchemy import true, and_, or_, func, literal, String, Text, JSON
from sqlalchemy.dialects.postgresql import JSONB


def safe_and_(*conditions):
    """Safe wrapper for and_() that handles empty conditions list."""
    if not conditions:
        return true()
    return and_(*conditions)


def safe_or_(*conditions):
    """Safe wrapper for or_() that handles empty conditions list."""
    if not conditions:
        return true()
    return or_(*conditions)



def get_conditions(model, **filters) -> list:
    def _get_cond(key, value):
        if isinstance(value, bool):
            return getattr(model, key).is_(value)
        elif isinstance(value, list):
            return getattr(model, key).in_(value)
        elif isinstance(value, Callable):
            return value(getattr(model, key))

        if isinstance(getattr(model, key).type, JSONB):
            value = cast(value, JSONB)
        return getattr(model, key) == value

    return [
        _get_cond(key, value)
        for key, value in filters.items()
    ]


def update_jsonb(field, updates: dict):
    expr = field  # поле уже Mapped/Column(JSONB)

    for key, value in updates.items():
        if isinstance(value, dict):
            value = literal(json.dumps(value))  # преобразуем dict в JSON строку
        expr = func.jsonb_set(
            func.to_jsonb(expr),
            [str(key)],
            func.to_jsonb(value),  # приводим значение к JSONB
            True
        )

    return expr


# def update_jsonb(field, updates: dict):
#     expr = field
#
#     for key, value in updates.items():
#         if isinstance(value, dict):
#             value = json.dumps(value)
#
#         value_literal = literal(value, type_=JSONB)
#
#         expr = func.jsonb_set(
#             expr,
#             [str(key)],
#             value_literal,
#             True
#         )
#
#     return expr