#!/bin/bash

REMOTE_USER="kody"
REMOTE_HOST="10.206.2.11"
REMOTE_DIR="/home/kody/kanghao/PyRobotIO-ESP32"
LOCAL_DIR="."

# Check if running from project root
if [ ! -f "Dockerfile" ]; then
    echo "Error: Dockerfile not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Sync files
rsync -avz --progress \
    --exclude '.git' \
    --exclude '.gitignore' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude 'dist' \
    --exclude 'build' \
    --exclude '*.egg-info' \
    --include 'main.py' \
    --include 'esp32fastapi.py' \
    --include 'esp32sensor.py' \
    --include 'requirements.txt' \
    --include 'docker-compose.yml' \
    --include 'Dockerfile' \
    --include 'setup.py' \
    $LOCAL_DIR/ $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/

# Check if sync was successful
if [ $? -eq 0 ]; then
    echo "ESP32 FastAPI project sync completed successfully"
else
    echo "Sync failed"
    exit 1
fi