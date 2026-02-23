# Use the official Python image from the Docker Hub
FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget gnupg2 apt-transport-https curl unzip

# Add Google Chrome signing key (NO apt-key)
RUN wget -q -O /usr/share/keyrings/google-linux-signing-key.gpg \
    https://dl.google.com/linux/linux_signing_key.pub

# Add official Google Chrome repository
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] \
    http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome Stable
RUN apt-get update && apt-get install -y google-chrome-stable

# Set display port as an environment variable
ENV DISPLAY=:99

# Set environment variable for ChromeDriver
ENV PATH="/usr/local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (if your application requires it)
EXPOSE 420

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV FLAG="YBN{dev_flag}"
ENV WEBSITE_URL="http://binder-website:5000"
# Run the AdminBot service
CMD ["flask", "run", "--host=0.0.0.0", "--port=420"]
