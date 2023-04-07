#!/usr/bin/python3
''' Star flask'''

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    '''Second function. Prints on /hbnb'''
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def index_2():
    '''Second function. Prints on /hbnb'''
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def index_3(text):
    '''Prints on /c/anything'''
    return "C {}".format(text).replace('_', ' ')


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def index_4(text='is cool'):
    '''Fourth function. Prints on /python/anything'''
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def index_5(n):
    '''Prints on number if n is int'''
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')