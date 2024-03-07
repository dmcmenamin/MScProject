import os

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import app
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
        app.logger.info('Deleting user')
        logged_in_user_id = get_jwt_identity()
        if not logged_in_user_id:
            app.logger.info('User not logged in')
            return {'message': 'You must be logged in to proceed'}, 401

        try:
            # check if the user is an admin, if not, they can only delete their own account
            app.logger.info('Checking if user is an admin')

            if str(logged_in_user_id) != user_id_to_delete:
                app.logger.info('User is not an admin and is trying to delete another user')
                check_admin = User.get_user_is_admin_by_id(logged_in_user_id)
                if not check_admin:
                    return {'message': 'You are not authorized to delete this user'}, 401
        except Exception as e:
            app.logger.error('Error getting user admin status' + str(e))
            return {'message': 'Error getting user admin status'}, 500

        try:
            # check if the user exists
            app.logger.info('User input: user_id_to_delete: %s', user_id_to_delete)
            user = User.query.filter_by(user_id=user_id_to_delete).first()
            if user:
                # delete the user's API keys
                ApiKey.delete_api_key_by_user_id(user_id_to_delete)
                app.logger.info('API keys deleted successfully')

                # delete the user's presentations
                historical_presentation_locations = (
                    Historical.find_all_historical_locations_by_user_id(user_id_to_delete))
                app.logger.info('Historical presentation locations: %s', historical_presentation_locations)
                # delete the files

                for location in historical_presentation_locations:
                    # check if the file exists
                    if os.path.exists(location):
                        delete_file_of_type_specified(location)
                        app.logger.info('Historical presentation deleted successfully')
                    else:
                        app.logger.info('Historical presentation not found')

                # delete the presentations from the database
                Historical.delete_all_presentations_by_user_id(user_id_to_delete)
                app.logger.info('Presentations deleted from the database successfully')

                # delete the user
                User.delete_user(user)
                app.logger.info('User deleted successfully')

                return {'message': 'User deleted successfully'}, 200
            else:
                app.logger.info('User does not exist')
                return {'message': 'User does not exist'}, 404
        except Exception as e:
            app.logger.error('User could not be deleted' + str(e))
            return {'message': 'User could not be deleted'}, 500
