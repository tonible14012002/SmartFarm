from datetime import datetime
import firebase_admin
from firebase_admin import db
from .settings import (
    AIO_FEED_IDs,
    DATABASE_SERVICE_UID,
    DATABASE_CERTIFICATE_PATH,
    DATABASE_URL
)

cred = firebase_admin.credentials.Certificate(DATABASE_CERTIFICATE_PATH)

firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL,
    'databaseAuthVariableOverride': {
        'uid': DATABASE_SERVICE_UID
    }
})

db_ref_dict = {
    'light': db.reference('light/'),
    'temperature': db.reference('temperature/'),
    'humidity': db.reference('humidity/')
}


def update_sensor_data(feed_id, data):
    db_ref = db_ref_dict[feed_id]
    current = str(datetime.utcnow())

    new_data = {
        'created_at': current,
        'value': data
    }

    db_ref.child('current').set(new_data)
    db_ref.child('pass').push(new_data)
