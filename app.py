"""
I keep app.py very thin.
"""
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

CONNECTION_STR = 'sqlite:///' + os.path.join(basedir, 'DB\\mydb.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STR
db = SQLAlchemy(app)



# Here I would set up the cache, a task queue, etc.