import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

import backend.commands as db


class G(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def g(self, ctx):
        content = ctx.message.content.split()[1:]
        user_ids = [int(s[3:-1]) for s in content[:10]]
        # guild = self.bot.get_guild(510115905041203200)
        guild = ctx.message.guild

        line = []
        for word in content:
            print(word)
            if word.upper() not in ["C", "I"]:
                line.append(guild.get_member(int(word[3:-1])).nick)
            else:
                line.append(word)

        members = line[:10]

        imps_wins = [] # List of tuples (imps[List], did imps win[Bool])
        imps = []
        for word in line[10:]:
            if len(imps) < 2:
                imps.append(word)
            else:
                imps_wins.append((imps, word.upper() == "C"))
                imps = []

        print(members)
        print(imps_wins)

        for t in imps_wins:
            db.addGame(members, t[0], t[1])

        await ctx.channel.send("Done")



def setup(bot):
    bot.add_cog(G(bot))
