from flask import Flask, render_template, redirect, url_for, request
from src.database.connection import MySQLConnection
from werkzeug.serving import run_simple

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
        # check if user exists
        user = MySQLConnection.query_return_first_match(username=username)
        # if user exists and password is correct
        if user and user.password == password:
            # login user
            login_user(user)
            # redirect to homepage
            return redirect(url_for('index'))
        # if user doesn't exist or password is incorrect
        else:
            # redirect to login page
            return redirect(url_for('index'))


if __name__ == '__main__':
    ssl_context = ('dynamicPowerPoint.crt', 'dynamicPowerPoint.key')
    run_simple('localhost', 443, app, use_reloader=True, use_debugger=True, use_evalex=True, ssl_context=ssl_context)
