from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
from dateutil.parser import ParserError


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def datetime_utc_from_str(datetime_str: str) -> datetime:
    return datetime.fromisoformat(datetime_str).astimezone(timezone.utc)


def ts_to_datetime_str(ts: float | int, dt_format: str = '%Y-%m-%dT%H:%M:%SZ'):
    return datetime.fromtimestamp(int(ts)).strftime(dt_format)


def try_parse_date(value):
    if not isinstance(value, str):
        return None
    try:
        return parse_date(value, dayfirst=True)  # dayfirst=True для европейских форматов
    except (ParserError, ValueError):
        return None
