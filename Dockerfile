# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Install system dependencies needed by yt-dlp and eventlet
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . /app

# Create downloads folder for videos
RUN mkdir -p /app/downloads

# Expose port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
