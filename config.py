import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'SecretKeyForSessionSigning'

DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.sql')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"

del os
