from flask import Flask

from build.config import Settings
from build.utils.routing import register_endpoints


def create_app(settings: Settings) -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = settings.debug

    # routing endpoints
    register_endpoints(app)

    app.app_context().push()

    return app
