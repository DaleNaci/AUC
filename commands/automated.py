import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed

from backend.game_database import GameDatabase
import backend.commands as db


class Automated(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_count = 10
        self.required_checks = 8 # Not including bot
        self.required_x = 5 # Not including bot
        self.game_db = GameDatabase()


    # Print out error as embed
    async def __show_error(self, ctx, error_message):
        embed = Embed(
            title="Error!",
            color=Color.red(),
            description=error_message
        )
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg_id = reaction.message.id

        # Check if message is a pending game
        if not msg_id in self.game_db.pending:
            return

        # Get game id and list of players in the game
        game_id = self.game_db.pending[msg_id]
        player_ids = self.game_db.games[game_id]

        # Remove reaction if user isn't in the game
        if not user.id in player_ids and not user.bot:
            await reaction.message.remove_reaction(reaction.emoji, user)

        # Score game if self.required_reactions threshold is met
        all_reactions = reaction.message.reactions

        if self.required_checks+1 == all_reactions[0].count \
                or self.required_x+1 == all_reactions[1].count:

            # Title variable is for embed
            title = "Game Results Canceled!"
            color = Color.red()
            if all_reactions[0].count == self.required_checks+1:
                title = "Game Results Submitted!"
                color = Color.green()

            # Get info from old embed
            old_embed = reaction.message.embeds[0]

            # Edit embed message
            embed = Embed(
                title=title,
                color=color,
                description=old_embed.description
            )

            for field in old_embed.fields:
                embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=True
                )

            await reaction.message.edit(embed=embed)

            # Don't score game if it's canceled
            if self.required_x+1 == all_reactions[1].count:
                self.game_db.reverse_pending(game_id)
                return

            # Remove game from pending games
            self.game_db.remove_pending_game(game_id)

            # To make a call to the scoring database, we need to fill
            # 4 parameters:
            # - [List] of ID's of all players
            # - [List] of display names of all players
            # - [List] of ID's of all impostors
            # - [Boolean] that represents whether crew won or not
            imp_ids, did_imps_win = self.game_db.imps[game_id]

            player_names = []
            for id in player_ids:
                player_names.append(
                    reaction.message.guild.get_member(id).display_name
                )

            # Add game to database
            player_ids = [str(i) for i in player_ids]
            imp_ids = [str(i) for i in imp_ids[0]]
            db.add_game(player_ids, player_names, imp_ids, not did_imps_win)



    @commands.command()
    async def start(self, ctx):
        # Find VC of player who typed command
        member = ctx.author
        voice_state = member.voice

        # Error if not in a VC
        if voice_state is None:
            await self.__show_error(ctx, "You are not in a voice channel!")
            return

        # Get list of all 10 ID's
        voice_channel = voice_state.channel
        member_ids = list(voice_channel.voice_states.keys())


        # Error if VC does not have self.player_count players
        if len(member_ids) != self.player_count:
            error_message = "There are not enough people in your voice channel!"
            await self.__show_error(ctx, error_message)
            return

        # Store in database
        self.game_db.add_game(member_ids)

        # Send embed listing all ids as mentions
        players_str = ""

        number = 1
        for id in member_ids:
            players_str += f"{number}. <@{id}>\n"
            number += 1

        embed = Embed(
            title="Game Setup",
            color=Color.blue(),
        )

        embed.add_field(
            name="Players",
            value=players_str,
            inline=True
        )

        scoring_help = "Type `!score # # [I/C]`.\n\
                        The # refers to the imp's\n\
                        place on the list."
        embed.add_field(
            name="When finished...",
            value=scoring_help,
            inline=True
        )

        embed.set_footer(text=f"Game ID: {self.game_db.game_number-1}")

        await ctx.send(embed=embed)


    @commands.command()
    async def score(self, ctx):
        # Get message
        content = ctx.message.content.split()[1:]

        # Error if format is incorrect
        if len(content) != 3:
            await self.__show_error(ctx, "Incorrect format!")
            return

        valid_nums = [str(i) for i in range(1, 11)]
        format_checks = [
            content[0] in valid_nums, # Imps are valid numbers
            content[1] in valid_nums, # Imps are valid numbers
            content[2].upper() in ["I", "C"], # Valid game winner
            content[0] != content[1] # Imps are not the same
        ]

        if not all(format_checks):
            await self.__show_error(ctx, "Incorrect format!")
            return

        # Find game with author
        try:
            author_id = ctx.author.id
            player_ids = self.game_db.get_game(author_id)
            game_id = self.game_db.get_game_id(author_id)
        except:
            # Error if no game found
            await self.__show_error(ctx, "You are not in a game!")
            return

        # Check if game is already being scored
        if self.game_db.is_game_pending(game_id):
            await self.__show_error(ctx, "Game is already being scored!")
            return

        # Description of embed will be based on winner
        if content[2].upper() == "I":
            winner_str = "`Impostors Win!`"
        else:
            winner_str = "`Crewmates Win!`"


        # Print out game and wait for 6 reactions
        embed = Embed(
            title="Pending Game Results!",
            description=winner_str,
            color=Color.blue()
        )

        # crew_str = "1. Dale\n2. Peter\n 3. Steve"
        # crew_counter = 1
        # imp_str = "1. John\n2. David"
        # imp_counter = 1
        crew_str = imp_str = ""
        crew_counter = imp_counter = 1
        for i in range(len(player_ids)):
            if i+1 != int(content[0]) and i+1 != int(content[1]):
                crew_str += f"{crew_counter}. <@{player_ids[i]}>\n"
                crew_counter += 1
            else:
                imp_str += f"{imp_counter}. <@{player_ids[i]}>\n"
                imp_counter += 1


        embed.add_field(
            name="Crewmates",
            value=crew_str,
            inline=True
        )
        embed.add_field(
            name="Impostors",
            value=imp_str,
            inline=True
        )

        embed.set_footer(text=f"{self.required_checks} reactions required.")

        pending_msg = await ctx.send(embed=embed)

        # React to the message with the check and X Emoji
        await pending_msg.add_reaction("\U00002705")
        await pending_msg.add_reaction("\U0000274C")

        # Give embed message id to game database
        imp_ids = [player_ids[int(content[0])-1], player_ids[int(content[1])-1]]
        self.game_db.add_pending_game(
            pending_msg.id,
            game_id,
            [imp_ids],
            content[2].upper() == "C"
        )


    # @commands.command()
    # async def void(self, ctx):
    #     desc = "Void"
    #
    #     embed = Embed(
    #         title="Void",
    #         color=Color.dark_gray(),
    #         description=desc
    #     )
    #
    #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Automated(bot))
