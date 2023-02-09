FROM python:3.10-bullseye

# Keeps Python from generating .pyc files in the container 
ENV PYTHONDONTWRITEBYTECODE=1 
 
# Turns off buffering for easier container logging 
ENV PYTHONUNBUFFERED=1 

# Copying the requirements, this is needed because at this point the volume isn't mounted yet
COPY requirements.txt .
RUN pip install -r requirements.txt

# Similar to the above, but with just the development-specific requirements
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Add vs code user so dev container doesn't run as root
RUN useradd -ms /bin/bash vscode
