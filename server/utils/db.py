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
    'threshold': db.reference('threshold/'),
    'log':db.reference('log/'),
    'token': db.reference('token/')
}

def get_threshold(feed_id):
    assert feed_id in AIO_FEED_IDs
    ref = get_ref['threshold']
    return ref.child(feed_id).get()

def update_threshold(feed_id, value):
    assert feed_id in AIO_FEED_IDs
    ref = get_ref['threshold']
    ref.child(feed_id).set(value)

def append_log_data(feed_id, event, value):
    log_data = {
        'feed': feed_id,
        'time': str(datetime.utcnow()),
        'event': event,
        'value': value
    }
    log_ref = get_ref['log']
    log_ref.push(log_data)