from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import settings

engine = create_async_engine(settings.profiles_pg_dsn, echo=True)


def get_session():
    return AsyncSession(engine)
