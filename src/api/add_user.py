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
        app.logger.info("Adding user")
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        # check if the user already exists, if not, create the user
        try:
            if not cls.add_user(username, password, first_name, last_name):
                return {"message": "User already exists"}, 401
        except Exception as e:
            app.logger.error("User could not be created" + str(e))
            return {"message": "User could not be created"}, 500

        # add the API keys
        try:
            cls.create_user_api_key(username, data)

        except Exception as e:
            app.logger.error("User created, but API keys could not be added" + str(e))
            return {"message": "User created, but API keys could not be added"}, 500

        # send the confirmation email
        try:
            if cls.send_confirmation_email(username):
                data = {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "user_id": User.get_user_id(username),
                }
                return {"message": "User created successfully, "
                                   "please check your email to confirm your account", "data": data}, 200
        except Exception as e:
            app.logger.error("User created, but confirmation email could not be sent" + str(e))
            return {"message": "User created, but confirmation email could not be sent"}, 500

    @classmethod
    def add_user(cls, username, password, first_name, last_name):
        """
        The method to add the user
        :param username: The username
        :param password: The password
        :param first_name: The first name
        :param last_name: The last name
        :return: None
        """

        # check if the user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return False
        else:
            app.logger.info("User input: username: %s, first_name: %s, last_name: %s", username, first_name,
                            last_name)
            # create the user
            user = User(username=username, user_first_name=first_name, user_last_name=last_name)
            # create the salt and hashed password
            user.user_salt, user.user_hashed_password = User.create_salted_user_password(password)
            db.session.add(user)
            db.session.commit()
            app.logger.info("User created successfully")
            return True

    @classmethod
    def create_user_api_key(cls, username, data):
        """
        The method to create the user's API key
        :param username: The username
        :param data: The data
        :return: None
        """

        app.logger.info("Adding API keys")
        # now add the api keys
        user_id = User.get_user_id(username)

        for models_and_keys in data.get("llm"):
            for llm_model, api_key in models_and_keys.items():
                app.logger.info("Adding API key for: %s", llm_model)
                if llm_model.startswith("api_key_") and api_key != "" and api_key is not None:
                    llm_model_id = Llm.get_llm_id(llm_model.replace("api_key_", ""))
                    app.logger.info("User id: %s, llm_model_id: %s, api_key: %s", user_id, llm_model_id,
                                    api_key)
                    api_key = ApiKey(api_key_user=user_id, api_key_llm=llm_model_id,
                                     api_key_user_key=api_key)
                    db.session.add(api_key)
                    db.session.commit()
                    app.logger.info("API key added successfully")

    @classmethod
    def send_confirmation_email(cls, username):
        """
        The method to send the confirmation email
        :param username: The username
        :return: None
        """
        # send the confirmation email
        app.logger.info("Sending confirmation email")
        token = generate_sign_up_token(username)

        app.logger.info("Token: %s", token)
        confirmation_url = url_for("confirm_signup", token=token, _external=True)

        app.logger.info("Confirmation URL: %s", confirmation_url)
        html = render_template("email.html", confirmation_url=confirmation_url)

        app.logger.info("HTML: %s", html)
        subject = "Please confirm your email"
        send_confirmation_email(username, subject, html)
        app.logger.info("User created successfully, please check your email to confirm your account")

        return True
