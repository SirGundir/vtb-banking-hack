from uuid import uuid4

from sqlalchemy import Uuid, Boolean, JSON, String, Text, DateTime, Integer, \
    BigInteger, ForeignKey, ARRAY, text
from sqlalchemy.orm import mapped_column, relationship

from infrastructure.db.base import TimestampedMixin, Base
from infrastructure.db.tablenames import USER_TABLE
from utils.datetime import utcnow
from utils.enum import StrEnum
from utils.ids import get_uuid_str


class UserModel(TimestampedMixin, Base):
    __tablename__ = USER_TABLE

    id = mapped_column(Uuid, default=uuid4, primary_key=True)
    is_active = mapped_column(Boolean, default=True)
    email_verified = mapped_column(Boolean, default=False)

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

    date_joined = mapped_column(DateTime(timezone=True), default=utcnow)

    def __repr__(self):
        return f"{self.id}: {self.username})"
