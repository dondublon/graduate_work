from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import Session

engine = create_engine(settings.profiles_pg_dsn, echo=True)


def get_session():
    return Session(engine)
