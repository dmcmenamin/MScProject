from flask import request, url_for, render_template
from flask_restful import Resource

from app import db, app
from src.models.api_key import ApiKey
from src.models.llm_name import Llm
from src.models.user_information import User
from src.utils.send_confirmation_email import send_confirmation_email
from src.utils.sign_up_token import generate_sign_up_token


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
        print(data)
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
                print(data.get("llm"))
                for models_and_keys in data.get("llm"):
                    for llm_model, api_key in models_and_keys.items():
                        app.logger.info('Adding API key for: %s', llm_model)
                        if llm_model.startswith('api_key_') and api_key != "" and api_key is not None:
                            llm_model_id = Llm.get_llm_id(llm_model.replace('api_key_', ''))
                            app.logger.info('User id: %s, llm_model_id: %s, api_key: %s', user_id, llm_model_id, api_key)
                            api_key = ApiKey(api_key_user=user_id, api_key_llm=llm_model_id,
                                             api_key_user_key=api_key)
                            db.session.add(api_key)
                            db.session.commit()
                            app.logger.info('API key added successfully')
            except Exception as e:
                app.logger.error('User created, but API keys could not be added' + str(e))
                return {'message': 'User created, but API keys could not be added'}, 500

            try:
                # send the confirmation email
                app.logger.info('Sending confirmation email')
                token = generate_sign_up_token(username)

                app.logger.info('Token: %s', token)
                confirmation_url = url_for('confirm_signup', token=token, _external=True)

                app.logger.info('Confirmation URL: %s', confirmation_url)
                html = render_template('email.html', confirmation_url=confirmation_url)

                app.logger.info('HTML: %s', html)
                subject = "Please confirm your email"
                send_confirmation_email(username, subject, html)
                app.logger.info('User created successfully, please check your email to confirm your account')

                return {'message': 'User created successfully, '
                                   'please check your email to confirm your account'}, 200
            except Exception as e:
                app.logger.error('User created, but confirmation email could not be sent' + str(e))
                return {'message': 'User created, but confirmation email could not be sent'}, 500




