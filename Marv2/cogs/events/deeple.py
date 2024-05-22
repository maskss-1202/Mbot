import discord
from discord.ext import commands
import requests
from langdetect import detect
import os
from colorama import init, Fore

class language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DeepL_Token = "f68f4bae-4228-1fe4-25e6-668076a4a1d3:fx"
        self.DeepL_API_URL = "https://api-free.deepl.com/v2/translate"
        self.Translation_Channel_Name = "和訳"

    def language(self, text):
        lang = detect(text)
        return lang

    @commands.Cog.listener()
    async def on_ready(self):
        print("languが準備完了しました")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Bot自身のメッセージは無視
        if message.author == self.bot.user:
            return

        # チャンネルが作成された場合
        if message.content.startswith("チャンネル作成"):
            guild = message.guild
            existing_channel = discord.utils.get(guild.channels, name=self.Translation_Channel_Name)

            # 既に存在する場合
            if existing_channel:
                await message.channel.send(f"{self.Translation_Channel_Name} チャンネルは既に存在します。和訳機能が有効です。")
            else:
                # 存在しない場合、新しいチャンネルを作成
                new_channel = await guild.create_text_channel(self.Translation_Channel_Name)
                await message.channel.send(f"{self.Translation_Channel_Name} チャンネルが作成されました。和訳機能が有効です。")

        # 和訳チャンネルでの処理
        elif message.channel.name == self.Translation_Channel_Name:
            # 言語を自動判定する
            source_lang = self.language(message.content)

            if source_lang == "ja":
                target_lang = "EN"
            else:
                target_lang = "JA"

            params = {
                "auth_key": self.DeepL_Token,
                "text": message.content,
                "source_lang": source_lang,
                "target_lang": target_lang
            }

            response = requests.post(self.DeepL_API_URL, data=params)

            # HTTPリクエストが成功した場合
            if response.status_code == 200:
                response_json = response.json()
                translated_text = response_json["translations"][0]["text"]
                await message.channel.send(translated_text)

            # エラーメッセージ
            else:
                await message.channel.send(f"翻訳エラー。HTTPステータスコード: {response.status_code}")
                await message.channel.send(response.text)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'deeple          [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()

async def setup(bot):
    await bot.add_cog(language(bot))
