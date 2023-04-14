import smtplib


def connect_smtp_sever(server: str, port: int, user: str, password: str) -> smtplib.SMTP_SSL:
    """Cоединение smtp-сервера закрывается после app.run().
    Каждый раз его открывать-закрывать не стоит, потому что открытие долгое."""
    mail_server = smtplib.SMTP_SSL(server, port)
    mail_server.login(user, password)
    return mail_server
