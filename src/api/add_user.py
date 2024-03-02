from flask import request
from flask_restful import Resource

from app import db, app
from src.models.api_key import ApiKey
from src.models.llm_name import Llm
from src.models.user_information import User


class AddUser(Resource):
    """
    The post method for the signup
    :return: The response and status code
    """
    @classmethod
    def post(cls):
        """
        The post method for the signup
        :return: The response and status code
        """
        app.logger.info('Adding user')
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user = User.query.filter_by(username=username).first()
        if user:
            return {'message': 'User already exists'}, 401
        else:
            try:
                app.logger.info('User input: username: %s, first_name: %s, last_name: %s', username, first_name,
                                last_name)
                # create the user
                user = User(username=username, user_first_name=first_name, user_last_name=last_name)
                # create the salt and hashed password
                user.user_salt, user.user_hashed_password = User.create_salted_user_password(password)
                db.session.add(user)
                db.session.commit()
                app.logger.info('User created successfully')
            except Exception as e:
                app.logger.error('User could not be created' + str(e))
                return {'message': 'User could not be created'}, 500

            try:
                app.logger.info('Adding API keys')
                # now add the api keys
                user_id = User.get_user_id(username)
                for llm_model, api_key in data.get("llm").items():
                    app.logger.info('Adding API key for: %s', llm_model)
                    if llm_model.startswith('api_key_') and api_key != "" and api_key is not None:
                        llm_model_id = Llm.get_llm_id(llm_model.replace('api_key_', ''))
                        app.logger.info('User id: %s, llm_model_id: %s, api_key: %s', user_id, llm_model_id, api_key)
                        api_key = ApiKey(api_key_user=user_id, api_key_llm=llm_model_id,
                                         api_key_user_key=api_key)
                        db.session.add(api_key)
                        db.session.commit()
                        app.logger.info('API key added successfully')
                        return {'message': 'User created successfully'}, 200
            except Exception as e:
                app.logger.error('User created, but API keys could not be added' + str(e))
                return {'message': 'User created, but API keys could not be added'}, 500



