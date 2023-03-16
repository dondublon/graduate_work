from apscheduler.schedulers.background import BackgroundScheduler

from .time_action import on_time


def start_scheduler(app):
    sched = BackgroundScheduler()

    def send_by_time():
        print("Executing sending by time")
        with app.app_context():  # Because we use flask
            on_time()

    sched.add_job(send_by_time, 'interval', seconds=10)

    sched.start()
