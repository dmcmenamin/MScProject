import os

from flask import Flask, render_template, redirect, url_for, request, session, jsonify

from src.api.login_endpoint import login_api
from src.api.signup_endpoint import signup_get, signup_post
from src.controllers import controller
from src.database import queries, database_scripts
from src.database.connection import RelDBConnection

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html', session=session)


@app.route('/login', methods=['POST'])
def login():
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
    if request.method == 'GET':
        # if user is not logged in, redirect to login page
        if 'username' not in session:
            return render_template('index.html', login_error="Please login to access this page.")
        else:
            # get user's available llm model names
            database_connection = RelDBConnection()
            params = (session['username'],)
            returned_llm_model_names = (
                database_connection.
                query_return_all_matches_with_parameter(queries.get_all_llms_which_user_has_access_to(), params))
            # convert list of tuples to list of strings
            for i in range(len(returned_llm_model_names)):
                returned_llm_model_names[i] = returned_llm_model_names[i][0]

            # get specific llm models
            specific_llm_models = {}
            llm_names_and_models = {}
            for llm_model in returned_llm_model_names:
                llm_names_and_models[llm_model] = []
                params = (llm_model,)
                returned_llm_model_information = (
                    database_connection.
                    query_return_all_matches_with_parameter(queries.get_specific_llm(), params))

                text_llm_model_information = []
                # convert list of tuples to list of strings for each llm model
                for i in range(len(returned_llm_model_information)):
                    if returned_llm_model_information[i][3] == "text":
                        text_llm_model_information.append(returned_llm_model_information[i][2])
                llm_names_and_models[llm_model] = text_llm_model_information
            # render presentation generator page with list of available llm model names
            return render_template('presentation_generator.html',
                                   llm_names_and_models=llm_names_and_models)
    elif request.method == 'POST':
        # get user input
        presenter_name = session['first_name'] + " " + session['last_name']
        topic = request.form['presentation_topic']
        audience_size = request.form['audience_size']
        time = request.form['presentation_length']
        audience_outcome = request.form['expected_outcome']

        # get large language model & exact model name
        # split the string to get the large language model name and the specific model name
        large_language_model, model_name = request.form['llm_model_name'].split("_")
        controller.generate_presentation(topic, audience_size, time, audience_outcome, large_language_model, model_name)
        return render_template('index.html')


@app.route('/logout_endpoint')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
