# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR .

# Copy the rest of your application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (Django's default port)
EXPOSE 8000

# Run Django app
CMD ["python", "./src/manage.py", "runserver", "0.0.0.0:8000"]
