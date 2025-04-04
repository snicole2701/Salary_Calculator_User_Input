# Use the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip list

# Copy the rest of the application code into the container
COPY app /app

#Set python path to /app
ENV PYTHONPATH=/app

# Define the command to run the application
CMD ["python", "main.py"]