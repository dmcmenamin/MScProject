from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app


def generate_sign_up_token(username):
    """ Generate a sign-up token
    :param username: The username
    :return: The sign-up token
    """
    # create a serializer
    serializer = URLSafeTimedSerializer(app.config["EMAIL_SECRET_KEY"])
    # create a token
    return serializer.dumps(username, salt=app.config["SECURITY_PASSWORD_SALT"])


def verify_sign_up_token(token, expiration=3600):
    """ Verify the sign-up
    :param token: The token
    :param expiration: The expiration time
    :return: The username
    """
    # create a serializer
    serializer = URLSafeTimedSerializer(app.config["EMAIL_SECRET_KEY"])
    # verify the token
    try:
        username = serializer.loads(token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration)
        return username
    except Exception as e:
        app.logger.error(f"Error verifying sign-up token: {e}")
        return False
