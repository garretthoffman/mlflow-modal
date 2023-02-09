# Development

## Remote Interpreter using Docker and VS Code

For convienences a docker based development environment is provided in `./.devcontainer` that can be easy built and used as a remote environment in Visual Studio Code. To leverage this development environment: 

### Getting Started

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