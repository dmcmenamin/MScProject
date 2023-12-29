import os

from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.serving import run_simple

from src.database import queries, database_scripts
from src.database.connection import RelDBConnection

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get user input
        username = request.form['username']
        password = request.form['password']
        database_connection = RelDBConnection()

        # Check if there is a connection to the database, if there is, check if the user exists
        if not isinstance(database_connection.connect(), Exception):

            # check if user exists
            params = (username,)
            returned_user_information = (database_connection.
                                         query_return_first_match_with_parameter(queries.check_user_exists(), params))
            # if user exists
            if returned_user_information:
                # get user information
                user_id = returned_user_information[0]
                username = returned_user_information[1]
                user_first_name = returned_user_information[2]
                user_last_name = returned_user_information[3]
                user_password = returned_user_information[4]
                user_salt = returned_user_information[5]
                # check password
                if database_scripts.check_password(password, user_salt, user_password):
                    # successful login user

                    # get api key
                    find_api_key_query, params = queries.get_api_key(username, "ChatGPT")
                    returned_api_information = (
                        database_connection.query_return_first_match_with_parameter(find_api_key_query, params))
                    # store api key in session
                    session['api_key'] = returned_api_information[0]
                    # store user information in session
                    session['user_id'] = user_id
                    session['username'] = username
                    session['user_first_name'] = user_first_name
                    session['user_last_name'] = user_last_name
                    # redirect to chatbot page
                    return render_template('index.html', session=session)
                else:
                    # if password is incorrect
                    # redirect to login page
                    return render_template('index.html', login_error="Password is incorrect")
            else:
                # if user does not exist
                # redirect to login page
                return render_template('index.html', login_error="User does not exist")
        else:
            # can't connect to database for login
            return render_template('index.html', database_error="Database error. "
                                                                "Please try again later.")


@app.route('/signup_endpoint', methods=['GET', 'POST'])
def signup():
    # if it is a get request
    if request.method == 'GET':
        available_llms_query = queries.get_available_llms()
        database_connection = RelDBConnection()
        # if the connection is not an exception, get the available llm model names
        # otherwise, return an error message to the user and render the signup page
        if not isinstance(database_connection.connect(), Exception):
            returned_llm_model_names = (database_connection.
                                        query_return_matches_specified(available_llms_query, 100))
            # convert list of tuples to list of strings
            for i in range(len(returned_llm_model_names)):
                returned_llm_model_names[i] = returned_llm_model_names[i][0]
            # render signup page with list of available llm model names
            return render_template('signup.html', llm_model_names=list(returned_llm_model_names))
        else:
            return render_template('signup.html', database_error="Database error. "
                                                                 "Please try again later.")

    elif request.method == 'POST':
        # get user input
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # get api keys for each llm model name and store in dictionary
        llm = {}
        if (request.form.get('api_key_{{llm_model_name}})' is not None) or
                (request.form.get('api_key_{{llm_model_name}})' is not ""))):
            llm[request.form['llm_model_name']] = request.form['api_key_{{llm_model_name}}']
        # check if user exists
        database_connection = RelDBConnection()
        params = (username,)
        returned_user_information = (
            database_connection.query_return_first_match_with_parameter(queries.check_user_exists(), params))
        # if user exists
        if returned_user_information:
            # get available llm model names
            # TODO: Clean up reused code
            available_llms_query = queries.get_available_llms()
            returned_llm_model_names = (database_connection.
                                        query_return_matches_specified(available_llms_query, 100))
            # convert list of tuples to list of strings
            for i in range(len(returned_llm_model_names)):
                returned_llm_model_names[i] = returned_llm_model_names[i][0]
            # redirect to login page
            return render_template('signup.html', username_taken_error="User already exists",
                                   llm_model_names=list(returned_llm_model_names))
        # if user does not exist
        else:
            # create salt and hashed password
            salt, hashed_password = database_scripts.create_salted_user_password(password)
            # create user in database
            params = (username, first_name, last_name, hashed_password, salt)
            database_connection.commit_query_with_parameter(queries.create_user(), params)

            # store api keys in database
            for key, value in llm.items():
                params = (username, key, value)
                database_connection.commit_query_with_parameter(queries.create_api_key(), params)

            # store user information in session
            session['username'] = username
            session['user_first_name'] = first_name
            session['user_last_name'] = last_name

            # get first llm model name & api key from dictionary
            first_llm_model_name = list(llm.keys())[0]
            first_api_key = list(llm.values())[0]
            # store api key in session
            session['api_key'] = first_api_key

            # redirect to login page
            return render_template('index.html', session=session)
    else:
        return render_template('signup.html', database_error="Database error. "
                                                             "Please try again later.")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
