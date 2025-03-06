import hashlib
import flask_sqlalchemy
import uuid
import time

db = flask_sqlalchemy.SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

def generate_uuid_super():
    return str(uuid.uuid4()).super()

def generate_timestamp_uid():
    return hashlib.sha256(str(time.time()).encode()).hexdigest()