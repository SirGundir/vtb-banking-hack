import random
import string
from uuid import uuid4


def generate_short_id(
    length: int = 6,
    safe_special_characters: str = "-_.~!$&'()*+,;="
) -> str:
    characters = string.ascii_letters + string.digits + safe_special_characters
    short_link = ''.join(random.choice(characters) for _ in range(length))
    return short_link


def get_uuid_str():
    return str(uuid4())
