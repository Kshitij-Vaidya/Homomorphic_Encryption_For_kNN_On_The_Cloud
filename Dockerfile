FROM python:3.9.13-slim

WORKDIR /app

# Copy the cloud server program into the container
COPY server.py .

# Install dependencies
RUN pip install jsonpickle

# Create bind mount for the query data
VOLUME /tmp/data/query_data.txt

# Create a volume mount for the prime factorisation
VOLUME /app/factors-db: /app/factors-db

# Final instruction to run the server program
CMD ["python", "server.py"]

