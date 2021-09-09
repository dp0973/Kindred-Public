from discord.ext import commands
from discord.ext.commands.core import is_owner
import static_data

from bot import Kindred
from utils.embeds import Embeds
from utils.request import BaseRequest, RiotRequest
from utils.static.data import emoji_servers


class Admin(commands.Cog):
    def __init__(self, bot: Kindred):
        self.bot = bot
        self.custom_emojis = bot.custom_emojis
        self.embeds = Embeds()
        self.b_request = BaseRequest()
        self.r_request = RiotRequest()
        self.ddragon = static_data.ddragon()

    @commands.command()
    @is_owner()
    async def update_emoji(self, ctx: commands.Context, index: int):
        msg = await ctx.send(embed=self.embeds.loadEmbed)

        self.custom_emojis.dict = self.bot.emojis
        emoji_dict = self.custom_emojis.dict

        server = self.bot.get_guild(emoji_servers[index - 1])

        n = 0

        champions = await self.r_request.get_ddragon("champion")
        for champion in champions["data"]:
            if champion not in emoji_dict.keys():
                url = self.ddragon.getChampion(champions["data"][champion]["key"]).image
                image = await self.b_request.request(url, "bytes")
                await server.create_custom_emoji(name=champion, image=image)
                print(f"{champion} emoji added to {server.name}")
                n += 1

        items = await self.r_request.get_ddragon("item")
        for item in items["data"]:
            if item not in emoji_dict.keys():
                url = self.ddragon.getItem(item).image
                image = await self.b_request.request(url, "bytes")
                await server.create_custom_emoji(name=item, image=image)
                print(f"{item} emoji added to {server.name}")
                n += 1

        runes = await self.r_request.get_perk_ids()
        for rune in runes:
            if str(rune) not in emoji_dict.keys():
                url = self.ddragon.getRune(rune).image
                image = await self.b_request.request(url, "bytes")
                await server.create_custom_emoji(name=str(rune), image=image)
                print(f"{rune[0]} emoji added to {server.name}")
                n += 1

        spells = await self.r_request.get_ddragon("summoner")
        for spell in spells["data"]:
            if spell not in emoji_dict.keys():
                url = self.ddragon.getSummoner(spells["data"][spell]["key"]).image
                image = await self.b_request.request(url, "bytes")
                await server.create_custom_emoji(name=spell, image=image)
                print(f"{spell} emoji added to {server.name}")
                n += 1

        self.custom_emojis.dict = self.bot.emojis

        await msg.edit(embed=self.embeds.emj_updated_embed(n, server.name))


def setup(bot: Kindred):
    bot.add_cog(Admin(bot))
