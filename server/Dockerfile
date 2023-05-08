FROM python:3.10-alpine

WORKDIR /server

COPY . .

RUN python -m pip install -r requirements.txt

CMD ["python", "main.py"]