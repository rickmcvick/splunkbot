# search.py

import aiohttp
import asyncio
import discord
from discord.ext import commands


class bot_commands(commands.Cog):
    """Commands involving examples."""

    def __init__(self, bot, *args, **kwargs):
        self.bot = breakpoint

    @commands.command(description='Allows the search of Go Splunk. Format for querey \'.gosplunk search_term\'', 
                      help = 'Be sure to always use \'.\' before using bot commands!'
                      )
                      
    async def gosplunk(self, ctx, *, message):
        search_term = message.replace(' ', '+')
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://gosplunk.com/wp-json/relevanssi/v1/search?s={search_term}&posts_per_page=5') as response:
                search_result = await response.json()
        count = len(search_result)

        no_results_key = 'code'

        if no_results_key in search_result:
            embed=discord.Embed(title=f'No Results For: ***{message}.***', 
                    colour=discord.Colour.red())
            embed.add_field(name='No Results Found', value='Please Try Again', inline=False)
        else:
            embed=discord.Embed(title=f'Top {count} Search Results For: ***{message}.***', 
                    colour=discord.Colour.green())
            for entry in search_result:
                embed.add_field(name=entry['title']['rendered'], value=entry['link'], inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(bot_commands(bot))
    print('Search Loaded')