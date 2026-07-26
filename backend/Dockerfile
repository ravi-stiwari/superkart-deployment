# Use a minimal base image with Python 3.9 installed
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory on the host to the container's /app directory
COPY . .

# Install Python dependencies listed in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 7860 for the Flask API (used by the Codespace forwarded port)
EXPOSE 7860

# Define the command to run the Flask app using gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
