import discord
from discord.ext import commands
from colorama import init, Fore

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(name='ping', description='ping!')
    async def ping(self, interaction:discord.Interaction):
        raw_pingspeed = self.client.latency
        pingspeed = round(raw_pingspeed * 1000)
        await interaction.response.send_message(f'pong! {pingspeed}ms', ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'ping            [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()

async def setup(client:commands.Bot):
    await client.add_cog(ping(client))