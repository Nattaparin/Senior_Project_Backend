# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /Senior_Project_Backend

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the environment variables
ENV MYSQL_HOST localhost
ENV MYSQL_PORT 3306
ENV MYSQL_USER root
ENV MYSQL_PASSWORD marty1234
ENV MYSQL_DB pro

# Start the Flask app
CMD python ./main.py