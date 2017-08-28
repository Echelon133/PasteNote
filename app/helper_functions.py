import uuid
import datetime


def get_hash():
    return uuid.uuid4().hex[:10]


def is_expired(expiration_date):
    return expiration_date < datetime.datetime.now()    
