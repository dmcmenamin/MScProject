from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db
from src.models.user_information import User

# Class UpdatePassword
# This class allows the user to update their password or an admin to update another user's password
# - put: Updates the password


class UpdatePassword(Resource):
    """
    The put method for updating the password
    :return: The response and status code
    """
    @classmethod
    @jwt_required()
    def put(cls, user_id_for_password_update):
        """
        The put method for updating the password
        :return: The response and status code
        """
        logged_in_user_id = get_jwt_identity()
        # check if the user is logged in
        if not logged_in_user_id:
            return {"message": "User not logged in"}, 401
        # check if the user is an admin, if not, they can only update their own password
        elif logged_in_user_id != user_id_for_password_update:
            if not User.get_user_is_admin_by_id(logged_in_user_id):
                return {"message": "You are not authorized to update this user\'s password"}, 401#

        # get the user's username
        data = request.get_json()
        password = data.get("password")
        user = User.query.filter_by(user_id=user_id_for_password_update).first()
        if user:
            user.user_salt, user.user_hashed_password = User.create_salted_user_password(password)
            try:
                db.session.commit()
                return {"message": "Password updated successfully"}, 200
            except Exception:
                return {"message": "Password could not be updated"}, 500
        else:
            return {"message": "User does not exist"}, 404
