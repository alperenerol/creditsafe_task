# Use an official Python runtime as a base image
FROM python:3.10-slim
# if macOS Silicon: 
# FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies: Poppler and Tesseract OCR
RUN apt-get update && apt-get install -y \
    poppler-utils \  
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*  # Clean up APT cache to reduce image size

# Copy the requirements file and install dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Copy the rest of the application code into the container
COPY . /workspace

# Command to keep the container running (can be overridden by devcontainer.json)
CMD ["sleep", "infinity"]