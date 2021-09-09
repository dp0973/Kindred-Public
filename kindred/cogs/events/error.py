from discord.ext import commands
from discord.ext.commands.cog import Cog
from pantheon.utils.exceptions import NotFound

from bot import Kindred
from utils.embeds import Embeds


class Error(Cog):
    def __init__(self, bot: Kindred):
        self.bot = bot
        self.embeds = Embeds()

    @Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.errors):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("Parameter error.")

        if isinstance(error, commands.errors.CommandInvokeError):
            if isinstance(error.original, NotFound):
                return await ctx.send(embed=self.embeds.summonerNotFound)


def setup(bot: Kindred):
    bot.add_cog(Error(bot))
