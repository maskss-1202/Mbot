from config import settings  # config.pyから設定をインポート

import discord
from discord import app_commands
from discord.ext import commands
from colorama import init, Fore

class SModeration(commands.Cog):
    """モデレーション"""

    def __init__(self, bot):
        self.bot = bot

    # clearコマンド: チャンネル内のメッセージを一括で削除
    @app_commands.command(name="clear", description="複数のメッセージをクリアします")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(amount="削除するメッセージの数",
                           member="削除するメッセージのユーザー")
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 500], member: discord.Member = None):
        channel = interaction.channel

        def check_(m):
            return m.author == member

        if not member:
            await channel.purge(limit=amount)
        else:
            await channel.purge(limit=amount, check=check_)
        await interaction.response.send_message(f"{self.bot.get_emoji(settings['emojis']['squid_cleaning'])} {amount}件のメッセージを削除しました")

    # kickコマンド: メンバーをキック
    @app_commands.command(name="kick", description="特定のメンバーをキックします")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction,
                   member: discord.Member, reason: str = "指定なし"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member}をキックしました。理由: {reason}")

    # banコマンド: メンバーをバン
    @app_commands.command(name="ban", description="特定のメンバーをバンします")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction,
                  member: discord.Member, reason: str = "指定なし"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member}をバンしました。理由: {reason}")


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'slash/moderetion[{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()


# CogをBotに追加するための関数
async def setup(bot):
    await bot.add_cog(SModeration(bot))
