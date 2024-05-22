import discord
from discord.ext import commands, tasks
import asyncio

class CooldownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_cooldowns = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        command = message.content.lower()

        # ユーザーごとにクールダウン情報を初期化
        if user_id not in self.user_cooldowns:
            self.user_cooldowns[user_id] = {"count": 0, "cooldown": False}

        # コマンド/発言ごとのカウントを増やす
        self.user_cooldowns[user_id]["count"] += 1

        # カウントが10回以上かつクールダウン中でない場合
        if self.user_cooldowns[user_id]["count"] >= 10 and not self.user_cooldowns[user_id]["cooldown"]:
            self.user_cooldowns[user_id]["cooldown"] = True

            # ミュートロールを取得し、ユーザーに付与
            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if mute_role is not None:
                await message.author.add_roles(mute_role)

            await message.channel.send(f"{message.author.mention} を一時的にチャット制限をしてください。")

            # 5分間の待機時間後にミュートロールを削除
            await asyncio.sleep(300)

            # ミュートロールを削除し、クールダウン情報をリセット
            await message.author.remove_roles(mute_role)
            self.user_cooldowns[user_id]["count"] = 0
            self.user_cooldowns[user_id]["cooldown"] = False


async def setup(client:commands.Bot):
    await client.add_cog(CooldownCog(client))