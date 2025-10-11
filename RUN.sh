#!/bin/bash

echo "🏓 Foosball Tournament Manager - One-Click Launcher"
echo "================================================"

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

# Function to kill process on port
kill_port_process() {
    local port=$1
    echo "🔍 Finding process using port $port..."
    
    if command -v lsof &> /dev/null; then
        local pid=$(lsof -ti :$port)
        if [ ! -z "$pid" ]; then
            echo "⚡ Killing process $pid on port $port..."
            kill -9 $pid 2>/dev/null
            sleep 2
            return 0
        fi
    fi
    return 1
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "📦 Node.js not found. Running auto-installer..."
    ./setup.sh
else
    # Check if dependencies are installed
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing dependencies..."
        npm install
    fi
    
    # Check if port 3000 is in use
    if check_port 3000; then
        echo "⚠️  Port 3000 is already in use!"
        echo "Options:"
        echo "1) Kill the existing process and use port 3000"
        echo "2) Use a different port (3001)"
        echo "3) Exit"
        
        read -p "Choose option (1/2/3): " -n 1 -r
        echo
        
        case $REPLY in
            1)
                if kill_port_process 3000; then
                    echo "✅ Port 3000 is now available"
                    export PORT=3000
                else
                    echo "❌ Could not free port 3000, using port 3001"
                    export PORT=3001
                fi
                ;;
            2)
                echo "✅ Using port 3001"
                export PORT=3001
                ;;
            3)
                echo "❌ Exiting..."
                exit 0
                ;;
            *)
                echo "✅ Using port 3001 (default choice)"
                export PORT=3001
                ;;
        esac
    fi
    
    echo "🚀 Starting Foosball Tournament Manager..."
    echo "Server will be available at: http://localhost:${PORT:-3000}"
    echo "Press Ctrl+C to stop the server"
    echo ""
    npm start
fi