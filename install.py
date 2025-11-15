#!/usr/bin/env python3
"""
Foosball Tournament Manager - Universal Auto Installer
This Python script automatically installs Node.js and sets up the application on any platform
"""

import os
import sys
import platform
import subprocess
import urllib.request
import json
import shutil
from pathlib import Path

def print_colored(text, color='white'):
    """Print colored text to console"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def run_command(command, shell=True, check=True):
    """Run a system command and return the result"""
    try:
        result = subprocess.run(command, shell=shell, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else ""
    except Exception as e:
        return False, "", str(e)

def check_node_installed():
    """Check if Node.js is installed and get version"""
    success, stdout, _ = run_command("node --version", check=False)
    if success and stdout:
        version = stdout.replace('v', '')
        major_version = int(version.split('.')[0])
        return True, version, major_version >= 14
    return False, None, False

def check_npm_installed():
    """Check if npm is installed"""
    success, stdout, _ = run_command("npm --version", check=False)
    return success, stdout if success else None

def install_node_linux():
    """Install Node.js on Linux systems"""
    print_colored("🐧 Installing Node.js on Linux...", 'yellow')
    
    # Try different package managers
    if shutil.which('apt-get'):
        print_colored("📦 Using apt-get (Ubuntu/Debian)", 'blue')
        commands = [
            "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -",
            "sudo apt-get install -y nodejs"
        ]
    elif shutil.which('yum'):
        print_colored("📦 Using yum (CentOS/RHEL)", 'blue')
        commands = [
            "curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -",
            "sudo yum install -y nodejs"
        ]
    elif shutil.which('dnf'):
        print_colored("📦 Using dnf (Fedora)", 'blue')
        commands = [
            "curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -",
            "sudo dnf install -y nodejs"
        ]
    elif shutil.which('pacman'):
        print_colored("📦 Using pacman (Arch Linux)", 'blue')
        commands = ["sudo pacman -S nodejs npm --noconfirm"]
    else:
        print_colored("❌ Unsupported Linux distribution", 'red')
        return False
    
    for command in commands:
        print_colored(f"Running: {command}", 'blue')
        success, stdout, stderr = run_command(command)
        if not success:
            print_colored(f"❌ Command failed: {stderr}", 'red')
            return False
    
    return True

def install_node_macos():
    """Install Node.js on macOS"""
    print_colored("🍎 Installing Node.js on macOS...", 'yellow')
    
    if shutil.which('brew'):
        print_colored("📦 Using Homebrew", 'blue')
        success, _, stderr = run_command("brew install node")
        if not success:
            print_colored(f"❌ Homebrew installation failed: {stderr}", 'red')
            return False
    else:
        print_colored("📦 Installing Homebrew first...", 'blue')
        install_brew_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        success, _, stderr = run_command(install_brew_cmd)
        if not success:
            print_colored(f"❌ Homebrew installation failed: {stderr}", 'red')
            return False
        
        print_colored("📦 Installing Node.js with Homebrew...", 'blue')
        success, _, stderr = run_command("brew install node")
        if not success:
            print_colored(f"❌ Node.js installation failed: {stderr}", 'red')
            return False
    
    return True

def install_node_windows():
    """Install Node.js on Windows"""
    print_colored("🪟 Installing Node.js on Windows...", 'yellow')
    
    # Check if running on Windows
    if platform.system() != 'Windows':
        print_colored("❌ This function should only run on Windows", 'red')
        return False
    
    try:
        # Detect architecture
        arch = "x64" if platform.machine().endswith('64') else "x86"
        node_version = "18.19.0"
        
        # Download URL
        url = f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-win-{arch}.msi"
        installer_path = "node-installer.msi"
        
        print_colored(f"🌐 Downloading Node.js v{node_version} for {arch}...", 'blue')
        urllib.request.urlretrieve(url, installer_path)
        
        print_colored("🚀 Installing Node.js...", 'blue')
        success, _, stderr = run_command(f'msiexec /i "{installer_path}" /quiet /norestart')
        
        # Clean up
        if os.path.exists(installer_path):
            os.remove(installer_path)
        
        if not success:
            print_colored(f"❌ Installation failed: {stderr}", 'red')
            return False
        
        print_colored("✅ Node.js installed successfully!", 'green')
        return True
        
    except Exception as e:
        print_colored(f"❌ Error during installation: {str(e)}", 'red')
        return False

def install_nodejs():
    """Install Node.js based on the current platform"""
    system = platform.system().lower()
    
    if system == 'linux':
        return install_node_linux()
    elif system == 'darwin':
        return install_node_macos()
    elif system == 'windows':
        return install_node_windows()
    else:
        print_colored(f"❌ Unsupported operating system: {system}", 'red')
        return False

def create_default_players_json():
    """Create default players.json file"""
    default_data = {
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
            {"name": "ghayem", "seed": 1},
            {"name": "elini", "seed": 3},
            {"name": "dinparvar", "seed": 3},
            {"name": "alivand", "seed": 1},
            {"name": "hoseinizade", "seed": 3},
            {"name": "hajali", "seed": 3},
            {"name": "dariushi", "seed": 1}
        ]
    }
    
    with open('players.json', 'w', encoding='utf-8') as f:
        json.dump(default_data, f, indent=4, ensure_ascii=False)

def main():
    """Main installation function"""
    print_colored("⚽︎ Foosball Tournament Manager - Universal Auto Installer", 'cyan')
    print_colored("=" * 60, 'cyan')
    print_colored(f"🖥️  Platform: {platform.system()} {platform.release()}", 'blue')
    print_colored(f"🏗️  Architecture: {platform.machine()}", 'blue')
    print()
    
    # Check if Node.js is installed
    node_installed, node_version, version_ok = check_node_installed()
    
    if node_installed and version_ok:
        print_colored(f"✅ Node.js v{node_version} is already installed", 'green')
    else:
        if node_installed:
            print_colored(f"⚠️  Node.js v{node_version} is installed but version 14+ is recommended", 'yellow')
        else:
            print_colored("❌ Node.js is not installed", 'red')
        
        print_colored("🚀 Attempting to install Node.js automatically...", 'yellow')
        
        # Ask for permission
        try:
            choice = input("Do you want to install/update Node.js automatically? (y/N): ").strip().lower()
            if choice in ['y', 'yes']:
                if install_nodejs():
                    print_colored("✅ Node.js installation completed!", 'green')
                    
                    # Verify installation
                    node_installed, node_version, version_ok = check_node_installed()
                    if node_installed and version_ok:
                        print_colored(f"✅ Node.js v{node_version} verified!", 'green')
                    else:
                        print_colored("❌ Node.js installation verification failed", 'red')
                        print_colored("Please restart your terminal and try again", 'yellow')
                        return False
                else:
                    print_colored("❌ Failed to install Node.js automatically", 'red')
                    print_colored("Please install Node.js manually from https://nodejs.org/", 'yellow')
                    return False
            else:
                print_colored("❌ Node.js installation cancelled", 'red')
                print_colored("Please install Node.js from https://nodejs.org/ and run this script again", 'yellow')
                return False
        except KeyboardInterrupt:
            print_colored("\n❌ Installation cancelled by user", 'red')
            return False
    
    # Check npm
    npm_installed, npm_version = check_npm_installed()
    if npm_installed:
        print_colored(f"✅ npm v{npm_version} detected", 'green')
    else:
        print_colored("❌ npm is not available!", 'red')
        print_colored("npm should be installed with Node.js. Please restart your terminal.", 'yellow')
        return False
    
    # Install project dependencies
    print()
    print_colored("📦 Installing project dependencies...", 'yellow')
    success, stdout, stderr = run_command("npm install")
    if success:
        print_colored("✅ Dependencies installed successfully", 'green')
    else:
        print_colored(f"❌ Failed to install dependencies: {stderr}", 'red')
        return False
    
    # Create players.json if it doesn't exist
    if not os.path.exists('players.json'):
        print()
        print_colored("📄 Creating default players.json file...", 'yellow')
        create_default_players_json()
        print_colored("✅ Default players.json created", 'green')
    else:
        print_colored("✅ players.json already exists", 'green')
    
    # Create backups directory
    if not os.path.exists('backups'):
        os.makedirs('backups')
        print_colored("✅ Backups directory created", 'green')
    
    print()
    print_colored("🎉 Setup completed successfully!", 'green')
    print()
    
    # Auto-start the application
    print_colored("🚀 Starting the application automatically...", 'yellow')
    print_colored("The server will start at http://localhost:3000", 'cyan')
    print_colored("Press Ctrl+C to stop the server", 'yellow')
    print()
    
    try:
        # Start the application
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print_colored("\n✅ Application stopped by user", 'green')
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Failed to start application: {e}", 'red')
        print_colored("You can start it manually with: npm start", 'yellow')
        return False
    except Exception as e:
        print_colored(f"❌ Unexpected error starting application: {e}", 'red')
        print_colored("You can start it manually with: npm start", 'yellow')
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_colored("\n❌ Installation cancelled by user", 'red')
        sys.exit(1)
    except Exception as e:
        print_colored(f"❌ An unexpected error occurred: {str(e)}", 'red')
        sys.exit(1)