import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

import backend.commands as db


class Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def name(self, ctx):
        old_name = ctx.author.display_name
        new_name = ctx.message.content[6:]

        print(old_name)
        print(new_name)

        db.changeName(old_name, new_name)

        await ctx.author.edit(nick=new_name)
        await ctx.channel.send("Name Changed!")



def setup(bot):
    bot.add_cog(Name(bot))
