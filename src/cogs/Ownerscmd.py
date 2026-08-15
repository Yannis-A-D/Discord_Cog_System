import os
import sys
import discord
from pathlib import Path
from discord.ext import commands
from discord import app_commands

# Owner user IDs
OWNER_USER_IDS = {1390183168157417522, 818106391411163217}

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._synced = False

    @commands.command(name="shutdown", aliases=["stop", "logout"])
    async def shutdown(self, ctx):
        """Owner-only command to cleanly shut down the bot."""
        if ctx.author.id not in OWNER_USER_IDS:
            await ctx.send("Only the bot owner can use this command.")
            return
        await ctx.send("Shutting down — bye!")
        await self.bot.close()

    @commands.command(name="restart")
    async def restart(self, ctx):
        """Owner-only command to restart the bot."""
        if ctx.author.id not in OWNER_USER_IDS:
            await ctx.send("Only the bot owner can use this command.")
            return
        await ctx.send("Restarting — be right back!")
        await self.bot.close()
        python = sys.executable
        os.execv(python, [python] + sys.argv)

    @app_commands.command(name="shutdown", description="Shut down the bot (owner only)")
    async def shutdown_slash(self, interaction: discord.Interaction):
        """Owner-only slash command to cleanly shut down the bot."""
        if interaction.user.id not in OWNER_USER_IDS:
            await interaction.response.send_message("Only the bot owner can use this command.", ephemeral=True)
            return

        await interaction.response.send_message("Shutting down — bye!", ephemeral=True)
        await self.bot.close()

    @app_commands.command(name="restart", description="Restart the bot (owner only)")
    async def restart_slash(self, interaction: discord.Interaction):
        """Owner-only slash command to restart the bot."""
        if interaction.user.id not in OWNER_USER_IDS:
            await interaction.response.send_message("Only the bot owner can use this command.", ephemeral=True)
            return

        await interaction.response.send_message("Restarting — be right back!", ephemeral=True)
        await self.bot.close()
        python = sys.executable
        os.execv(python, [python] + sys.argv)

    async def _reload_cogs(self, cog: str):
        """Reload a specific cog or all cogs. Returns list of (module, ok, message)."""
        results = []
        cogs_dir = Path(__file__).parent
        bot = self.bot

        if cog.lower() in ("all", "*"):
            for file in cogs_dir.iterdir():
                if file.suffix == '.py' and file.name != '__init__.py':
                    # Skip uptime.py and staffapp.py from reload if they exist
                    if file.name in ('uptime.py', 'staffapp.py'):
                        continue
                    
                    stem = file.stem
                    module = None
                    for ext in list(bot.extensions.keys()):
                        if ext.endswith(f".{stem}") or ext == stem:
                            module = ext
                            break
                    if not module:
                        module = f"cogs.{stem}"

                    try:
                        await bot.reload_extension(module)
                        results.append((module, True, 'reloaded'))
                    except Exception as e:
                        try:
                            await bot.load_extension(module)
                            results.append((module, True, 'loaded'))
                        except Exception as e2:
                            results.append((module, False, f"reload: {e}; load: {e2}"))
        else:
            candidates = []
            if cog.startswith('cogs.') or cog.startswith('src.cogs.'):
                candidates.append(cog)
            else:
                candidates.append(f'cogs.{cog}')
                candidates.append(f'src.cogs.{cog}')
                candidates.append(cog)

            last_err = 'not found'
            for module in candidates:
                try:
                    await bot.reload_extension(module)
                    results.append((module, True, 'reloaded'))
                    break
                except Exception as e:
                    try:
                        await bot.load_extension(module)
                        results.append((module, True, 'loaded'))
                        break
                    except Exception as e2:
                        last_err = f"reload: {e}; load: {e2}"
            if not results:
                results.append((cog, False, last_err))

        return results

    @commands.command(name="reload")
    async def reload(self, ctx, *, cog: str = 'all'):
        """Reload a cog or all cogs. Usage: !reload Ownerscmd | !reload all"""
        if ctx.author.id not in OWNER_USER_IDS:
            await ctx.send("Only the bot owner can use this command.")
            return
        
        loading_msg = await ctx.send("Reloading cogs...")
        results = await self._reload_cogs(cog)
        
        failed = any(not ok for _, ok, _ in results)
        color = discord.Color.red() if failed else discord.Color.green()
        title = "Reload Complete (With Errors)" if failed else "Reload Complete"
        
        embed = discord.Embed(title=title, color=color, timestamp=discord.utils.utcnow())
        
        success = []
        failed_items = []
        
        for module, ok, msg in results:
            clean_module = module.split('.')[-1]
            if ok:
                action = "Reloaded" if msg == 'reloaded' else "Loaded"
                success.append(f"{action} `{clean_module}`")
            else:
                error_msg = msg.split(';')[0] if ';' in msg else msg
                if len(error_msg) > 50:
                    error_msg = error_msg[:47] + "..."
                failed_items.append(f"Failed `{clean_module}` — {error_msg}")
        
        if success:
            embed.add_field(name=f"Successful ({len(success)})", value="\n".join(success), inline=False)
        if failed_items:
            embed.add_field(name=f"Failed ({len(failed_items)})", value="\n".join(failed_items), inline=False)
        
        embed.set_footer(text=f"Total: {len(success)}/{len(results)} successful")
        await loading_msg.edit(content=None, embed=embed)

    @app_commands.command(name="reload", description="Reload a cog or all cogs (owner only)")
    @app_commands.describe(cog='Name of cog to reload; use "all" to reload all')
    async def reload_slash(self, interaction: discord.Interaction, cog: str = 'all'):
        """Owner-only slash command to reload cogs."""
        if interaction.user.id not in OWNER_USER_IDS:
            await interaction.response.send_message("Only the bot owner can use this command.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        results = await self._reload_cogs(cog)
        
        failed = any(not ok for _, ok, _ in results)
        color = discord.Color.red() if failed else discord.Color.green()
        title = "Reload Complete (With Errors)" if failed else "Reload Complete"
        
        embed = discord.Embed(title=title, color=color, timestamp=discord.utils.utcnow())
        
        success = []
        failed_items = []
        
        for module, ok, msg in results:
            clean_module = module.split('.')[-1]
            if ok:
                action = "Reloaded" if msg == 'reloaded' else "Loaded"
                success.append(f"{action} `{clean_module}`")
            else:
                error_msg = msg.split(';')[0] if ';' in msg else msg
                if len(error_msg) > 50:
                    error_msg = error_msg[:47] + "..."
                failed_items.append(f"Failed `{clean_module}` — {error_msg}")
        
        if success:
            embed.add_field(name=f"Successful ({len(success)})", value="\n".join(success), inline=False)
        if failed_items:
            embed.add_field(name=f"Failed ({len(failed_items)})", value="\n".join(failed_items), inline=False)
        
        embed.set_footer(text=f"Total: {len(success)}/{len(results)} successful")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")
        if getattr(self, '_synced', False):
            return
        self._synced = True
        try:
            dev_guild = os.getenv('DEV_GUILD_ID')
            if dev_guild:
                guild_obj = discord.Object(id=int(dev_guild))
                await self.bot.tree.sync(guild=guild_obj)
                print(f"Synced application commands to dev guild {dev_guild}")
            else:
                await self.bot.tree.sync()
                print("Synced application commands globally")
        except Exception as e:
            print(f"Failed to sync application commands in on_ready: {e}")

async def setup(bot):
    cog = ExampleCog(bot)
    await bot.add_cog(cog)
    try:
        if bot.tree.get_command('shutdown') is None:
            bot.tree.add_command(cog.shutdown_slash)
        if bot.tree.get_command('restart') is None:
            bot.tree.add_command(cog.restart_slash)
        if bot.tree.get_command('reload') is None:
            bot.tree.add_command(cog.reload_slash)
    except Exception as e:
        print(f"Failed to add slash command(s): {e}")
