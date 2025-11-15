#!/bin/bash

# Foosball Tournament Manager - Auto Deploy Script
# This script automatically deploys the application using Docker

echo "⚽︎ Foosball Tournament Manager - Auto Deploy"
echo "==========================================="

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed!"
        echo "Please install Docker from https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed!"
        echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
        exit 1
    fi

    echo "✅ Docker and Docker Compose detected"
}

# Function to check if port is in use
check_port() {
    local port=$1
    if command -v lsof &> /dev/null; then
        lsof -i :$port &> /dev/null
    elif command -v netstat &> /dev/null; then
        netstat -ln | grep ":$port " &> /dev/null
    else
        # Fallback: try to bind to the port
        (echo >/dev/tcp/localhost/$port) &>/dev/null
    fi
}

# Function to stop existing containers
stop_containers() {
    echo "🛑 Stopping existing containers..."
    docker-compose down 2>/dev/null || true
}

# Function to clean up Docker resources
cleanup_docker() {
    echo "🧹 Cleaning up Docker resources..."

    # Stop all containers
    docker stop $(docker ps -aq) 2>/dev/null || true

    # Remove all containers
    docker rm $(docker ps -aq) 2>/dev/null || true

    # Remove all networks
    docker network prune -f 2>/dev/null || true

    # Remove dangling images
    docker image prune -f 2>/dev/null || true

    # Remove unused volumes
    docker volume prune -f 2>/dev/null || true

    echo "✅ Docker cleanup completed"
}

# Function to build and start containers
deploy_app() {
    echo "🏗️  Building and starting containers..."

    # Check if port 8080 is in use
    if check_port 8080; then
        echo "⚠️  Port 8080 is already in use!"
        echo "Stopping existing deployment..."
        stop_containers
        sleep 2
    fi

    # Build and start containers
    if docker-compose up -d --build; then
        echo "✅ Deployment successful!"
        echo ""
        echo "🌐 Application is running at:"
        echo "   http://localhost:8080"
        echo ""
        echo "📊 To view logs: docker-compose logs -f"
        echo "🛑 To stop: docker-compose down"
        echo "🔄 To restart: docker-compose restart"
    else
        echo "❌ Deployment failed!"
        exit 1
    fi
}

# Function to deploy with production profile (includes nginx)
deploy_production() {
    echo "🏗️  Building and starting production containers (with nginx)..."

    # Check if port 8899 is in use
    if check_port 8899; then
        echo "⚠️  Port 8899 is already in use!"
        echo "Cleaning up existing deployment..."
        cleanup_docker
        sleep 2
    fi

    # Build and start containers with production profile
    if docker-compose --profile production up -d --build; then
        echo "✅ Production deployment successful!"
        echo ""
        echo "🌐 Application is running at:"
        echo "   http://localhost:8899"
        echo ""
        echo "📊 To view logs: docker-compose logs -f"
        echo "🛑 To stop: docker-compose down"
        echo "🔄 To restart: docker-compose restart"
    else
        echo "❌ Production deployment failed!"
        exit 1
    fi
}

# Main script
main() {
    # Check Docker installation
    check_docker

    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        echo "❌ docker-compose.yml not found!"
        exit 1
    fi

    # Check if Dockerfile exists
    if [ ! -f "Dockerfile" ]; then
        echo "❌ Dockerfile not found!"
        exit 1
    fi

    # Check if players.json exists
    if [ ! -f "players.json" ]; then
        echo "⚠️  players.json not found. Creating default..."
        cat > players.json << 'EOF'
{
    "championships": {
        "ghayem": 6,
        "elini": 2,
        "dinparvar": 1,
        "alivand": 1,
        "hoseinizade": 3,
        "hajali": 2,
        "dariushi": 3
    },
    "players": [
        {
            "name": "ghayem",
            "seed": 1
        },
        {
            "name": "elini",
            "seed": 3
        },
        {
            "name": "dinparvar",
            "seed": 3
        },
        {
            "name": "alivand",
            "seed": 1
        },
        {
            "name": "hoseinizade",
            "seed": 3
        },
        {
            "name": "hajali",
            "seed": 3
        },
        {
            "name": "dariushi",
            "seed": 1
        }
    ]
}
EOF
        echo "✅ Default players.json created"
    fi

    # Create backups directory if it doesn't exist
    if [ ! -d "backups" ]; then
        mkdir backups
        echo "✅ Backups directory created"
    fi

    # Deploy to production with nginx reverse proxy
    deploy_production
}

# Run main function
main