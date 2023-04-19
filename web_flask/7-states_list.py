#!/usr/bin/python3
''' starts a Flask web application'''
from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def st_list():
    st = storage.all(State).values()
    return render_template('7-states_list.html', st=st)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
