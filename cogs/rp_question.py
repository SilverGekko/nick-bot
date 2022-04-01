import random
from pony import orm
import discord
from discord.ext import commands


class RPQuestionCog(commands.Cog):
  def __init__(self, bot, db):
    '''constructor for the RPQuestionCog class'''

    self.bot = bot
    self.db = db

  @commands.command(name='rpq', help='Provide an RP Question')
  async def rp_question(self, context):
    ''''''

    with orm.db_session:
      user = self.db.User.find_or_create_by_name(str(context.author))

      questions = list(orm.select(rpq for rpq in self.db.RPQuestion if rpq not in user.rp_questions))

      if not questions:
        await self.send_error(context)
        return

      question = random.choice(questions)

      user.rp_questions.add(question)

    embed = discord.Embed(title=f"RP Question #{question.id}", description=str(context.author))
    embed.add_field(name="Prompt", value=question.prompt)

    await context.send(embed=embed)

  async def send_error(self, context):
    ''''''

    embed = discord.Embed(title="RP Question Error", description=str(context.author))
    embed.add_field(name="Error", value="No more questions available to this user")

    await context.send(embed=embed)

