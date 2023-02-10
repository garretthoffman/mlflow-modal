import logging
from typing import List, Optional

import mlflow.pyfunc
from mlflow.deployments import BaseDeploymentClient, PredictionsResponse
from mlflow.exceptions import MlflowException

from mlflow_modal.config import ModalConfig

try:
    import ujson as json
except ModuleNotFoundError:
    import json

logger = logging.getLogger(__name__)


def target_help() -> str:
    help_string = (
        "The mlflow-modal plugin integrates Modal"
        "with the MLFlow deployments API.\n\n"
        "Before using this plugin, you must set create an account"
        "and API Token at https://modal.com/.\n\n"
        "You must have the following environment variabled configured to allow"
        "the plugin to integrate with your modal workspace\n\n"
        "    * MODAL_TOKEN_ID\n"
        "    * MODAL_TOKEN_SECRET\n"
        "    * MODAL_WORKSPACE\n\n"
        "Basic usage:\n\n"
        "    mlflow deployments <command> -t modal\n\n"
        "For more details and examples, see the README at"
        "https://github.com/garretthoffman/mlflow-modal/blob/main/README.md\n\n"
    )
    return help_string


def run_local(name, model_uri, flavor=None, config=None):
    # TODO implement
    raise MlflowException("mlflow-modal does not currently support run_local")


class ModalPlugin(BaseDeploymentClient):
    def __init__(self, uri: str) -> None:
        super().__init__(uri)
        self.modal_config = ModalConfig()

    def help(self) -> str:
        return target_help()

    def create_deployment(
        self,
        name: str,
        model_uri: str,
        flavor: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> dict:
        # TODO: implement
        pass

    def delete_deployment(self, name: str) -> None:
        # TODO: implement
        pass

    def update_deployment(
        self,
        name: str,
        model_uri: str,
        flavor: Optional[str] = None,
        config: Optional[dict] = None,
    ):
        # TODO: implement
        pass

    def list_deployments(self) -> List[dict]:
        # TODO: implement
        pass

    def get_deployment(self, name: str) -> dict:
        # TODO: implement
        pass

    def predict(
        self,
        deployment_name: str = None,
        inputs: List[List] = None,
    ) -> PredictionsResponse:
        # TODO: implement
        pass
