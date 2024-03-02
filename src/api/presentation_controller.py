from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from src.controllers import controller
from src.models.user_information import User


class PresentationController(Resource):
    """
    The presentation controller for the website
    :return: The response and status code

    """

    @classmethod
    @jwt_required()
    def post(cls):
        """ The presentation page for the website
            :return: The presentation page
            """
        user_id = get_jwt_identity()
        if not user_id:
            return {'message': 'User not logged in'}, 401
        else:
            username, first_name, last_name, is_admin = User.get_user_information(user_id)
            if not username:
                return {'message': 'User not found'}, 404

            data = request.get_json()
            presenter_first_name = first_name
            presenter_last_name = last_name
            presentation_topic = data.get('presentation_topic')
            audience_size = data.get('audience_size')
            presentation_length = data.get('presentation_length')
            expected_outcome = data.get('expected_outcome')
            who_is_the_audience = data.get('audience')
            large_language_model = data.get('large_language_model')
            specific_model_name = data.get('specific_model_name')
            api_key = data.get('api_key')
            presentation_theme = data.get('presentation_theme')
            return controller.generate_presentation(username, presenter_first_name, presenter_last_name,
                                                    presentation_topic, audience_size, presentation_length,
                                                    expected_outcome, who_is_the_audience, large_language_model,
                                                    specific_model_name, api_key, presentation_theme)
