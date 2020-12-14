#!/usr/bin/env python
import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find

# TEST
client = discord.Client()

# "Intents" are permissions set up by Discord.
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "!", intents=intents)

bot.remove_command("help")

# These are all the cogs. When you add a command or a task, add a
# reference point to this list using the "folder.file" format.
cogs = [
    "commands.help",
    "commands.g",
    "commands.name",
    "commands.test",
    "commands.maps",
    "commands.pick",
    "commands.strike",
    "commands.unstrike",
    "commands.addids",
    "commands.newseason"
]

if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Bot is ready!")


with open("token.txt", "r") as f:
    lines = f.readlines()
    token = lines[0].strip()

bot.run(token)
