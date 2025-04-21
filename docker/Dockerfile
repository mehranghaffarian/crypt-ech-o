# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first to install dependencies
COPY ../requirements.txt /app/requirements.txt

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including main.py) into the container
COPY ../ /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "main.py"]
