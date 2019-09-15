from app import celery, db
from models import Contact

from datetime import timedelta, datetime
import random
import string


@celery.task()
def create_contact():
    username = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    first_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    last_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    contact = Contact(username=username, first_name=first_name, last_name=last_name)
    db.session.add(contact)
    db.session.commit()


@celery.task()
def remove_contact():
    time_threshold = datetime.now() - timedelta(seconds=60)
    contacts_old = Contact.query.filter(Contact.creation_time <= time_threshold)
    for c in contacts_old:
        db.session.delete(c)
    db.session.commit()
