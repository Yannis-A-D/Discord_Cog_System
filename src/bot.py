import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure the root directory and src directory are in sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))

import discord
from discord.ext import commands

# Load environment from bot.env in project root if present, otherwise fallback
env_path = root_dir / "bot.env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')
MASTER_USER_ID = 818106391411163217  # Master permissions for all commands

if not TOKEN:
    sys.exit("DISCORD_TOKEN not set. Add it to bot.env or the environment.")

from utils.helpers import ALLOWED_GUILD_ID

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

def _iter_cog_modules():
    cogs_dir = Path(__file__).parent / 'cogs'
    if not cogs_dir.exists():
        return
    for file in cogs_dir.iterdir():
        if file.suffix == '.py' and file.name != '__init__.py':
            yield file

def create_bot():
    bot_local = commands.Bot(command_prefix=PREFIX, intents=intents)

    @bot_local.check
    async def globally_block_non_master(ctx):
        if ctx.author.id == MASTER_USER_ID:
            return True
        return True

    @bot_local.event
    async def on_ready():
        print(f'Logged in as {bot_local.user} ({bot_local.user.id})')
        print('------')
        try:
            if not getattr(bot_local, '_presence_set', False):
                await bot_local.change_presence(status=discord.Status.dnd)
                bot_local._presence_set = True
                print('Presence set to DND')
        except Exception as e:
            print(f'Failed to set presence: {e}')

        # Sync slash commands
        try:
            guild = bot_local.get_guild(ALLOWED_GUILD_ID)
            if guild:
                await bot_local.tree.sync(guild=guild)
                print(f'Synced slash commands to guild {guild.name} ({guild.id})')
            await bot_local.tree.sync()
            print('Synced slash commands globally')
        except Exception as e:
            print(f'Failed to sync slash commands: {e}')

    async def _setup_hook():
        for file in _iter_cog_modules():
            # Try loading as src.cogs or cogs
            loaded = False
            for prefix in ("src.cogs", "cogs"):
                module_name = f"{prefix}.{file.stem}"
                try:
                    await bot_local.load_extension(module_name)
                    print(f"Loaded extension {module_name}")
                    loaded = True
                    break
                except ModuleNotFoundError:
                    continue
                except Exception as e:
                    print(f"Failed to load extension {module_name}: {e}")
                    loaded = True
                    break
            if not loaded:
                print(f"Failed to find module for cog: {file.name}")

    bot_local.setup_hook = _setup_hook
    return bot_local

if __name__ == '__main__':
    bot = create_bot()
    bot.run(TOKEN)
