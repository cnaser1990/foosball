const express = require("express");
const fs = require("fs").promises;
const path = require("path");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = "players.json";

// Function to find an available port
async function findAvailablePort(startPort) {
  const net = require("net");

  return new Promise((resolve) => {
    const server = net.createServer();

    server.listen(startPort, () => {
      const port = server.address().port;
      server.close(() => {
        resolve(port);
      });
    });

    server.on("error", () => {
      // Port is in use, try next one
      findAvailablePort(startPort + 1).then(resolve);
    });
  });
}

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static("."));

// Serve the main HTML file
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// API endpoint to get players data
app.get("/api/players", async (req, res) => {
  try {
    const data = await fs.readFile(DATA_FILE, "utf8");
    res.json(JSON.parse(data));
  } catch (error) {
    console.error("Error reading players.json:", error);
    // Return default data if file doesn't exist or can't be read
    const defaultData = {
      players: [
        { name: "ghayem", seed: 1 },
        { name: "elini", seed: 3 },
        { name: "dinparvar", seed: 3 },
        { name: "alivand", seed: 1 },
        { name: "hoseinizade", seed: 3 },
        { name: "hajali", seed: 3 },
        { name: "dariushi", seed: 1 },
      ],
      championships: {
        ghayem: 6,
        elini: 2,
        dinparvar: 1,
        alivand: 1,
        hoseinizade: 3,
        hajali: 2,
        dariushi: 3,
      },
      scores: {
        ghayem: 0,
        elini: 0,
        dinparvar: 0,
        alivand: 0,
        hoseinizade: 0,
        hajali: 0,
        dariushi: 0,
      },
    };
    res.json(defaultData);
  }
});

// API endpoint to save players data
app.post("/api/players", async (req, res) => {
  try {
    const data = JSON.stringify(req.body, null, 4);
    await fs.writeFile(DATA_FILE, data, "utf8");
    res.json({ success: true, message: "Data saved successfully" });
  } catch (error) {
    console.error("Error writing to players.json:", error);
    res.status(500).json({ success: false, message: "Error saving data" });
  }
});

// Start server with automatic port detection
(async () => {
  try {
    const availablePort = await findAvailablePort(PORT);

    if (availablePort !== PORT) {
      console.log(
        `⚠️  Port ${PORT} is in use, using port ${availablePort} instead`
      );
    }

    app.listen(availablePort, "0.0.0.0", () => {
      console.log(
        `⚽︎ Foosball Tournament Server running at http://0.0.0.0:${availablePort}`
      );
      console.log(
        `🌐 Access from other devices: http://your-ip-address:${availablePort}`
      );
      console.log(`📄 Data stored in: ${DATA_FILE}`);
      console.log(`⏹️  Press Ctrl+C to stop the server`);
    });
  } catch (error) {
    console.error("❌ Failed to start server:", error);
    process.exit(1);
  }
})();
