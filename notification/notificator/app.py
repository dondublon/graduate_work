from build.config import settings
from build.utils.app_factory import create_app
from build import scheduler  # <- Shedule starts here

app = create_app(settings)


@app.route("/")
def index():
    return "Hello to Flask!"


if __name__ == "__main__":
    app.run()
