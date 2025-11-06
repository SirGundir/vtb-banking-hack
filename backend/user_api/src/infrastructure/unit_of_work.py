from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from log import get_logger
from utils.exceptions import str_exception, type_exc


logger = get_logger(__name__)


@dataclass
class UnitOfWork:
    session: AsyncSession

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            error_message = str_exception(exc, with_traceback=False)
            logger.error(error_message)
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
