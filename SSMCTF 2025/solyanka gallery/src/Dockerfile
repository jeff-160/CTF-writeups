# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application and templates
COPY app.py .
COPY templates/ templates/
COPY flag.txt .

# Create the uploads directory and ensure it's writable
RUN mkdir uploads
RUN chmod 777 uploads # Make it world-writable for the app to save files

# Set the flag
ENV FLAG="SSMCTF{test}"

# Set a default port as an environment variable
ENV APP_PORT=5000

# Expose the port using the variable.
EXPOSE $APP_PORT

# CORRECTED CMD: Use shell form to allow variable expansion
CMD flask run --host=0.0.0.0 --port $APP_PORT