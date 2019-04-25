FROM python:latest

WORKDIR /tmp/datasource

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV AWS_SERVER_PUBLIC_KEY $AWS_SERVER_PUBLIC_KEY
ENV AWS_SERVER_SECRET_KEY $AWS_SERVER_SECRET_KEY

CMD ["python", "workoutfetcher.py"]
