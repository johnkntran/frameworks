FROM python:3.7-slim

RUN apt-get update && apt-get install -y build-essential python-dev

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uwsgi uwsgi.ini
