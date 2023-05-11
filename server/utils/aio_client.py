from Adafruit_IO import Client
from .settings import AIO_USERNAME, AIO_KEY


aio = Client(AIO_USERNAME, AIO_KEY)