import logging
from typing import Optional

from mlflow_modal.config import ModalConfig

import mlflow.pyfunc
from mlflow.deployments import BaseDeploymentClient
from mlflow.exceptions import MlflowException

try:
    import ujson as json
except ModuleNotFoundError:
    import json

logger = logging.getLogger(__name__)


def target_help():
    # TODO: implement
    pass


def run_local(name, model_uri, flavor=None, config=None):
    # TODO implement
    raise MlflowException("mlflow-modal does not currently support run_local")


class ModalPlugin(BaseDeploymentClient):
    def __init__(self, target_uri):
        super().__init__(target_uri)
        self.modal_config = ModalConfig()
        # TODO: implement
        pass

    def help(self):
        return target_help()

    def create_deployment(
        self, name, model_uri, flavor=None, config=None, endpoint=None
    ):
        # TODO: implement
        pass

    def delete_deployment(self, name, config=None, endpoint=None):
        # TODO: implement
        pass

    def update_deployment(
        self, name, model_uri=None, flavor=None, config=None, endpoint=None
    ):
        # TODO: implement
        pass

    def list_deployments(self, endpoint=None):
        # TODO: implement
        pass

    def get_deployment(self, name, endpoint=None):
        # TODO: implement
        pass

    def predict(self, deployment_name=None, inputs=None, endpoint=None):
        # TODO: implement
        pass
