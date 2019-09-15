from app import app, db, manager
from api import api
from models import *
from views import *

if __name__ == '__main__':
    db.create_all()
    # manager.run()
    app.run(debug=True)
