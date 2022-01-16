FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev

COPY prefect/*.py /app/
COPY prefect/requirements.txt /app/requirements.txt
COPY data/*.csv /app/data/

USER root

RUN pip install -r requirements.txt