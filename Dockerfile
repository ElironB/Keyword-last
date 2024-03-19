# Use the official Selenium Chrome standalone image as the base
FROM selenium/standalone-chrome:latest

# Switch to root to install additional dependencies
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app

# Document that the service listens on port 5000.
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
