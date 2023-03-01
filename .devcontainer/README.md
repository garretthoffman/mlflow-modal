# Development Container With VS Code

For convienences a docker based development environment is provided in that can be easy built and used as a remote environment in Visual Studio Code.

## Getting Started

1. Install [Docker]
2. Install the [Visual Studio Code]
3. Install the [Dev Containers] extension
4. Open this source code in VS Code
5. Open the Command Pallete (Cmd + Shift + P) and type `Dev Containers` 
6. Select `Dev Containers: Rebuild and Reopen in Container`
7. VS Code will restart and reload, opening our workspace in the dev environment with the workspace mounted to your host
8. If prompted, select OK on the prompt to reload the workspace to load the configured VS Code plugins

[Docker]: https://www.docker.com/
[Visual Studio Code]: https://code.visualstudio.com/
[Dev Containers]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

## Environment Variables

For convenience, `.devcontainer.json` includes placeholders to set the required environment variables - `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET` and `MODAL_WORKSPACE` - in your local development environment. 

## Local Testing

An end to end test is included in `tests/test_mlflow_plugin.py`. This test is intended to be run manually as it will interact with the Modal workspace configured in your development environment. To run the test first perform a local install of the `mlflow-modal` plugin by running `pip install .` from the root of this repository. Once installed the test can be run with `python tests/test_mlflow_plugin.py`.
