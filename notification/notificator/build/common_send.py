import logging
from typing import Iterable

from build.db.helper import db_helper
from build.senders.email import EmailSender
from flask import current_app

logger = logging.getLogger()


def send_all(users: Iterable[dict], patterns, message_id=None):
    """Send to all channels - email, telegram and so on.
    message_id actual only for event from RabbitMQ.
    """
    if message_id is not None:
        if db_helper.already_was_msg_id(message_id):
            logger.warning("Message id %s already sent, exiting.", message_id)
            return
    for pattern in patterns:
        for user in users:
            send_email(user, pattern)
        db_helper.add_notification_event(message_id, pattern["id"])


def send_email(user: dict, pattern):
    """
    Sample notification_pattern row:
    type_: 2
    pattern_file: mail.html
    actual_time: 600
    settings_: {"subject": "Привет", "title": "Новое письмо!", "text": "Произошло что-то интересное! :)",
        "image": "https://upload.wikimedia.org/wikipedia/ru/4/4d/Wojak.png"}
    """
    addresses = user["email"]
    file_pattern = pattern["pattern_file"]
    settings_ = pattern["settings_"]
    EmailSender.send_mail(addresses, settings_["subject"], file_pattern, settings_["title"],
                          settings_["text"], settings_["image"])
    current_app.logger.info(f"Sent to {addresses}, {file_pattern}, {settings_}")
