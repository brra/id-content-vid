# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get install -y git curl && \
    apt-get install -y exiftool && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install opencv-python-headless deepface google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Create application directories
RUN mkdir -p /app/input /app/output /app/scripts /app/logs

# Copy scripts into the container
COPY analyze_video.py /app/scripts/
COPY file_operations.py /app/scripts/
COPY google_sheets.py /app/scripts/

# Set the working directory
WORKDIR /app

# Set environment variables
ENV INPUT_DIR=/app/input
ENV OUTPUT_DIR=/app/output

# Set the entry point to the file_operations script
ENTRYPOINT ["python", "/app/scripts/file_operations.py"]
