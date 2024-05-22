import discord
from discord.ext import commands
import random
import asyncio
from colorama import init, Fore

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def login(self, ctx):

        """ m!login このコマンドでMemberのroleが自動ででき認証制にできます。"""
        answer = random.randint(10000000000, 99999999999)
        role = discord.utils.get(ctx.guild.roles, name="Member")

        if not role:
            role = await ctx.guild.create_role(name="Member")

        await role.edit(permissions=discord.Permissions(view_channel=True))

        # Send the password via DM
        # Send the password via DM
        await ctx.author.send(
        f"{ctx.author.mention}, 認証用パスワード: {answer}\n"
         "ここに送られて来た認証パスワードを送信してください"
        )


        embed = discord.Embed(
            title="認証用パスワードをDMに送信しました。",
            description=f"DMを確認して、パスワードを認証してください。",
            color=0xe4ff14
        )

        nope = discord.Embed(
            title="コマンドを再実行してください",
            description="Codeが一致しませんでした",
            color=0xe4ff14
        )

        auth_ok = discord.Embed(
            title="認証を完了しました。",
            description=f"{ctx.author.mention} に Member ロールを付与しました。",
            color=0xe4ff14
        )

        timeout = discord.Embed(
            title="コマンドを再実行してください",
            description="120秒以内に認証できませんでした。",
            color=0xe4ff14
        )

        def answer_check(m):
            return m.author == ctx.author and m.channel == ctx.author.dm_channel and m.content.isdigit()

        try:
            wait_resp = await self.bot.wait_for('message', timeout=120, check=answer_check)
        except asyncio.TimeoutError:
            await ctx.send(embed=timeout)
        else:
            if wait_resp.content == str(answer):
                await ctx.send(embed=auth_ok)
                await ctx.author.add_roles(role)  # ロールをユーザーに付与
            else:
                await ctx.send(embed=nope)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'login           [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()

async def setup(bot):
    await bot.add_cog(Login(bot))
