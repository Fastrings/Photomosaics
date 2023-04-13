FROM python:3.11-slim

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install opencv-python-headless Flask numpy scipy gunicorn colorspacious

CMD gunicorn --workers 1 --timeout 0 --bind 0.0.0.0:8000 server:app 