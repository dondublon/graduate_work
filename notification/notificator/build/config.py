import logging
from logging.config import dictConfig

from pydantic import BaseSettings, Field

from build.utils.smtp_connect import connect_smtp_sever


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")
    host: str = Field("0.0.0.0", env="NOTIFICATOR_HOST")
    port: int = Field(5000, env="NOTIFICATOR_PORT")
    email_user: str = Field("example@email.com", env="EMAIL_USER")
    email_password: str = Field("password", env="EMAIL_PASSWORD")
    postgres_host: str = Field("notificator_postgres", env="NOTIFICATION_PG_HOST")
    postgres_port: int = Field(5433, env="NOTIFICATION_PG_PORT")
    postgres_user: str = Field("app", env="NOTIFICATION_PG_USER")
    postgres_password: str = Field("123qwe", env="NOTIFICATION_PG_PASSWORD")
    postgres_db_name: str = Field("notification", env="NOTIFICATION_DB_NAME")
    smtp_server: str = Field("smtp.yandex.ru", env="SMTP_SERVER")
    smtp_server_port: int = Field(465, env="SMTP_SERVER_PORT")

    auth_login: str = Field(env="AUTH_LOGIN")
    auth_password: str = Field(env="AUTH_PASSWORD")
    auth_host: str = Field("auth", env="AUTH_HOST")
    auth_port: str = Field(5001, env="AUTH_PORT")
    auth_emails_url: str = Field("/api/v1/user/users-emails", env="AUTH_EMAILS_URL")
    auth_login_url: str = Field("/api/v1/user/login", env="AUTH_LOGIN_URL")

    @property
    def auth_protocol_host_port(self):
        return f"http://{self.auth_host}:{self.auth_port}"

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

logger = logging.getLogger()
logger.setLevel(logging.INFO)

mail_server = connect_smtp_sever(settings.smtp_server, settings.smtp_server_port,
                                 settings.email_user, settings.email_password)
