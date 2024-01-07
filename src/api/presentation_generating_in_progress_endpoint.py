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
        topic = data.get('topic')
        audience_size = data.get('audience_size')
        time = data.get('time')
        audience_outcome = data.get('audience_outcome')
        large_language_model = data.get('large_language_model')
        specific_model_name = data.get('model_name')

        if controller.generate_presentation(topic, audience_size, time, audience_outcome,
                                            large_language_model, specific_model_name):
            return jsonify({"success": "Presentation generated"}), 200
        else:
            return jsonify({"error": "Presentation not generated"}), 500
