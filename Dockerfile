# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

RUN mkdir config
RUN mkdir downloads
RUN mkdir utils

# Copy the FastAPI application code and requirements file into the container
COPY app.py .
COPY auth.py .
COPY config config
COPY utils utils
COPY requirements.txt .
COPY automated_unittest.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port (change if your FastAPI app uses a different port)
EXPOSE 8000

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
