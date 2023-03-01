FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y g++ curl

COPY requirements.txt .

RUN pip install -r requirements.txt