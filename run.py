import os
from app import app
from app.database import init_db

if __name__ == '__main__':
    if not os.path.exists('app.sqlite'):
        init_db()
    app.run(debug=True, threaded=True)
