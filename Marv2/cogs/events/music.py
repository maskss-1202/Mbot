import discord
from discord.ext import commands
from colorama import init, Fore


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def deleted(self, ctx, cmd_name: str):
        await ctx.send(f"このコマンドはもう使用できません。代わりに `{cmd_name}` を使用してください。")

    @commands.command()
    async def play(self, ctx):
        """YouTubeから曲を再生するか、現在再生中の曲があればリストに追加します。
        このコマンドはもう使用できません。代わりに /play を使用してください。"""
        await self.deleted(ctx, "/play")

    @commands.command()
    async def skip(self, ctx):
        """現在の曲をスキップします。
        このコマンドはもう使用できません。代わりに /skip を使用してください。"""
        await self.deleted(ctx, "/skip")

    @commands.command(name="queue")
    async def queue_embed(self, ctx):
        """次に再生する曲のリストを表示します。
        このコマンドはもう使用できません。代わりに /queue を使用してください。"""
        await self.deleted(ctx, "/queue")

    @commands.command()
    async def leave(self, ctx):
        """ボットをボイスチャンネルから切断します。
        このコマンドはもう使用できません。代わりに /leave を使用してください。"""
        await self.deleted(ctx, "/leave")

    @commands.command()
    async def stop(self, ctx):
        """現在の曲を停止し、再生リストをクリアします。
        このコマンドはもう使用できません。代わりに /stop を使用してください。"""
        await self.deleted(ctx, "/stop")

    @commands.command()
    async def pause(self, ctx):
        """曲を一時停止します。
        このコマンドはもう使用できません。代わりに /switch_pause を使用してください。"""
        await self.deleted(ctx, "/switch_pause")

    @commands.command()
    async def resume(self, ctx):
        """一時停止した曲を再開します。
        このコマンドはもう使用できません。代わりに /switch_pause を使用してください。"""

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'musicc          [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()

async def setup(bot):
    await bot.add_cog(Music(bot))
