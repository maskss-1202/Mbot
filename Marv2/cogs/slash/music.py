from config import settings

import asyncio
import datetime
import os
import discord
from discord.errors import ClientException
from discord import app_commands
from discord.ext import commands
from colorama import init, Fore
from yt_dlp import YoutubeDL, utils

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class Queue:
    def __init__(self):
        self.__vc = None
        self.__queue = []
        self.__playing_now = None

    def add_track(self, title):
        self.__queue.append(title)

    def play_next(self):
        if len(self.__queue) > 0:
            next_track = self.__queue.pop(0)
            self.__playing_now = next_track
            return next_track
        else:
            return 0

    def get_playing_now(self):
        print(self.__playing_now)
        return self.__playing_now

    def set_playing_now(self, track):
        self.__playing_now = track

    def clear(self):
        self.__queue = []
        self.__playing_now = None

    def is_empty(self):
        if len(self.__queue):
            return False
        else:
            return True

    def length(self):
        return len(self.__queue)

    def get_by_id(self, id):
        return self.__queue[id]


class SMusic(commands.Cog):
    """音楽"""

    def __init__(self, bot):
        self.bot = bot
        self.__queue = Queue()
        self.vc = None

    def __get_info(self, song):
        video = None
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                video = ydl.extract_info(f"ytsearch3:{song}", download=False)['entries']
                return video
            except utils.DownloadError:  # 基本的な検索でビデオが見つからない場合
                video = ydl.extract_info(song, download=False)
                return video
            except utils.DownloadError:  # URLが見つからない場合
                raise IndexError()

    class PlayerButtons(discord.ui.View):
        def __init__(self, voice_chat, leave, stop, pause, resume, skip):
            super().__init__()
            self.__vc = voice_chat
            self.__leave = leave
            self.__stop = stop
            self.__pause = pause
            self.__resume = resume
            self.__skip = skip

        @discord.ui.button(style=discord.ButtonStyle.red, label='退出', emoji='🚪')
        async def button_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("わかった、もう出るよ。",
                                                    ephemeral=True)
            self.__leave()

        @discord.ui.button(style=discord.ButtonStyle.red, label='停止', emoji='🛑')
        async def button_stop(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("わかった、止めるわ",
                                                    ephemeral=True)
            self.__stop()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label='一時停止 / 再開', emoji='⏯️')
        async def button_pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.__vc.is_playing():
                await interaction.response.send_message("わかった、一時停止する",
                                                        ephemeral=True)
                self.__vc.pause()
            elif self.__vc.is_paused():
                await interaction.response.send_message("再開するよ。",
                                                        ephemeral=True)
                self.__vc.resume()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label='スキップ', emoji='⏭️')
        async def button_skip(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("この曲はスキップするよ。",
                                                    ephemeral=True)
            self.__skip(interaction)

    # 以下、コードの他の部分も同様に和訳が続きます
    async def __play(self, interaction, video):
        self.vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'],
                                            source=video.get("url"), **FFMPEG_OPTIONS),
                     after=lambda e: self.__skip(interaction=interaction))

        duration = video.get("duration")
        upload_date = video.get("upload_date")
        upload_date = f"{upload_date[:4]}.{upload_date[4:6]}.{upload_date[6:]}"
        embed = (discord.Embed(title=f'{self.bot.get_emoji(settings["emojis"]["youtube"])} 今再生中',
                               description=f"**{video.get('title')}**",
                               color=0xff2a2a)
                 .add_field(name="👤 作者", value=video.get("uploader"), inline=False)
                 .add_field(name="⌛ 持続時間", value=datetime.timedelta(seconds=duration))
                 .add_field(name="📅 アップロード日", value=upload_date)
                 .add_field(name="👍 いいねの数", value=video.get('like_count', '非表示'), inline=False)
                 .add_field(name="🔔 リクエストしたユーザー", value=interaction.user.name, inline=False)
                 .set_thumbnail(url=video.get("thumbnail")))
        await interaction.followup.send(embed=embed, view=self.PlayerButtons(self.vc,
                                                                             self.__leave,
                                                                             self.__stop,
                                                                             self.__pause,
                                                                             self.__resume,
                                                                             self.__skip))

        title = video.get('title')
        self.__queue.set_playing_now(title)

    def __skip(self, interaction):
        if self.vc.is_playing():
            self.vc.pause()
        if not self.__queue.is_empty():
            next_track = self.__queue.play_next()
            asyncio.run_coroutine_threadsafe(self.__play(interaction, next_track), self.bot.loop)

    def __stop(self):
        asyncio.run_coroutine_threadsafe(
        self.bot.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(name=f"m!help | {len(self.bot.guilds)} server", type=discord.ActivityType.watching)),
            self.bot.loop)

        self.__queue.clear()
        if self.vc.is_playing():
            self.vc.stop()
        elif self.vc.is_paused():
            self.vc.stop()

    def __leave(self):
        asyncio.run_coroutine_threadsafe(
        self.bot.change_presence(status=discord.Status.online, 
                                 activity=discord.Activity(name=f"m!help | {len(self.bot.guilds)} server", type=discord.ActivityType.watching)),    
            self.bot.loop)
        self.__pause()
        asyncio.run_coroutine_threadsafe(self.vc.disconnect(), self.bot.loop)

    def __pause(self):
        if not self.vc.is_paused():
            self.vc.pause()

    def __resume(self):
        if not not self.vc.is_playing():
            self.vc.resume()

    class SelectSongButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            self.value = None

        @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='1️⃣')
        async def button_first(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("オーケー、最初の曲を選びました", ephemeral=True)
            self.value = 0
            self.stop()

        @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='2️⃣')
        async def button_second(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("オッケー、2番目の曲にします", ephemeral=True)
            self.value = 1
            self.stop()

        @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='3️⃣')
        async def button_third(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("いいよ、3番目の曲だ", ephemeral=True)
            self.value = 2
            self.stop()

    @app_commands.command(name="mplay", description="曲を再生する")
    @app_commands.describe(song="検索テキスト")
    async def play(self, interaction: discord.Interaction,
                   song: str):
        if interaction.user.voice is not None:
            try:
                self.vc = await interaction.user.voice.channel.connect()
            except ClientException:
                pass
        else:
            await interaction.response.send_message("ボイスチャンネルに接続していません")
            return

        await interaction.response.send_message(f"**\"{song}\"** で曲を検索中、少々お待ちください")
        reply = await interaction.original_response()

        videos = self.__get_info(song)
        view = self.SelectSongButtons()
        embed = (discord.Embed(title=f"🔍 \"{song}\" での検索結果", color=0xf0cd4f))
        for i in range(3):
            upload_date = f"{videos[i]['upload_date'][:4]}.{videos[i]['upload_date'][4:6]}.{videos[i]['upload_date'][6:]}"
            embed.add_field(name=f"{i + 1}. {videos[i].get('title')}",
                            value=f"👤 {videos[i]['uploader']} \n"
                                  f"⏳ {datetime.timedelta(seconds=videos[i]['duration'])} \n"
                                  f"📅 {upload_date}",
                            inline=False)
        await reply.edit(content="", embed=embed, view=view)
        await view.wait()

        if view.value is None:
            await reply.edit(content="## ⌛ タイムアウト \n"
                                     "次回はもっと早く考えてくださいよ。30秒以上待機できません。", embed=None, view=None)
            return
        try:
            vid = videos[view.value]
        except IndexError:
            await interaction.response.send_message(":x: 残念ながらわかりませんでした。"
                                                    "申し訳ございませんがわかりませんでした。")
            await self.vc.disconnect()
            return

        if not self.vc.is_playing():
            await self.__play(interaction, vid)
        else:
            self.__queue.add_track(vid)
            await interaction.followup.send(f"**{vid.get('title')}** がキューに追加されました。")

    @app_commands.command(name="mpause", description="ボイスチャンネルでの音楽の一時停止/再開")
    async def switch_pause(self, interaction: discord.Interaction):
        if self.vc is not None:
            if self.vc.is_playing():
                await interaction.response.send_message("わかった、一時停止します")
                self.vc.pause()
            elif self.vc.is_paused():
                await interaction.response.send_message("再開します。",
                                                        ephemeral=True)
                self.vc.resume()
        else:
            await interaction.response.send_message("ボットがボイスチャンネルに接続していません")

    @app_commands.command(name="mskip", description="次の曲へスキップ")
    async def skip(self, interaction: discord.Interaction):
        if self.vc is not None:
            self.__skip(interaction)
            await interaction.response.send_message("この音楽をスキップします")
        else:
            await interaction.response.send_message("ボットがボイスチャンネルに接続していません")

    @app_commands.command(name="mstop", description="音楽を停止し、再生リストをクリア")
    async def stop(self, interaction: discord.Interaction):
        if self.vc is not None:
            self.__stop()
            await interaction.response.send_message("この音楽を停止します")
        else:
            await interaction.response.send_message("ボットがボイスチャンネルに接続していません")

    @app_commands.command(name="mleave", description="ボイスチャンネルから退出")
    async def leave(self, interaction: discord.Interaction):
        if self.vc is not None:
            await self.vc.disconnect()
            await interaction.response.send_message("この音楽をストップします")
        else:
            await interaction.response.send_message("ボットがボイスチャンネルに接続していません")

    @app_commands.command(name="mqueue", description="次の曲のリストを表示")
    async def queue_embed(self, interaction: discord.Interaction):
        now = self.__queue.get_playing_now()
        if now is not None:
            embed = (discord.Embed(title="📜 再生リスト", color=0xf0cd4f))
            embed.add_field(name="▶️ 今再生中", value=now, inline=False)
            for i in range(self.__queue.length()):
                video = self.__queue.get_by_id(i)
                embed.add_field(name=f"{i + 1} 位", value=video.get('title'), inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            embed = (discord.Embed(title="📜 再生リスト",
                                   color=0xf0cd4f,
                                   description="再生リストは空です。"))
            await interaction.response.send_message(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'musiccommand    [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()


async def setup(bot):
    await bot.add_cog(SMusic(bot))

