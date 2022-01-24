import os
import webbrowser
from asyncio import sleep
# import validators
from urllib.parse import urlparse
import discord
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

PREFIX = "-nb "

# client = discord.Client()
bot = commands.Bot(command_prefix=PREFIX)
voice = None
player = None

def search(query):
  with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ytdl:
    try: requests.get(query)
    except: info = ytdl.extract_info(f'ytsearch:{query}', download=False)['entries'][0]
    else: info = ytdl.extract_info(query, download=False)
  return (info, info['formats'][0]['url'])

# def is_connected(context):
#   voice_client = discord.get(context.bot.voice_clients, guild=context.guild)
#   return voice_client and voice_client.is_connected()

async def join(context):
  channel = context.author.voice.channel
  return await channel.connect() 

@bot.command(name="play", help="Play a youtube URL.")
async def play(context, arg):
  global player
  global voice
  # response = f'You enetered {context.message.content}.'
  FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  video, source = search(arg)
  print("bot.voice_clients", bot.voice_clients)
  print("context.guild", context.guild)
  # if not voice:
    # voice = discord.utils.get(context.bot.voice_clients, guild=GUILD)
  # voice = discord.utils.get(bot.guilds, name=GUILD)
  # user = context.message.author
  # voice = user.voice.channel

  if voice and voice.is_connected():
    if voice.is_playing():
      voice.stop()
    player = voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
  else:
    try:
      voice = await join(context)
    except discord.errors.ClientException:
      pass
    if voice.is_playing():
      voice.stop()
    await context.send(f'Now playing {arg}.')
    playing = False
    while not playing:
      try:
        player = voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
        playing = True
      except discord.errors.ClientException:
        voice = await join(context)

  # while (voice.is_playing()):
  #   await sleep(1)
  # await voice.disconnect()
  # if not voice.is_connected():
  #   voice = None

  # response = f'You entered {arg}.'
  # domain = urlparse(arg).netloc.split('.')[1]
  # # domain = domain
  # if domain == "youtube":
  #   response += " That is a valid URL."
  #   user = context.message.author
  #   voice_channel = user.voice.channel
  #   channel=None
  #   if voice_channel:
  #     channel = voice_channel
  #     await channel.connect()
  #   webbrowser.get("firefox").open(arg)
  # else:
  #   response += " Invalid URL location."

  # await context.send(response)

# @bot.command(name="volume", help="Change the volume.")
# async def volume(context, arg):
#   global player
#   print("volume called with", int(arg) / 100)
#   print("voice", voice)
#   print("voice.is_playing()", voice.is_playing())
#   print("player", player)
#   if voice and voice.is_playing():
#     if player:
#       print("setting volume to", int(arg) / 100)
#       player.volume = int(arg) / 100
    

@bot.command(name="stop", help="Stop the current song. There is no queue; position will be lost.")
async def stop(context):
  if voice and voice.is_playing():
    voice.stop()

@bot.command(name="pause", help="Pause the current song, or play the currently paused song.")
async def pause(context):
  if voice:
    if voice.is_paused():
      voice.resume()
    else:
      voice.pause()

@bot.command(name="dc", help="Disconnect the bot from its currently joined channel.")
async def dc(context):
  if voice:
    await voice.disconnect()
  # if is_connected(context):
  #   voice_client = discord.get(context.bot.voice_clients, guild=context.guild)
  #   voice_client.disconnect()


# @bot.event
# async def on_ready():
#   # for guild in client.guilds:
#   #   if guild.name == GUILD:
#   #     break
#   # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
#   guild = discord.utils.get(client.guilds, name=GUILD)
#   print(f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})')

#   members = '\n - '.join([member.name for member in guild.members])
#   print(f'Guild Members:\n - {members}')

# @bot.event
# async def on_member_join(member):
#   await member.create_dm()
#   await member.dm_channel.send(
#     f'Welcome, {member.name}.'
#   )

# @bot.event
# async def on_message(message):
#   if message.author == client.user:
#     return

#   if message.content.startswith("-nb"):
#     response = "Command implementation pending."
#     await message.channel.send(response)
#   elif message.content == 'raise-exception':
#     raise discord.DiscordException

# @bot.event
# async def on_error(event, *args, **kwards):
#   with open('err.log', 'a') as f:
#     if event == "on_message":
#       f.write(f'Unhandled message: {args[0]}\n')
#     else:
#       raise

if __name__ == "__main__":
  bot.run(TOKEN)