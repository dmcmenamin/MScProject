import ast

from flask import jsonify, session

from src.controllers import controller


def presentation_generating_in_progress_post(data):
    """ The presentation generator endpoint for the API - for POST requests
    :param data: contains the presenter name, topic, audience size, time, audience outcome, large language model, and
    specific model name
    :return: The response and status code
    """

    if not data:
        return jsonify({"error": "No data was provided."}), 400
    elif 'username' not in session:
        return jsonify({"error": "User not logged in"}), 401
    else:
        response_string = data.get('response')
        response_dictionary = ast.literal_eval(response_string) if response_string else {}

        topic = response_dictionary.get('topic')
        audience_size = response_dictionary.get('audience_size')
        time = response_dictionary.get('time')
        audience_outcome = response_dictionary.get('audience_outcome')
        large_language_model = response_dictionary.get('large_language_model')
        specific_model_name = response_dictionary.get('model_name')

        return controller.generate_presentation(topic, audience_size, time, audience_outcome,
                                                large_language_model, specific_model_name)
