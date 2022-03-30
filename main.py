import os
from dotenv import load_dotenv

from discord.ext import commands

from bot import YoutubeCog

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('DISCORD_GUILD')
PREFIX='-nb '

if __name__ == "__main__":
  bot = commands.Bot(command_prefix=PREFIX)
  bot.add_cog(YoutubeCog(bot))
  bot.run(TOKEN)
