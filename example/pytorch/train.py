import mlflow
import torch
import torch.nn as nn
import torch.nn.functional as F

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from torch.autograd import Variable


class Model(nn.Module):
    def __init__(self, nodes):
        super(Model, self).__init__()
        self.fc = nn.Linear(4, nodes, dtype=torch.float64)
        self.out = nn.Linear(nodes, 3, dtype=torch.float64)

    def forward(self, x):
        x = F.relu(self.fc(x))
        x = F.softmax(self.out(x), dim=1)
        return x

    def __call__(self, x):
        x = self.forward(x)
        x = torch.argmax(x, dim=1)
        return x


def parse_data():
    iris = load_iris()

    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train = Variable(torch.from_numpy(X_train)).double()
    y_train = Variable(torch.from_numpy(y_train)).long()
    X_test = Variable(torch.from_numpy(X_test)).double()
    y_test = Variable(torch.from_numpy(y_test)).long()

    return X_train, X_test, y_train, y_test


def train_model(model, epochs, optimizer, loss_fn, X_train, y_train):
    for i in range(epochs):
        y_pred = model.forward(X_train)
        loss = loss_fn(y_pred, y_train)

        if i % 10 == 0:
            print(f"Epoch: {i} Loss: {loss}")

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


def evaluate_model(model, X_test, y_test):
    with torch.no_grad():
        y_pred = model.forward(X_test)
        correct = (torch.argmax(y_pred, dim=1) == y_test).type(torch.FloatTensor)

    return correct.mean().item()


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = parse_data()

    mlflow.set_tag("mlflow.runName", "pytorch")

    epochs = 100
    nodes = 50
    lr = 0.001

    mlflow.log_param("epochs", epochs)
    mlflow.log_param("nodes", nodes)
    mlflow.log_param("lr", lr)

    model = Model(nodes)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    train_model(model, epochs, optimizer, criterion, X_train, y_train)
    test_acc = evaluate_model(model, X_test, y_test)

    mlflow.log_metric("test_acc", test_acc)

    mlflow.pytorch.log_model(model, "iris-torch")

    run_id = mlflow.last_active_run().info.run_id
    model_uri = "runs:/{}/iris-torch".format(run_id)

    mv = mlflow.register_model(model_uri, "iris-torch")
    print(f"Registered mlflow model with Name: {mv.name} and Version: {mv.version}")
