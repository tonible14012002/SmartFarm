from utils import db
from utils.aio_client import (
    initialize_client,
    register_handlers,
    start_client
)

initialize_client()

@register_handlers('on_message', feed_id='light')
def handle_sensor_data_change(client, payload):
    db.update_sensor_data('light', payload)

@register_handlers('on_message', feed_id='humidity')
def handle_sensor_data_change(client, payload):
    db.update_sensor_data('humidity', payload)

@register_handlers('on_message', feed_id='temperature')
def handle_sensor_data_change(client, payload):
    db.update_sensor_data('temperature', payload)

@register_handlers('on_subscribe')
def handle_subscribe_success(*args, **kwargs):
    print(args, kwargs)
    print('=> Subscribed feed')

start_client()

while True:
    pass
