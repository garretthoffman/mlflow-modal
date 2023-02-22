from pathlib import Path

import modal
import numpy as np

from fastapi.responses import JSONResponse
from modal_utils.async_utils import synchronizer
from synchronicity import Interface

from mlflow_modal.api import PredictRequest
from mlflow_modal.config import DynamicStubConfig
from mlflow_modal.constants import DEPLOYMENT_PREFIX, ENDPOINT_PREFIX, ENDPOINT_POSTFIX

REMOTE_MODEL_PATH = "/model"


stub_config = DynamicStubConfig()

image = modal.Image.debian_slim()

if modal.is_local():
    requirements_path: Path = stub_config.get("model_path", "") / "requirements.txt"

    if requirements_path.exists():
        image = image.pip_install_from_requirements(requirements_path)
    else:
        image = image.pip_install("mlflow>=1.12.0")


deployment_stub = modal.Stub(
    name=f"{DEPLOYMENT_PREFIX}-{stub_config.get('name')}", image=image
)


class MlflowModel:
    def __enter__(self) -> None:
        import mlflow.pyfunc

        self.model = mlflow.pyfunc.load_model(REMOTE_MODEL_PATH)

    @deployment_stub.webhook(
        method="POST",
        label=f"{ENDPOINT_PREFIX}-{stub_config.get('name')}-{ENDPOINT_POSTFIX}",
        mounts=[
            *modal.create_package_mounts(["mlflow_modal"]),
            modal.Mount.from_local_dir(
                local_path=stub_config.get("model_path", ""),
                remote_path=REMOTE_MODEL_PATH,
                recursive=True,
            ),
        ],
        **stub_config.get("deploy_config", {}),
    )
    def predict(self, request: PredictRequest):
        input_data: np.ndarray = np.array(request.input)
        predictions: np.ndarray = self.model.predict(input_data)
        return JSONResponse(content={"predictions": predictions.tolist()})


def serve(stub: modal.Stub) -> None:
    blocking_stub = synchronizer._translate_out(stub, Interface.BLOCKING)
    blocking_stub.serve()
