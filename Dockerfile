# Use Python slim image as base
FROM python:3.9-slim

# Set environment variables to avoid Python buffer issues
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code, excluding unnecessary files
COPY . .

# Exclude specific directories and files
RUN rm -rf model/training_data

# Expose port 8080
EXPOSE 8080

# Command to run the FastAPI app
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8080"]
