from build.config import settings, mail_server
from build.utils.app_factory import create_app
from build.scheduler import start_scheduler  # <- Shedule starts here

app = create_app(settings)
smtp_server = mail_server

@app.route("/")
def index():
    return "Hello to Flask!"


start_scheduler(app)

if __name__ == "__main__":
    app.run()
    smtp_server.close()
