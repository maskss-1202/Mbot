import discord
from discord.ext import commands
from colorama import init, Fore


class vote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def vote(self, ctx, question, *options: str):
        """m!vote 題 一つ目から最大五つ目まで投票を作る事ができます。"""
        author = ctx.message.author
        server = ctx.message.guild

        DISCORD_SERVER_ERROR_MSG = "このコマンドを実行する権限がありません。"    

        if not author.guild_permissions.manage_messages:
            return await ctx.send(DISCORD_SERVER_ERROR_MSG)

        if len(options) <= 1:
            await ctx.send("```Error! ポールは2つ以上の選択肢が必要です。```")
            return
        if len(options) > 5:
            await ctx.send("```Error! ポールには5つ以上の選択肢は使用できません。```")
            return

        if len(options) == 5 and options[0] == "yes" and options[1] == "no":
            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        else:
            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)

        embed = discord.Embed(title=question, color=3553599, description=''.join(description))

        react_message = await ctx.send(embed=embed)

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

        embed.set_footer(text='ポールID: {}'.format(react_message.id))

        await react_message.edit(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'vote            [{Fore.GREEN}online{Fore.RESET}]')
        await self.client.tree.sync()      

async def setup(client:commands.Bot):
    await client.add_cog(vote(client))
