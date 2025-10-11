# 🏓 Foosball Tournament Manager - Quick Start Guide

## For New Users (Easiest Method - Auto Install Everything!)

### Option 1: Universal Python Installer (Recommended)
**Works on Windows, Mac, and Linux - Automatically installs Node.js if needed!**

1. **Download/copy** the entire project folder to your computer
2. **Run the universal installer**:
   ```bash
   python3 install.py
   # or on Windows:
   python install.py
   ```
3. **Start the app**: `npm start`
4. **Open** http://localhost:3000 in your browser

### Option 2: Platform-Specific Auto Installers

#### Windows Users:
**Choose one of these methods:**

**Method A: PowerShell (Recommended)**
1. **Right-click** on `setup.ps1` → "Run with PowerShell"
2. **Or run in PowerShell**: `.\setup.ps1`
3. **Start the app**: `npm start`

**Method B: Batch File**
1. **Double-click** `setup.bat`
2. **Start the app**: `npm start`

#### Mac/Linux Users:
1. **Download/copy** the entire project folder to your computer
2. **Open terminal** in the project folder
3. **Run** `./setup.sh` (automatically installs Node.js if needed)
4. **Start the app**: `npm start`
5. **Open** http://localhost:3000 in your browser

### Option 3: Manual Installation (If auto-install fails)
1. **Install Node.js** manually from https://nodejs.org/
2. **Run** `npm install` in the project folder
3. **Start the app**: `npm start`

## Moving to Another Computer

### Method 1: Simple Copy (Recommended)
1. **Copy the entire folder** to the new computer
2. **Run setup script** (`setup.bat` on Windows, `./setup.sh` on Mac/Linux)
3. **Start the app** with `npm start`

### Method 2: Using Git (For Developers)
```bash
git clone <your-repository-url>
cd foosball
npm install
npm start
```

### Method 3: Docker (For Servers)
```bash
# Simple Docker run
docker build -t foosball-tournament .
docker run -p 3000:3000 foosball-tournament

# Or with Docker Compose
docker-compose up
```

## Network Access

### Allow Other Computers to Access:
1. **Find your IP address**:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `ip addr`
2. **Others can access** at: `http://your-ip-address:3000`

### Change Port (if 3000 is busy):
```bash
# Windows
set PORT=8080 && npm start

# Mac/Linux
PORT=8080 npm start
```

## File Structure
```
foosball/
├── 📄 players.json          # Championship data (IMPORTANT!)
├── 🖥️ server.js             # Web server
├── 🌐 index.html            # Web interface
├── 📱 script.js             # Web app logic
├── 🎨 styles.css            # Styling
├── 🐍 foosball.py           # Desktop app (Python)
├── ⚙️ package.json          # Dependencies
├── 🚀 setup.sh/.bat         # Setup scripts
└── 📚 Documentation files
```

## Important Notes

- **`players.json`** contains all championship data - always backup this file!
- **Both web and desktop apps** share the same data
- **Port 3000** must be available (or change it)
- **Node.js required** for web version, Python for desktop version

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Port 3000 in use" | Change port: `PORT=8080 npm start` |
| "Node.js not found" | Install from https://nodejs.org/ |
| "Permission denied" | Run `chmod +x setup.sh` on Mac/Linux |
| "Can't access from other PCs" | Check firewall, use correct IP address |

## Need Help?

- 📖 **Detailed guide**: See `DEPLOYMENT_GUIDE.md`
- 🔧 **Technical details**: See `README_UPDATED.md`
- 🐳 **Docker setup**: Use `docker-compose up`

## Auto-Installation Features

### ✨ What Gets Installed Automatically:
- **Node.js** (Latest LTS version 18.x) - if not present or outdated
- **npm** (comes with Node.js)
- **Project dependencies** (express, cors, etc.)
- **Default players.json** - if not present
- **Backups directory** - for data safety

### 🔧 Supported Platforms:
- **Windows** (7, 8, 10, 11) - x86 and x64
- **macOS** (Intel and Apple Silicon)
- **Linux** (Ubuntu, Debian, CentOS, RHEL, Fedora, Arch)

### 📋 Installation Scripts Available:
| Script | Platform | Features |
|--------|----------|----------|
| `install.py` | Universal (All) | 🌟 **Best choice** - Works everywhere |
| `setup.ps1` | Windows | PowerShell with admin privileges |
| `setup.bat` | Windows | Batch file with auto-download |
| `setup.sh` | Mac/Linux | Bash script with package managers |

---

**Quick Commands:**
```bash
# Universal installer (recommended)
python3 install.py

# Platform-specific installers
./setup.sh          # Mac/Linux
.\setup.ps1          # Windows PowerShell
setup.bat            # Windows Batch

# Manual installation
# Install and start
npm install && npm start

# Start on different port
PORT=8080 npm start

# Docker version
docker-compose up

# Backup data
cp players.json players_backup.json