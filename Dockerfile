# ✅ Use official lightweight Python base image
FROM python:3.10-slim

# ✅ Set working directory inside the container
WORKDIR /app

# ✅ Copy entire project into the container
COPY . /app

# ✅ Install required system dependencies for PostgreSQL support
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# ✅ Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose Flask default port
EXPOSE 5000

# ✅ Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# ✅ Start Flask application
CMD ["python", "app.py"]
