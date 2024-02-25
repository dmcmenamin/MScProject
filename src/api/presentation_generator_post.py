from flask import request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db
from src.models.api_key import ApiKey
from src.models.user_information import User


class PresentationGeneratorPost(Resource):
    """
    The post method for the presentation generator
    :return: The response and status code
    """

    @jwt_required()
    def post(self):
        """
        The post method for the presentation generator
        :return:
        """
        user_id = get_jwt_identity()
        if not user_id:
            return {'message': 'User not logged in'}, 401
        else:
            # get user input
            data = request.get_json()
            topic = data.get('presentation_topic')  # The presentation topic
            audience_size = data.get('audience_size')  # The audience size
            time = data.get('presentation_length')  # The presentation length
            audience_outcome = data.get('expected_outcome')  # The expected outcome
            who_is_the_audience = data.get('audience')  # Who the audience is
            presentation_theme = data.get('presentation_theme')  # The presentation theme

            large_language_model, model_name = data.get('llm_model_name').split("_")  # The large language model and

            username = User.find_username_by_id(user_id)

            api_key = db.session.query(ApiKey.api_key_user_key).join(User, User.user_id == ApiKey.api_key_user).filter(
                User.username == username).first()
            if not api_key:
                return {'message': 'User not authorized to use the large language model'}, 401
            else:
                # set the API Key in the session
                data = {"llm": large_language_model, "llm_model_name": model_name, "presentation_topic": topic,
                        "audience_size": audience_size, "presentation_length": time,
                        "expected_outcome": audience_outcome, "audience": who_is_the_audience,
                        "presentation_theme": presentation_theme, "api_key": api_key[0]}

                return {"message": "User authorized to use the large language model", "data": data}, 200
