FROM python:3.9

WORKDIR /app

# Copy the cloud server code into the docker container
COPY cloud_server.py .

# Installing the required dependencies
RUN pip install jsonpickle
RUN pip install numpy
RUN pip install sage

# Command to run the cloud server program which is inside the docker container
CMD ["python", "cloud_server.py"]