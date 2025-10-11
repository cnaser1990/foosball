# Foosball Tournament Manager - Deployment Guide

This guide explains how to move and deploy the Foosball Tournament Manager application on different computers and servers.

## Prerequisites

Before deploying, ensure the target system has:
- **Node.js** (version 14 or higher) - [Download from nodejs.org](https://nodejs.org/)
- **Python** (version 3.6 or higher) - for the desktop application
- **Git** (optional, for version control)

## Deployment Methods

### Method 1: Simple File Transfer (Recommended for Local Deployment)

1. **Copy the entire project folder** to the target computer:
   ```
   foosball/
   ├── server.js
   ├── package.json
   ├── players.json
   ├── script.js
   ├── index.html
   ├── styles.css
   ├── foosball.py
   └── README files
   ```

2. **On the target computer**, open terminal/command prompt in the project folder

3. **Install dependencies**:
   ```bash
   npm install
   ```

4. **Start the application**:
   ```bash
   npm start
   ```

5. **Access the application** at `http://localhost:3000`

### Method 2: Git Repository (Recommended for Team/Server Deployment)

1. **Initialize Git repository** (on original computer):
   ```bash
   git init
   git add .
   git commit -m "Initial foosball tournament app"
   ```

2. **Push to remote repository** (GitHub, GitLab, etc.):
   ```bash
   git remote add origin <your-repository-url>
   git push -u origin main
   ```

3. **On target computer/server**, clone the repository:
   ```bash
   git clone <your-repository-url>
   cd foosball
   npm install
   npm start
   ```

### Method 3: Server Deployment (Production)

#### Option A: Simple VPS/Cloud Server

1. **Upload files** to your server (via SCP, FTP, or Git)

2. **Install Node.js** on the server:
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # CentOS/RHEL
   curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
   sudo yum install -y nodejs
   ```

3. **Install dependencies and start**:
   ```bash
   cd foosball
   npm install
   npm start
   ```

4. **Access via server IP**: `http://your-server-ip:3000`

#### Option B: Production Deployment with PM2

1. **Install PM2** (Process Manager):
   ```bash
   npm install -g pm2
   ```

2. **Create PM2 configuration** (`ecosystem.config.js`):
   ```javascript
   module.exports = {
     apps: [{
       name: 'foosball-tournament',
       script: 'server.js',
       instances: 1,
       autorestart: true,
       watch: false,
       max_memory_restart: '1G',
       env: {
         NODE_ENV: 'production',
         PORT: 3000
       }
     }]
   };
   ```

3. **Start with PM2**:
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

#### Option C: Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM node:18-alpine
   
   WORKDIR /app
   
   COPY package*.json ./
   RUN npm install --only=production
   
   COPY . .
   
   EXPOSE 3000
   
   CMD ["npm", "start"]
   ```

2. **Build and run**:
   ```bash
   docker build -t foosball-tournament .
   docker run -p 3000:3000 -v $(pwd)/players.json:/app/players.json foosball-tournament
   ```

## Network Configuration

### Local Network Access

To allow other computers on your local network to access the application:

1. **Modify server.js** to bind to all interfaces:
   ```javascript
   app.listen(PORT, '0.0.0.0', () => {
       console.log(`Foosball Tournament Server running at http://0.0.0.0:${PORT}`);
   });
   ```

2. **Find your computer's IP address**:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   # or
   ip addr show
   ```

3. **Access from other computers**: `http://your-computer-ip:3000`

### Firewall Configuration

Ensure port 3000 is open:

```bash
# Ubuntu/Debian
sudo ufw allow 3000

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload

# Windows
# Use Windows Firewall settings to allow port 3000
```

## Environment Configuration

### Custom Port Configuration

1. **Modify server.js**:
   ```javascript
   const PORT = process.env.PORT || 3000;
   ```

2. **Set environment variable**:
   ```bash
   # Linux/Mac
   export PORT=8080
   npm start
   
   # Windows
   set PORT=8080
   npm start
   ```

### Production Environment Variables

Create `.env` file:
```
NODE_ENV=production
PORT=3000
DATA_FILE=players.json
```

## Data Migration

### Preserving Championship Data

When moving to a new system:

1. **Backup current data**:
   ```bash
   cp players.json players_backup.json
   ```

2. **Transfer the `players.json` file** to the new system

3. **Verify data integrity** after deployment

### Multiple Environment Data

For different environments (development, staging, production):

```bash
# Development
cp players.json players_dev.json

# Staging
cp players.json players_staging.json

# Production
cp players.json players_prod.json
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port 3000
   lsof -i :3000
   # Kill the process
   kill -9 <PID>
   ```

2. **Permission denied**:
   ```bash
   # Make sure you have write permissions for players.json
   chmod 664 players.json
   ```

3. **Node.js not found**:
   ```bash
   # Verify Node.js installation
   node --version
   npm --version
   ```

### Log Files

Monitor application logs:
```bash
# With PM2
pm2 logs foosball-tournament

# Direct execution
npm start > app.log 2>&1 &
tail -f app.log
```

## Security Considerations

### Basic Security

1. **Change default port** in production
2. **Use HTTPS** with SSL certificates
3. **Implement authentication** if needed
4. **Regular backups** of `players.json`

### Reverse Proxy Setup (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Backup Strategy

### Automated Backups

Create backup script (`backup.sh`):
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp players.json "backups/players_${DATE}.json"
# Keep only last 30 backups
ls -t backups/players_*.json | tail -n +31 | xargs rm -f
```

Run daily with cron:
```bash
0 2 * * * /path/to/backup.sh
```

## Summary

Choose the deployment method that best fits your needs:
- **Simple file transfer**: For single computer deployment
- **Git repository**: For team collaboration and version control
- **Server deployment**: For multi-user access
- **Docker**: For containerized deployment

The application will maintain all championship data through the `players.json` file, ensuring continuity across different deployments.