# Use official Python slim image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install build dependencies (some ML packages need gcc)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to leverage cache)
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code, templates, static files, and model
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/
COPY model/ ./model/

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the app with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
