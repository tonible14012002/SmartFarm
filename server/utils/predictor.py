import threading
from .settings import AIO_FEED_IDs
from sklearn.linear_model import LinearRegression
import numpy as np

MAX_SAMPLE_SIZE = 20

feed_data_samples = {
    # AIO_FEED_IDs
}

def extract_datapoint_value(data):
    return data.value

def init_predictor(aio_client):
    for feed_id in AIO_FEED_IDs:
        feed_data_list = aio_client.data(feed_id, max_results=MAX_SAMPLE_SIZE)
        values = list(map(extract_datapoint_value, feed_data_list))
        feed_data_samples[feed_id] = values

def append_sample(feed_id, value):
    feed_data_samples[feed_id].append(value)
    if len(feed_data_samples[feed_id]) == MAX_SAMPLE_SIZE:
        feed_data_samples[feed_id].pop(0)
    
def predict(feed_id):
    samples = feed_data_samples[feed_id]
    X = np.arange(len(samples)).reshape(-1,1)
    Y = np.array(samples)
    model = LinearRegression().fit(X, Y)
    next_index = len(samples)
    return model.predict([[next_index]])[0]

timer = None
def reset_timer():
    global timer
    timer = False

def set_timer(time):
    threading.Timer(time,reset_timer).start()

def is_timeout():
    return timer