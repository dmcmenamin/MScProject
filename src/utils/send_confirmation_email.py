from flask_mail import Message

from src import mail
from flask import current_app as app


def send_confirmation_email(recipient_email, subject, html_body):
    """ Send the confirmation email
    :param recipient_email: The recipient email
    :param subject: The subject of the email
    :param html_body: The body of the email
    :return: None
    """
    msg = Message(
        subject,
        recipients=[recipient_email],
        html=html_body,
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )
    mail.send(msg)
