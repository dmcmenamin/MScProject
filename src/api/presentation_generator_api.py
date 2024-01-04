from flask import jsonify, session

from src.controllers import controller
from src.database import queries, database_scripts
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
                    text_llm_model_information.append(returned_llm_model_information[i][2])
            llm_names_and_models[llm_model] = text_llm_model_information
        # render presentation generator page with list of available llm model names
        return jsonify({"llm_model_names": returned_llm_model_names,
                        "llm_names_and_models": llm_names_and_models}), 200


def presentation_generator_post(data):
    # get user input
    topic = data.get('presentation_topic')
    audience_size = data.get('audience_size')
    time = data.get('presentation_length')
    audience_outcome = data.get('expected_outcome')

    # get large language model & exact model name
    # split the string to get the large language model name and the specific model name
    large_language_model, model_name = data.get('llm_model_name').split("_")
    return controller.generate_presentation(topic, audience_size, time, audience_outcome,
                                            large_language_model, model_name)
