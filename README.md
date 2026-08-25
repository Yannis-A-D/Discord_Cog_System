# 🤖 Discord Cog System Bot Template

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.0%2B-5865F2.svg?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**A modular, production-ready Discord bot template built with [discord.py](https://github.com/Rapptz/discord.py).**

*Features automatic Cog extension discovery, slash command sync, owner utilities (hot-reloading, restart, shutdown), multi-platform startup scripts, and native Docker containerization.*

</div>

---

## ✨ Key Features

- 🧩 **Modular Cog Architecture**: Automatically discovers and registers every cog inside `src/cogs/` on startup.
- ⚡ **Zero-Downtime Hot-Reloading**: Reload individual cogs or all extensions dynamically using `!reload` or `/reload` without restarting the process.
- 🐳 **Docker & Docker Compose Ready**: One-command containerized deployment with volume mounts for live cog updates.
- 🔄 **Slash Command Synchronization**: Seamless global and development-guild application command sync.
- 👑 **Owner & Admin Controls**: Built-in restricted commands for shutdown, restart, and manual tree syncing.
- ⚙️ **Flexible Configuration**: Secure credential management via `.env` / `bot.env`.
- 🚀 **Automated Local Setup**: `run_bot.py` and `run_bot.bat` auto-create a virtual environment (`.venv`), install dependencies, and launch the bot in one step.

---

## 📁 Project Structure

```text
Discord_Cog_System/
├── src/
│   ├── bot.py             # Main bot initialization, intents, presence & cog loader
│   ├── cogs/
│   │   ├── Ownerscmd.py   # Owner commands (reload, restart, shutdown)
│   │   └── sync.py        # Slash command synchronization cog
│   └── utils/
│       └── helpers.py     # Utility functions & guild permission checks
├── .dockerignore          # Docker build exclusions
├── .env.example           # Configuration template
├── .gitignore             # Git excluded files
├── Dockerfile             # Production container image definition
├── docker-compose.yml     # Multi-container orchestration
├── requirements.txt       # Python package dependencies
├── run_bot.bat            # Windows one-click startup batch script
├── run_bot.py             # Cross-platform startup & dependency manager
└── README.md              # Documentation
```

---

## ⚙️ Configuration

1. Copy `.env.example` to `bot.env` (or `.env`):
   ```bash
   cp .env.example bot.env
   ```

2. Open `bot.env` and configure your credentials:

| Variable | Required | Description | Example |
| :--- | :---: | :--- | :--- |
| `DISCORD_TOKEN` | **Yes** | Your Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications) | `MTE...` |
| `PREFIX` | No | Command prefix for traditional text commands (Default: `!`) | `!` |
| `MASTER_USER_ID` | No | Discord User ID of the primary bot owner for restricted commands | `123456789012345678` |
| `OWNER_USER_IDS` | No | Comma-separated Discord User IDs for co-owners | `12345678,23456789` |
| `DEV_GUILD_ID` | No | Development Discord Server ID for instant slash command sync | `987654321098765432` |
| `ALLOWED_GUILD_ID` | No | Target server ID for restricted feature execution | `987654321098765432` |

---

## 🚀 Getting Started

### Option 1: Run with Docker (Recommended for Production)

Ensure you have [Docker](https://docs.docker.com/get-docker/) installed.

```bash
# 1. Build and start the container in the background
docker compose up -d --build

# 2. View live bot logs
docker compose logs -f

# 3. Stop the bot
docker compose down
```

*Or run directly with the Docker CLI:*
```bash
docker build -t discord-cog-bot .
docker run -d --env-file bot.env --name discord_bot --restart unless-stopped discord-cog-bot
```

> [!TIP]
> The `docker-compose.yml` mounts `./src/cogs` as a volume, meaning you can edit or add cogs on your host machine and use `/reload` inside Discord **without rebuilding the Docker container**!

---

### Option 2: Windows (One-Click Setup)

Double-click **`run_bot.bat`** or execute it in PowerShell / Command Prompt:

```cmd
run_bot.bat
```

*The batch script will automatically check for Python, create a virtual environment (`.venv`), install missing packages from `requirements.txt`, and start the bot.*

---

### Option 3: Cross-Platform (Linux / macOS / Windows)

Run the automated Python runner:

```bash
python run_bot.py
```

*Or manually using standard virtual environment commands:*
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies and run
pip install -r requirements.txt
python src/bot.py
```

---

## 🛠️ Bot Commands

### 👑 Owner & Administrative Controls

| Command | Type | Description |
| :--- | :--- | :--- |
| `!reload [cog/all]` | Prefix & Slash (`/reload`) | Hot-reloads a specific cog or all cogs without restarting |
| `!restart` | Prefix & Slash (`/restart`) | Gracefully restarts the bot process |
| `!shutdown` | Prefix & Slash (`/shutdown`) | Safely disconnects and shuts down the bot |
| `!sync` | Prefix | Manually forces a slash command tree sync with Discord |

---

## 🧩 Adding New Cogs

To add a new feature or command suite, create a new `.py` file inside `src/cogs/` (e.g., `src/cogs/fun.py`):

```python
import discord
from discord import app_commands
from discord.ext import commands


class FunCog(commands.Cog):
    """Example feature cog with prefix and slash commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # 1. Traditional Prefix Command (!ping)
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

    # 2. Slash Command (/hello)
    @app_commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"👋 Hello {interaction.user.mention}!", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FunCog(bot))
```

> [!NOTE]
> The bot will automatically detect and load your new cog on next launch. You can also run `!reload all` (or `/reload all`) in Discord to load it instantly without restarting!

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more details.
