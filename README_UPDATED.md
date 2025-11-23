# Foosball Tournament Manager - Updated with Persistent Storage

This foosball tournament manager has been updated to use `players.json` for persistent data storage instead of localStorage. Both the JavaScript web application and Python desktop application now share the same data source.

## Changes Made

### 1. Fixed CSS Issue
- Fixed vendor prefix issue in `styles.css` by adding the standard `appearance` property alongside `-moz-appearance` for cross-browser compatibility.

### 2. Added Node.js Server
- Created `server.js` - Express server that handles reading from and writing to `players.json`
- Added `package.json` with necessary dependencies (express, cors)
- Server provides REST API endpoints for data operations

### 3. Updated JavaScript Application
- Modified `script.js` to use server API endpoints instead of localStorage
- Updated `loadData()` method to fetch data from `/api/players` endpoint
- Updated `saveData()` method to POST data to `/api/players` endpoint
- Made necessary methods async to handle API calls properly

## How to Use

### For Web Application (JavaScript)

1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Start the Server:**
   ```bash
   npm start
   ```
   The server will start at `http://localhost:3000`

3. **Access the Application:**
   Open your web browser and navigate to `http://localhost:3000`

### For Desktop Application (Python)

The Python application (`foosball.py`) continues to work as before, directly reading from and writing to `players.json`.

```bash
python foosball.py
```

## Data Synchronization

Both applications now use the same `players.json` file:
- **JavaScript app**: Reads/writes via server API endpoints
- **Python app**: Reads/writes directly to the file
- **Championship data**: Automatically synchronized between both applications

## API Endpoints

- `GET /api/players` - Retrieve all player and championship data
- `POST /api/players` - Save player and championship data

## File Structure

```
foosball/
├── server.js              # Node.js Express server
├── package.json           # Node.js dependencies
├── players.json           # Shared data file
├── script.js              # Updated JavaScript application
├── index.html             # Web application HTML
├── styles.css             # Updated CSS with fixes
├── foosball.py            # Python desktop application
└── README_UPDATED.md      # This file
```

## Benefits

1. **Shared Data**: Both web and desktop applications use the same championship data
2. **Persistent Storage**: Data survives browser seasons and application restarts
3. **Cross-Platform**: Championship records are maintained across different application versions
4. **Real-time Sync**: Changes made in one application are immediately available to the other

## Technical Details

- Server runs on port 3000 by default
- CORS enabled for cross-origin requests
- Automatic error handling and fallback to default data
- Async/await pattern used throughout JavaScript application for proper API handling