import mlflow

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical

def parse_data():
    iris = load_iris()
    
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_labels = to_categorical(y_train)
    test_labels = to_categorical(y_test)

    return X_train, X_test, train_labels, test_labels


def build_model(nodes):
    model = models.Sequential()
    model.add(layers.Dense(nodes, activation='relu', input_shape=(4,)))
    model.add(layers.Dense(3, activation='softmax'))
    model.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    
    X_train, X_test, train_labels, test_labels = parse_data()
    
    mlflow.set_experiment("mlflow-modal-example")
    mlflow.set_tag("mlflow.runName", "tensorflow")

    epochs = 50
    batch_size = 20
    nodes = 512

    mlflow.log_param("epochs", epochs)
    mlflow.log_param("batch_size", batch_size)
    mlflow.log_param("nodes", nodes)

    model = build_model(nodes)
    model.fit(X_train, train_labels, epochs=epochs, batch_size=batch_size)
    test_loss, test_acc = model.evaluate(X_test, test_labels)

    mlflow.log_metric("test_loss", test_loss)
    mlflow.log_metric("test_acc", test_acc)

    mlflow.tensorflow.log_model(model, "iris-tf")
