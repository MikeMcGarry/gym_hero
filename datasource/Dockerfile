FROM python:latest

WORKDIR /tmp/datasource

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV GYM_HERO_USERNAME $GYM_HERO_USERNAME
ENV GYM_HERO_APP_TOKEN $GYM_HERO_APP_TOKEN

CMD ["python", "workoutfetcher.py"]
