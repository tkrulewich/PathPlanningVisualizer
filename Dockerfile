# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for non-interactive apt installations
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in Docker to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the required system packages and then the Python packages from requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tk \
    tcl \
    python3-tk && \
    pip install --trusted-host pypi.python.org -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
ENTRYPOINT ["python", "index.py"]
