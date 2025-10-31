from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from utils.datetime import utcnow


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TimestampedMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __mapper_args__ = {"eager_defaults": True}

    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(),
                               onupdate=func.now())
