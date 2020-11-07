import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands

import backend.commands as db
from backend import admin


# This command is used to add people's ID's to a spreadsheet.
class Addids(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.has_role(admin)
    async def addids(self, ctx):
        members = ctx.message.guild.members
        names_ids = [(m.display_name, m.id) for m in members]

        db.add_ids(names_ids)





def setup(bot):
    bot.add_cog(Addids(bot))
