import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

import backend.commands as db
from backend import admin
from backend import strikechannel

class Unstrike(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.strike_channel_id = strikechannel


    @commands.command()
    @commands.has_role("Admin")
    async def unstrike(self, ctx):
        channel = self.bot.get_channel(self.strike_channel_id)

        mention = ctx.message.content.split()[1]
        guild = ctx.guild
        member = guild.get_member(int(mention[3:-1]))
        display_name = member.display_name

        count = 0
        async for m in channel.history(limit=None):
            count = 1
            msg = m

        if count == 0:
            text = f"{display_name} - 1"

            await channel.send(f"```\n{text}```")
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

        # Adding the strike
        if display_name in d:
            d[display_name] -= 1

        if d[display_name] == 0:
            del d[display_name]

        inner_text = ""
        for k, v in d.items():
            inner_text += f"{k} - {v}\n"


        full_text = f"```\n{inner_text}```"
        await msg.edit(content=full_text)

        db.elo_loss(display_name)



def setup(bot):
    bot.add_cog(Unstrike(bot))
