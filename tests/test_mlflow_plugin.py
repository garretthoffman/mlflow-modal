import os

import mlflow.pyfunc
import numpy as np
import pandas as pd
import requests

from mlflow.deployments import get_deploy_client
from mlflow.exceptions import MlflowException
from mlflow_modal import PredictRequest

try:
    import ujson as json
except ModuleNotFoundError:
    import json

modal_workspace = os.environ.get("MODAL_WORKSPACE")


class AddN(mlflow.pyfunc.PythonModel):
    def __init__(self, n):
        self.n = n

    def predict(self, context, model_input):
        return model_input + self.n


# Construct and save the model
model_path = os.path.abspath("add_n_model")

try:
    mlflow.pyfunc.save_model(path=model_path, python_model=AddN(n=5))
except MlflowException as e:
    pass

client = get_deploy_client("modal")

client.create_deployment(name="add5", model_uri=model_path)

deployment = client.get_deployment("add5")
deployments = client.list_deployments()
assert deployment in deployments

model_input = pd.DataFrame(np.arange(10.0).reshape(2, 5))
expected_output = pd.DataFrame(np.arange(5.0, 15.0).reshape(2, 5))
model_output = client.predict("add5", model_input)
assert model_output.get_predictions().equals(expected_output)

request_body = PredictRequest(input=model_input.to_numpy().tolist())
response = requests.post(
    f"https://{modal_workspace}--mlflow-add5-predict.modal.run",
    data=request_body.json(),
    headers={"Content-Type": "application/json"},
    timeout=5,
)

assert response.status_code == 200

parsed_response_body = json.loads(response.content)
assert pd.DataFrame(parsed_response_body.get("predictions")).equals(expected_output)

client.delete_deployment("add5")
