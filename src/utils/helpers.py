import os
import re
from typing import Optional, Union
import discord
from discord.ext import commands

# Load guild ID from environment
ALLOWED_GUILD_ID = int(os.getenv("ALLOWED_GUILD_ID", 0)) if os.getenv("ALLOWED_GUILD_ID", "").strip().isdigit() else 0

def get_owner_ids() -> set[int]:
    """Parse comma-separated owner IDs from environment variable OWNER_USER_IDS."""
    raw = os.getenv("OWNER_USER_IDS", "")
    return {int(uid.strip()) for uid in raw.split(",") if uid.strip().isdigit()}

async def is_allowed_guild_check(ctx: commands.Context) -> bool:
    """Check if command is used in the allowed guild."""
    if ctx.guild is None:
        print("[Guild Check] Command used in DMs - blocking")
        return False
    
    match = ctx.guild.id == ALLOWED_GUILD_ID
    print(f"[Guild Check] Guild ID: {ctx.guild.id}, Allowed: {ALLOWED_GUILD_ID}, Match: {match}")
    return match

def is_allowed_guild():
    """Check decorator to ensure commands only work in the allowed guild."""
    return commands.check(is_allowed_guild_check)

def parse_money(val: str) -> Optional[int]:
    """Parses money input string like '500k', '2.5m', '1.2b', '500000' into integer."""
    if not val:
        return None
    cleaned = str(val).strip().replace("$", "").replace(",", "")
    match = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*([kKmMbB]?)$", cleaned)
    if not match:
        return None

    number_part = float(match.group(1))
    suffix = match.group(2).lower()

    multiplier = 1
    if suffix == "k":
        multiplier = 1_000
    elif suffix == "m":
        multiplier = 1_000_000
    elif suffix == "b":
        multiplier = 1_000_000_000

    return int(round(number_part * multiplier))

def format_money(amount: Union[int, float]) -> str:
    """Formats numeric amount into readable string with K, M, B suffixes."""
    amount_abs = abs(amount)
    prefix = "-" if amount < 0 else ""

    if amount_abs >= 1_000_000_000:
        val = amount_abs / 1_000_000_000
        formatted = f"{val:.2f}".rstrip("0").rstrip(".")
        return f"{prefix}${formatted}B"
    elif amount_abs >= 1_000_000:
        val = amount_abs / 1_000_000
        formatted = f"{val:.2f}".rstrip("0").rstrip(".")
        return f"{prefix}${formatted}M"
    elif amount_abs >= 1_000:
        val = amount_abs / 1_000
        formatted = f"{val:.2f}".rstrip("0").rstrip(".")
        return f"{prefix}${formatted}K"
    else:
        return f"{prefix}${int(amount_abs):,}"

