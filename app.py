from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from celery_init import make_celery
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

CONNECTION_STR = 'sqlite:///' + os.path.join(basedir, 'mydb.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERYBEAT_SCHEDULE={
        'run-every-15-seconds': {
            'task': 'views.create_contact',
            'schedule': timedelta(seconds=15)
        },
        'run-every-1-minute': {
            'task': 'views.remove_contact',
            'schedule': timedelta(seconds=60)
        }
    }
)
celery = make_celery(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

