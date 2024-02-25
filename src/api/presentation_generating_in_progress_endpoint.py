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
    else:
        response_string = data.get('response')

        print("response_string: ", response_string)

        # convert string to dictionary
        # if response string is empty, set response dictionary to empty dictionary
        response_dictionary = ast.literal_eval(response_string) if response_string else {}

        # The response dictionary contains a message and a data dictionary. The data dictionary contains the
        # presentation topic, audience size, time, audience outcome, large language model, specific model name,
        # and API key
        data_dictionary = response_dictionary.get('data')

        topic = data_dictionary.get('presentation_topic')
        audience_size = data_dictionary.get('audience_size')
        time = data_dictionary.get('presentation_length')
        audience_outcome = data_dictionary.get('expected_outcome')
        large_language_model = data_dictionary.get('llm')
        model_name = data_dictionary.get('llm_model_name')
        api_key = data_dictionary.get('api_key')
        # TODO: clean up where image model name is set
        # if session['large_language_model'] == "ChatGPT":
        #     session['image_model_name'] = "dall-e-3"
        audience = data_dictionary.get('audience')

        print("topic: ", topic)

        return controller.generate_presentation(topic, audience_size, time, audience_outcome, audience,
                                                large_language_model, model_name, api_key)
