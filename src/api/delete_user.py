from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from src.models import historical
from src.models.api_key import ApiKey
from src.models.historical import Historical
from src.models.user_information import User
from src.utils.common_scripts import delete_file_of_type_specified


class DeleteUser(Resource):
    """
    The delete method for the user
    :return: The response and status code
    """

    @classmethod
    @jwt_required()
    def delete(cls, user_id_to_delete):
        """
        The delete method for the user
        :return: The response and status code
        """
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            return {'message': 'You must be logged in to proceed'}, 401

        # check if the user is an admin, if not, they can only delete their own account
        if logged_in_user_id != user_id_to_delete:
            check_admin = User.get_user_is_admin_by_id(logged_in_user_id)
            if not check_admin:
                return {'message': 'You are not authorized to delete this user'}, 401

        user = User.query.filter_by(user_id=user_id_to_delete).first()
        if user:
            # delete the user
            User.delete_user(user)
            # delete the user's API keys
            ApiKey.delete_api_key_by_user_id(user_id_to_delete)
            # delete the user's presentations
            historical_presentation_locations = Historical.get_all_historical_presentation_locations_by_user_id(
                user_id_to_delete)
            # delete the files
            for location in historical_presentation_locations:
                delete_file_of_type_specified(location)
            # delete the presentations from the database
            Historical.delete_all_presentations_by_user_id(user_id_to_delete)

            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User does not exist'}, 404
