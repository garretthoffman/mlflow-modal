FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y g++ curl

WORKDIR /src

COPY requirements.txt predict_input_api.json predict_input_plugin.json .

RUN pip install -r requirements.txt