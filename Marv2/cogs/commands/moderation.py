import discord
from discord.ext import commands
from discord.errors import NotFound
from discord.ext.commands import has_permissions, CommandInvokeError, MissingPermissions
from colorama import init, Fore

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason='指定なし'):
        """m!kick or / 指定されたメンバーをキックします。"""
        await member.kick(reason=reason)
        await ctx.send(f"メンバー {member} を理由: {reason} でキックしました。")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send(
                '❌ ボットにキックの権限がありません！ボットをサーバーから削除し、次のリンクから再度追加してください：https://discord.com/api/oauth2/authorize?client_id=1130867219195240538&permissions=8&scope=bot')
            raise error

    @has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason='指定なし'):
        """m!ban or / 指定されたメンバーをBANします。"""
        await member.ban(reason=reason)
        await ctx.send(f"メンバー {member} を理由: {reason} でBANしました。")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send(
                '❌ ボットにBANの権限がありません！ボットをサーバーから削除し、次のリンクから再度追加してください：https://discord.com/api/oauth2/authorize?client_id=1130867219195240538&permissions=8&scope=bot')

    @has_permissions(manage_messages=True)
    @commands.command()
    async def idclear(self, ctx, message):
        """m!idclear or / メッセージIDでメッセージを削除します。"""
        await ctx.message.delete()
        try:
            msg = await ctx.channel.fetch_message(message)
            await msg.delete()
        except NotFound as e:
            await ctx.send(
                '❌ 正しいメッセージIDを入力してください！メッセージIDをコピーするには、ユーザー設定>詳細に移動し、開発者モードを有効にしてください。それからメッセージIDをコピーできます。')

    @idclear.error
    async def idclear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(
                '❌ 申し訳ありませんが、このコマンドにアクセスするための権限がありません。コマンドを実行するには「メッセージの管理」権限が必要です。')
        elif isinstance(error, CommandInvokeError):
            await ctx.send(
                '❌ ボットにメッセージの管理権限がありません！ボットをサーバーから削除し、次のリンクから再度追加してください：https://discord.com/api/oauth2/authorize?client_id=1130867219195240538&permissions=8&scope=bot')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'modereation     [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()

async def setup(bot):
    await bot.add_cog(Moderation(bot))
