import os

import requests
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from flask_mail import Mail
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from src.api.historical_endpoint import historical_endpoint_get, historical_endpoint_get_specific_presentation, \
    historical_endpoint_delete_specific_presentation
from src.api.login_endpoint import login_api

from src.api.presentation_generating_in_progress_endpoint import presentation_generating_in_progress_post
from src.api.presentation_generator_endpoint import presentation_generator_get, presentation_generator_post

from src.api.signup_confirmation_endpoint import confirm_signup_get
from src.api.signup_endpoint import signup_get, signup_post

from src.utils.common_scripts import user_session
from src.utils.send_confirmation_email import send_confirmation_email
from src.utils.sign_up_token import generate_sign_up_token, verify_sign_up_token
from src.utils.decorators import confirmed_login_required, user_authenticated


def create_app(test_config=None):
    """ Create the app
    :param test_config: The test config to use if passed in (default is None)
    :return: The app
    """

    # create and configure the app
    created_app = Flask(__name__, instance_relative_config=True)
    created_app.secret_key = os.urandom(24)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        created_app.config.from_pyfile('/Users/mcmen/PycharmProjects/MScProject/configs/config.py', silent=True)
    else:
        # load the test config if passed in
        created_app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(created_app.instance_path)
    except OSError:
        pass

    return created_app


app = create_app()

jwt = JWTManager(app)
api = Api(app)
mail = Mail(app)
db = SQLAlchemy(app)

from src.api.login_service import UserLogin
from src.api.available_llms_get import AvailableLlmsGet
from src.api.add_user import AddUser
from src.api.presentation_generator_get import PresentationGeneratorGet
from src.api.presentation_generator_post import PresentationGeneratorPost
from src.api.update_password import UpdatePassword
from src.api.add_llm_and_model import AddLlmAndModel
from src.api.add_model import AddModel
from src.api.delete_llm_model import DeleteLlmModel
from src.api.delete_llm_model_and_api_keys import DeleteLlmAndModelAndApiKeys
from src.api.add_or_update_api_key import AddOrUpdateApiKey
from src.api.delete_user import DeleteUser




@app.route('/')
def index():
    """ The index page for the website
    :return: The index page
    """
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """ The login endpoint for the website
    :return: If successful, the presentation generator page, otherwise, the login page with an error message
    """
    if request.method == 'POST':
        data = {'username': request.form['username'],
                'password': request.form['password']}

        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:5000/user_login', json=data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            user_session(data['username'], data['first_name'], data['last_name'], data['is_admin'],
                         data['access_token'])
            print("session: ", session)
            return redirect(url_for('presentation_creator'))
        else:
            return render_template('index.html', response=response)


# @app.route('/signup_endpoint', methods=['GET', 'POST'])
# def signup():
#     """ The signup endpoint for the website
#     :return: If successful, the presentation generator page, otherwise, the signup page with an error message
#     """

    # # if it is a get request
    # if request.method == 'GET':
    #     response, status_code = signup_get()
    #     if status_code == 200:
    #         return render_template('signup.html', llm_model_names=response.json['llm_model_names'])
    #     else:
    #         return render_template('signup.html', response=response)
    #
    # # if it is a post request
    # elif request.method == 'POST':
    #     response, status_code = signup_post(request.form)
    #     if status_code == 200:
    #         token = generate_sign_up_token(response.json['username'])
    #         confirmation_url = url_for('confirm_signup', token=token, _external=True)
    #         html = render_template('email.html', confirmation_url=confirmation_url)
    #         subject = "Please confirm your email"
    #         send_confirmation_email(response.json['username'], subject, html)
    #         return redirect(url_for('presentation_generator'))
    #     else:
    #         return render_template('signup.html', response=response)


@app.route('/confirm_signup/<token>', methods=['GET'])
def confirm_signup(token):
    """ The confirm signup endpoint for the website
    :return: If successful, the index page, otherwise, the index page with an error message
    """

    if request.method == 'GET':
        response, status_code = confirm_signup_get(token)
        if status_code == 200:
            return redirect(url_for('index'))
        else:
            return render_template('index.html', response=response)


@app.route('/presentation_creator', methods=['GET', 'POST'])
@user_authenticated
def presentation_creator():
    """ The presentation creator endpoint for the website
    :return: If successful, the presentation creator page, otherwise, the index page with an error message
    """
    jwt_token = session['jwt_token']
    if request.method == 'GET':
        headers = {'Authorization': 'Bearer ' + jwt_token,
                   'Content-Type': 'application/json'}
        response = requests.get('http://localhost:5000/presentation_generator', headers=headers)
        if response.status_code == 200:
            response_data = response.json()  # Corrected to call the method
            return render_template('presentation_creator.html',
                                   llm_model_names=response_data['data']['llm_model_names'],
                                   llm_names_and_models=response_data['data']['llm_names_and_models'],
                                   presentation_themes=response_data['data']['presentation_themes'])
        else:
            return render_template('index.html',
                                   response=response.text)
    elif request.method == 'POST':
        headers = {'Authorization': 'Bearer ' + jwt_token,
                   'Content-Type': 'application/json'}

        data = {'presentation_topic': request.form['presentation_topic'],
                'audience_size': request.form['audience_size'],
                'presentation_length': request.form['presentation_length'],
                'expected_outcome': request.form['expected_outcome'],
                'audience': request.form['audience'],
                'presentation_theme': request.form['presentation_theme'],
                'llm_model_name': request.form['llm_model_name'],
                }

        response = requests.post('http://localhost:5000/presentation_generator', headers=headers, json=data)
        if response.status_code == 200:
            return render_template('presentation_generating.html', response=response.text)
        else:
            return render_template('index.html', response=response.text)
    else:
        return render_template('index.html', json={'message': 'Invalid request method'})


# @app.route('/presentation_generator_endpoint', methods=['GET', 'POST'])
# @confirmed_login_required
# def presentation_generator():
#     """ The presentation generator endpoint for the website
#     :return: If successful, the presentation generator page, otherwise, the presentation generator page with an error
#     message
#     """
#
#     # if it is a get request
#     if request.method == 'GET':
#         response, status_code = presentation_generator_get()
#         if status_code == 200:
#             return render_template('presentation_creator.html', llm_model_names=response.json['llm_model_names'],
#                                    llm_names_and_models=response.json['llm_names_and_models'],
#                                    presentation_themes=response.json['presentation_themes'])
#         else:
#             return render_template('presentation_creator.html', response=response)
#
#     elif request.method == 'POST':
#         """ The presentation generator endpoint for the website - for POST requests
#         Calls the presentation generating in progress function from the controller
#         :return: If successful, the presentation generator page, otherwise,
#         the presentation generator page with an error
#         """
#         response, status_code = presentation_generator_post(request.form)
#
#         if status_code == 200:
#             return render_template('presentation_generating.html', response=response.json)
#         else:
#             return render_template('index.html', response=response)


@app.route('/presentation_generating_in_progress_endpoint', methods=['POST'])
@user_authenticated
def presentation_generating_in_progress():
    """ The presentation generating in progress endpoint for the website
    :return: If successful, the presentation generating in progress page, otherwise, the presentation generator page
    with an error message
    """
    if request.method == 'POST':
        """ The presentation generating in progress endpoint for the website - for POST requests
        Calls the generate_presentation function from the controller
        :return: If successful, the presentation generating in progress page, otherwise, 
        the presentation generator page with an error
        """
        print("request.form: ", request.form)
        response, status_code = presentation_generating_in_progress_post(request.form)
        if status_code == 200:
            return render_template('presentation_success.html', response=response)
        else:
            return render_template('index.html', response=response)


@app.route('/historical_endpoint', methods=['GET'])
@confirmed_login_required
def historical_endpoint():
    """ The historical endpoint for the website
    :return: The historical page
    """
    response, status_code = historical_endpoint_get()

    if status_code == 200:
        return render_template('historical.html', response=response)
    else:
        return render_template('index.html', response=response)


@app.route('/historical_endpoint_get_specific_presentation/<presentation_id>', methods=['GET'])
@confirmed_login_required
def get_specific_historical_presentation_endpoint(presentation_id):
    """ The get specific historical presentation endpoint for the website
    :return: The historical page
    """

    # call the get specific historical presentation endpoint
    response, status_code = historical_endpoint_get_specific_presentation(presentation_id)

    if status_code == 200:
        return render_template('presentation_success.html')
    else:
        return render_template('index.html', response=response)


@app.route('/delete_presentation_endpoint/<presentation_id>', methods=['POST'])
@confirmed_login_required
def delete_presentation_endpoint(presentation_id):
    """ The delete presentation endpoint for the website
    :return: The historical page
    """

    response, status_code = historical_endpoint_delete_specific_presentation(presentation_id)

    if status_code == 200:
        return redirect(url_for('historical_endpoint'))
    else:
        return render_template('index.html', response=response)


@app.route('/account_settings', methods=['GET'])
@confirmed_login_required
def account_settings():
    """ The account settings endpoint for the website
    :return: The account settings page
    """
    return render_template('account_settings.html', session=session)


@app.route('/logout_endpoint')
@confirmed_login_required
def logout():
    """ The logout endpoint for the website, clears the session information
    :return: The index page
    """

    session.clear()
    return redirect(url_for('index'))


api.add_resource(UserLogin, '/user_login')
api.add_resource(AddUser, '/add_user')
api.add_resource(AvailableLlmsGet, '/available_llms')
# api.add_resource(Signup, '/signup')
# api.add_resource(ConfirmSignup, '/confirm_signup/<token>')
api.add_resource(PresentationGeneratorGet, '/presentation_generator')
api.add_resource(PresentationGeneratorPost, '/presentation_generator')
# api.add_resource(PresentationGeneratingInProgress, '/presentation_generating_in_progress')
# api.add_resource(Historical, '/historical')
# api.add_resource(GetSpecificHistoricalPresentation, '/historical/<presentation_id>')
# api.add_resource(DeletePresentation, '/delete_presentation/<presentation_id>')
# api.add_resource(AccountSettings, '/account_settings')
api.add_resource(AddLlmAndModel, '/add_llm_and_model')
api.add_resource(AddModel, '/add_model')
api.add_resource(DeleteLlmModel, '/delete_llm_model/<llm_model_id>')
api.add_resource(DeleteLlmAndModelAndApiKeys, '/delete_llm_and_model_and_api_keys/<llm_id>')
api.add_resource(UpdatePassword, '/update_password/<user_id_for_password_update>')
api.add_resource(AddOrUpdateApiKey, '/add_or_update_api_key')
api.add_resource(DeleteUser, '/delete_user/<user_id_to_delete>')
# api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
