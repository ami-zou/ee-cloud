#!/bin/bash

# Ensure Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Please install Docker Desktop."
    exit 1
fi

echo "Starting Docker Compose on macOS..."
docker-compose up --build -d