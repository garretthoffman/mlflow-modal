FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y g++

WORKDIR /src

COPY requirements.txt .
COPY train.py /src

RUN pip install -r requirements.txt