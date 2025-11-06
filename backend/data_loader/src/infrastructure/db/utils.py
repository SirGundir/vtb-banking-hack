from typing import Callable, cast

from sqlalchemy import true, and_, or_
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