from flask import Flask, request
from utils import db
from utils.aio_client import (
    initialize_client,
    register_handlers,
    start_client,
)
from utils.settings import (
    AIO_BUTTON_FEED_IDs,
    AIO_FEED_IDs
)

class LogEvent:
    overbound = 'overbound'
    buttonswitch = 'button'

app = Flask(__name__)

aio = initialize_client()

# update feed data to firebase
@register_handlers('on_message', feed_id='light')
def handle_sensor_data_change(client, payload):
    db.update_sensor_data('light', payload)

@register_handlers('on_message', feed_id='humidity')
def handle_sensor_data_change(client, payload):
    db.update_sensor_data('humidity', payload)

@register_handlers('on_message', feed_id='temperature')
def handle_sensor_data_change(client, payload):
    db.update_sensor_data('temperature', payload)

# check bound for logging
@register_handlers('on_message', feed_id="light")
def handle_check_bound(client, payload):
    payload = int(payload)
    light_threshold = db.get_threshold("light")

    if payload < light_threshold:
        db.append_log_data(
            feed_id='light',
            event='overbound',
            value=payload
        )

# server views
@app.route('/button/<feed_id>', methods=['POST'])
def public_feed(feed_id):
    if (feed_id) not in AIO_BUTTON_FEED_IDs:
        return {'status': 'error', 'msg': 'Can only public to button feed'}, 400
        
    if not request.is_json:
        return {'status': 'error', 'msg': 'Request must be json'}, 400

    value = request.json.get('value')
    if value is None:
        return {'status': 'error', 'msg': 'Request must include feed value'}, 400

    try:
        aio.publish(feed_id, value=value)
        db.append_log_data(feed_id, event=LogEvent.buttonswitch, value=value)
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}, 400
    return {'status': 'ok', 'data': value}, 200


@app.route('/threshold/<feed_id>', methods=['POST'])
def set_bound(feed_id):
    if feed_id not in AIO_FEED_IDs:
        return {'status':'error', 'msg': 'Set bound only work wiht sensor feed id'}, 400
    if not request.is_json:
        return {'status': 'error', 'msg': 'Request must be json'}, 400
    value = request.json.get('value')
    try:
        db.update_threshold(feed_id=feed_id, value=value)
        return {'status': 'ok', 'data': value}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}, 400

if __name__ == '__main__':
    start_client()
    app.run(host='0.0.0.0')