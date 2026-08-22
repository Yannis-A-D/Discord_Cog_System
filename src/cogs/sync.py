import discord
from discord.ext import commands
import os

from utils.helpers import ALLOWED_GUILD_ID, get_owner_ids

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    async def sync(self, ctx):
        """Manually sync slash commands."""
        owner_ids = get_owner_ids()
        if ctx.author.id not in owner_ids and ctx.author.id != getattr(self.bot, "owner_id", None):
            await ctx.send("Only the bot owners can use this command.")
            return
        try:
            guild = self.bot.get_guild(ALLOWED_GUILD_ID) if ALLOWED_GUILD_ID else None
            if guild:
                await self.bot.tree.sync(guild=guild)
                await ctx.send(f"Synced slash commands to guild `{guild.name}` ({guild.id})")
            else:
                await self.bot.tree.sync()
                await ctx.send("Synced slash commands globally")
        except Exception as e:
            await ctx.send(f"Failed to sync slash commands: {e}")

async def setup(bot):
    await bot.add_cog(Sync(bot))
