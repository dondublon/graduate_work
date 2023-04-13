from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from sqlalchemy.orm import Session as Session_sync

engine = create_async_engine(settings.profiles_pg_dsn, echo=True)
Session = async_sessionmaker(engine)


def get_session_sync():
    engine_sync = create_engine(settings.profiles_pg_dsn_sync, echo=True)
    return Session_sync(engine_sync)
