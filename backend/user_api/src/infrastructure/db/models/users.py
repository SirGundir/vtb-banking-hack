from typing import TypedDict
from uuid import uuid4

from sqlalchemy import Uuid, Boolean, JSON, String, Text, DateTime, Integer, \
    BigInteger, ForeignKey, ARRAY, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import expression

from infrastructure.db.base import TimestampedMixin, Base
from infrastructure.db.tablenames import USER_TABLE
from utils.datetime import utcnow


class ConsentData(TypedDict):
    bank_client_id: str
    consent_id: str
    api_url: str


class UserModel(TimestampedMixin, Base):
    __tablename__ = USER_TABLE

    id = mapped_column(Uuid, default=uuid4, primary_key=True)
    is_active = mapped_column(Boolean, default=True)
    email_verified = mapped_column(Boolean, default=False)

    consents = mapped_column(JSONB, nullable=False, default=dict)

    is_admin = mapped_column(Boolean, default=False)
    is_superuser = mapped_column(Boolean, default=False)
    is_staff = mapped_column(Boolean, default=False)

    email = mapped_column(String(254), unique=True)
    password = mapped_column(Text, nullable=True)
    username = mapped_column(Text, server_default=text("gen_random_uuid()"))
    first_name = mapped_column(Text, nullable=True, default=None)
    last_name = mapped_column(Text, default=None, nullable=True)
    # image_url = mapped_column(Text, nullable=True, default=None)

    language = mapped_column(String(3), default='ru')

    updated_accounts = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    updated_balances = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    updated_transactions = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    date_joined = mapped_column(DateTime(timezone=True), default=utcnow)

    def __repr__(self):
        return f"{self.id}: {self.username})"
