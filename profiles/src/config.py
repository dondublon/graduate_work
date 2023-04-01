from logging.config import dictConfig

from pydantic import BaseSettings, PostgresDsn, Field  # RedisDsn


class Settings(BaseSettings):
    # redis_dsn: RedisDsn
    pg_dsn: PostgresDsn
    pg_schema: str = Field("public", env="PROFILES_PG_DEFAULT_SCHEMA")
    name: str = Field("app", env="PROFILES_PG_USER")
    host: str = Field("profiles", env="PROFILES_PG_HOST")
    port: int = Field(5432, env="PROFILES_PG_PORT")
    debug: bool = Field(False, env="PROFILES_DEBUG")
    password: str = Field("", env="PROFILES_PG_PASSWORD")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })


settings = Settings()
