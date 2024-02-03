from flask import jsonify

from src.database import queries, database_scripts
from src.database.connection import RelDBConnection


def signup_get():
    """ The signup endpoint for the API - for GET requests
    Checks all available llm model names and returns them
    :return: The response and status code
    """
    # get available llm model names
    available_llms_query = queries.get_available_llms()
    database_connection = RelDBConnection()
    # if the connection is not an exception, get the available llm model names
    # otherwise, return an error message to the user and render the signup page
    try:
        returned_llm_model_names = (database_connection.
                                    query_return_matches_specified(available_llms_query, 100))
        # convert list of tuples to list of strings
        for i in range(len(returned_llm_model_names)):
            returned_llm_model_names[i] = returned_llm_model_names[i][0]
        # render signup page with list of available llm model names
        return jsonify({"llm_model_names": list(returned_llm_model_names)}), 200
    except ConnectionError as e:
        # can't connect to database for login
        return jsonify({"error": f"fDatabase Connection error. Please try again later."}), 500
    except AttributeError as e:
        # Catching attribute error here
        return jsonify({"error": f"Database error. Please try again later."}), 500
    except Exception as e:
        # Catching any other errors
        response_value = {"Connection Error, please try again later. "}
    return jsonify(response_value), 500


def signup_post(data):
    """ The signup endpoint for the API - for POST requests
    Checks if the user exists, if not, creates the user, and returns the user information
    :param data: The data from the request containing the username, password, first name, last name, and api keys
    :return: The response and status code
    """

    if not data:
        return jsonify({"error": "No data was provided."}), 400

    # get user input
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # get api keys for each llm model name and store in dictionary
    llm = {key: value for key, value in data.items() if key.startswith('llm_name_') and value != "" and value is
           not None}
    if len(llm) == 0:
        return jsonify({"error": "Please provide API Key for at least 1 large language model."}), 400

    # check if user exists
    database_connection = RelDBConnection()
    try:
        # check if user exists
        params = (username,)
        returned_user_information = (
            database_connection.query_return_first_match_with_parameter(queries.check_user_exists(), params))
        # if user exists
        if returned_user_information:
            # get available llm model names
            available_llms_query = queries.get_available_llms()
            returned_llm_model_names = (database_connection.
                                        query_return_matches_specified(available_llms_query, 100))
            # convert list of tuples to list of strings
            for i in range(len(returned_llm_model_names)):
                returned_llm_model_names[i] = returned_llm_model_names[i][0]
            # redirect to login page
            return jsonify({"error": "User already exists"}), 401
        # if user does not exist
        else:
            # create salt and hashed password
            salt, hashed_password = database_scripts.create_salted_user_password(password)
            # create user in database
            params = (username, first_name, last_name, hashed_password, salt)
            database_connection.commit_query_with_parameter(queries.create_user(), params)

            # store api keys in database
            for key, value in llm.items():
                params = (username, key, value)
                database_connection.commit_query_with_parameter(queries.create_api_key(), params)

            # successful login, return user information
            return jsonify({"username": username,
                            "first_name": first_name,
                            "last_name": last_name}), 200

    except ConnectionError as e:
        # can't connect to database for login
        return jsonify({"error": f"fDatabase error: {str(e)}. Please try again later."}), 500
    except AttributeError as e:
        # Catching attribute error here
        return jsonify({"error": f"Database error: {str(e)}. Please try again later."}), 500
    except Exception as e:
        # Catching any other errors
        return jsonify({"error": f" {str(e)}. "}), 500
    finally:
        # close the connection, just in case it is still open
        database_connection.close_connection()