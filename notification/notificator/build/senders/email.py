import os
from email.message import EmailMessage
from http import HTTPStatus

from flask import current_app
from jinja2 import Environment, FileSystemLoader

from build.config import settings
from build.utils.smtp_connect import connect_smtp_sever


class EmailSender:
    @classmethod
    def send_mail(cls,
                  destination: list,
                  subject: str,
                  html_template: str,
                  title: str,
                  text: str,
                  image: str = ""
                  ) -> (str, HTTPStatus):  # type: ignore

        message = EmailMessage()
        message["From"] = settings.email_user
        message["To"] = destination
        message["Subject"] = subject

        path = f'{os.path.dirname(__file__)}/html_template'  # TODO to config

        env = Environment(loader=FileSystemLoader(path))  # расположение шаблонов
        template = env.get_template(html_template)  # Загружаем нужный шаблон в переменную
        output = template.render(**{
            'title': title,
            'text': text,
            'image': image
        })
        message.add_alternative(output, subtype='html')
        try:
            global smtp_server
            smtp_server.sendmail(settings.email_user, destination, message.as_string())  # type: ignore
        except Exception as e:
            current_app.logger.error(e)
            smtp_server = connect_smtp_sever(settings.smtp_server, settings.smtp_server_port,  # type: ignore
                                             settings.email_user, settings.email_password)

        return "Success", HTTPStatus.OK
