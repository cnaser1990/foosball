@echo off
setlocal enabledelayedexpansion

echo 🏓 Foosball Tournament Manager - One-Click Launcher
echo ================================================

REM Function to check if port is in use
:check_port
netstat -an | find "LISTENING" | find ":3000" >nul 2>&1
goto :eof

REM Function to kill process on port 3000
:kill_port_process
echo 🔍 Finding process using port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":3000" ^| find "LISTENING"') do (
    set pid=%%a
    if defined pid (
        echo ⚡ Killing process !pid! on port 3000...
        taskkill /PID !pid! /F >nul 2>&1
        timeout /t 2 /nobreak >nul
        goto :eof
    )
)
goto :eof

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Node.js not found. Running auto-installer...
    call setup.bat
    goto :end
)

REM Check if dependencies are installed
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if port 3000 is in use
call :check_port
if %errorlevel% equ 0 (
    echo ⚠️  Port 3000 is already in use!
    echo Options:
    echo 1) Kill the existing process and use port 3000
    echo 2) Use a different port (3001)
    echo 3) Exit
    echo.
    
    set /p "choice=Choose option (1/2/3): "
    
    if "!choice!"=="1" (
        call :kill_port_process
        echo ✅ Port 3000 should now be available
        set PORT=3000
    ) else if "!choice!"=="2" (
        echo ✅ Using port 3001
        set PORT=3001
    ) else if "!choice!"=="3" (
        echo ❌ Exiting...
        goto :end
    ) else (
        echo ✅ Using port 3001 (default choice)
        set PORT=3001
    )
) else (
    set PORT=3000
)

echo 🚀 Starting Foosball Tournament Manager...
echo Server will be available at: http://localhost:!PORT!
echo Press Ctrl+C to stop the server
echo.

REM Start the application with the chosen port
set PORT=!PORT!
npm start

:end
pause