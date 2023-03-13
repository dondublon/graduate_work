from flask import Flask

from build.config import Settings
from build.utils.routing import register_endpoints


def create_app(settings: Settings) -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = settings.debug

    # app.config["JWT_SECRET_KEY"] = settings.jwt_secrete_key
    # app.config["JWT_COOKIE_SECURE"] = settings.jwt_cookie_secure
    # app.config["JWT_TOKEN_LOCATION"] = settings.jwt_token_location
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.jwt_access_token_expires
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.jwt_refresh_token_expires

    # routing endpoints
    register_endpoints(app)

    app.app_context().push()

    return app
