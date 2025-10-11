# 🚀 Foosball Tournament Manager - Installation Methods

This document provides a comprehensive overview of all available installation methods for the Foosball Tournament Manager application.

## 🌟 Recommended Method: Universal Python Installer

**Best for: All users, all platforms**

```bash
python3 install.py
```

### Features:
- ✅ **Automatic Node.js detection and installation**
- ✅ **Cross-platform support** (Windows, Mac, Linux)
- ✅ **Intelligent package manager detection**
- ✅ **Administrator privilege handling**
- ✅ **Comprehensive error handling**
- ✅ **Progress feedback and colored output**

---

## 📋 All Available Installation Methods

### 1. Universal Python Installer (`install.py`)
**Platform:** Windows, Mac, Linux  
**Requirements:** Python 3.6+  
**Features:** Full automation, Node.js auto-install

```bash
# Run the universal installer
python3 install.py
# or on Windows:
python install.py
```

### 2. PowerShell Script (`setup.ps1`)
**Platform:** Windows  
**Requirements:** PowerShell 5.0+  
**Features:** Admin privilege elevation, MSI installer download

```powershell
# Right-click and "Run with PowerShell" or:
.\setup.ps1
```

### 3. Bash Script (`setup.sh`)
**Platform:** Mac, Linux  
**Requirements:** Bash shell  
**Features:** Package manager detection, Homebrew auto-install

```bash
# Make executable and run
chmod +x setup.sh
./setup.sh
```

### 4. Windows Batch File (`setup.bat`)
**Platform:** Windows  
**Requirements:** Command Prompt  
**Features:** Basic Node.js download and install

```cmd
# Double-click or run in Command Prompt
setup.bat
```

### 5. Docker Container
**Platform:** Any with Docker  
**Requirements:** Docker installed  
**Features:** Containerized deployment, no local dependencies

```bash
# Build and run with Docker
docker build -t foosball-tournament .
docker run -p 3000:3000 -v $(pwd)/players.json:/app/players.json foosball-tournament

# Or use Docker Compose
docker-compose up
```

### 6. Manual Installation
**Platform:** Any  
**Requirements:** Node.js pre-installed  
**Features:** Full control, no automation

```bash
# Install Node.js from https://nodejs.org/ first, then:
npm install
npm start
```

---

## 🔧 Platform-Specific Recommendations

### Windows Users
1. **Best:** `install.py` (Universal Python installer)
2. **Alternative:** `setup.ps1` (PowerShell script)
3. **Simple:** `setup.bat` (Batch file)

### Mac Users
1. **Best:** `install.py` (Universal Python installer)
2. **Alternative:** `setup.sh` (Bash script with Homebrew)

### Linux Users
1. **Best:** `install.py` (Universal Python installer)
2. **Alternative:** `setup.sh` (Bash script with package managers)

### Server Deployment
1. **Best:** Docker (`docker-compose up`)
2. **Alternative:** Manual installation with PM2

---

## 🎯 What Each Method Installs

### Automatic Installers Install:
- **Node.js** (Latest LTS version 18.x)
- **npm** (Node Package Manager)
- **Project dependencies** (express, cors, etc.)
- **Default players.json** (if not present)
- **Backups directory**

### Manual Method Requires:
- Pre-installed Node.js and npm
- Manual dependency installation (`npm install`)

---

## 🚨 Troubleshooting Installation Issues

### Common Problems and Solutions:

| Problem | Solution |
|---------|----------|
| **Python not found** | Install Python from https://python.org/ |
| **Permission denied (Linux/Mac)** | Run `chmod +x install.py setup.sh` |
| **PowerShell execution policy** | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| **Node.js download fails** | Check internet connection, try manual install |
| **Port 3000 in use** | Change port: `PORT=8080 npm start` |
| **npm install fails** | Delete `node_modules` and `package-lock.json`, retry |

### Platform-Specific Issues:

#### Windows
- **MSI installer blocked:** Right-click installer → Properties → Unblock
- **Antivirus interference:** Temporarily disable during installation
- **Path not updated:** Restart Command Prompt/PowerShell after Node.js install

#### Mac
- **Homebrew permission issues:** Run `sudo chown -R $(whoami) /usr/local/Homebrew`
- **Xcode tools missing:** Run `xcode-select --install`

#### Linux
- **Package manager not found:** Install curl first: `sudo apt install curl`
- **Repository key issues:** Update package lists: `sudo apt update`

---

## 📊 Installation Method Comparison

| Method | Ease of Use | Automation Level | Platform Support | Prerequisites |
|--------|-------------|------------------|------------------|---------------|
| `install.py` | ⭐⭐⭐⭐⭐ | Full | All | Python 3.6+ |
| `setup.ps1` | ⭐⭐⭐⭐ | High | Windows | PowerShell 5.0+ |
| `setup.sh` | ⭐⭐⭐⭐ | High | Mac/Linux | Bash |
| `setup.bat` | ⭐⭐⭐ | Medium | Windows | Command Prompt |
| Docker | ⭐⭐⭐ | Medium | All | Docker |
| Manual | ⭐⭐ | None | All | Node.js |

---

## 🎉 After Installation

Once installation is complete, regardless of method used:

1. **Start the application:**
   ```bash
   npm start
   ```

2. **Open your browser:**
   ```
   http://localhost:3000
   ```

3. **For network access:**
   - Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
   - Others access: `http://your-ip:3000`

4. **Championship data:**
   - Stored in `players.json`
   - Automatically backed up to `backups/` folder
   - Shared between web and desktop applications

---

## 📚 Additional Resources

- **Quick Start Guide:** `QUICK_START.md`
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Technical Documentation:** `README_UPDATED.md`
- **Docker Configuration:** `docker-compose.yml`

Choose the installation method that best fits your technical comfort level and platform requirements!