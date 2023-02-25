from pathlib import Path
from typing import Any, Callable, Optional, Type, Union

from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE


def validate_bool_input(input: str):
    truthy = {"1", "true"}
    falsey = {"0", "false"}

    if input.lower() not in truthy | falsey:
        raise ValueError(f"bool input must be one of {truthy | falsey}")

    return input.lower in truthy


class DeploymentParamValidator:
    def __init__(self, expected_type: Type, validation_fn: Callable[[str], Any] = None):
        self.expected_type = expected_type
        self.validation_fn = validation_fn if validation_fn else self.expected_type

    def validate(self, input):
        return self.validation_fn(input)


class DynamicStubConfig:
    """
    Dynamic config object to allow global state to be configured via the plugin
    and propagated to the Modal stub. This is necesary as there are current
    restrictions around the scope that Modal functions can be defined under
    (must be functions defined in global scope or methods of classes defined in
    global scope).

    The intended use of this configuration is that an instance can be created
    during plugin invocation and used to set the configuration passed by the
    user to the plugin. Another instance is later instantiated and used by our
    stub. This second isntance will have the same state as the first instance
    used to set the state.
    """

    __shared_state = {}

    _DEPLOY_CONFIG_VALIDATORS = {
        "gpu": DeploymentParamValidator(str),
        "cpu": DeploymentParamValidator(float),
        "memory": DeploymentParamValidator(int),
        "retries": DeploymentParamValidator(int),
        "concurrency_limit": DeploymentParamValidator(int),
        "container_idle_timeout": DeploymentParamValidator(int),
        "timeout": DeploymentParamValidator(int),
        "keep_warm": DeploymentParamValidator(bool, validate_bool_input),
        "cloud": DeploymentParamValidator(str),
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    def set(self, name: str, model_path: Path, deploy_config: Optional[dict]) -> None:
        self.name = name
        self.model_path = model_path
        self.deploy_config = self.parse_deploy_config(deploy_config)

    def get(self, attribute, default=None) -> Optional[Union[str, Path, dict]]:
        return self.__dict__.get(attribute, default)

    def parse_deploy_config(self, deploy_config: dict) -> None:
        parsed_config = {}

        if deploy_config:
            for key, value in deploy_config.items():
                if key not in self._DEPLOY_CONFIG_VALIDATORS:
                    raise MlflowException(
                        message=(
                            f"{key} is not a configurable parameter for a Modal webhook. See Modal "
                            "webhook documentation: https://modal.com/docs/reference/modal.Stub"
                        ),
                        error_code=INVALID_PARAMETER_VALUE,
                    )

                try:
                    validated_value = self._DEPLOY_CONFIG_VALIDATORS[key].validate(
                        value
                    )
                    parsed_config[key] = validated_value
                except ValueError as exc:
                    raise MlflowException(
                        message=(
                            f"deployment configuration '{key}' must be "
                            f"type {self._DEPLOY_CONFIG_VALIDATORS[key].expected_type}"
                        ),
                        error_code=INVALID_PARAMETER_VALUE,
                    ) from exc

        return parsed_config
