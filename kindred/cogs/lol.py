from discord.ext import commands
import os
from pantheon import pantheon
from typing import Optional

from bot import Kindred
from utils.embeds import Embeds
from utils.lol import LolExt
from utils.request import MongoRequest


class Lol(commands.Cog):
    def __init__(self, bot: Kindred):
        self.bot = bot
        self.lol_ext = LolExt(bot.custom_emojis)
        self.mg_request = MongoRequest()
        self.embeds = Embeds()
        self.pantheon = pantheon.Pantheon("kr", os.environ["RIOT_API_KEY"])

    @commands.command()
    async def match(
        self,
        ctx: commands.Context,
        num: Optional[int] = None,
        *,
        name: Optional[str] = None,
    ):
        """
        Get a match info by match number and summoner name
        """
        await ctx.send(f"**:mag: Searching summoner `{name}`...**", delete_after=5)

        if not num or not name or not 0 < num < 21:
            return await ctx.send(embed=self.embeds.matchHelp)

        region = await self.mg_request.get_region(ctx.author.id)
        if not region:
            return await ctx.send(embed=self.embeds.noRegion)

        self.pantheon._server = region

        user = await self.pantheon.getSummonerByName(name)
        user_name = user["name"]

        msg_embed = await ctx.send(embed=self.embeds.loadMatchEmbed)

        matchlist = await self.pantheon.getMatchlist(
            user["accountId"], params={"endIndex": 20}
        )
        match = await self.pantheon.getMatch(matchlist["matches"][num - 1]["gameId"])

        data = await self.lol_ext.parse_match(match, user_name)
        embed, view = self.embeds.match_embed(ctx, data, num)

        await msg_embed.edit(embed=embed, view=view)

    @commands.command()
    async def region(self, ctx: commands.Context, region: Optional[str] = None):
        """
        Show or set your region
        """
        if not region:
            if region := await self.mg_request.get_region(ctx.author.id):
                return await ctx.send(self.embeds.your_region(ctx, region))

            return await ctx.send(embed=self.embeds.regionHelp)

        if await self.mg_request.set_region(ctx.author.id, region):
            return await ctx.send(embed=self.embeds.region_success(ctx, region))

        await ctx.send(embed=self.embeds.regionHelp)


def setup(bot: Kindred):
    bot.add_cog(Lol(bot))
