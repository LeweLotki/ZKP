# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code into the container
COPY ./server /app

# Expose the port on which the FastAPI server will run
EXPOSE 8000

# Set the environment variable for FastAPI to know where to look for the app
ENV UVICORN_CMD="uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Command to run the FastAPI app
CMD ["sh", "-c", "$UVICORN_CMD"]

