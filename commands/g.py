import asyncio
import re

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

import backend.commands as db
from backend import mod


class G(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_role(mod)
    async def g(self, ctx):
        content = ctx.message.content
        content = re.sub(" +", " ", content)
        content = content.split()[1:]

        user_ids = [int(s[3:-1]) for s in content[:10]]
        guild = ctx.message.guild

        line = []
        for word in content:
            print(word)
            tmp = re.sub('[<@!>]', '', word)
            if tmp.upper() not in ["C", "I"]:
                member = guild.get_member(int(tmp))
                line.append(guild.get_member(int(tmp)).display_name)
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

        for t in imps_wins:
            db.add_game(members, t[0], t[1])

        embed = Embed(
            title="Game Results",
            color=Color.from_rgb(0, 0, 0)
        )

        embed.add_field(
            name="Players",
            value=", ".join(members),
            inline=False
        )

        i = 1
        for t in imps_wins:
            imps = f"{t[0][0]}, {t[0][1]}"
            if t[1]:
                text = "CREWMATES WIN"
            else:
                text = "IMPOSTORS WIN"

            embed.add_field(
                name=f"Game {i}",
                value=f"Imps: {imps}\n`{text}`",
                inline=False
            )
            i += 1

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(G(bot))
