# OS
FROM python:3.6

# Port to access to the app
ENV PORT 8002

# Workdir in which there is the app
WORKDIR .

# Copy the requirements file in order to install the depedencies
COPY docker_requirements.txt src/ app.py docker_requirements.txt run_huey.sh ./

# Update the SO and pip. Then, the libraries will be installed
RUN apt-get update && pip install --upgrade pip && pip install --requirement docker_requirements.txt

# Create a non-user root to run the container with it
RUN useradd -m user_lidia
USER user_lidia

# Info about the avalaible port to access the app.
EXPOSE 8002

# Run the server task Huey from a bash script
RUN /bin/bash run_huey.sh

# Run the dash app through Gunicorn.
CMD gunicorn -b 0.0.0.0:8002 app:server
