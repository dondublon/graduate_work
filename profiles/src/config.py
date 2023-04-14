from logging.config import dictConfig

from pydantic import BaseSettings, PostgresDsn, Field  # RedisDsn


class Settings(BaseSettings):
    # redis_dsn: RedisDsn
    profiles_pg_dsn: PostgresDsn
    profiles_pg_dsn_sync: PostgresDsn
    pg_schema: str = Field("public", env="PROFILES_PG_DEFAULT_SCHEMA")
    pg_name: str = Field("app", env="PROFILES_PG_USER")
    pg_host: str = Field("profiles", env="PROFILES_PG_HOST")
    pg_port: int = Field(5432, env="PROFILES_PG_PORT")
    debug: bool = Field(False, env="PROFILES_DEBUG")
    pg_password: str = Field("", env="PROFILES_PG_PASSWORD")
    service_port: int = Field(50051, env="PROFILES_SERVICE_PORT")
    # region Logging
    sentry_dsn: str = Field(
        "https://1976fd7fecf84863ad877101deebe352@o4504758500720640.ingest.sentry.io/4504758503735296",
        env="SENTRY_DSN",
    )
    logstash_host: str = Field("logstash", env="LOGSTASH_HOST")
    logstash_port: int = Field(5044, env="LOGSTASH_PORT")
    logstash_traces_sample_rate: float = Field(1.0, env="LOGSTASH_TRACES_SAMPLE_RATE")
    avatar_path: str = Field('/avatars', env="PROFILES_AVATARS_PATH")
    # endregion

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
