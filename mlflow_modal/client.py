import os
import modal

from datetime import datetime
from google.protobuf import empty_pb2
from mlflow.exceptions import MissingConfigException, MlflowException
from modal.cli.utils import timestamp_to_local
from modal_proto import api_pb2
from modal_utils.async_utils import synchronizer
from typing import Optional

from mlflow_modal.constants import DEPLOYMENT_PREFIX, ENDPOINT_PREFIX, ENDPOINT_POSTFIX

EXPECTED_ENV_VARs = ["MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET", "MODAL_WORKSPACE"]


class ModalClient:
    """
    A class to validate and parse required mlflow-modal configuration

    mlflow-modal expects the following environment variables to be set:

    - MODAL_TOKEN_ID: your modal client token id
    - MODAL_TOKEN_SECRET: your modal client token secret
    - MODAL_WORKSPACE: the name of your modal workspace name
    """

    def __init__(self) -> None:
        self._validate_enironment()

        self.workspace: str = os.environ.get("MODAL_WORKSPACE")
        self.client: modal.app._Client = self._get_synchronous_modal_client()

    def _validate_enironment(self) -> None:
        for env_var in EXPECTED_ENV_VARs:
            if env_var not in os.environ:
                raise MissingConfigException(
                    f"mlflow-modal requires {env_var} to be set."
                )

    @synchronizer
    def _get_synchronous_modal_client(self) -> modal.app._Client:
        return modal.app._Client.from_env()

    @synchronizer
    async def list_deployments(self) -> dict[str]:
        deployments = []

        res: api_pb2.AppListResponse = await self.client.stub.AppList(empty_pb2.Empty())
        for app in res.apps:
            if (
                app.state == api_pb2.AppState.APP_STATE_DEPLOYED
                and app.name.startswith(DEPLOYMENT_PREFIX)
            ):
                deployment_name = app.name.replace(DEPLOYMENT_PREFIX + "-", "")
                deployment_data = {
                    "name": deployment_name,
                    "app_id": app.app_id,
                    "created_at": timestamp_to_local(app.created_at),
                    "endpoint": self.get_deployment_endpoint(deployment_name),
                }
                deployments.append(deployment_data)

        return deployments

    @synchronizer
    async def get_deployment(self, name: str) -> Optional[dict]:
        deployements = await self.list_deployments()
        for deployment in deployements:
            if deployment.get("name", "") == name:
                return deployment

        raise MlflowException(f"No deployment with name {name} found")

    @synchronizer
    async def stop_deployment(self, name: str) -> None:
        deployment = await self.get_deployment(name)
        req = api_pb2.AppStopRequest(app_id=deployment.get("app_id"))
        await self.client.stub.AppStop(req)

    def get_deployment_endpoint(self, name: str) -> str:
        return f"https://{self.workspace}--{ENDPOINT_PREFIX}-{name}-{ENDPOINT_POSTFIX}.modal.run"
