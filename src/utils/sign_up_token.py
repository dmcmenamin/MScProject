import os

from itsdangerous import URLSafeTimedSerializer
from src.utils.common_scripts import get_email_secret_key
from flask import current_app as app


def generate_sign_up_token(username):
    """ Generate a sign-up token
    :param username: The username
    :return: The sign-up token
    """
    # create a serializer
    serializer = URLSafeTimedSerializer(get_email_secret_key())
    # create a token
    return serializer.dumps(username, salt=app.config['SECURITY_PASSWORD_SALT'])


def verify_sign_up_token(token, expiration=3600):
    """ Verify the sign-up
    :param token: The token
    :param expiration: The expiration time
    :return: The username
    """
    # create a serializer
    serializer = URLSafeTimedSerializer(get_email_secret_key())
    # verify the token
    try:
        username = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return username
    except:
        return False
