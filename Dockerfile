# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# We assume main.py and any other necessary files are in the same directory as the Dockerfile
# or in subdirectories that will be copied.
# For this project, main.py is in the root of project_files.
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

# Run main.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

