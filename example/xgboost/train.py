import mlflow
import numpy as np

from sklearn import metrics
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

def parse_data():
    iris = load_iris()
    
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    
    X_train, X_test, y_train, y_test = parse_data()
    
    mlflow.set_tag("mlflow.runName", "xgb")

    model = XGBClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    test_acc = metrics.accuracy_score(y_test, y_pred)

    mlflow.log_metric("test_acc", test_acc)

    mlflow.xgboost.log_model(model, "iris-xgb")
