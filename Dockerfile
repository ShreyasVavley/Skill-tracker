# Use the official lightweight Python image
FROM python:3.10-slim

# Set the working directory to the root of the project
WORKDIR /app

# Copy the backend requirements and install dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the application files
COPY backend ./backend
COPY frontend ./frontend

# Change working directory to backend so Uvicorn runs correctly with relative imports
WORKDIR /app/backend

# Expose the port Uvicorn will run on
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
