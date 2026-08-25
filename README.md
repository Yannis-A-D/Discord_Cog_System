# 🐳 Discord Cog System (Docker Edition)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.0%2B-5865F2.svg?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Branch](https://img.shields.io/badge/Branch-docker-blueviolet.svg?logo=git&logoColor=white)](https://github.com/Yannis-A-D/Discord_Cog_System/tree/docker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Official Docker containerized branch of [Discord_Cog_System](https://github.com/Yannis-A-D/Discord_Cog_System).**

*One-command containerized Discord bot deployment with live volume hot-reloading.*

</div>

---

## 🌟 Other Branches
- 📦 **[`main`](https://github.com/Yannis-A-D/Discord_Cog_System)**: Standard cross-platform setup with auto-virtualenv runner.
- ⚡ **[`pm2`](https://github.com/Yannis-A-D/Discord_Cog_System/tree/pm2)**: Production VPS deployment with PM2 process manager (`ecosystem.config.js`).

---

## 🐳 Quick Start with Docker Compose

### 1. Clone & Checkout Docker Branch
```bash
git clone -b docker https://github.com/Yannis-A-D/Discord_Cog_System.git
cd Discord_Cog_System
```

### 2. Configure Environment Variables
Copy `.env.example` to `bot.env`:
```bash
cp .env.example bot.env
```
Fill in your credentials in `bot.env` (`DISCORD_TOKEN`, `PREFIX`, `MASTER_USER_ID`, etc.).

### 3. Start the Bot
```bash
# Build and run the container in the background
docker compose up -d --build

# View live bot logs
docker compose logs -f

# Stop the bot
docker compose down
```

> [!TIP]
> **Live Hot-Reloading in Docker**: `docker-compose.yml` mounts `./src/cogs` directly into the container. You can add or edit any cog on your host machine and simply trigger `/reload all` in Discord without rebuilding or restarting the Docker container!

---

## 📁 Docker Branch Structure

```text
Discord_Cog_System/
├── src/
│   ├── bot.py             # Main bot initialization & cog loader
│   ├── cogs/              # Modular cog extensions (mounted into container)
│   │   ├── Ownerscmd.py   # Owner commands (reload, restart, shutdown)
│   │   └── sync.py        # Slash command sync
│   └── utils/
│       └── helpers.py     # Helpers & permission checks
├── .dockerignore          # Docker build exclusions
├── .env.example           # Environment template
├── Dockerfile             # Multi-stage lightweight Python 3.12-slim container
├── docker-compose.yml     # Container orchestration & live volume mounts
├── requirements.txt       # Dependencies
└── README.md
```

---

## 🛠️ Bot Commands

| Command | Type | Description |
| :--- | :--- | :--- |
| `!reload [cog/all]` | Prefix & Slash (`/reload`) | Hot-reloads specific cog or all cogs inside container |
| `!restart` | Prefix & Slash (`/restart`) | Gracefully restarts the bot |
| `!shutdown` | Prefix & Slash (`/shutdown`) | Safely shuts down the container |
| `!sync` | Prefix | Manually forces a slash command sync to Discord |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
