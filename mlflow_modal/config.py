import os
import typing


class ModalConfig(typing.NamedTuple):
    token_id: str = os.environ.get("MODAL_TOKEN_ID")
    token_secret: str = os.environ.get("MODAL_TOKEN_SECRET")
    workspace: str = os.environ.get("MODAL_WORKSPACE")
