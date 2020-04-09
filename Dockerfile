FROM python:3.8.2-slim-buster

LABEL name="heroku-django-celery-boilerplate"
MAINTAINER "Kacper Łukawski <kacper.lukawski@embassy.ai>"

RUN apt-get update && apt-get -y install gcc curl libpq-dev

RUN curl https://cli-assets.heroku.com/install.sh | sh

RUN mkdir -p /app
ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
ADD .docker/entrypoint.sh /entrypoint.sh

COPY . /app
WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
