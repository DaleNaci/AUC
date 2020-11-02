import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed


# This command is used for banning maps.
#
# !maps
#
# This brings up a list of the maps paired with a reaction. Players
# can use these reactions to vote on the map to ban.
class Maps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def maps(self, ctx):
        embed = Embed(
            title="Map Bans",
            color=Color.from_rgb(0, 0, 0)
        )

        # The numbers are used for the map picker
        text = """
        :green_circle: **The Skeld** (1)
        :blue_circle: **Mira HQ** (2)
        :red_circle: **Polus** (3)
        """

        embed.add_field(
            name="VOTE",
            value=text
        )


        msg = await ctx.send(embed=embed)

        reactions = [
            "🟢",
            "🔵",
            "🔴"
        ]

        for r in reactions:
            await msg.add_reaction(r)



def setup(bot):
    bot.add_cog(Maps(bot))
