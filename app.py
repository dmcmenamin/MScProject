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

    # enable logging for the app
    if not created_app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        # create the log file
        file_handler = RotatingFileHandler('tmp/presentation_creator.log', 'a', 1 * 1024 * 1024, 10)
        # set the log file format
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        # add the log file handler to the app
        created_app.logger.addHandler(file_handler)
        # set the log level to info
        created_app.logger.setLevel(logging.INFO)

        created_app.logger.info('Presentation Creator startup')

    return created_app


app = create_app()

jwt = JWTManager(app)
api = Api(app)
mail = Mail(app)
db = SQLAlchemy(app)

# set the server and port for the app
server_and_port = 'http://' + app.config['SERVER_NAME']

from src.api.login_service import UserLogin
from src.api.get_available_llms import GetAvailableLlms
from src.api.add_user import AddUser
from src.api.presentation_generator_get import PresentationGeneratorGet
from src.api.presentation_generator_post import PresentationGeneratorPost
from src.api.presentation_controller import PresentationController
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
        app.logger.info('Login endpoint called')
        data = {'username': request.form['username'],
                'password': request.form['password']}

        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_and_port + '/user_login', json=data, headers=headers)
        if response.status_code == 200:
            app.logger.info('Login successful for user: ' + request.form['username'])
            data = response.json()
            # set the session information
            user_session(data['username'], data['first_name'], data['last_name'], data['is_admin'],
                         data['access_token'])
            return redirect(url_for('presentation_creator'))
        else:
            app.logger.info('Login failed for user: ' + request.form['username'] + ' with error: ' + response.text)
            return render_template('index.html', response=response)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        app.logger.info('Signup endpoint called')
        response = requests.get(server_and_port + '/available_llms')
        if response.status_code == 200:
            app.logger.info('Available LLMs retrieved successfully')
            data_list = {key: value for key, value in response.json().items() if key == 'data'}
            return render_template('signup.html', llm_names=data_list['data'])
        else:
            app.logger.info('Available LLMs could not be retrieved with error: ' + response.text)
            data = {key: value for key, value in response.json()}
            return render_template('signup.html', response=data)
    elif request.method == 'POST':

        app.logger.info('Signup endpoint called')

        # get the llm names and api keys, and convert them to a list of dictionaries; each dictionary contains the llm
        # name and the api key, and the list is then added to the data dictionary
        llm = [{'llm_name': request.form['llm_name'], 'api_key': request.form['api_key']} for key, value in
               request.form.items() if key == 'llm_name' or key == 'api_key']

        # create the data dictionary, and add the username, password, first name, last name, and llm to it
        data = {'username': request.form['username'],
                'password': request.form['password'],
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'llm': llm}

        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_and_port + '/add_user', json=data, headers=headers)
        if response.status_code == 200:
            app.logger.info('User created successfully' + request.form['username'])
            token = generate_sign_up_token(request.form['username'])
            confirmation_url = url_for('confirm_signup', token=token, _external=True)
            html = render_template('email.html', confirmation_url=confirmation_url)
            subject = "Please confirm your email"
            send_confirmation_email(request.form['username'], subject, html)
            response = {'message': 'User created successfully, please check your email to confirm your account'}
            return render_template('index.html', response=response)
        else:
            app.logger.info('User could not be created with error: ' + response.text)
            response = {'message': 'User could not be created: ' + value for key, value in response.json().items()}
            return render_template('signup.html', response=response)


@app.route('/confirm_signup/<token>', methods=['GET'])
def confirm_signup(token):
    """ The confirm signup endpoint for the website
    :return: If successful, the index page, otherwise, the index page with an error message
    """
    app.logger.info('Confirm signup endpoint called')
    if request.method == 'GET':
        app.logger.info('Confirm signup endpoint called')
        response, status_code = confirm_signup_get(token)
        if status_code == 200:
            return redirect(url_for('index'))
        else:
            app.logger.info('Confirm signup failed with error: ' + response)
            return render_template('index.html', response=response)


@app.route('/presentation_creator', methods=['GET', 'POST'])
@user_authenticated
def presentation_creator():
    """ The presentation creator endpoint for the website
    :return: If successful, the presentation creator page, otherwise, the index page with an error message
    """
    jwt_token = session['jwt_token']
    if request.method == 'GET':
        app.logger.info('Presentation creator endpoint called with GET request')
        headers = {'Authorization': 'Bearer ' + jwt_token,
                   'Content-Type': 'application/json'}
        response = requests.get(server_and_port + '/presentation_generator', headers=headers)
        if response.status_code == 200:
            app.logger.info('Presentation creator endpoint called successfully with GET request')
            response_data = response.json()  # Corrected to call the method
            return render_template('presentation_creator.html',
                                   llm_model_names=response_data['data']['llm_model_names'],
                                   llm_names_and_models=response_data['data']['llm_names_and_models'],
                                   presentation_themes=response_data['data']['presentation_themes'])
        else:
            app.logger.info('Presentation creator endpoint failed with GET request with error: ' + response.text)
            return render_template('index.html',
                                   response=response.text)
    elif request.method == 'POST':
        app.logger.info('Presentation creator endpoint called with POST request')
        headers = {'Authorization': 'Bearer ' + jwt_token,
                   'Content-Type': 'application/json'}

        # get the form data, and convert it to a dictionary
        data = {key: value for key, value in request.form.items()}

        response = requests.post(server_and_port + '/presentation_generator', headers=headers, json=data)
        if response.status_code == 200:
            app.logger.info('Presentation creator endpoint called successfully with POST request')
            return render_template('presentation_generating.html', response=response.text)
        else:
            app.logger.info('Presentation creator endpoint failed with POST request with error: ' + response.text)
            return render_template('index.html', response=response.text)
    else:
        app.logger.info('Invalid request method')
        return render_template('index.html', json={'message': 'Invalid request method'})


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
        app.logger.info('Presentation generating in progress endpoint called with POST request')
        response, status_code = presentation_generating_in_progress_post(request.form)
        if status_code == 200:
            app.logger.info('Presentation generating in progress endpoint called successfully with POST request')
            return render_template('presentation_success.html', response=response)
        else:
            app.logger.info('Presentation generating in progress endpoint failed with POST request with '
                            'error: ' + response)
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
api.add_resource(GetAvailableLlms, '/available_llms')
api.add_resource(PresentationGeneratorGet, '/presentation_generator')
api.add_resource(PresentationGeneratorPost, '/presentation_generator')
api.add_resource(PresentationController, '/presentation_controller')
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
    app.run(debug=False)
