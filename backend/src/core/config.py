import logging
from logging import config as logging_config

import logstash
from pydantic import BaseSettings, Field, BaseModel

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

class Settings(BaseSettings):
    retry_backoff_ms: int = Field(1000, env="RETRY_BACKOFF_MS")
    connections_max_idle_ms: int = Field(5000, env="CONNECTIONS_MAX_IDLE_MS")
    sentry_dsn: str = Field(
        "https://1976fd7fecf84863ad877101deebe352@o4504758500720640.ingest.sentry.io/4504758503735296",
        env="SENTRY_DSN",
    )
    logstash_host: str = Field("0.0.0.0", env="LOGSTASH_HOST")
    logstash_port: int = Field(5044, env="LOGSTASH_PORT")
    logstash_traces_sample_rate: float = Field(1.0, env="LOGSTASH_TRACES_SAMPLE_RATE")
    mongo_dsn: str = Field("0.0.0.0", env="MONGO_DSN")
    db_name: str = Field("cinema", env="DB_NAME")
    auth_host: str = Field("0.0.0.0", env="AUTH_HOST")
    auth_port: int = Field(5001, env="AUTH_PORT")
    auth_secret_key: str = Field("foo", env="JWT_SECRETE_KEY")
    auth_login_url: str = Field("/api/v1/user/login", env="AUTH_LOGIN_URL")
    auth_role_url: str = Field("/api/v1/user/user-role", env="AUTH_ROLE_URL")
    auth_register_url: str = Field("/api/v1/user/register", env="AUTH_REGISTER_URL")
    auth_change_email: str = Field("/api/v1/user/profile/change-email", env="AUTH_CHANGE_EMAIL")
    rabbitmq_host: str = Field("0.0.0.0", env="BROKER_HOST")
    rabbitmq_host_dlq: str = Field("rabbitmq_dlq", env="BROKER_HOST_DLQ")
    rabbitmq_queue: str = Field("ugc_events", env="QUEUE_NAME")
    profiles_host: str = Field("0.0.0.0", env="PROFILES_SERVICE_HOST")
    profiles_port: int = Field(50051, env="PROFILES_SERVICE_PORT")
    admin_roles: str = Field('admin', env="ADMIN_ROLES")

    # We get environment variables from the docker-compose, reference to .env.

    @property
    def auth_protocol_host_port(self):
        return f"http://{self.auth_host}:{self.auth_port}"

    @property
    def profiles_host_port(self):
        return f'{self.profiles_host}:{self.profiles_port}'


class JWTSettings(BaseModel):
    authjwt_secret_key: str = Field("foo", env="JWT_SECRETE_KEY")


jwt_settings = JWTSettings()
settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logstash.LogstashHandler(settings.logstash_host, settings.logstash_port, version=1, tags="backend"))
