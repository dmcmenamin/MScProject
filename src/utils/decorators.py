from functools import wraps

from flask import session, redirect, url_for


def user_authenticated(f):
    """ Decorator to check if the user is logged in, if not redirect to the index page
    :param f: The function to be decorated
    :return: The decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "jwt_token" not in session:
            return redirect(url_for("index"))

        return f(*args, **kwargs)

    return decorated_function

