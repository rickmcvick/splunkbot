import discord
from discord.ext import commands
from datetime import datetime

class NewHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()

        for page in self.paginator.pages:
            embed = discord.Embed(
                title='Help',
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow(),
                description=page
            )

            await destination.send(embed=embed)