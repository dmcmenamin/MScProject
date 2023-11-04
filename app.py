from flask import Flask, render_template
from werkzeug.serving import run_simple

app = Flask(__name__)


@app.route('/')
def index():
    # return 'Hello World!'
    return render_template('index.html')


if __name__ == '__main__':
    # ssl_context = ('dynamic_powerpoint.pem', 'dynamic_powerpoint.pem')
    ssl_context = ('dynamicPowerPoint.crt', 'dynamicPowerPoint.key')
    run_simple('localhost', 443, app, use_reloader=True, use_debugger=True, use_evalex=True, ssl_context=ssl_context)
    # app.run(ssl_context=ssl_context, debug=True, threaded=True, port=5050)
