import json
import os
import pkg_resources
import requests

from flask import Flask, render_template, redirect, url_for, request, session
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from src.utils.common_scripts import user_session
from src.utils.decorators import user_authenticated


def create_app(test_config=None):
    """ Create the app
    :param test_config: The test config to use if passed in (default is None)
    :return: The app
    """

    # create and configure the app
    created_app = Flask(__name__, instance_relative_config=True)
    created_app.secret_key = os.urandom(24)

    if test_config is None:
        # use the pkg_resources to get the config file
        config_file = pkg_resources.resource_filename('configs', 'config.py')
        print("config_file", config_file)
        # load the instance config, if it exists, when not testing
        created_app.config.from_pyfile(config_file, silent=True)
    else:
        # use the pkg_resources to get the test config file
        test_config_file = pkg_resources.resource_filename('configs', 'test_config.py')
        # load the test config if passed in
        created_app.config.from_pyfile(test_config_file, silent=True)

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

from src.api.get_login import UserLogin
from src.api.get_available_llms import GetAvailableLlms
from src.api.add_user import AddUser
from src.api.get_signup_confirmation import GetSignupConfirmation
from src.api.get_presentation_generator import PresentationGeneratorGet
from src.api.post_presentation_generator import PresentationGeneratorPost
from src.api.post_presentation_controller import PresentationController
from src.api.put_update_password import UpdatePassword
from src.api.add_llm_and_model import AddLlmAndModel
from src.api.add_model import AddModel
from src.api.delete_llm_model import DeleteLlmModel
from src.api.delete_llm_model_and_api_keys import DeleteLlmAndModelAndApiKeys
from src.api.add_or_update_api_key import AddOrUpdateApiKey
from src.api.delete_user import DeleteUser
from src.api.get_historical import GetAllHistoricalForUser
from src.api.add_historical import AddHistoricalPresentation
from src.api.get_specific_historical_presentation import GetSpecificHistoricalPresentation
from src.api.delete_historical import DeleteHistoricalPresentation


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
            app.logger.info('Login successful for user')
            data = response.json()
            # set the session information
            user_session(data['username'], data['first_name'], data['last_name'], data['is_admin'],
                         data['access_token'], data['user_id'])
            return redirect(url_for('presentation_creator'))
        else:
            app.logger.info('Login failed for user with error: ' + response.text)
            data = {'message': 'Login failed: ' + value for key, value in response.json().items() if key == 'message'}
            return render_template('index.html', error_or_warning=data)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        app.logger.info('Signup endpoint called')
        response = requests.get(server_and_port + '/available_llms')

        # Successful response, render the signup page with the available LLMs
        if response.status_code == 200:
            app.logger.info('Available LLMs retrieved successfully')
            data_list = {key: value for key, value in response.json().items() if key == 'data'}
            return render_template('signup.html', llm_names=data_list['data'])
        else:
            # Unsuccessful response, render the signup page with an error message
            app.logger.info('Available LLMs could not be retrieved with error: ' + response.text)
            data = {key: value for key, value in response.json().items() if key == 'message'}
            return render_template('signup.html', error_or_warning=data)

    elif request.method == 'POST':
        app.logger.info('Signup endpoint called')

        # get the llm names and api keys, and convert them to a list of dictionaries; each dictionary contains the llm
        # name and the api key, and the list is then added to the data dictionary
        llm = []
        llm_data = {}
        for key, value in request.form.items():
            if key.startswith('api_key_') and value != '':
                llm_data['llm_model_name'] = key.replace('api_key_', '')
                llm_data[key] = value
                llm.append(llm_data)
                llm_data = {}

        print(llm)
        # create the data dictionary, and add the username, password, first name, last name, and llm to it
        data = {'username': request.form['username'],
                'password': request.form['password'],
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'llm': llm}

        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_and_port + '/add_user', json=data, headers=headers)
        if response.status_code == 200:
            # Successful response, render the index page with a success message
            app.logger.info('User created successfully')

            response = {'message': 'User created successfully, please check your email to confirm your account'}
            return render_template('index.html', error_or_warning=response)
        else:
            # Unsuccessful response, render the signup page with an error message
            app.logger.info('User could not be created with error: ' + response.text)
            response = {'message': 'User could not be created: ' + value
                        for key, value in response.json().items() if key == 'message'}
            return render_template('signup.html', error_or_warning=response)


@app.route('/confirm_signup/<token>', methods=['GET'])
def confirm_signup(token):
    """ The confirm signup endpoint for the website
    :return: If successful, the index page, otherwise, the index page with an error message
    """
    app.logger.info('Confirm signup endpoint called')
    if request.method == 'GET':
        app.logger.info('Confirm signup endpoint called')
        response, status_code = GetSignupConfirmation.get(token)
        if status_code == 200:
            app.logger.info('Confirm signup successful')
            return render_template('index.html', error_or_warning=response)
        else:
            app.logger.info('Confirm signup failed with error: ' + response['message'])
            return render_template('index.html', error_or_warning=response)


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
            data = {key: value for key, value in response.json().items() if key == 'message'}
            return render_template('index.html',
                                   error_or_warning=data)
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
            data = {key: value for key, value in response.json().items() if key == 'message'}
            return render_template('index.html', error_or_warning=data)
    else:
        app.logger.info('Invalid request method in presentation creator endpoint')
        return render_template('index.html', json={'message': 'Invalid request method, please contact'
                                                              'system Administrator'})


@app.route('/presentation_generating_in_progress', methods=['POST'])
@user_authenticated
def presentation_generating_in_progress():
    """ The presentation generating in progress endpoint for the website
    :return: If successful, the presentation generating in progress page, otherwise, the presentation generator page
    with an error message
    """
    try:
        if request.method == 'POST':
            jwt_token = session['jwt_token']
            app.logger.info('Presentation generating in progress called with POST request')
            headers = {'Authorization': 'Bearer ' + jwt_token,
                       'Content-Type': 'application/json'}
            # get the form data, and convert it to a dictionary
            data_string = request.form['response']
            data = json.loads(data_string)['data']

            # call the presentation generating in progress endpoint
            response = requests.post(server_and_port + '/presentation_controller', json=data,
                                     headers=headers)
            app.logger.info('Response: ' + response.text)
            if response.status_code == 200:
                app.logger.info('Presentation generating in progress called successfully with POST request')

                app.logger.info("Adding historical presentation")

                data = {key: value for key, value in response.json().items() if key == 'data'}
                app.logger.info("data: " + str(data))
                location_and_name = {'presentation_name': data['data']['presentation_name'],
                                     'presentation_location': data['data']['presentation_location']}

                app.logger.info("location_and_name: " + str(location_and_name))
                response = requests.post(server_and_port + '/add_historical_presentation', json=location_and_name,
                                         headers=headers)

                return render_template('presentation_success.html', response=response.text)
            else:
                app.logger.info('Presentation generating in progress failed with POST request with error: ' +
                                response.text)
                data = {key: value for key, value in response.json().items() if key == 'message'}
                return render_template('index.html', error_or_warning=data)
    except Exception as e:
        app.logger.error('An error occurred' + str(e))
        return render_template('index.html',
                               error_or_warning={'message': 'An error occurred, please check database'})


@app.route('/historical', methods=['GET'])
@user_authenticated
def historical():
    """ The historical endpoint for the website
    :return: If successful, the historical page, otherwise, the index page with an error message
    """
    jwt_token = session['jwt_token']
    app.logger.info('Historical endpoint called')
    headers = {'Authorization': 'Bearer ' + jwt_token,
               'Content-Type': 'application/json'}
    response = requests.get(server_and_port + '/available_historical/' + str(session['user_id']), headers=headers)
    if response.status_code == 200:
        app.logger.info('Historical endpoint called successfully')
        response_data = response.json()
        historical_data = {"historical_data": [{"historical_id": historical_info['historical_id'],
                                                "presentation_name": historical_info['presentation_name'],
                                                "presentation_location": historical_info['presentation_location'],
                                                "presentation_time_stamp": historical_info['presentation_time_stamp'],
                                                "user_id": historical_info['user_id']}
                                               for historical_info in response_data['data']['historical_data']]}

        return render_template('historical.html', historical=historical_data)
    else:
        app.logger.info('Historical endpoint failed with error: ' + response.text)
        data = {key: value for key, value in response.json().items() if key == 'message'}
        return render_template('historical.html', error_or_warning=data)


@app.route('/historical_endpoint_get_specific_presentation/<historical_id>', methods=['GET'])
@user_authenticated
def historical_endpoint_get_specific_presentation(historical_id):
    """ The historical endpoint get specific presentation for the website
    :return: If successful, download the presentation, otherwise, display the historical page with an error message
    """
    jwt_token = session['jwt_token']
    app.logger.info('Historical endpoint get specific presentation called')
    headers = {'Authorization': 'Bearer ' + jwt_token,
               'Content-Type': 'application/json'}
    response = requests.get(server_and_port + '/retrieve_historical/' + historical_id, headers=headers)
    if response.status_code == 200:
        data = {key: value for key, value in response.json().items() if key == 'message'}
        app.logger.info('Historical endpoint get specific presentation called successfully')

        # refresh the historical page with the success message, and the historical data
        get_response = requests.get(server_and_port + '/available_historical/' + str(session['user_id']),
                                    headers=headers)

        response_data = get_response.json()
        historical_data = {"historical_data": [{"historical_id": historical_info['historical_id'],
                                                "presentation_name": historical_info['presentation_name'],
                                                "presentation_location": historical_info['presentation_location'],
                                                "presentation_time_stamp": historical_info['presentation_time_stamp'],
                                                "user_id": historical_info['user_id']}
                                               for historical_info in response_data['data']['historical_data']]}

        return render_template('historical.html', historical=historical_data, information=data)
    else:
        data = {key: value for key, value in response.json().items() if key == 'message'}
        get_response = requests.get(server_and_port + '/available_historical/' + str(session['user_id']),
                                    headers=headers)

        # get the historical data for the user, and render the historical page with the error message
        response_data = get_response.json()
        app.logger.info('Historical endpoint get specific presentation failed with error: ' + response.text)
        return render_template('historical.html', error_or_warning=data,
                               historical=response_data['historical_data'])


@app.route('/historical_endpoint_delete_presentation/<historical_id>', methods=['GET'])
@user_authenticated
def historical_endpoint_delete_presentation(historical_id):
    """ The historical endpoint delete presentation for the website
    :return: If successful, the historical page, otherwise, the index page with an error message
    """
    jwt_token = session['jwt_token']
    app.logger.info('Historical endpoint delete presentation called')
    headers = {'Authorization': 'Bearer ' + jwt_token,
               'Content-Type': 'application/json'}
    response = requests.delete(server_and_port + '/delete_historical_presentation/' + historical_id, headers=headers)

    if response.status_code == 200:
        data = {key: value for key, value in response.json().items() if key == 'message'}
        app.logger.info('Historical endpoint delete presentation called successfully')

        # refresh the historical page with the success message, and the historical data
        get_response = requests.get(server_and_port + '/available_historical/' + str(session['user_id']),
                                    headers=headers)

        response_data = get_response.json()
        historical_data = {"historical_data": [{"historical_id": historical_info['historical_id'],
                                                "presentation_name": historical_info['presentation_name'],
                                                "presentation_location": historical_info['presentation_location'],
                                                "presentation_time_stamp": historical_info['presentation_time_stamp'],
                                                "user_id": historical_info['user_id']}
                                               for historical_info in response_data['data']['historical_data']]}

        return render_template('historical.html', historical=historical_data, information=data)
    else:
        app.logger.info('Historical endpoint delete presentation failed with error: ' + response.text)
        data = {key: value for key, value in response.json().items() if key == 'message'}

        # refresh the historical page with the error message, and the historical data
        get_response = requests.get(server_and_port + '/available_historical/' + str(session['user_id']),
                                    headers=headers)
        response_data = get_response.json()

        return render_template('index.html', error_or_warning=data,
                               historical=response_data['historical_data'])


@app.route('/account_settings', methods=['GET'])
@user_authenticated
def account_settings():
    """ The account settings endpoint for the website
    :return: The account settings page
    """
    return render_template('account_settings.html', session=session)


@app.route('/change_password/<user_id_for_password_update>', methods=['POST'])
@user_authenticated
def change_user_password(user_id_for_password_update):
    """ The change user password endpoint for the website
    :return: If successful, the account settings page, otherwise, the index page with an error message
    """
    if request.method == 'POST' and request.form.get('_method') == 'PUT':

        if request.form['new_password'] != request.form['confirm_password']:
            app.logger.info('Change user password endpoint called with error: '
                            'New password and confirm password do not match')
            return render_template('account_settings.html',
                                   error_or_warning={'message': 'New password and confirm password do not match'})

        jwt_token = session['jwt_token']
        app.logger.info('Change user password endpoint called')

        headers = {'Authorization': 'Bearer ' + jwt_token,
                   'Content-Type': 'application/json'}
        data = {'password': request.form['confirm_password']}
        response = requests.put(server_and_port + '/update_password/' + user_id_for_password_update,
                                json=data, headers=headers)

        data = {key: value for key, value in response.json().items() if key == 'message'}
        if response.status_code == 200:
            app.logger.info('Change user password endpoint called successfully')
            return render_template('account_settings.html', error_or_warning=data)
        else:
            app.logger.info('Change user password endpoint failed with error: ' + response.text)
            return render_template('account_settings.html', error_or_warning=data)
    else:
        app.logger.info('Invalid request method, please contact system Administrator')
        return render_template('index.html', json={'message': 'Invalid request method, '
                                                              'please contact system Administrator'})


@app.route('/delete_user_endpoint/<user_id_to_delete>', methods=['POST'])
@user_authenticated
def delete_user_endpoint(user_id_to_delete):
    """ The delete user endpoint for the website
    :return: If successful, the index page, otherwise, the account settings page with an error message
    """
    if request.method == 'POST' and request.form.get('_method') == 'DELETE':
        jwt_token = session['jwt_token']
        app.logger.info('Delete user endpoint called')
        headers = {'Authorization': 'Bearer ' + jwt_token,
                   'Content-Type': 'application/json'}
        response = requests.delete(server_and_port + '/delete_user/' + user_id_to_delete, headers=headers)
        data = {key: value for key, value in response.json().items() if key == 'message'}
        if response.status_code == 200:
            session.clear()
            app.logger.info('Delete user endpoint called successfully')
            return render_template('index.html', error_or_warning=data)
        else:
            app.logger.info('Delete user endpoint failed with error: ' + response.text)
            return render_template('account_settings.html', error_or_warning=data)
    else:
        app.logger.info('Invalid request method, please contact system Administrator')
        return render_template('index.html', json={'message': 'Invalid request method, '
                                                              'please contact system Administrator'})


@app.route('/logout_endpoint')
@user_authenticated
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
api.add_resource(GetAllHistoricalForUser, '/available_historical/<user_id>')
api.add_resource(AddHistoricalPresentation, '/add_historical_presentation')
api.add_resource(DeleteHistoricalPresentation, '/delete_historical_presentation/<historical_id>')
api.add_resource(GetSpecificHistoricalPresentation, '/retrieve_historical/<historical_id>')
api.add_resource(AddLlmAndModel, '/add_llm_and_model')
api.add_resource(AddModel, '/add_model')
api.add_resource(DeleteLlmModel, '/delete_llm_model/<llm_model_id>')
api.add_resource(DeleteLlmAndModelAndApiKeys, '/delete_llm_and_model_and_api_keys/<llm_id>')
api.add_resource(UpdatePassword, '/update_password/<user_id_for_password_update>')
api.add_resource(AddOrUpdateApiKey, '/add_or_update_api_key')
api.add_resource(DeleteUser, '/delete_user/<user_id_to_delete>')

if __name__ == '__main__':
    app.run(debug=False)
