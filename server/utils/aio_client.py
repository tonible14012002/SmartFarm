from Adafruit_IO import Client
from .settings import AIO_USERNAME, AIO_KEY


# aio_client
def initialize_aio_api_client():
    return Client(AIO_USERNAME, AIO_KEY)
