from uuid import uuid4

from sqlalchemy import Uuid, Boolean, String, Text, DateTime, text
from sqlalchemy.orm import mapped_column

from infrastructure.db.base import Base
from infrastructure.db.tablenames import USER_TABLE



class UserModel(Base):
    __tablename__ = USER_TABLE

    id = mapped_column(Uuid, default=uuid4, primary_key=True)
    is_active = mapped_column(Boolean, default=True)
    email_verified = mapped_column(Boolean, default=False)

    consent_id = mapped_column(String(64), default=None, nullable=True)

    def __repr__(self):
        return f"User ({self.id})"
