from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from app import app
from src.models.user_information import User

# Class UserLogin
# This class allows the user to login
# - post: Logs in the user and returns an access token


class UserLogin(Resource):

    @classmethod
    def post(cls):
        """ The login page for the website
        :return: The login page
        """
        app.logger.info("Logging in user")
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            app.logger.info("User input: username: %s", username)
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password, user.user_salt, user.user_hashed_password):
                access_token = create_access_token(identity=user.user_id, expires_delta=None)
                app.logger.info("User logged in successfully")
                data = {
                    "username": user.username,
                    "user_id": user.user_id,
                    "first_name": user.user_first_name,
                    "last_name": user.user_last_name,
                    "is_admin": user.user_is_admin,
                    "account_confirmed": user.account_confirmed,
                    "access_token": access_token
                }
                return {"message": "User logged in successfully", "data": data}, 200
            else:
                app.logger.info("Invalid credentials")
                return {"message": "Invalid credentials"}, 401
        except Exception as e:
            app.logger.error("An error occurred" + str(e))
            return {"message": "An error occurred, please check database"}, 500
