import asyncio
from random import sample

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pick(self, ctx, player_count=8):
        if player_count < 2:
            await ctx.send("Invalid player count given!")
            return

        embed = Embed(
                    title="Starting Game...",
                    description="Team Captains are:",
                    color=Color.from_rgb(156, 245, 255)
                )

        captains = sample(range(1, player_count+1), 2)

        embed.add_field(name="First Captain", value=f"Player {captains[0]}")
        embed.add_field(name="Second Captain", value=f"Player {captains[1]}")

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Test(bot))
