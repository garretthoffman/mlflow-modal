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


## Usage
The `mlflow-modal` plugin integrates Modal with the MLFlow deployments API.

Before using this plugin, you must set create an account and API Token at https://modal.com/.

You must have the following environment variables configured to allow the plugin to integrate with your Modal workspace:

* `MODAL_TOKEN_ID`
* `MODAL_TOKEN_SECRET`
* `MODAL_WORKSPACE`

The API is summarized below. For full details see the MLflow deployment plugin [Python API] and [command-line interface] documentation.

### Create deployment
Deploy a model built with MLflow as a Modal webhook with the desired [configuration parameters]; for example, `gpu` or `keep_warm`.  Currently this plugin only supports the `python_function` flavor of MLflow models that expect a numpy array as input and return a numpy array as output. The `python_function` flavor is the default flavor so this is not required to be specified in commands.

Model deployments on Modal create a REST API endpoint at `https://<modal workspace>--mlflow-<deployment name>-predict.modal.run`. The endpoint accepts POST requests with a body specifying `input` and returns a response with a body specifying `predictions`. For example:

```bash
vscode@ccd6dde2dbf5:/workspaces/mlflow-modal$ curl -X POST https://workspace--mlflow-add5-predict.modal.run -d '{"input": [[1,2,3,4,5],[6,7,8,9,10]]}' --header "Content-Type: application/json"
{"predictions":[[6.0,7.0,8.0,9.0,10.0],[11.0,12.0,13.0,14.0,15.0]]}
```

##### CLI
```bash
mlflow deployments create -t modal -m <model uri> --name <deployment name> -C gpu=T4 -C keep_warm=true
```

##### Python API
```python
from mlflow.deployments import get_deploy_client
target_uri = "modal"
plugin = get_deploy_client(target_uri)
plugin.create_deployment(
    name="<deployment name>",
    model_uri="<model uri>",
    config={"gpu": "T4", "keep_warm"=True})
```

### Update deployment
Modify the configuration of a deployed model and/or replace the deployment with a new model URI.

##### CLI
```bash
mlflow deployments update -t modal --name <deployment name> -C gpu=A100
```

##### Python API
```python
plugin.update_deployment(name="<deployment name>", config={"gpu": "A100"})
```

### Delete deployment
Delete an existing deployment.

##### CLI
```bash
mlflow deployments delete -t modal --name <deployment name>
```

##### Python API
```python
plugin.delete_deployment(name="<deployment name>")
```

### List deployments
List the details of all the models deployed on Modal. This includes only models deployed via this plugin.

##### CLI
```bash
mlflow deployments list -t modal
```

##### Python API
```python
plugin.list_deployments()
```

### Get deployment details
Fetch the details associated with a given deployment. This includes Modal `app_id`, `created_at` timestamp, and the `endpoint` for the Modal webhook.

##### CLI
```bash
mlflow deployments get -t modal --name <deployment name>
```

##### Python API
```python
plugin.get_deployment(name="<deployment name>")
```

### Run prediction on deployed model
For the prediction inputs, the Python API expects a pandas DataFrame. To invoke via the command line, pass in the path to a JSON file containing the input.

##### CLI
```bash
mlflow deployments predict -t modal --name <deployment name> --input-path <input file path> --output-path <output file path>
```

`output-path` is an optional parameter. Without it, the result will be printed in the terminal.

##### Python API
```python
plugin.predict(name="<deployment name>", inputs=<prediction input>)
```

### Run the model deployment "locally"
Run an ephemeral deployment of your model using [`modal serve`]. This will behave exactly the same as `mlflow deployments create -t modal` however the app will stop running approximately 5 minutes after you hit Ctrl-C. While the app is running Modal will create a temporary URL that you can use like the normal web endpoint created by Modal. 

##### CLI
```bash
mlflow deployments run-local -t modal -m <model uri> --name <deployment name> -C gpu=T4 -C keep_warm=true
```

### Plugin help
Prints the plugin help string.

##### CLI
```bash
mlflow deployments help -t modal
```

[Python API]: https://www.mlflow.org/docs/latest/python_api/mlflow.deployments.html
[command-line interface]: https://www.mlflow.org/docs/latest/cli.html#mlflow-deployments
[configuration parameters]: https://modal.com/docs/reference/modal.Stub#webhook
[`modal serve`]: https://modal.com/docs/guide/webhooks#developing-with-modal-serve
