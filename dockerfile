# Use the official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 8090

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
