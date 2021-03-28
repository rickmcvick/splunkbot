# protoSplunkBot.py

import os
import random
import traceback
import sys
from dotenv import load_dotenv
import feedparser
import discord
from discord.ext import commands, tasks
from HelpCommand import NewHelpCommand
import re

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents, help_command=NewHelpCommand())

initial_extensions = [
    'cogs.cmd_error_handling',
    'cogs.version',
    'cogs.search'
]

d = feedparser.parse('https://www.splunk.com/page/release_rss')

version_alert = False

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()

@tasks.loop(hours=1)
async def loops():
    d = feedparser.parse('https://www.splunk.com/page/release_rss')
    version_list = []
    guild = discord.utils.get(bot.guilds, name=GUILD)
    general = guild.get_channel(807662519811702874)
    global version_alert
    for entry in d['entries']:
        feed = entry['title']
        reg_version = re.search('(\d+\.)?(\d+\.)?(\d+\.)?(\*|\d+)', feed)
        version_string = reg_version.group()
        version_split = version_string.split('.')
        version_list.append(version_split)
        max_version = max(version_list)
        splunk_version = version_list.index(max_version)
        version_alert = max_version
    
    print_version = d['entries'][splunk_version]['title']
    link = d['entries'][splunk_version]['link']
    pub_date = d['entries'][splunk_version]['published']
    embed=discord.Embed(title='Current Splunk Version', 
                        colour=discord.Colour.green())
    embed.add_field(name=print_version, value=link)
    embed.add_field(name='Published On:', value=pub_date, inline=False)
    if version_alert != max_version:
        await general.send(embed=embed)
        version_alert = max_version

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='your sweet SaaS'))
    print(f'{bot.user.name} has connected to Discord!')
    loops.start()

bot.run(TOKEN)