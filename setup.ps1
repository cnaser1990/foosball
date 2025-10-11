# Foosball Tournament Manager - PowerShell Auto Setup Script
# This script automatically downloads and installs Node.js if needed

Write-Host "🏓 Foosball Tournament Manager - PowerShell Auto Setup Script" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan

# Function to install Node.js
function Install-NodeJS {
    Write-Host "📦 Installing Node.js..." -ForegroundColor Yellow
    
    # Detect system architecture
    $arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
    
    # Set Node.js version and download URL
    $nodeVersion = "18.19.0"
    $nodeUrl = "https://nodejs.org/dist/v$nodeVersion/node-v$nodeVersion-win-$arch.msi"
    $nodeFile = "node-installer.msi"
    
    Write-Host "🌐 Downloading Node.js v$nodeVersion for $arch..." -ForegroundColor Green
    
    try {
        # Enable TLS 1.2 for secure download
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        
        # Download Node.js installer
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeFile -UseBasicParsing
        
        if (Test-Path $nodeFile) {
            Write-Host "✅ Download completed successfully!" -ForegroundColor Green
            
            Write-Host "🚀 Installing Node.js... (This may take a few minutes)" -ForegroundColor Yellow
            Write-Host "Please wait for the installation to complete." -ForegroundColor Yellow
            
            # Install Node.js silently
            $process = Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$nodeFile`" /quiet /norestart" -Wait -PassThru
            
            if ($process.ExitCode -eq 0) {
                Write-Host "✅ Node.js installed successfully!" -ForegroundColor Green
                
                # Refresh environment variables
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                
                # Clean up installer file
                Remove-Item $nodeFile -Force -ErrorAction SilentlyContinue
                
                return $true
            } else {
                Write-Host "❌ Node.js installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
                return $false
            }
        } else {
            Write-Host "❌ Failed to download Node.js installer" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error during Node.js installation: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check if running as Administrator for installation
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Main script execution
try {
    # Check if Node.js is installed
    $nodeInstalled = $false
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Host "✅ Node.js $nodeVersion detected" -ForegroundColor Green
            $nodeInstalled = $true
            
            # Check version (extract major version number)
            $majorVersion = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
            if ($majorVersion -lt 14) {
                Write-Host "⚠️  Node.js version $majorVersion detected. Version 14+ recommended." -ForegroundColor Yellow
                Write-Host "🚀 Attempting to update Node.js..." -ForegroundColor Yellow
                $nodeInstalled = $false
            }
        }
    }
    catch {
        # Node.js not found
    }
    
    if (-not $nodeInstalled) {
        Write-Host "❌ Node.js is not installed or needs updating!" -ForegroundColor Red
        
        # Check if running as administrator
        if (-not (Test-Administrator)) {
            Write-Host "⚠️  Administrator privileges required for installation." -ForegroundColor Yellow
            Write-Host "🚀 Attempting to restart as administrator..." -ForegroundColor Yellow
            
            # Restart as administrator
            $scriptPath = $MyInvocation.MyCommand.Path
            Start-Process PowerShell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$scriptPath`""
            exit
        }
        
        $installChoice = Read-Host "Do you want to install/update Node.js automatically? (y/N)"
        if ($installChoice -match '^[Yy]$') {
            $installSuccess = Install-NodeJS
            
            if (-not $installSuccess) {
                Write-Host "❌ Failed to install Node.js automatically" -ForegroundColor Red
                Write-Host "Please install Node.js manually from https://nodejs.org/" -ForegroundColor Yellow
                Read-Host "Press Enter to exit"
                exit 1
            }
            
            # Verify installation
            try {
                $nodeVersion = node --version 2>$null
                if (-not $nodeVersion) {
                    throw "Node.js not found after installation"
                }
                Write-Host "✅ Node.js $nodeVersion verified!" -ForegroundColor Green
            }
            catch {
                Write-Host "❌ Node.js installation verification failed" -ForegroundColor Red
                Write-Host "Please restart your PowerShell/Command Prompt and try again" -ForegroundColor Yellow
                Read-Host "Press Enter to exit"
                exit 1
            }
        } else {
            Write-Host "❌ Node.js installation cancelled" -ForegroundColor Red
            Write-Host "Please install Node.js from https://nodejs.org/ and run this script again" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    # Check if npm is available
    try {
        $npmVersion = npm --version 2>$null
        if ($npmVersion) {
            Write-Host "✅ npm $npmVersion detected" -ForegroundColor Green
        } else {
            throw "npm not found"
        }
    }
    catch {
        Write-Host "❌ npm is not available!" -ForegroundColor Red
        Write-Host "🚀 npm should be installed with Node.js. Please restart your PowerShell." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Install project dependencies
    Write-Host "" 
    Write-Host "📦 Installing project dependencies..." -ForegroundColor Yellow
    $npmInstall = npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Check if players.json exists, if not create default
    if (-not (Test-Path "players.json")) {
        Write-Host ""
        Write-Host "📄 Creating default players.json file..." -ForegroundColor Yellow
        
        $defaultData = @{
            championships = @{
                ghayem = 6
                elini = 2
                dinparvar = 1
                alivand = 1
                hoseinizade = 3
                hajali = 2
                dariushi = 3
            }
            players = @(
                @{ name = "ghayem"; seed = 1 }
                @{ name = "elini"; seed = 3 }
                @{ name = "dinparvar"; seed = 3 }
                @{ name = "alivand"; seed = 1 }
                @{ name = "hoseinizade"; seed = 3 }
                @{ name = "hajali"; seed = 3 }
                @{ name = "dariushi"; seed = 1 }
            )
        }
        
        $defaultData | ConvertTo-Json -Depth 10 | Out-File -FilePath "players.json" -Encoding UTF8
        Write-Host "✅ Default players.json created" -ForegroundColor Green
    } else {
        Write-Host "✅ players.json already exists" -ForegroundColor Green
    }
    
    # Create backups directory
    if (-not (Test-Path "backups")) {
        New-Item -ItemType Directory -Path "backups" | Out-Null
        Write-Host "✅ Backups directory created" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Starting the application automatically..." -ForegroundColor Yellow
    Write-Host "The server will start at http://localhost:3000" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    
    # Auto-start the application
    try {
        npm start
        Write-Host "✅ Application started successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to start application: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "You can start it manually with: npm start" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}
catch {
    Write-Host "❌ An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}