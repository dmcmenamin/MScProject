from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.serving import run_simple

from src.database import queries, database_scripts
from src.database.connection import MySQLConnection

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get user input
        username = request.form['username']
        password = request.form['password']
        find_user_query = queries.check_user_exists(username)
        database_connection = MySQLConnection()
        returned_user_information = database_connection.query_return_first_match(find_user_query)
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
                find_api_key_query = queries.get_api_key(username, "chat")
                returned_api_key_information = database_connection.query_return_first_match(find_api_key_query)
                # store api key in session
                session['api_key'] = returned_api_key_information[0]
                return redirect(url_for('chatbot'))
            # if password is incorrect
            else:
                # redirect to login page
                return redirect(url_for('index'))
        # if user does not exist
        else:
            # redirect to login page
            return redirect(url_for('index'))
    else:
        return render_template('index.html')



if __name__ == '__main__':
    ssl_context = ('dynamicPowerPoint.crt', 'dynamicPowerPoint.key')
    run_simple('localhost', 443, app, use_reloader=True, use_debugger=True, use_evalex=True, ssl_context=ssl_context)
