import asyncio
import re

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
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

        user_ids = [int(re.sub('[<@!>]', '', s)) for s in content[:self.player_count]]
        guild = ctx.message.guild

        # "line" represents original content except each tagged player
        # is replaced by their id
        line = []

        # "names" holds each player's display name
        names = []

        i = 0
        for word in content:
            print(word)
            tmp = re.sub('[<@!>]', '', word)
            if tmp.upper() not in ["C", "I"]:
                member = guild.get_member(int(tmp))
                line.append(guild.get_member(int(tmp)).id)
                if i < self.player_count:
                    names.append(guild.get_member(int(tmp)).display_name)
                    i += 1
            else:
                line.append(word)

        # List of the X players' ids
        player_ids = line[:self.player_count]

        # List of tuples (imps[List], did imps win[Bool])
        imps_wins = []

        # Data collection used for the embed

        # Populate imps_wins
        imps = []
        for word in line[self.player_count:]:
            if len(imps) < 2:
                imps.append(word)
            else:
                imps_wins.append((imps, word.upper() == "C"))
                imps = []

        # Calculating the actual games and ELO changes
        lst = [str(i) for i in player_ids]
        for t in imps_wins:
            lst2 = [str(i) for i in t[0]]
            db.add_game(lst, names, lst2, t[1])

        # Checking if a role change is needed for every player
        role_600 = get(ctx.message.guild.roles, name="600+")
        role_900 = get(ctx.message.guild.roles, name="900+")

        for id in player_ids:
            member = guild.get_member(int(id))

            elo_req = (db.get_elo(id) >= 600)
            has_role = (role_600 in member.roles)

            if elo_req and not has_role:
                await member.add_roles(role_600)
            if not elo_req and has_role:
                await member.remove_roles(role_600)

            elo_req = (db.get_elo(id) >= 900)
            has_role = (role_900 in member.roles)

            if elo_req and not has_role:
                await member.add_roles(role_900)
            if not elo_req and has_role:
                await member.remove_roles(role_900)

        # An embed is used for the output
        embed = Embed(
            title="Game Results",
            color=Color.from_rgb(0, 0, 0)
        )

        embed.add_field(
            name="Players",
            value=", ".join(names),
            inline=False
        )

        i = 1
        for t in imps_wins:
            # imps_wins stores the id's of the player, so imp_names is
            # used to get the display names of the players
            imp_names = [
                guild.get_member(t[0][0]).display_name,
                guild.get_member(t[0][1]).display_name
            ]
            imps = f"{imp_names[0]}, {imp_names[1]}"
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
