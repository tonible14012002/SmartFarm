FROM python:3.10-alpine

WORKDIR /server

# environment var
ENV aio_username=ducanh_24
ENV aio_key=aio_EMIx55ifI5UW2wzM1q5UHvlC8y7S


COPY . .

RUN python -m pip install -r requirements.txt

CMD ["python", "main.py"]