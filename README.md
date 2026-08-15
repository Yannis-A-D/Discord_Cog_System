# Discord Cog System Bot Template

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.0%2B-blueviolet)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular, scalable, and production-ready Discord bot template built with [discord.py](https://github.com/Rapptz/discord.py). Features dynamic Cog extension loading, slash command synchronization, owner utilities (hot-reloading, restart, shutdown), environment-based configuration, and automated startup scripting.

---

## Features

* **Modular Architecture**: Automatically discovers and loads all cogs from the `src/cogs/` directory on startup.
* **Hot-Reloading**: Reload individual cogs or all cogs on the fly without restarting the bot using `!reload` or `/reload`.
* **Owner Controls**: Built-in owner-only commands for `shutdown`, `restart`, and `sync`.
* **Slash Command Synchronization**: Automatic global and dev-guild sync support.
* **Environment-Based Config**: Safe credential and setting management via `.env` / `bot.env`.
* **Automated Setup Script**: `run_bot.py` / `run_bot.bat` creates a virtual environment, installs dependencies, and runs the bot with a single click.

---

## Project Structure

```text
├── src/
│   ├── bot.py             # Main bot initialization & cog loader
│   ├── cogs/
│   │   ├── Ownerscmd.py   # Owner commands (reload, restart, shutdown)
│   │   └── sync.py        # Slash command synchronization
│   └── utils/
│       └── helpers.py     # Utility functions & guild permission checks
├── .env.example           # Configuration template
├── .gitignore             # Excluded secret & runtime files
├── requirements.txt       # Python package dependencies
├── run_bot.bat            # Windows one-click startup batch script
├── run_bot.py             # Cross-platform startup & dependency manager
└── README.md
```

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Yannis-A-D/Discord_Cog_System.git
cd Discord_Cog_System
```

### 2. Configure Environment Variables
Copy `.env.example` to `bot.env` (or `.env`) and fill in your credentials:
```bash
cp .env.example bot.env
```

Edit `bot.env`:
```env
DISCORD_TOKEN=your_discord_bot_token_here
PREFIX=!
DEV_GUILD_ID=your_development_guild_id
ALLOWED_GUILD_ID=your_allowed_guild_id
```

### 3. Run the Bot

**Windows (One-Click):**
Double-click `run_bot.bat` or run in terminal:
```cmd
run_bot.bat
```

**Cross-Platform (Python):**
```bash
python run_bot.py
```

*The startup script will automatically create a virtual environment (`.venv`), install all requirements, and start the bot.*

---

## Commands

### Owner / Admin Commands

| Command | Type | Description |
| :--- | :--- | :--- |
| `!reload [cog/all]` | Prefix & Slash (`/reload`) | Hot-reloads specified cog module or all cogs |
| `!restart` | Prefix & Slash (`/restart`) | Gracefully restarts the bot process |
| `!shutdown` | Prefix & Slash (`/shutdown`) | Safely shuts down the bot |
| `!sync` | Prefix | Manually forces a slash command sync to Discord |

---

## Adding New Cogs

To add a new feature or command set, create a new `.py` file inside `src/cogs/`:

```python
import discord
from discord.ext import commands

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
```

The bot will automatically detect and load your new cog on next launch, or you can run `!reload all` while the bot is running.

---

## License

This project is licensed under the MIT License.
