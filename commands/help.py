import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_descs = {
            "!help": "Provides information about all commands.",
            "!g": "Scorers use this to score games.",
            "!name": "Use this to rename yourself.",
            "!maps": "Lists out maps for banning"
        }


    @commands.command()
    async def help(self, ctx):
        desc = ""
        for k, v in self.command_descs.items():
            desc += f"`{k}`: {v}\n"

        embed = Embed(
            title="Commands",
            color=Color.dark_gray(),
            description=desc
        )

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Help(bot))
