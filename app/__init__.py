from flask import Flask, abort, request, jsonify, g, url_for

#--------- App Config ----------------------

app = Flask(__name__)
app.config.from_object('config')

# must take place after app is defined, as database use app.config
from app.database import db_session, Model

# import modules route, use blueprint ??
from app.auth.views import *
from app.todo.views import todo, todos

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


#---------- Main url ----------
@app.route('/')
@auth.login_required
def initialize():
    return "Hello World"

