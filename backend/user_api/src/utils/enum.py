from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        try:
            cls(value)
        except ValueError:
            return False
        return True


class DbFieldEnum(Enum):
    def __init__(self, value: str, db_field: str):
        self._value_ = value
        self.db_field = db_field

    def __str__(self):
        return self.value
