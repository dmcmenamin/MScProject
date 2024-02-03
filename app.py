import os
import asyncio

from flask import Flask, render_template, redirect, url_for, request, session, jsonify

from src.api.historical_endpoint import historical_endpoint_get, historical_endpoint_get_specific_presentation, \
    historical_endpoint_delete_specific_presentation
from src.api.login_endpoint import login_api
from src.api.presentation_generating_in_progress_endpoint import presentation_generating_in_progress_post
from src.api.presentation_generator_endpoint import presentation_generator_get, presentation_generator_post
from src.api.signup_endpoint import signup_get, signup_post
from src.controllers import controller
from src.controllers.controller import generate_presentation

app = Flask(__name__)
app.secret_key = os.urandom(24)


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
        session['username'] = response.json['username']
        session['user_id'] = response.json['user_id']
        session['first_name'] = response.json['first_name']
        session['last_name'] = response.json['last_name']
        session['api_key'] = response.json['api_key']
        return redirect(url_for('presentation_generator'))
    else:
        return render_template('index.html', response=response)


@app.route('/signup_endpoint', methods=['GET', 'POST'])
def signup():
    """ The signup endpoint for the website
    :return: If successful, the presentation generator page, otherwise, the signup page with an error message
    """

    # if user is logged in, redirect to presentation generator page
    if 'username' in session:
        return redirect(url_for('presentation_generator'))

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
            return redirect(url_for('presentation_generator'))
        else:
            return render_template('signup.html', response=response)


@app.route('/presentation_generator_endpoint', methods=['GET', 'POST'])
def presentation_generator():
    """ The presentation generator endpoint for the website
    :return: If successful, the presentation generator page, otherwise, the presentation generator page with an error
    message
    """

    # if user is not logged in, redirect to login page
    if 'username' not in session:
        return redirect(url_for('index'))

    # if it is a get request
    if request.method == 'GET':
        response, status_code = presentation_generator_get()
        if status_code == 200:
            return render_template('presentation_generator.html', llm_model_names=response.json['llm_model_names'],
                                   llm_names_and_models=response.json['llm_names_and_models'])
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
def presentation_generating_in_progress():
    """ The presentation generating in progress endpoint for the website
    :return: If successful, the presentation generating in progress page, otherwise, the presentation generator page
    with an error message
    """

    # if user is not logged in, redirect to login page
    if 'username' not in session:
        return redirect(url_for('index'))

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
def historical_endpoint():
    """ The historical endpoint for the website
    :return: The historical page
    """

    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        response, status_code = historical_endpoint_get()

        if status_code == 200:
            return render_template('historical.html', response=response)
        else:
            return render_template('index.html', response=response)


@app.route('/historical_endpoint_get_specific_presentation/<presentation_id>', methods=['GET'])
def get_specific_historical_presentation_endpoint(presentation_id):
    """ The get specific historical presentation endpoint for the website
    :return: The historical page
    """

    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        response, status_code = historical_endpoint_get_specific_presentation(presentation_id)

        if status_code == 200:
            return render_template('presentation_success.html')
        else:
            return render_template('index.html', response=response)


@app.route('/delete_presentation_endpoint/<presentation_id>', methods=['POST'])
def delete_presentation_endpoint(presentation_id):
    """ The delete presentation endpoint for the website
    :return: The historical page
    """

    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        response, status_code = historical_endpoint_delete_specific_presentation(presentation_id)
        print(response, status_code)

        if status_code == 200:
            return redirect(url_for('historical_endpoint'))
        else:
            return render_template('index.html', response=response)


@app.route('/logout_endpoint')
def logout():
    """ The logout endpoint for the website, clears the session information
    :return: The index page
    """

    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
