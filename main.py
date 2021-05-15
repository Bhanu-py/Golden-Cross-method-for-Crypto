# bot.py
import os
import Script
import keep_alive

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(help='Responds with a latency of the bot')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(name='cry', help='Returns crypto currency data')
async def cry(ctx, tick: str, s_a=5, l_a=20, period='9d', interval='90m'):
    Script.crypto(tick, s_a, l_a, period=period, interval=interval)
    file = discord.File('plot.png')
    form = discord.Embed(title='Live Report', colour=0xE91E63)
    form.add_field(name=f'{tick.upper()}-USD last {period} days and {interval} interval', value=f'{tick.upper()}-USD', inline=True)
    form.set_image(url="attachment://plot.png")
    await ctx.send(embed=form, file=file)

keep_alive.keep_alive()
bot.run(TOKEN, bot=True, reconnect=True)