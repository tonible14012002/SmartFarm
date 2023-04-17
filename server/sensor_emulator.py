import time
import random
from Adafruit_IO import MQTTClient
import sys


AIO_USERNAME = 'ducanh_24'
AIO_KEY = 'aio_hlBu30Wb2WD9537ZeF0HRTyvd8hS'
AIO_FEED_IDs = ['light', 'temperature', 'humidity']


def connect(client):
    print("=> Connected to server")
    for feed in AIO_FEED_IDs:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("=> Subscribed to feed")

def message(client , feed_id , payload):
    print("=> Received data " + feed_id + ": " + payload)

def disconnect(client):
    sys.exit(0)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect    = connect
client.on_message    = message
client.on_subscribe  = subscribe
client.on_disconnect = disconnect
client.connect()
client.loop_background()

count = 0
frequency = 8

while(True):
    count+=1

    if count == frequency:
        client.publish('light', str(random.randint(0, 300)))
        client.publish('temperature', str(random.randint(15, 60)))
        client.publish('humidity', str(random.randint(0, 100)))
        count = 0

    time.sleep(1)