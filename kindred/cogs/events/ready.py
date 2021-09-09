import discord
from discord.ext.commands.cog import Cog

from bot import Kindred


class Ready(Cog):
    def __init__(self, bot: Kindred):
        self.bot = bot
        self.custom_emojis = bot.custom_emojis

    @Cog.listener()
    async def on_ready(self):
        print(f'Login with: {self.bot.user.name}, {self.bot.user.id}')
        game = discord.Game('[help')
        await self.bot.change_presence(status=discord.Status.online, activity=game)

        self.custom_emojis.init(self.bot.emojis)

        self.bot.load_extension('cogs.lol')


def setup(bot: Kindred):
    bot.add_cog(Ready(bot))