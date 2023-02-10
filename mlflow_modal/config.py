import os

from mlflow.exceptions import MissingConfigException

EXPECTED_ENV_VARs = ["MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET", "MODAL_WORKSPACE"]


class ModalConfig:
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

    def _validate_enironment(self) -> None:
        for env_var in EXPECTED_ENV_VARs:
            if env_var not in os.environ:
                raise MissingConfigException(
                    f"mlflow-modal requires {env_var} to be set."
                )
