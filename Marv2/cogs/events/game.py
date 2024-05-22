import random
import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup as bs
from colorama import init, Fore

class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class JankenButtons(discord.ui.View):
        def __init__(self, embed):
            super().__init__()
            self.__answers = ['グー', 'チョキ', 'パー']
            self.__user_choice = None
            self.__embed = embed

        async def __edit_message(self, interaction):
            answer = random.choice(self.__answers)
            victory = None

            if self.__user_choice == 'グー' and answer == 'チョキ':
                victory = True

            elif self.__user_choice == 'チョキ' and answer == 'パー':
                victory = True

            elif self.__user_choice == 'パー' and answer == 'グー':
                victory = True

            elif self.__user_choice is answer:
                victory = None

            else:
                victory = False

            if victory:
                await interaction.response.edit_message(content=None,
                                                        view=None,
                                                        embed=discord.Embed(
                                                            color=self.__embed.color,
                                                            title=self.__embed.title,
                                                            description=f"{self.__embed.description} \n"
                                                                        f"あなたは `{self.__user_choice}` を選びました。私は `{answer}` を選びました。\n"
                                                                        "初めての勝利ですね... やったね！ 🎉🥳🥳"))
            elif not victory and victory is not None:
                await interaction.response.edit_message(content=None,
                                                        view=None,
                                                        embed=discord.Embed(
                                                            color=self.__embed.color,
                                                            title=self.__embed.title,
                                                            description=f"{self.__embed.description} \n"
                                                                        f"あなたは `{self.__user_choice}` を選びました。私は `{answer}` を選びました。\n"
                                                                        "残念ですね。いつものように負けましたね、ハハハハハ！ 🤪🤣"))

            else:
                await interaction.response.edit_message(content=None,
                                                        view=None,
                                                        embed=discord.Embed(
                                                            color=self.__embed.color,
                                                            title=self.__embed.title,
                                                            description=f"{self.__embed.description} \n"
                                                                        f"あなたは `{self.__user_choice}` を選びました。私は `{answer}` を選びました。\n"
                                                                        "引き分けですね、やっぱり。もう一度やろう、若造！ 😐"))

        @discord.ui.button(label="グー", emoji="🗿", style=discord.ButtonStyle.blurple)
        async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.__user_choice = "グー"
            await self.__edit_message(interaction)

        @discord.ui.button(label="チョキ", emoji="✂️", style=discord.ButtonStyle.red)
        async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.__user_choice = "チョキ"
            await self.__edit_message(interaction)

        @discord.ui.button(label="パー", emoji="📄", style=discord.ButtonStyle.gray)
        async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.__user_choice = "パー"
            await self.__edit_message(interaction)

    @commands.command(aliases=['rps', 'rockpaperscissors'])
    async def janken(self, ctx):
        """m!janken じゃんけんゲーム！"""
        description = '私とじゃんけんをしよう！以下から一つ選んでください：'
        embed = discord.Embed(color=0xffcd4c, title=f'{ctx.message.author}: グー チョキ パー',
                              description=description)
        await ctx.send(embed=embed, view=self.JankenButtons(embed=embed))

    @commands.command()
    async def slots(self, ctx):
        """m!slots スロットマシンゲーム"""
        author_id = str(ctx.author.id)

        symbols = ['🍒', '🔔', '7️⃣', '👑', '☠️']

        slot = [0, 1, 2]

        for i in range(3):
            slot[i] = symbols[random.randint(0, 3)]

        is_same = True if slot[0] == slot[1] == slot[2] else False

        if is_same and symbols[4] in slot:
            footer = '負け！あなたのバランスはリセットされました。'
        elif is_same and symbols[3] in slot:
            footer = '+ 5,000ドルがあなたのアカウントに追加されました。'
        elif is_same and symbols[2] in slot:
            footer = '+ 10,000ドルがあなたのアカウントに追加されました。'
        elif is_same and symbols[1] in slot:
            footer = '+ 15,000ドルがあなたのアカウントに追加されました。'
        elif is_same and symbols[0] in slot:
            footer = 'ジャックポット!!! + 1,000,000ドルがあなたのアカウントに追加されました。'
        elif symbols[0] == slot[0] == slot[1] or slot[0] == slot[2] == symbols[0] or slot[1] == slot[2] == symbols[0]:
            footer = '+ 3,500ドルがあなたのアカウントに追加されました。'
        elif symbols[0] in slot:
            footer = '+ 1,500ドルがあなたのアカウントに追加されました。'
        else:
            footer = '何も当たりませんでした。'
        embed = discord.Embed(color=0x36c600, title='🎰 Slots Azino777',
                              description=str(slot[0]) + str(slot[1]) + str(slot[2]))
        embed.set_footer(text=footer, icon_url="https://i.imgur.com/uZIlRnK.png")
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'game            [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()

async def setup(bot):
    await bot.add_cog(game(bot))

