import discord
from discord.ext import commands

from bot import Kindred


class General(commands.Cog):
    def __init__(self, bot: Kindred):
        self.bot = bot

    @commands.command(name="invite")
    async def _invite(self, ctx: commands.Context):
        url = discord.utils.oauth_url(
            self.bot.user.id, permissions=discord.Permissions(8)
        )
        await ctx.send(url)


def setup(bot: Kindred):
    bot.add_cog(General(bot))
