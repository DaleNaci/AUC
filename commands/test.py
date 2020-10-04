import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def test(self, ctx):
        guild = ctx.message.guild
        content = ctx.message.content.split()[1:]

        word = content[0]

        print(guild.get_member(int(word[3:-1])).nick)



def setup(bot):
    bot.add_cog(Test(bot))
