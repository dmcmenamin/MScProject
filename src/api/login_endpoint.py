from flask import jsonify

from src.database import queries, database_scripts
from src.database.connection import RelDBConnection


def login_api(data):
    # Get the data from the request
    username = data.get("username")
    password = data.get("password")

    # Check if username and password are empty
    # If so, raise a ValueError
    # Otherwise, return the username and password
    if not username:
        return jsonify({"error": "Username cannot be empty."}), 400
    elif not password:
        return jsonify({"error": "Password cannot be empty."}), 400

    database_connection = RelDBConnection()

    # Check if there is a connection to the database, if there is, check if the user exists
    try:
        # check if user exists
        params = (username,)
        returned_user_information = (database_connection.
                                     query_return_first_match_with_parameter(queries.check_user_exists(), params))
        # if user exists
        if returned_user_information:
            # get user information
            user_id, username, user_first_name, user_last_name, user_password, user_salt = returned_user_information
            # check password
            if database_scripts.check_password(password, user_salt, user_password):
                # successful login user
                # get api key
                find_api_key_query, params = queries.get_api_key(username, "ChatGPT")
                returned_api_information = (
                    database_connection.query_return_first_match_with_parameter(find_api_key_query, params))
                response_value = {"api_key": returned_api_information[0],
                                  "user_id": user_id,
                                  "username": username,
                                  "first_name": user_first_name,
                                  "last_name": user_last_name}
                return jsonify(response_value), 200
            else:
                # if password is incorrect
                # redirect to login page
                response_value = {"error": "Password is incorrect."}
                return jsonify(response_value), 401
        else:
            # if user does not exist
            # redirect to login page
            response_value = {"error": "User does not exist."}
            return jsonify(response_value), 401
    except ConnectionError as e:
        # can't connect to database for login
        response_value = {"error": f"fDatabase error: {str(e)}. Please try again later."}
        return jsonify(response_value), 500
    except AttributeError as e:
        # Catching attribute error here
        response_value = {"error": f"Database error: {str(e)}. Please try again later."}
        return jsonify(response_value), 500
    except Exception as e:
        # Catching any other errors
        response_value = {"error": f" {str(e)}. "}
        return jsonify(response_value), 500

