FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /receipt-reader-bot

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for temporary receipts
RUN mkdir -p temp_receipts

# Set environment variables
ENV PYTHONPATH=/receipt-reader-bot
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE ${PORT:-8080}

# Command to run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
