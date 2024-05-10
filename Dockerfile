# Use the official Python base image
FROM python:3.11.6-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirement.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# # Run app.py when the container launches
# CMD ["python", "app.py"]