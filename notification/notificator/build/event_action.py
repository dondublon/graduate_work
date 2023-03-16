from flask import Blueprint, request, current_app

from .common_send import send_all
from .resources.parsers.event_action import manual_sender_parser
from .senders.email import EmailSender
from .db.helper import db_helper
from .db.helper_auth import auth_helper


V1 = "/v1"
event_page = Blueprint('event_page', __name__, url_prefix=V1)
manual = Blueprint('manual', __name__, url_prefix=V1)


@event_page.route('/on_event', methods=['POST'])
def on_event():
    # TODO Place some dispatching code here, "if .... :",
    # refer to request.data.
    payload = request.json["payload"]
    notification_event_pattern = db_helper.choose_event_pattern(payload["event_type"])

    user_uuid = payload["author_id"]
    user_dict = auth_helper.get_users_emails([user_uuid])
    users = [user_dict]
    message_id = request.json["message_id"]
    send_all(users, [notification_event_pattern], message_id)
    # if True:
    #     #  DATA FOR DEBUG
    #     destination = ["yp.group10@yandex.ru"]#, "kaysaki@yandex.ru"]
    #     subject = "Привет!"
    #     html_template = 'mail.html'
    #     title = 'Новое письмо!'
    #     text = 'Произошло что-то интересное! :)'
    #     image = 'https://upload.wikimedia.org/wikipedia/ru/4/4d/Wojak.png'
    #
    #     EmailSender.send_mail(destination, subject, html_template, title, text, image)
    current_app.logger.info(f"route works, data: %s", request.data)
    return f"route works, data: {request.data}"


@manual.route('/manual_sender', methods=['POST'])
def manual_sender():
    data = manual_sender_parser.parse_args()
    payload, status = EmailSender.send_mail(data['destination'],
                                            data['subject'],
                                            data['html_template'],
                                            data['title'],
                                            data['text'],
                                            data['image'])
    current_app.logger.info("Successful")
    return payload, status
