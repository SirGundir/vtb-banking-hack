from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from utils.datetime import utcnow


class Base(AsyncAttrs, DeclarativeBase):
    pass

