import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

from backend import admin
from backend import strikechannel


# This command should be run at the start of every season. This is a
# running list of everything it does (updated as code updates):
#
# > Removes one strike from every player
class Newseason(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.strike_channel_id = strikechannel


    @commands.command()
    @commands.has_role(admin)
    async def newseason(self, ctx):
        channel = self.bot.get_channel(self.strike_channel_id)

        guild = ctx.guild

        count = 0
        async for m in channel.history(limit=None):
            count = 1
            msg = m

        if count == 0:
            return

        text = msg.content.replace("```", "")
        text_lst = text.split("\n")

        d = {}
        for line in text_lst:
            try:
                name, strikes = line.rsplit(" - ", 1)
            except:
                continue
            d[name] = int(strikes)

        # Removes 1 strike from every player, and completely removes
        # their name from the list if they're at 0 strikes
        for k in list(d.keys()).copy():
            d[k] -= 1
            if d[k] == 0:
                del d[k]


        inner_text = ""
        for k, v in d.items():
            inner_text += f"{k} - {v}\n"


        full_text = f"```\n{inner_text}```"
        await msg.edit(content=full_text)



def setup(bot):
    bot.add_cog(Newseason(bot))
