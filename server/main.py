from utils import db
from firebase_admin import messaging
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
from utils.aio_client import initialize_aio_api_client
from utils import predictor

def create_notify_message(feed, value):
    FCM_TOPIC = 'notify'
    body = str(feed) + ' is currently ' + str(value) + ' and can be overboud.'
    return messaging.Message(
        notification= messaging.Notification(
            title= 'Overbound Warning',
            body= body
        ),
        topic=FCM_TOPIC
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
aio = initialize_aio_api_client()
# init predictor
predictor.init_predictor(aio)

# In memory Button feed state
buttons = {feed_id: False for feed_id in AIO_BUTTON_FEED_IDs}

# Update button state
@register_handlers('on_message', feed_ids=AIO_BUTTON_FEED_IDs)
def handle_update_auto(_, payload, feed_id):
    buttons[feed_id]=int_str_to_bool(payload)
    print('set', buttons[feed_id])

# Check bound for logging
@register_handlers('on_message', feed_ids=AIO_FEED_IDs)
def handle_overbound(_, payload, feed_id):
    print('receive message')
    payload = int(payload)
    threshold = int(db.get_threshold(feed_id))

    check_is_overbound = lambda data, thres: data < thres 
    if feed_id == 'temperature':
        check_is_overbound = lambda data, thres: data > thres

    predictor.append_sample(feed_id, payload)
    predict_value = predictor.predict(feed_id)

    if check_is_overbound(predict_value, threshold):
        response = messaging.send(create_notify_message(feed_id, payload))
        print(response)

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

        button_id = AIO_CORRESPOND_BUTTON_FEEDs[feed_id]
        if is_overbound:
            print('overbound')
            mqtt_aio.publish(button_id, 1)
            set_timer(FIVE_MINUTES)
            return 

        mqtt_aio.publish(button_id, 0)

if __name__ == '__main__':

    start_mqtt_client()
    # wait for mqttto start
    import time
    time.sleep(1)

    # Fork mqtt server to broadcast button feed value
    for feed_id in buttons:
        mqtt_aio.publish(f'{feed_id}/get', value=None)

    while True:
        pass