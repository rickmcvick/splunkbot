# cmd_error_handling.py

import os
import discord
from discord.ext import commands
import re
import feedparser

class bot_commands(commands.Cog):
    """Commands involving examples."""

    def __init__(self, bot, *args, **kwargs):
        self.bot = breakpoint

    @commands.command(description='Displays the most current version of Splunk', 
                      help = 'Be sure to always use \'.\' before using bot commands!'
                      )
                      
    async def version(self, ctx):
        d = feedparser.parse('https://www.splunk.com/page/release_rss')
        version_list = []
        for entry in d['entries']:
            feed = entry['title']
            reg_version = re.search('(\d+\.)?(\d+\.)?(\d+\.)?(\*|\d+)', feed)
            version_string = reg_version.group()
            version_split = version_string.split('.')
            version_list.append(version_split)
            max_version = max(version_list)
            splunk_version = version_list.index(max_version)
        
        print_version = d['entries'][splunk_version]['title']
        link = d['entries'][splunk_version]['link']
        pub_date = d['entries'][splunk_version]['published']
        embed=discord.Embed(title='Current Splunk Version', 
                            colour=discord.Colour.green())
        embed.add_field(name=print_version, value=link)
        embed.add_field(name='Published On:', value=pub_date, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(bot_commands(bot))
    print('Version Loaded')