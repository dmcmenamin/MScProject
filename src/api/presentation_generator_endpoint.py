from flask import jsonify, session

from src.utils.common_scripts import set_session_values, get_themes_available, set_presentation_themes_available
from src.database import queries
from src.database.connection import RelDBConnection


def presentation_generator_get():
    """ The presentation generator endpoint for the API - for GET requests
    Checks all available llm model names and returns them
    :return: The response and status code
    """

    # if user is not logged in, redirect to login page
    if 'username' not in session:
        return jsonify({"error": "User not logged in"}), 401
    else:
        # get user's available llm model names
        database_connection = RelDBConnection()
        params = (session['username'],)
        returned_llm_model_names = (
            database_connection.
            query_return_all_matches_with_parameter(queries.get_all_llms_which_user_has_access_to(), params))
        # convert list of tuples to list of strings
        for i in range(len(returned_llm_model_names)):
            returned_llm_model_names[i] = returned_llm_model_names[i][0]

        # get specific llm models
        llm_names_and_models = {}
        for llm_model in returned_llm_model_names:
            llm_names_and_models[llm_model] = []
            params = (llm_model,)
            returned_llm_model_information = (
                database_connection.
                query_return_all_matches_with_parameter(queries.get_specific_llm(), params))

            text_llm_model_information = []
            # convert list of tuples to list of strings for each llm model
            for i in range(len(returned_llm_model_information)):
                if returned_llm_model_information[i][3] == "text":
                    # create a list of tuples containing the model name and description
                    text_model_name_and_description = (returned_llm_model_information[i][2],
                                                       returned_llm_model_information[i][4])
                    text_llm_model_information.append(text_model_name_and_description)
            llm_names_and_models[llm_model] = text_llm_model_information

        #  get the themes available
        presentation_themes = get_themes_available()

        # render presentation generator page with list of available llm model names
        return jsonify({"llm_model_names": returned_llm_model_names,
                        "llm_names_and_models": llm_names_and_models,
                        "presentation_themes": presentation_themes}), 200


def presentation_generator_post(data):
    # get user input
    topic = data.get('presentation_topic')
    audience_size = data.get('audience_size')
    time = data.get('presentation_length')
    audience_outcome = data.get('expected_outcome')
    who_is_the_audience = data.get('audience')
    presentation_theme = data.get('presentation_theme')

    # get large language model & exact model name
    # split the string to get the large language model name and the specific model name
    large_language_model, model_name = data.get('llm_model_name').split("_")
    set_session_values('large_language_model', large_language_model)
    set_session_values('model_name', model_name)

    # set the presentation theme
    set_session_values('presentation_theme', set_presentation_themes_available(presentation_theme))

    # get the api key
    database_connection = RelDBConnection()
    try:
        params = (session['username'], session['large_language_model'])
        api_key = (database_connection.
                   query_return_first_match_with_parameter(queries.get_api_key(), params))
        if api_key:
            set_session_values('api_key', api_key[0])
        else:
            return jsonify({"error": "API key not found"}), 400
    except ConnectionError as e:
        return jsonify({"error": "Database currently not available. Please try again later."}), 500
    except AttributeError as e:
        return jsonify({"error": "Database currently not available. Please try again later."}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500
    finally:
        # close the database connection just in case it is still open
        database_connection.close_connection()

    return jsonify({"topic": topic, "audience_size": audience_size, "time": time, "audience_outcome": audience_outcome,
                    "large_language_model": large_language_model, "model_name": model_name,
                    "audience": who_is_the_audience}), 200
