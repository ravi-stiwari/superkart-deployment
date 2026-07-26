# Use a minimal base image with Python 3.9 installed
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory on the host to the container's /app directory
COPY . .

# Install Python dependencies listed in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 8501 for Streamlit (used by the Codespace forwarded port)
EXPOSE 8501

# Run the Streamlit app, accessible externally
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]

# NOTE: XSRF protection is disabled to allow batch-file uploads through the forwarded URL
