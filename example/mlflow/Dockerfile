FROM ghcr.io/mlflow/mlflow:v2.1.1

RUN apt-get update && apt-get -y install gcc libpq-dev

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt