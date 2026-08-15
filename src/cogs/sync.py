import discord
from discord.ext import commands
import os

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    async def sync(self, ctx):
        """Manually sync slash commands."""
        if ctx.author.id not in (1390183168157417522, 818106391411163217):
            await ctx.send("Only the bot owners can use this command.")
            return
        try:
            from utils.helpers import ALLOWED_GUILD_ID
            guild = self.bot.get_guild(ALLOWED_GUILD_ID)
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
