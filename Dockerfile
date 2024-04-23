# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the FastAPI application code and requirements file into the container
COPY app_langchain.py .
COPY requirements_langchain.txt .
COPY .env .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_langchain.txt

# Expose the FastAPI port (change if your FastAPI app uses a different port)
EXPOSE 8000

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "app_langchain:app", "--host", "0.0.0.0", "--port", "8000"]
