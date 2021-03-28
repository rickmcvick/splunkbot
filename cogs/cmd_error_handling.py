# cmd_error_handling.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

class fun_things(commands.Cog):
    """Commands involving examples."""

    def __init__(self, bot, *args, **kwargs):
        self.bot = breakpoint

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        author = ctx.author
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{author.mention} command 404. Please use `.help` for list of commands')

def setup(bot):
    bot.add_cog(fun_things(bot))
    print('Handling Loaded')