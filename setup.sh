#!/bin/bash

# Foosball Tournament Manager - Auto Setup Script
# This script automatically installs dependencies and sets up the application

echo "🏓 Foosball Tournament Manager - Auto Setup Script"
echo "=================================================="

# Function to install Node.js on different systems
install_nodejs() {
    echo "📦 Installing Node.js..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            # Ubuntu/Debian
            echo "🐧 Detected Ubuntu/Debian system"
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL/Fedora
            echo "🐧 Detected CentOS/RHEL/Fedora system"
            curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
            sudo yum install -y nodejs
        elif command -v dnf &> /dev/null; then
            # Fedora with dnf
            echo "🐧 Detected Fedora system with dnf"
            curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
            sudo dnf install -y nodejs
        elif command -v pacman &> /dev/null; then
            # Arch Linux
            echo "🐧 Detected Arch Linux system"
            sudo pacman -S nodejs npm
        else
            echo "❌ Unsupported Linux distribution"
            echo "Please install Node.js manually from https://nodejs.org/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "🍎 Detected macOS system"
        if command -v brew &> /dev/null; then
            # Use Homebrew if available
            brew install node
        else
            # Install Homebrew first, then Node.js
            echo "📦 Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install node
        fi
    else
        echo "❌ Unsupported operating system: $OSTYPE"
        echo "Please install Node.js manually from https://nodejs.org/"
        exit 1
    fi
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "🚀 Attempting to install Node.js automatically..."
    
    # Ask for permission to install
    read -p "Do you want to install Node.js automatically? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_nodejs
        
        # Verify installation
        if ! command -v node &> /dev/null; then
            echo "❌ Failed to install Node.js automatically"
            echo "Please install Node.js manually from https://nodejs.org/"
            exit 1
        fi
        echo "✅ Node.js installed successfully!"
    else
        echo "❌ Node.js installation cancelled"
        echo "Please install Node.js from https://nodejs.org/ and run this script again"
        exit 1
    fi
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "⚠️  Node.js version $NODE_VERSION detected. Version 14+ recommended."
    echo "🚀 Attempting to update Node.js..."
    install_nodejs
fi

echo "✅ Node.js $(node --version) detected"

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not available!"
    echo "🚀 npm should be installed with Node.js. Trying to fix..."
    install_nodejs
    
    if ! command -v npm &> /dev/null; then
        echo "❌ Failed to install npm"
        exit 1
    fi
fi

echo "✅ npm $(npm --version) detected"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if npm install; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if players.json exists, if not create default
if [ ! -f "players.json" ]; then
    echo ""
    echo "📄 Creating default players.json file..."
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
else
    echo "✅ players.json already exists"
fi

# Create backups directory
if [ ! -d "backups" ]; then
    mkdir backups
    echo "✅ Backups directory created"
fi

# Make the script executable
chmod +x setup.sh

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 Starting the application automatically..."
echo "The server will start at http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

# Auto-start the application
if npm start; then
    echo "✅ Application started successfully!"
else
    echo "❌ Failed to start application"
    echo "You can start it manually with: npm start"
    exit 1
fi