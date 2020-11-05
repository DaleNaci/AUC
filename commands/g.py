import asyncio
import re

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

import backend.commands as db
from backend import mod


# This command is used to score games.
#
# !g [tag X players] ([tag two imps] ['I' or 'C'])
#
# X is the number of players in a game.
# The first ten tagged players are the X players in the game.
# The text in the parenthesis tag the 2 imps and then the team that won
# each game, and can extend for as many games as needed.
class G(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_count = 10


    @commands.command()
    @commands.has_role(mod)
    async def g(self, ctx):
        # Splitting content into a list of each word
        content = ctx.message.content
        content = re.sub(" +", " ", content)
        content = content.split()[1:]

        user_ids = [int(s[3:-1]) for s in content[:self.player_count]]
        guild = ctx.message.guild

        # "line" represents original content except each tagged player
        # is replaced by their display name
        line = []
        names = []
        for word in content:
            print(word)
            tmp = re.sub('[<@!>]', '', word)
            if tmp.upper() not in ["C", "I"]:
                member = guild.get_member(int(tmp))
                names.append(guild.get_member(int(tmp)).display_name)
                line.append(guild.get_member(int(tmp)).id)
            else:
                line.append(word)

        # List of the X players
        members = line[:self.player_count]

        # List of tuples (imps[List], did imps win[Bool])
        imps_wins = []

        # Populate imps_wins
        imps = []
        for word in line[self.player_count:]:
            if len(imps) < 2:
                imps.append(word)
            else:
                imps_wins.append((imps, word.upper() == "C"))
                imps = []

        for t in imps_wins:
            db.add_game(members, names, t[0], t[1])

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
