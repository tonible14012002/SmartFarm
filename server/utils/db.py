from datetime import datetime
import firebase_admin
from firebase_admin import db
from .settings import (
    DATABASE_SERVICE_UID,
    DATABASE_CERTIFICATE_PATH,
    DATABASE_URL,
    AIO_FEED_IDs
)

cred = firebase_admin.credentials.Certificate(DATABASE_CERTIFICATE_PATH)

firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL,
    'databaseAuthVariableOverride': {
        'uid': DATABASE_SERVICE_UID
    }
})

get_ref = {
    'light': db.reference('light/'),
    'temperature': db.reference('temperature/'),
    'humidity': db.reference('humidity/'),
    'log':db.reference('log/')
}

def update_sensor_data(feed_id, data):
    db_ref = get_ref[feed_id]
    current = str(datetime.utcnow())

    new_data = {
        'created_at': current,
        'value': data
    }

    db_ref.child('current').set(new_data)
    db_ref.child('pass').push(new_data)

def get_threshold(feed_id):
    assert feed_id in AIO_FEED_IDs
    ref = get_ref[feed_id]
    return ref.child('threshold').get()

def update_threshold(feed_id, value):
    assert feed_id in AIO_FEED_IDs
    ref = get_ref[feed_id]
    ref.child('threshold').set(value)

def append_log_data(feed_id, event, value):
    log_data = {
        'feed': feed_id,
        'time': str(datetime.utcnow()),
        'event': event,
        'value': value
    }
    log_ref = get_ref['log']
    log_ref.push(log_data)