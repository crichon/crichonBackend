from app.database import *
from app.auth.model import *
from app.todo.model import *

def add_user(username, password):
    user = User()
    user.username = username
    user.hash_password(password)
    db_session.add(user)
    db_session.commit()

def init():
    pass

