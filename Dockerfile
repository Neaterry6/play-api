# Use official lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app files into container
COPY . .

# Expose port
EXPOSE 5000

# Run the Flask app with Gunicorn and Eventlet for Socket.IO support
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
