#!/usr/bin/python3
''' Start flask'''

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
