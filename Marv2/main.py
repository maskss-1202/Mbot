import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from colorama import init, Fore
from banner import print_banner 

load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="m!", intents=intents)

@bot.event
async def on_ready():
    print_banner()
    print(bot.user.name)
    print(bot.user.id) 
    print(discord.__version__)
    print('--------------')

    await bot.change_presence(activity=discord.Activity(name=f"m!help | {len(bot.guilds)} server", type=discord.ActivityType.watching))

async def load_extension(type):
    cogs = os.listdir(f'./cogs/{type}/')
    for cog in cogs:
        if cog[0:2] != '__' and cog[-3:] == '.py' and os.path.getsize(f'./cogs/{type}/{cog}') != 0:
            cog = cog.replace('.py', '')
            try:
                await bot.load_extension(f'cogs.{type}.{cog}')  # await を追加
            except Exception as e:
                print(f"拡張機能 {cog} の読み込みに失敗しました: {e}")


async def main():
    await load_extension('commands')
    await load_extension('events')
    await load_extension('slash')

    await bot.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())