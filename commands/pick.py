import asyncio
import random

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed


# This command randomly picks between the two non-banned maps.
#
# !pick [#] [#]
#
# The two numbers represent the two maps that were not banned from
# running the !maps command.
class Pick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def pick(self, ctx):
        # These numbers are the same as the ones listed in !maps
        d = {
            "1": "The Skeld",
            "2": "Mira HQ",
            "3": "Polus"
        }
        msg = ctx.message.content
        nums = msg.split(" ")[1:]

        # Must be two unique numbers that are 1, 2, 3
        if len(nums)!=2 or not all(n in d for n in nums) or nums[0]==nums[1]:
            await ctx.send("Invalid Input!")
            return

        text = d[random.choice(nums)]

        embed = Embed(
            title="Map",
            color=Color.from_rgb(0, 0, 0),
            description=text
        )

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Pick(bot))
