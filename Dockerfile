# Use an official Python runtime as a parent image
FROM python:3.7.9-slim-buster

# Set the working directory
WORKDIR /home/albuminator

# Copy the current directory contents into the container
COPY requirements.txt /home/albuminator

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt --no-cache-dir

# 

COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

RUN chmod +x "entry-point.sh"

# Run when the container launches
ENTRYPOINT ["./entry-point.sh"]
