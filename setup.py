import setuptools

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setuptools.setup(
    name="mlflow-modal",
    version="0.1.0",
    author="garretthoffman",
    author_email="garrett.lee.hoffman@gmail.com",
    description="Modal MLflow deployment plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/garretthoffman/mlflow-modal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: System :: Distributed Computing",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    install_requires=["modal-client", "mlflow>=1.12.0"],
    entry_points={"mlflow.deployments": "modal=mlflow_modal"},
    license="Apache 2.0",
)
