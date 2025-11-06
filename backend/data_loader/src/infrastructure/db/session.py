from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


AsyncSessionType = async_sessionmaker[AsyncSession]


def get_session(engine) -> AsyncSessionType:
    return async_sessionmaker(
        engine, expire_on_commit=False
    )
