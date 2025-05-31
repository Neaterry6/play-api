# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the app files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 10000

# Command to run the app
CMD ["python", "app.py"]
