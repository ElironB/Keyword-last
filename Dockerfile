# Use the official Google Chrome base image
FROM docker.io/render/chromium:103.0.5060.134

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Set the entry point
CMD ["flask", "run", "--host=0.0.0.0"]
