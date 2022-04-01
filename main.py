import os
from dotenv import load_dotenv
from discord.ext import commands

from pony import orm

from database import db, loader
from cogs.youtube import YoutubeCog
from cogs.rp_question import RPQuestionCog

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('DISCORD_GUILD')
PREFIX='-nb '

if __name__ == "__main__":
  loader.load_resources(resource_dir='rp_questions', table="RPQuestion")

  bot = commands.Bot(command_prefix=PREFIX)
  bot.add_cog(YoutubeCog(bot))
  bot.add_cog(RPQuestionCog(bot, db))
  bot.run(TOKEN)
