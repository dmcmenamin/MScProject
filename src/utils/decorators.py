from functools import wraps

from flask import session, redirect, url_for, jsonify

from src.database import queries
from src.database.connection import RelDBConnection


def login_required(f):
    """ Decorator to check if the user is logged in
    :param f: The function to be decorated
    :return: The decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index'))
        else:
            database_connection = RelDBConnection()
            try:
                # check if user is already confirmed
                params = (session['username'],)
                query = queries.check_user_confirmed()
                returned_user_information = (database_connection.query_return_first_match_with_parameter(query, params))
                if returned_user_information[0] == 0:
                    return redirect(url_for('index'))
            except Exception as e:
                return jsonify({"error": f"Database error: {str(e)}. Please try again later."}), 500

        return f(*args, **kwargs)

    return decorated_function
