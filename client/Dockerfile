# Use a base image that includes Python
FROM python:3.12-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire client directory into the container
COPY ./client /app

# Sleep indefinitely, allowing you to exec into the container later
CMD ["sleep", "infinity"]

