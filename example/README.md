# `mlflow-modal` Deployment Plugin Example

In this example, we will demonstrate how to deploy models from MLflow to Modal using the MLflow Modal Plugin. Once deployed, we demonstrate making predictions to deployed model using the plugin or hitting the model endpoints directly.

## Prerequisites

To run this example, you must install Docker and create an account and API Token at https://modal.com/.

## Environment Setup

A Docker Compose Environment is provided to handle infrastructure setup and perform model training so that we can focus on the functionality of the MLflow Modal Plugin. Before spinning up the environment, you must configure your Modal environment in `.env` by setting `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET`, and `MODAL_WORKSPACE`.

Once these are set, navigate to this directory in the terminal and run `docker-compose up -d`. This will spin up the following containers:

* `minio` - runs MinIO, an open source, high-performance object store with an Amazon S3 compatible API. This will serve as our MLflow artifact store.
* `mc` - runs commands to configure MinIO and create a bucket to store MLflow artifacts.
* `mlflow` - runs MLflow, an open-source platform for the ML lifecycle. We use this to log metrics, and artifacts from ML training job runs. We can register these runs as MLflow models and use our MLflow Modal Plugin to deploy these models directly from MLflow to Modal.
* `xgboost` - runs a script to train an xgboost model on the iris dataset, log metrics and artifacts to MLflow and register the resulting model in MLflow as `iris-xbg/1`. The training script is located in `/xgboost/train.py`.
* `pytorch` - runs a script to train a pytorch model on the iris dataset, log metrics and artifacts to MLflow and register the resulting model in MLflow as `iris-torch/1`. The training script is located in `/pytorch/train.py`.
* `mlflow-modal` - sets up an environment with the `mlflow-modal` package and its dependencies installed. We will ssh into this container to run through the example.

It may take a few seconds for the environment to spin up and for the training scripts to run. Once the environment is up and running, you can view logs for the containers by running `docker-compose logs <container name>`. You can also view the MLflow console at http://localhost:8000/ to explore runs, metrics, artifacts, and models.

## Instructions

Once your environment is up and running, run `docker-compose exec -it mlflow-modal /bin/bash` to ssh into the `mlflow-modal` container.

From inside the container, run the following command to deploy the xgboost model:

```
root@d262cf11ccf5:/src# mlflow deployments create -t modal -m models:/iris-xgb/1 --name iris-xgb
```

The `-t` parameter is the deployment target, which in our case is Modal. The `-m` parameter is the Model URI, which consists of the registered model name and version in the MLflow Model Registry.

Once run, logs will start streaming from Modal into your terminal. If this is your first time running through this example, you should be seeing logs associated with a docker image for the model deployment being built. Once the model deployment is complete, you should see logs that resemble the following:

```
✓ Initialized. View app at https://modal.com/apps/ap-{hash}
✓ Created objects.
├── 🔨 Created MlflowModel.predict => https://{workspace}--mlflow-iris-xgb-predict.modal.run
├── 🔨 Created mount /usr/local/lib/python3.10/site-packages/mlflow_modal
├── 🔨 Created mount /usr/local/lib/python3.10/site-packages/mlflow_modal
└── 🔨 Created mount /tmp/tmp{hash}
Timed out waiting for logs. View logs at https://modal.com/logs/ap-{hash} for remaining output.
✓ App deployed! 🎉

View Deployment: https://modal.com/apps/{workspace}/mlflow-deployment-iris-xgb

python_function deployment iris-xgb is created
```

Now run the same command to deploy our pytorch model and wait to see a similar output: 

```
root@d262cf11ccf5:/src# mlflow deployments create -t modal -m models:/iris-torch/1 --name iris-torch
```

We can list all of our deployed models with the `list` command:

```
root@4a80cab64fa2:/src# mlflow deployments list -t modal
List of all deployments:
[{'name': 'iris-torch', 'app_id': 'ap-{hash}', 'created_at': '2023-03-03 06:39:54+00:00', 'endpoint': 'https://{workspace}--mlflow-iris-torch-predict.modal.run'}, {'name': 'iris-xgb', 'app_id': 'ap-{hash}', 'created_at': '2023-03-03 06:34:25+00:00', 'endpoint': 'https://{workspace}--mlflow-iris-xgb-predict.modal.run'}]
```

This gives us the `name`, Modal `app_id`, `created_at` time, and Modal `endpoint` for each model.

With the models deployed, we have Modal endpoints available to make predictions. We can make predictions using the plugin. This is a good way to perform manual testing on the model deployment. The plugin expects a JSON-encoded array of records with floating point data as input. The sample data for this example can be found in `mlflow-modal/predict_input_plugin.json`. We run the predict commands as follows:

```
root@80f9e6f0e670:/src# mlflow deployments predict -t modal --name iris-xgb --input-path predict_input_plugin.json
{"status": 200, "reason": "OK", "predictions": [0, 0]}
root@80f9e6f0e670:/src# mlflow deployments predict -t modal --name iris-torch --input-path predict_input_plugin.json
{"status": 200, "reason": "OK", "predictions": [0, 0]}
```

The first few times you run these commands, you may receive timeout failures that look like the following:

```
requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='{workspace}--mlflow-iris-xgb-predict.modal.run', port=443): Read timed out. (read timeout=5)
```

This is okay! Modal does not keep containers warm by default. On this initial request, a new container is being provisioned. Our plugin allows us to pass in Modal-specific configuration via the `-C` flag. We can update our model deployments to have Modal keep the containers warm by running:

```
root@d262cf11ccf5:/src# mlflow deployments update -t modal -m models:/iris-xgb/1 --name iris-xgb -C keep_warm=true
✓ Initialized. View app at https://modal.com/apps/ap-{hash}
✓ Created objects.
├── 🔨 Created MlflowModel.predict => https://{workspace}--mlflow-iris-xgb-predict.modal.run
├── 🔨 Created mount /usr/local/lib/python3.10/site-packages/mlflow_modal
├── 🔨 Created mount /usr/local/lib/python3.10/site-packages/mlflow_modal
└── 🔨 Created mount /tmp/tmp{hash}
Timed out waiting for logs. View logs at https://modal.com/logs/ap-{hash} for remaining output.
✓ App deployed! 🎉

View Deployment: https://modal.com/apps/{workspace}/mlflow-deployment-iris-xgb
Deployment iris-xgb is updated (with flavor python_function)
```

We can also make predictions directly against the model endpoint configured by Modal. The endpoint accepts POST requests with a body specifying `input` and returns a response with a body specifying `predictions`. The sample data for this example can be found in `mlflow-modal/predict_input_api.json`. We can use `curl` to make the request (be sure to replace `{workspace}` below with the name of your Modal workspace):

```
root@d262cf11ccf5:/src# curl -X POST https://{workspace}--mlflow-iris-xgb-predict.modal.run -d @predict_input_api.json --header "Content-Type: application/json"
{"predictions":[0,0]}
root@d262cf11ccf5:/src# curl -X POST https://{workspace}--mlflow-iris-torch-predict.modal.run -d @predict_input_api.json --header "Content-Type: application/json"
{"predictions":[0,0]}
```

Now that we are done using our models, we can delete the deployments with the `delete` command:

```
root@d262cf11ccf5:/src# mlflow deployments delete -t modal --name iris-xgb
Deployment iris-xgb is deleted
root@d262cf11ccf5:/src# mlflow deployments delete -t modal --name iris-torch
Deployment iris-torch is deleted
```

Finally, run `exit` to leave the `mlflow-modal` container. Once you are back in your host machine's terminal, run `docker-compose down` to tear down the MLflow environment.
