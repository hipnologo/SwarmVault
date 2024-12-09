# Use the official Python 3.9 image as the base
FROM python:3.9-slim

# Set environment variables to ensure consistent behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (if any)
# For example, if your application requires additional packages, install them here
# RUN apt-get update && apt-get install -y <package-name> && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the create_env.sh script executable (if it's needed during runtime)
RUN chmod +x create_env.sh

# (Optional) Source the environment variables script
# If your application relies on environment variables set by create_env.sh,
# you might need to source it. However, it's generally better to set
# environment variables via Docker or Swarm configurations.
# You can include the script in the entrypoint if necessary.

# Define the default command to run the backup script
# Adjust the command as needed, for example, to use an entrypoint script
CMD ["python", "swarmvault.py"]