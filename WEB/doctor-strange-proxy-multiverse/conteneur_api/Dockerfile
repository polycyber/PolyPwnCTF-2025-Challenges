# Use an official Python image as the base
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the application files
COPY server.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask server
CMD ["python", "server.py"]
