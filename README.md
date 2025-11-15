# ⚽︎ Foosball Tournament Manager

A comprehensive tournament management system with both web and desktop interfaces, featuring automatic dependency installation and one-click deployment.

## 🚀 One-Click Installation & Launch

### Windows Users (Easiest):

**Just double-click one of these files:**

- **`RUN.bat`** - One-click launcher (checks dependencies and auto-starts)
- **`setup.bat`** - Full auto-installer with Node.js download

### Mac/Linux Users (Easiest):

**Just run one of these in terminal:**

```bash
./RUN.sh        # One-click launcher
./setup.sh      # Full auto-installer with Node.js download
python3 install.py  # Universal installer (works on all platforms)
```

## ✨ What Happens Automatically

### The scripts automatically:

1. **Check for Node.js** - Install if missing or outdated
2. **Download dependencies** - Install express, cors, etc.
3. **Create data files** - Set up players.json with default data
4. **Start the server** - Launch at http://localhost:3000
5. **Open ready to use** - No manual steps required!

## 📋 Available Installation Methods

| Method           | Platform  | Description                     | Auto-Start |
| ---------------- | --------- | ------------------------------- | ---------- |
| **`RUN.bat`**    | Windows   | 🌟 **One-click launcher**       | ✅ Yes     |
| **`RUN.sh`**     | Mac/Linux | 🌟 **One-click launcher**       | ✅ Yes     |
| **`install.py`** | All       | Universal Python installer      | ✅ Yes     |
| **`setup.ps1`**  | Windows   | PowerShell with admin elevation | ✅ Yes     |
| **`setup.sh`**   | Mac/Linux | Bash with package managers      | ✅ Yes     |
| **`setup.bat`**  | Windows   | Batch with Node.js download     | ✅ Yes     |

## 🎯 For Different Use Cases

### First-Time Users:

- **Windows:** Double-click `RUN.bat`
- **Mac/Linux:** Run `./RUN.sh`

### Clean Installation:

- **Any Platform:** Run `python3 install.py`
- **Windows:** Run `setup.ps1` or `setup.bat`
- **Mac/Linux:** Run `./setup.sh`

### Server Deployment:

```bash
docker-compose up  # Containerized deployment
```

## 🌐 Network Access

After starting, the application is available at:

- **Local access:** http://localhost:3000
- **Network access:** http://your-ip-address:3000

To find your IP address:

```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

## 📁 Project Structure

```
foosball/
├── 🚀 RUN.bat/.sh           # One-click launchers
├── ⚙️ install.py            # Universal installer
├── ⚙️ setup.sh/.bat/.ps1    # Platform-specific installers
├── 📄 players.json          # Championship data (auto-created)
├── 🖥️ server.js             # Web server
├── 🌐 index.html            # Web interface
├── 📱 script.js             # Web app logic
├── 🎨 styles.css            # Styling (fixed CSS issues)
├── 🐍 foosball.py           # Python desktop app
├── 🐳 Dockerfile            # Container deployment
├── 🐳 docker-compose.yml    # Container orchestration
└── 📚 Documentation/        # Comprehensive guides
```

## 🔧 Features

### Web Application:

- **Tournament management** with multiple team formation modes
- **Real-time scoring** with intuitive +/- buttons
- **Championship tracking** with persistent storage
- **Responsive design** for mobile and desktop
- **Data synchronization** between web and desktop apps

### Desktop Application (Python):

- **Native GUI** using tkinter
- **Same functionality** as web version
- **Shared data storage** with web application
- **Cross-platform** compatibility

### Data Management:

- **Persistent storage** in `players.json`
- **Automatic backups** to `backups/` directory
- **Cross-application sync** between web and desktop
- **Import/export** capabilities

## 🛠️ Technical Details

### Dependencies Auto-Installed:

- **Node.js** (Latest LTS 18.x)
- **Express.js** (Web server framework)
- **CORS** (Cross-origin resource sharing)
- **npm packages** (All project dependencies)

### Supported Platforms:

- **Windows** (7, 8, 10, 11) - x86 and x64
- **macOS** (Intel and Apple Silicon)
- **Linux** (Ubuntu, Debian, CentOS, RHEL, Fedora, Arch)

### Package Managers Supported:

- **Windows:** MSI installer, Chocolatey
- **macOS:** Homebrew (auto-installed if missing)
- **Linux:** apt-get, yum, dnf, pacman

## 🚨 Troubleshooting

### Quick Fixes:

| Problem               | Solution                           |
| --------------------- | ---------------------------------- |
| Port 3000 in use      | Run: `PORT=8080 npm start`         |
| Permission denied     | Run as administrator/sudo          |
| Script won't run      | Make executable: `chmod +x RUN.sh` |
| Node.js install fails | Download manually from nodejs.org  |

### Getting Help:

- **Quick Start:** See `QUICK_START.md`
- **Deployment:** See `DEPLOYMENT_GUIDE.md`
- **Installation Methods:** See `INSTALLATION_METHODS.md`

## 🎉 Quick Start Summary

1. **Copy** the project folder to any computer
2. **Double-click** `RUN.bat` (Windows) or run `./RUN.sh` (Mac/Linux)
3. **Wait** for automatic installation and startup
4. **Open** http://localhost:3000 in your browser
5. **Start playing!** ⚽︎

That's it! The scripts handle everything automatically - no technical knowledge required!

---

**Made with ❤️ for foosball enthusiasts everywhere!**
