import os

from flask import Flask, render_template, redirect, url_for, request, session, jsonify

from src.api.login_endpoint import login_api
from src.api.presentation_generator_api import presentation_generator_get, presentation_generator_post
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
        Calls the generate_presentation function from the controller
        :return: If successful, the presentation generator page, otherwise, 
        the presentation generator page with an error
        """
        response, status_code = presentation_generator_post(request.form)
        if status_code == 200:
            return render_template('presentation_generator.html', response=response)
        else:
            return render_template('presentation_generator.html', response=response)


@app.route('/logout_endpoint')
def logout():
    """ The logout endpoint for the website, clears the session information
    :return: The index page
    """

    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
