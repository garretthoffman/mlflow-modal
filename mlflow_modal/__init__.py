import logging
import shutil
from pathlib import Path
from typing import List, Optional

import requests
import pandas as pd

from mlflow.deployments import BaseDeploymentClient, PredictionsResponse
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE
from mlflow.tracking.artifact_utils import _download_artifact_from_uri

from mlflow_modal.api import PredictRequest
from mlflow_modal.client import ModalClient
from mlflow_modal.config import DynamicStubConfig

try:
    import ujson as json
except ModuleNotFoundError:
    import json

logger = logging.getLogger(__name__)


def target_help() -> str:
    help_string = (
        "The mlflow-modal plugin integrates Modal "
        "with the MLFlow deployments API.\n\n"
        "Before using this plugin, you must set create an account "
        "and API Token at https://modal.com/.\n\n"
        "You must have the following environment variabled configured to allow "
        "the plugin to integrate with your modal workspace\n\n"
        "    * MODAL_TOKEN_ID\n"
        "    * MODAL_TOKEN_SECRET\n"
        "    * MODAL_WORKSPACE\n\n"
        "Basic usage:\n\n"
        "    mlflow deployments <command> -t modal\n\n"
        "For more details and examples, see the README at "
        "https://github.com/garretthoffman/mlflow-modal/blob/main/README.md\n\n"
    )
    return help_string


def run_local(name, model_uri, flavor=None, config=None):
    # TODO: implement support for other flavors besides pyfunc
    if flavor is not None and flavor != "python_function":
        raise MlflowException(
            message=(
                f"Flavor {flavor} specified, but only the python_function "
                f"flavor is currently supported by mlflow-modal."
            ),
            error_code=INVALID_PARAMETER_VALUE,
        )

    model_path = Path(_download_artifact_from_uri(model_uri))

    stub_config = DynamicStubConfig()
    stub_config.set(name, model_path, config)

    from mlflow_modal.stub import deployment_stub, serve

    serve(stub=deployment_stub)

    shutil.rmtree(model_path)


class ModalPlugin(BaseDeploymentClient):
    def __init__(self, uri: str) -> None:
        super().__init__(uri)
        self.modal_client = ModalClient()

    def help(self) -> str:
        return target_help()

    def create_deployment(
        self,
        name: str,
        model_uri: str,
        flavor: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> dict:
        # TODO: implement support for other flavors besides pyfunc
        if flavor is not None and flavor != "python_function":
            raise MlflowException(
                message=(
                    f"Flavor {flavor} specified, but only the python_function "
                    f"flavor is currently supported by mlflow-modal."
                ),
                error_code=INVALID_PARAMETER_VALUE,
            )

        model_path = Path(_download_artifact_from_uri(model_uri))

        stub_config = DynamicStubConfig()
        stub_config.set(name, model_path, config)

        from mlflow_modal.stub import deployment_stub

        deployment_stub.deploy()

        shutil.rmtree(model_path)

        return {
            "name": name,
            "flavor": flavor,
            "endpoint": self.modal_client.get_deployment_endpoint(name),
        }

    def delete_deployment(self, name: str) -> None:
        self.modal_client.stop_deployment(name)

    def update_deployment(
        self,
        name: str,
        model_uri: str,
        flavor: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> None:
        if not self._deployment_exists(name):
            raise MlflowException(
                f"Model {name} doesn't exist. If you trying to create new "
                "deployment, use ``create_deployment``"
            )
        self.create_deployment(name, model_uri, flavor, config)

    def list_deployments(self) -> List[dict]:
        return self.modal_client.list_deployments()

    def get_deployment(self, name: str) -> dict:
        return self.modal_client.get_deployment(name)

    def predict(
        self,
        deployment_name: str = None,
        inputs: pd.DataFrame = None,
    ) -> PredictionsResponse:
        request = PredictRequest(input=inputs.to_numpy().tolist())
        endpoint = self.modal_client.get_deployment_endpoint(deployment_name)
        response = requests.post(
            endpoint,
            data=request.json(),
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        parsed_response_body = json.loads(response.content)
        return PredictionsResponse(
            status=response.status_code, reason=response.reason, **parsed_response_body
        )

    def _deployment_exists(self, name: str) -> bool:
        deployments = self.list_deployments()
        for deploy in deployments:
            if deploy.get("name", "") == name:
                return True

        return False
