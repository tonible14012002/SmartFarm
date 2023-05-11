import threading
from utils import db
from utils.mqtt_client import (
    initialize_mqtt_client,
    register_handlers,
    start_mqtt_client,
    set_timer, 
    is_timeout
)

from utils.settings import (
    AIO_BUTTON_FEED_IDs,
    AIO_FEED_IDs,
    AIO_CORRESPOND_BUTTON_FEEDs
)

def int_str_to_bool(str):
    return bool(int(str))

FIVE_MINUTES = 14000

class LogEvent:
    """Enumerate for log envent name
    """
    overbound = 'overbound'
    buttonswitch = 'button'

# Mqtt_instance for talk with adafruit
mqtt_aio = initialize_mqtt_client()

# In memory Button feed state
buttons = {feed_id: False for feed_id in AIO_BUTTON_FEED_IDs}

def request_buttons_State():
    for feed_id in buttons:
        mqtt_aio.publish(f'{feed_id}/get', value=None)

# Update button state
@register_handlers('on_message', feed_ids=AIO_BUTTON_FEED_IDs)
def handle_update_auto(_, payload, feed_id):
    buttons[feed_id]=int_str_to_bool(payload)
    print('set', buttons[feed_id])

# Check bound for logging
@register_handlers('on_message', feed_ids=AIO_FEED_IDs)
def handle_overbound(_, payload, feed_id):
    payload = int(payload)
    threshold = db.get_threshold(feed_id)

    check_is_overbound = lambda data, thres: data < thres 
    if feed_id == 'temperature':
        check_is_overbound = lambda data, thres: data > thres
    is_overbound = check_is_overbound(payload, threshold)

    if is_overbound:
        db.append_log_data(
            feed_id=feed_id,
            event=LogEvent.overbound,
            value=payload
        )

    if buttons['auto-mode']:
        if is_timeout():
            print('is_time out')
            return

        print('not timeout')

        button_id = AIO_CORRESPOND_BUTTON_FEEDs[feed_id]
        if is_overbound:
            print('overbound')
            mqtt_aio.publish(button_id, 1)
            set_timer(FIVE_MINUTES)
            return 

        mqtt_aio.publish(button_id, 0)

if __name__ == '__main__':
    start_mqtt_client()
    import time
    time.sleep(1)
    request_buttons_State()
    while True:
        pass