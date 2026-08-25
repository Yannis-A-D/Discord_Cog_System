# ⚡ Discord Cog System (PM2 Edition)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.0%2B-5865F2.svg?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![PM2](https://img.shields.io/badge/PM2-Process_Manager-2B037A.svg?logo=pm2&logoColor=white)](https://pm2.keymetrics.io/)
[![Branch](https://img.shields.io/badge/Branch-pm2-blueviolet.svg?logo=git&logoColor=white)](https://github.com/Yannis-A-D/Discord_Cog_System/tree/pm2)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Official PM2 Process Management branch of [Discord_Cog_System](https://github.com/Yannis-A-D/Discord_Cog_System).**

*Production 24/7 background process management with auto-restart on crash, system reboot persistence, and live log monitoring.*

</div>

---

## 🌟 Other Branches
- 📦 **[`main`](https://github.com/Yannis-A-D/Discord_Cog_System)**: Standard cross-platform setup with auto-virtualenv runner.
- 🐳 **[`docker`](https://github.com/Yannis-A-D/Discord_Cog_System/tree/docker)**: Multi-stage Docker containerized deployment (`Dockerfile`, `docker-compose.yml`).

---

## 🚀 Quick Start with PM2

### 1. Prerequisites (Node.js & PM2)
Ensure [Node.js](https://nodejs.org/) and `pm2` are installed globally:
```bash
npm install -g pm2
```

### 2. Clone & Checkout PM2 Branch
```bash
git clone -b pm2 https://github.com/Yannis-A-D/Discord_Cog_System.git
cd Discord_Cog_System
```

### 3. Setup Python Virtual Environment
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `bot.env`:
```bash
cp .env.example bot.env
```
Fill in your credentials (`DISCORD_TOKEN`, `PREFIX`, `MASTER_USER_ID`, etc.).

---

## ⚡ Running & Managing with PM2

### Start the Bot
```bash
pm2 start ecosystem.config.js
```

### Essential PM2 Commands

| Command | Action |
| :--- | :--- |
| `pm2 status` | View bot process status, memory, CPU, and uptime |
| `pm2 logs discord-cog-bot` | Stream live real-time output and error logs |
| `pm2 restart discord-cog-bot` | Instantly restart the bot process |
| `pm2 stop discord-cog-bot` | Stop the bot |
| `pm2 monit` | Terminal dashboard monitoring CPU, memory, and logs |

---

## 🔄 24/7 Auto-Start on System Boot (Linux / VPS)

To guarantee your Discord bot restarts automatically if the server reboots:

```bash
# 1. Generate and configure startup script
pm2 startup

# 2. Save current running processes
pm2 save
```

---

## 📁 PM2 Branch Structure

```text
Discord_Cog_System/
├── src/
│   ├── bot.py             # Main bot initialization & cog loader
│   ├── cogs/
│   │   ├── Ownerscmd.py   # Owner commands (reload, restart, shutdown)
│   │   └── sync.py        # Slash command sync
│   └── utils/
│       └── helpers.py     # Helpers & permission checks
├── .env.example           # Environment template
├── ecosystem.config.js    # PM2 Process Manager configuration
├── requirements.txt       # Dependencies
├── run_bot.bat            # Windows startup script
├── run_bot.py             # Cross-platform runner
└── README.md
```

---

## 🛠️ Bot Commands

| Command | Type | Description |
| :--- | :--- | :--- |
| `!reload [cog/all]` | Prefix & Slash (`/reload`) | Hot-reloads specific cog or all cogs |
| `!restart` | Prefix & Slash (`/restart`) | Gracefully restarts the bot |
| `!shutdown` | Prefix & Slash (`/shutdown`) | Safely shuts down the bot |
| `!sync` | Prefix | Manually forces a slash command sync to Discord |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
