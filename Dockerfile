FROM python:3.11

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /app

COPY . /app

RUN pip install opencv-python-headless
RUN pip install Flask
RUN pip install numpy
RUN pip install scipy
RUN pip install gunicorn

EXPOSE 8080

CMD gunicorn --workers 1 --timeout 0 --bind 0.0.0.0:8000 server:app 