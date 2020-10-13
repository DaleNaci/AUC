import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

import backend.commands as db


class Strike(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.strike_channel_id = 764131932707487754
        self.strike_channel_id = 763981972883636225


    @commands.command()
    @commands.has_role("Administrator")
    async def strike(self, ctx):
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
            d[display_name] += 1
        else:
            d[display_name] = 1

        inner_text = ""
        for k, v in d.items():
            inner_text += f"{k} - {v}\n"


        full_text = f"```\n{inner_text}```"
        await msg.edit(content=full_text)

        db.eloLoss(display_name)



def setup(bot):
    bot.add_cog(Strike(bot))
