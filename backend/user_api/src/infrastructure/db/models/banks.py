from sqlalchemy import Integer, Boolean, String, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column

from infrastructure.db.base import TimestampedMixin, Base
from infrastructure.db.tablenames import BANK_TABLE


class BankModel(TimestampedMixin, Base):
    __tablename__ = BANK_TABLE

    id = mapped_column(Integer, primary_key=True)
    is_active = mapped_column(Boolean, default=True)

    name = mapped_column(String(32), unique=True)
    api_url = mapped_column(String(32), unique=True)
    client_id = mapped_column(String(32))
    client_secret = mapped_column(String(264))
    access_data = mapped_column(JSON)

    def __repr__(self):
        return f"{self.name}({self.id})"
