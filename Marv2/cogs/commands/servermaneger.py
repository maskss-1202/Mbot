import discord, os
import random
import string
from discord.ext import commands
from discord.utils import get
#from googletrans import Translator
from dotenv import load_dotenv
from colorama import init, Fore

class servermaneger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('ようこそ！ {0.mention}.'.format(member))

    @commands.command(name='hello', aliases=['hi', 'hey'])
    async def hello(self, ctx, *, member: discord.Member = None):
        """挨拶してくれます。"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member



#discordmyID
    @commands.command() #executes when user types '$myid'
    async def myid(self, ctx):  
        """m!myid 自分のIDの確認ができます。"""      
        embed=discord.Embed(title=f"ユーザープロフィール **{ctx.author}** ({ctx.author.display_name})", description=f"A summary of {ctx.author.display_name}'s profile.", color=ctx.author.accent_color)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.add_field(name="UID", value=ctx.author.id)
        embed.add_field(name="Date Created", value=ctx.author.created_at)
        await ctx.reply(embed=embed)
        print(__name__)



#passwordmaneger
    @commands.command(name='pass', description='Generate a random password.')
    async def generate_password(self, ctx, length: int = 10):
        """m!pass 数字でランダムにパスワードを作ってくれます。"""
        # パスワードの生成
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(password_characters) for i in range(length))

        # 個人のチャットにメッセージを送信
        await ctx.author.send(f'生成したパスワード: {password}')
        await ctx.send('個人チャットに送信しました。')        



#メッセージ一括削除
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def allclear(self, ctx, amount: int):
        """チャットをすべて削除します。"""
        try:
            # 指定された数のメッセージを削除
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"{amount}件のメッセージを削除しました。", delete_after=5)
        except commands.CheckFailure:
            await ctx.send("権限がありません。このコマンドを実行するためには `manage_messages` 権限が必要です。")

#翻訳



    @commands.Cog.listener()
    async def on_ready(self):
        print('pass起動')
        await self.client.tree.sync()  

    @commands.Cog.listener()
    async def on_ready(self):
        print('welc起動完了')
        await self.client.tree.sync()     

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'ID              [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()   

async def setup(bot):
    await bot.add_cog(servermaneger(bot))

