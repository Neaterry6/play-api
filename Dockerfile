# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files into container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"
