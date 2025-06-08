FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Only copy requirements first to leverage cache
COPY requirements.txt .
# Install dependencies separately to cache this layer
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all files from local cloud directory to /app in container
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]