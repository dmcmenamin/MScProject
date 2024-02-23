from flask import request
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Resource, reqparse
from src.models.user_information import User
from app import jwt


class Login(Resource):
    def post(self):
        """ The login page for the website
        :return: The login page
        """
        parser = reqparse.RequestParser()
        # parser.add_argument('username', help='This field cannot be blank', required=True)
        # parser.add_argument('password', help='This field cannot be blank', required=True)
        # data = parser.parse_args()
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password, user.user_salt, user.user_hashed_password):
            access_token = create_access_token(identity=user.user_id, expires_delta=False)
            return {
                'username': user.username,
                'user_id': user.user_id,
                'first_name': user.user_first_name,
                'last_name': user.user_last_name,
                'is_admin': user.user_is_admin,
                'account_confirmed': user.account_confirmed,
                'access_token': access_token
            }, 200
        else:
            return {'message': 'Invalid credentials'}, 401
