import os
import discord
from discord.ext import commands,tasks
import youtube_dl
import pyjokes as pyj
from random import choice
import urllib.request
import re
from keep_alive import keep_alive



client=commands.Bot(command_prefix='?',intents=discord.Intents. all())


youtube_dl.utils.bug_reports_message=lambda:''



status=['Jamming to music','Eating!','Sleeping zz...']

@client.event
async def on_ready():
    change_status.start()
    print('Musec is online :)')

@client.command(name='ping',help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'Latency = {round(client.latency*1000)}ms')

@client.command(name='heyloo',help='Returns a welcome message')
async def heyloo(ctx):
    responses=['Hey! Enjoy your music:)','Hope you have a good day :)','Enjoy your time here :)','Musec is here for great music:)']
    await ctx.send(choice(responses))

@client.command(name='joke',help='Tells you a joke')
async def joke(ctx):
    await ctx.send(pyj.get_joke('en','all'))


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))



@client.command(name='stop',help='Bot will leave the voice channel') 
async def disconnect(ctx):
  await ctx.send('⏹')
  await ctx.voice_client.disconnect()

@client.command(name='play',help='Bot will play music')
async def play(ctx,query):
  print(query)
  if ctx.author.voice is None:
    await ctx.send('You are not in a voice channel :(')
  voice_channel=ctx.author.voice.channel
  if ctx.voice_client is None:
    await voice_channel.connect()
  if query == '':
    await ctx.send('No song requests :(')
  else:
    await ctx.send('⏸️')
    await ctx.voice_client.move_to(voice_channel)
    ctx.voice_client.stop()
    s_url='https://www.youtube.com/results?search_query='+query
    html=urllib.request.urlopen(s_url)
    v_id=re.findall(r"watch\?v=(\S{11})",html.read().decode())
    url="https://www.youtube.com/watch?v="+v_id[0]
    print(url)
    ytdl_format_options={
      'format':'bestaudio/best',
      'outtmpl':'%(extractor)s-%(id)s-%(title)s.%(ext)s',
      'restrictfilenames':True,
      'noplaylist':True,
      'nocheckcertificate':True,
      'ignoreerrors':False,
      'logtostderr':False,
      'quiet':True,
      'no_warnings':True,
      'default_search':'auto',
      'source_address':'0.0.0.0'
    }

    ffmpeg_options={
      'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options':'-vn'
    }
    vc=ctx.voice_client
          
    with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
      info=ydl.extract_info(url,download=False)
      url2=info['formats'][0]['url']
      source=await discord.FFmpegOpusAudio.from_probe(url2,**ffmpeg_options)
      vc.play(source) 
    

@client.command(name='pause',help='Pauses music')
async def pause(ctx):
  await ctx.send('Paused ⏸️')
  await ctx.voice_client.pause()
  

@client.command(name='resume',help='Resumes music')
async def pause(ctx):
  await ctx.send('Resumed ▶️')
  await ctx.voice_client.resume()
  
@client.command(name='info',help='How to use musec...')
async def info(ctx):
  await ctx.send('- Join a voice channel before using ?play \n- ?play should be followed by a song request\n- Requests that include space should be joined using _\n\t E.g. ?play lauv_modern_loneliness')

keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)

