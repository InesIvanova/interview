"""
I keep app.py very thin.
"""
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

basedir = os.path.abspath(os.path.dirname(__file__))

CONNECTION_STR = 'sqlite:///' + os.path.join(basedir, 'mydb.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STR
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



# Here I would set up the cache, a task queue, etc.