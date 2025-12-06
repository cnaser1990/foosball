# ⚽ Foosball Tournament Manager

A full-stack web application designed to manage local foosball tournaments, track player statistics, balance teams based on skill levels, and archive seasonal history.

## ✨ Features

*   **Player Management**: Add or remove players and assign skill seeds (Pro, Intermediate, Beginner).
*   **Team Generation**:
    *   **Seed Balanced**: Automatically pairs strong players with beginners to ensure fair matches.
    *   **Random**: Completely random pairings.
    *   **Custom**: Manually build teams (supports 1v1 or 2v2).
*   **Live Match Tracking**: 
    *   Scoreboard interface.
    *   Postpone matches capability.
    *   Real-time goal difference updates.
*   **Statistics**:
    *   Track individual Championships won.
    *   Track cumulative Goal Difference (Score) across all games.
    *   Leaderboard visualization.
*   **Season Management**:
    *   Archive current stats and start a fresh season.
    *   View historical data from previous seasons.
*   **Admin System**: Password-protected area to manually correct stats.

## 🛠️ Tech Stack

*   **Frontend**: Vanilla JavaScript, HTML, CSS.
*   **Backend**: Node.js, Express.
*   **Data Storage**: JSON-based flat-file persistence.
*   **Infrastructure**: Docker & Nginx.

---

## 🚀 Installation & Setup

### Option A: Using Docker (Recommended)

This method includes an Nginx proxy and ensures data persistence via volumes.

1.  **Prerequisites**: Ensure [Docker](https://www.docker.com/) and Docker Compose are installed.
2.  **Create the Data Directory**:
    ```bash
    mkdir data
    ```
3.  **Start the Application**:
    ```bash
    docker-compose up -d --build
    ```
4.  **Access the App**:
    *   Open your browser to: `http://localhost:8899`

### Option B: Local Node.js Setup

1.  **Install Dependencies**:
    ```bash
    npm install
    ```
2.  **Start the Server**:
    ```bash
    npm start
    # Or for development with auto-reload:
    npm run dev
    ```
3.  **Access the App**:
    *   Open your browser to: `http://localhost:3000` (or the port displayed in the console).

---

## 📖 Usage Guide

### 1. Setting Up Players
*   Click **"Manage Players"**.
*   Add players and assign them a seed:
    *   **Seed 1**: Pro (Best players)
    *   **Seed 2**: Intermediate
    *   **Seed 3**: Beginner
*   *Tip: Proper seeding is crucial for the "Balanced" team generation mode.*

### 2. Starting a Tournament
*   Select the players present today from the main list.
*   Click **"Start Tournament"**.
*   Choose your mode:
    *   **Seed Mode**: Pairs Seed 1 with Seed 3 players.
    *   **Random Mode**: Random shuffle.
    *   **Custom Mode**: You pick the teams.

### 3. Playing Matches
*   The app will generate a match schedule.
*   Input goals using the `+` and `-` buttons.
*   Click **"Submit Result"** to save and move to the next match.
*   Use **"Postpone"** if players are currently unavailable; the match will move to the end of the queue.

### 4. Admin & Seasons
*   **Admin Login**: Click "Admin Login" in the menu.
    *   **Default Password**: `foosball`
    *   Allows manual editing of wins and goal scores.
*   **Finish Season**: When a "season" is over, click "Finish Season".
    *   Enter a name (e.g., "Winter_2023").
    *   This archives the current `players.json` to `_player_Winter_2023.json` and resets stats for the new season.

---

## 📂 Project Structure

*   **`server.js`**: Express server handling API routes (`/api/players`, `/api/finish-season`) and file I/O operations.
*   **`script.js`**: Core frontend logic containing the `TournamentApp` class, UI state management, and match algorithms.
*   **`players.json`**: The active database file storing current players and stats.
*   **`_player_[name].json`**: Archived season files.
*   **`docker-compose.yaml`**: Configuration for the Node app and Nginx reverse proxy.

## ⚠️ Data Persistence

If running via Docker, data is stored in the mapped `./data` volume. Ensure you do not delete this folder, or you will lose your tournament history.

---

## 🔧 Advanced Options

*   **Custom CSS**: Modify `style.css` to change colors, fonts, or layout.
*   **Custom Match Logic**: Edit the `generateMatches` method in `script.js` to implement your own pairing algorithm.