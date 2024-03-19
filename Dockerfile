# Use the official Selenium base image with standalone Chrome
FROM selenium/standalone-chrome:latest

USER root

# Install Python and pip
RUN sudo apt-get update && sudo apt-get install -y python3-pip

WORKDIR /app

# Copy the requirements and install the Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Define environment variable
ENV FLASK_APP=app.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
