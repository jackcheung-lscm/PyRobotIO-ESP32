#!/bin/bash

# Check if running from correct directory
if [ ! -f "docker-compose.yml" ]; then
    echo "Error: docker-compose.yml not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

case "$1" in
    "start")
        sudo docker-compose up -d --build
        ;;
    "stop")
        sudo docker-compose down
        ;;
    "restart")
        sudo docker-compose down
        sudo docker-compose up -d --build
        ;;
    "build")
        sudo docker-compose build
        ;;
    "logs")
        sudo docker-compose logs -f --tail=100
        ;;
    "status")
        sudo docker-compose ps
        curl -s http://localhost:8000/healthy
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|build|logs|status}"
        exit 1
        ;;
esac