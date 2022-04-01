import time

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands

from helpers.youtube import search

FFMPEG_OPTS = {
  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}

class YoutubeCog(commands.Cog):
  def __init__(self, bot):
    '''constructor for YoutubeCog class
    Params:
        bot ():
    '''

    self.bot = bot

    self.voice = None
    self.player = None

  @staticmethod
  async def join(context):
    channel = context.author.voice.channel
    return await channel.connect()

  @commands.command(name='play', help='Play a YouTube URL')
  async def play(self, context, search_string):
    '''play the selected resource from youtube to the discord channel
    of the calling user. handle when something is already playing by
    stopping it and starting the newly specified song.

    Params:
      context (discord.ext.commands.context.Context)
      search_string (str): user input search param
    '''
    _, source = search(search_string)

    if self.voice_connected():
      self.voice.stop()
      self.play_source(source)

      return

    try:
      self.voice = await self.join(context)
    except discord.errors.ClientException:
      print('Unable to join channel')
      return

    await context.send(f'Now playing {search_string}.')

    while True:
      try:
        self.play_source(source)
        break
      except discord.errors.ClientException:
        time.sleep(3)
        self.voice = await self.join(context)

  @commands.command(name="stop", help="Stop the current song.")
  async def stop(self, context):
    '''Stop the current song, there is no queue- all is lost

    Params:
      context (discord.ext.commands.context.Context)
    '''

    if self.voice_connected():
      self.voice.stop()

  @commands.command(name="pause", help="Pause the current song, or play the currently paused song.")
  async def pause(self, context):
    '''Pause the current song, or play the currently paused song

    Params:
      context (discord.ext.commands.context.Context)
    '''

    if self.voice_connected():
      if self.voice.is_paused():
        self.voice.resume()
      else:
        self.voice.pause()

  @commands.command(name="dc", help="Disconnect the bot from its currently joined channel.")
  async def dc(self, context):
    '''Disconnect the bot from its currently joined channel

    Params:
      context (discord.ext.commands.context.Context)
    '''

    if self.voice_connected:
      await self.voice.disconnect()

  def play_source(self, source):
    '''play the specified audio source (URL) to the connected voice channel

    Params:
      source (str): URL derived from youtube search of user input
    '''

    self.player = self.voice.play(
      FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e)
    )

  def voice_connected(self):
    '''check if the bot is currently voice connected'''

    return self.voice and self.voice.is_connected()
