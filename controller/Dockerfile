FROM python:latest

WORKDIR /tmp/controller

COPY ./python-flask-app/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /tmp/controller/python-flask-app

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
