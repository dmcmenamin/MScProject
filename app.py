import os

from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_mail import Mail

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
from src.utils.decorators import login_required

app = Flask(__name__)
app.secret_key = os.urandom(24)

# set_app_config_values()
app.config.from_pyfile('/Users/mcmen/PycharmProjects/MScProject/configs/email_config.py')

mail = Mail(app)


@app.route('/')
def index():
    """ The index page for the website
    :return: The index page
    """
    return render_template('index.html', session=session)


@app.route('/login', methods=['POST'])
def login():
    """ The login endpoint for the website
    :return: If successful, the presentation generator page, otherwise, the index page with an error message
    """

    response, status_code = login_api(request.form)
    if status_code == 200:
        user_session(response.json['username'], response.json['user_id'], response.json['first_name'],
                     response.json['last_name'], response.json['is_admin'])
        return redirect(url_for('presentation_generator'))
    else:
        return render_template('index.html', response=response)


@app.route('/signup_endpoint', methods=['GET', 'POST'])
def signup():
    """ The signup endpoint for the website
    :return: If successful, the presentation generator page, otherwise, the signup page with an error message
    """
    # if it is a get request
    if request.method == 'GET':
        response, status_code = signup_get()
        if status_code == 200:
            return render_template('signup.html', llm_model_names=response.json['llm_model_names'])
        else:
            return render_template('signup.html', response=response)

    # if it is a post request
    elif request.method == 'POST':
        response, status_code = signup_post(request.form)
        if status_code == 200:
            token = generate_sign_up_token(response.json['username'])
            confirmation_url = url_for('confirm_signup', token=token, _external=True)
            html = render_template('email.html', confirmation_url=confirmation_url)
            subject = "Please confirm your email"
            send_confirmation_email(response.json['username'], subject, html)
            return redirect(url_for('presentation_generator'))
        else:
            return render_template('signup.html', response=response)


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


@app.route('/presentation_generator_endpoint', methods=['GET', 'POST'])
@login_required
def presentation_generator():
    """ The presentation generator endpoint for the website
    :return: If successful, the presentation generator page, otherwise, the presentation generator page with an error
    message
    """

    # if it is a get request
    if request.method == 'GET':
        response, status_code = presentation_generator_get()
        if status_code == 200:
            return render_template('presentation_generator.html', llm_model_names=response.json['llm_model_names'],
                                   llm_names_and_models=response.json['llm_names_and_models'],
                                   presentation_themes=response.json['presentation_themes'])
        else:
            return render_template('presentation_generator.html', response=response)

    elif request.method == 'POST':
        """ The presentation generator endpoint for the website - for POST requests
        Calls the presentation generating in progress function from the controller
        :return: If successful, the presentation generator page, otherwise, 
        the presentation generator page with an error
        """
        response, status_code = presentation_generator_post(request.form)

        if status_code == 200:
            return render_template('presentation_generating.html', response=response.json)
        else:
            return render_template('index.html', response=response)


@app.route('/presentation_generating_in_progress_endpoint', methods=['POST'])
@login_required
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
        response, status_code = presentation_generating_in_progress_post(request.form)
        if status_code == 200:
            return render_template('presentation_success.html', response=response)
        else:
            return render_template('index.html', response=response)


@app.route('/historical_endpoint', methods=['GET'])
@login_required
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
@login_required
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
@login_required
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
@login_required
def account_settings():
    """ The account settings endpoint for the website
    :return: The account settings page
    """
    return render_template('account_settings.html', session=session)


@app.route('/logout_endpoint')
@login_required
def logout():
    """ The logout endpoint for the website, clears the session information
    :return: The index page
    """

    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
