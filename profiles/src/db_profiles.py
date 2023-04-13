from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import settings

engine = create_async_engine(settings.profiles_pg_dsn, echo=True)
Session = async_sessionmaker(engine)
