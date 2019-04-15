FROM python:latest

WORKDIR /tmp/datasource

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "workoutfetcher.py"]
