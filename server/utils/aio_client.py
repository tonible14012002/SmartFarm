import functools
from Adafruit_IO import MQTTClient
from .settings import (
    AIO_FEED_IDs,
    AIO_USERNAME,
    AIO_KEY
)

def __make_callback_dic(prev, cur):
    prev[cur] = []
    return prev

__handlers = {
    'on_message': functools.reduce(
        __make_callback_dic,AIO_FEED_IDs, {}
    ),
    'on_connect': [], 
    'on_subscribe': [],
    'on_disconnect': [],
}

client = None

def initialize_client():
    global client 
    client = MQTTClient(AIO_USERNAME, AIO_KEY)

    def handle_connect(*args, **kwargs):
        print('connected to adafruit')
        for handler in __handlers['on_connect']:
            handler(*args, **kwargs)

    def handle_message(client, feed_id, payload):
        message_handler = __handlers['on_message'][feed_id]
        print(message_handler)
        for handler in message_handler:
            print(handler)
            handler(client, payload)

    def handle_subscribe(*args, **kwargs):
        for handler in __handlers['on_subscribe']:
            handler(*args, **kwargs)
    
    def handle_disconnect(*args, **kwargs):
        for handler in __handlers['on_disconnect']:
            handler(*args, **kwargs)
    
    client.on_connect = handle_connect
    client.on_message = handle_message
    client.on_subscribe = handle_subscribe
    client.on_disconnect = handle_disconnect

def start_client():
    client.connect()
    for feed_id in AIO_FEED_IDs:
        client.subscribe(feed_id)
    client.loop_background()

def register_handlers(event_type='on_message', **kwargs):
    """Decorator"""
    if event_type == 'on_message' and not kwargs.get('feed_id'):
        raise KeyError('on_message event must include feed_id arguments')
    def dec(func):
        if event_type == 'on_message':
            feed_id = kwargs.get('feed_id')
            __handlers[event_type][feed_id].append(func)
        else:
            [event_type].append(func)
    return dec

