# mlflow-modal

A plugin that integrates [Modal] with MLflow. `mlflow-modal` enables MLflow users to deploy their models to serverless, scalable endpoints seamlessly with zero infrastructure.

[Modal]: https://www.modal.com

## Installation

```bash
pip install mlflow-modal
```

The following packages are required and will be installed with the plugin:

1. `"modal-client"`
2. `"mlflow>=1.12.0"`

## Development

### Remote Interpreter using Docker and VS Code

For convienences a docker based development environment is provided in `./.devcontainer` that can be easy built and used as a remote environment in Visual Studio Code. To leverage this development environment: 

1. Install the [Visual Studio Code]
2. Install the [Dev Containers] extension
3. Open this source code in VS Code
4. Open the Command Pallete (Cmd + Shift + P) and type `Dev Containers` 
5. Select `Dev Containers: Rebuild and Reopen in Container`
6. VS Code will restart and reload, opening our workspace in the dev environment with the workspace mounted to your host
7. If prompted, select OK on the prompt to reload the workspace to load the configured VS Code plugins

[Visual Studio Code]: https://code.visualstudio.com/
[Dev Containers]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
