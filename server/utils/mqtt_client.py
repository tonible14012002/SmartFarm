import threading
import functools
from Adafruit_IO import MQTTClient
from .settings import (
    AIO_FEED_IDs,
    AIO_BUTTON_FEED_IDs,
    AIO_USERNAME,
    AIO_KEY
)

def __make_callback_dic(prev, cur):
    prev[cur] = []
    return prev

__handlers = {
    'on_message': functools.reduce(
        __make_callback_dic, AIO_FEED_IDs + AIO_BUTTON_FEED_IDs, {}
    ),
    'on_connect': [], 
    'on_subscribe': [],
    'on_disconnect': [],
}

mqtt_client = None

def initialize_mqtt_client():
    global mqtt_client 
    mqtt_client = MQTTClient(AIO_USERNAME, AIO_KEY)

    def handle_connect(*args, **kwargs):
        print('connected to adafruit')
        for handler in __handlers['on_connect']:
            handler(*args, **kwargs)

    def handle_message(mqtt_client, feed_id, payload):
        message_handler = __handlers['on_message'][feed_id]
        for handler in message_handler:
            handler(mqtt_client, payload, feed_id=feed_id)

    def handle_subscribe(*args, **kwargs):
        for handler in __handlers['on_subscribe']:
            handler(*args, **kwargs)
    
    def handle_disconnect(*args, **kwargs):
        for handler in __handlers['on_disconnect']:
            handler(*args, **kwargs)
    
    mqtt_client.on_connect = handle_connect
    mqtt_client.on_message = handle_message
    mqtt_client.on_subscribe = handle_subscribe
    mqtt_client.on_disconnect = handle_disconnect

    return mqtt_client

def start_mqtt_client():
    mqtt_client.connect()
    for sensor_feed in AIO_FEED_IDs:
        mqtt_client.subscribe(sensor_feed)
    for button_feed in AIO_BUTTON_FEED_IDs:
        mqtt_client.subscribe(button_feed)
    mqtt_client.loop_background()

def register_handlers(event_type='on_message', **kwargs):
    """Decorator"""
    feed_id = kwargs.get('feed_id')
    feed_ids = kwargs.get('feed_ids') if not feed_id else None

    assert event_type != 'on_message' or feed_id or feed_ids, 'on_message event must include feed_id arguments'
    
    if not feed_id:
        assert isinstance(feed_ids, list)

    def dec(func):
        if event_type == 'on_message':
            if not feed_id:
                for feed in feed_ids:
                    __handlers[event_type][feed].append(func)
            else: 
                __handlers[event_type][feed_id].append(func)
        else:
            __handlers[event_type].append(func)
    return dec

timer = None
def reset_timer():
    global timer
    timer = False

def set_timer(time):
    threading.Timer(time,reset_timer).start()

def is_timeout():
    return timer