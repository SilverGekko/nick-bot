import requests
from youtube_dl import YoutubeDL

YOUTUBE_DOWNLOAD_FORMAT = { 'format': 'bestaudio', 'noplaylist': 'True' }

def search(query):
  '''search youtube for a specified URL. If unsuccessful at finding the exact video,
  instead take the first suggested result.

  Params:
    query (str): user-submitted URL of a YouTube video
  '''

  with YoutubeDL(YOUTUBE_DOWNLOAD_FORMAT) as ytdl:
    try:
      requests.get(query)
    except:
      info = ytdl.extract_info(f'ytsearch:{query}', download=False)['entries'][0]
    else:
      info = ytdl.extract_info(query, download=False)

  return (info, info['formats'][0]['url'])
