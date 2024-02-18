from flask import jsonify

from src.database import queries
from src.database.connection import RelDBConnection
from src.utils.sign_up_token import verify_sign_up_token


def confirm_signup_get(token):
    """ The confirm signup endpoint for the website
    :return: The response and status code
    """
    try:
        username = verify_sign_up_token(token)
    except:
        return jsonify({"error": "Invalid token"}), 400

    # check if user is already confirmed
    database_connection = RelDBConnection()
    try:
        params = (username,)
        query = queries.check_user_confirmed()
        returned_user_information = (database_connection.query_return_first_match_with_parameter(query, params))
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}. Please try again later."}), 500

    if returned_user_information[0] == 1:
        return jsonify({"error": "User already confirmed - Please Login"}), 404
    else:
        params = (username,)
        query = queries.confirm_user()
        database_connection.commit_query_with_parameter(query, params)
        return jsonify({"error": "User confirmed - Please Login"}), 202
