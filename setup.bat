@echo off
setlocal enabledelayedexpansion

echo ⚽︎ Foosball Tournament Manager - Auto Setup Script (Windows)
echo ===========================================================

REM Call the main function to start the script
call :main
goto :eof

REM Function to download and install Node.js
:install_nodejs
echo 📦 Downloading and installing Node.js...

REM Detect system architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set ARCH=x64
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    set ARCH=x86
) else (
    set ARCH=x64
)

REM Set Node.js download URL (LTS version)
set NODE_VERSION=18.19.0
set NODE_URL=https://nodejs.org/dist/v%NODE_VERSION%/node-v%NODE_VERSION%-win-%ARCH%.msi
set NODE_FILE=node-installer.msi

echo 🌐 Downloading Node.js v%NODE_VERSION% for %ARCH%...
echo URL: %NODE_URL%

REM Download Node.js installer using PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%NODE_URL%' -OutFile '%NODE_FILE%'}"

if not exist "%NODE_FILE%" (
    echo ❌ Failed to download Node.js installer
    echo Please download and install Node.js manually from https://nodejs.org/
    pause
    exit /b 1
)

echo 🚀 Installing Node.js... (This may take a few minutes)
echo Please follow the installation wizard prompts.

REM Install Node.js silently
msiexec /i "%NODE_FILE%" /quiet /norestart

REM Wait for installation to complete
timeout /t 10 /nobreak >nul

REM Clean up installer file
if exist "%NODE_FILE%" del "%NODE_FILE%"

REM Refresh environment variables
call refreshenv.cmd >nul 2>&1

echo ✅ Node.js installation completed!
goto :eof

REM Main script starts here
:main

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo 🚀 Attempting to install Node.js automatically...
    
    set /p "install_choice=Do you want to install Node.js automatically? (y/N): "
    if /i "!install_choice!"=="y" (
        call :install_nodejs
        
        REM Verify installation
        node --version >nul 2>&1
        if !errorlevel! neq 0 (
            echo ❌ Failed to install Node.js automatically
            echo Please install Node.js manually from https://nodejs.org/
            pause
            exit /b 1
        )
        echo ✅ Node.js installed successfully!
    ) else (
        echo ❌ Node.js installation cancelled
        echo Please install Node.js from https://nodejs.org/ and run this script again
        pause
        exit /b 1
    )
)

echo ✅ Node.js detected
node --version

REM Check if npm is available
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not available!
    echo 🚀 npm should be installed with Node.js. Please restart your command prompt.
    pause
    exit /b 1
)

echo ✅ npm detected
npm --version

REM Install dependencies
echo.
echo 📦 Installing dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Check if players.json exists, if not create default
if not exist "players.json" (
    echo.
    echo 📄 Creating default players.json file...
    (
        echo {
        echo     "championships": {
        echo         "ghayem": 6,
        echo         "elini": 2,
        echo         "dinparvar": 1,
        echo         "alivand": 1,
        echo         "hoseinizade": 3,
        echo         "hajali": 2,
        echo         "dariushi": 3
        echo     },
        echo     "players": [
        echo         {
        echo             "name": "ghayem",
        echo             "seed": 1
        echo         },
        echo         {
        echo             "name": "elini",
        echo             "seed": 3
        echo         },
        echo         {
        echo             "name": "dinparvar",
        echo             "seed": 3
        echo         },
        echo         {
        echo             "name": "alivand",
        echo             "seed": 1
        echo         },
        echo         {
        echo             "name": "hoseinizade",
        echo             "seed": 3
        echo         },
        echo         {
        echo             "name": "hajali",
        echo             "seed": 3
        echo         },
        echo         {
        echo             "name": "dariushi",
        echo             "seed": 1
        echo         }
        echo     ]
        echo }
    ) > players.json
    echo ✅ Default players.json created
) else (
    echo ✅ players.json already exists
)

REM Create backups directory
if not exist "backups" (
    mkdir backups
    echo ✅ Backups directory created
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 🚀 Starting the application automatically...
echo The server will start at http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

REM Auto-start the application
npm start
if %errorlevel% equ 0 (
    echo ✅ Application started successfully!
) else (
    echo ❌ Failed to start application
    echo You can start it manually with: npm start
    pause
    exit /b 1
)
