import discord
from discord.ext import commands

from utils.paginator import Paginator
from utils.static.dataclass import MatchData


class Embeds:
    def __init__(self):
        self.loadMatchEmbed = discord.Embed(
            title="Summoner Found! :white_check_mark:",
            color=discord.Colour.gold(),
            description=":alarm_clock: Loading Match Data...",
        )

        self.noRegion = discord.Embed(
            title=":x: No Region Found",
            color=discord.Colour.red(),
            description="Pls set your region by `[region` before using commands!",
        )

        self.regionHelp = discord.Embed(
            title=":x: [region Help",
            color=discord.Colour.red(),
            description="[region (Region Code)",
        )
        self.regionHelp.add_field(
            name="Region Code List",
            value=":earth_americas: **na1** - North America\n:flag_kr: **kr** - South Korea\n:flag_jp: **jp1** - Japan\n:flag_eu: **eun1** - North / East Europe\n"
            + ":flag_eu: **euw1** - West Europe\n:flag_au: **oc1** - Oceania\n:flag_ru: **ru** - Russia\n:flag_tr: **tr1** - Turkey\n:flag_br: **br1** - Brazil\n"
            + ":earth_americas: **la1** - Latin Am. North\n:earth_americas: **la2** - Latin Am. South",
        )

        self.matchHelp = discord.Embed(
            title=":x: [match Help",
            color=discord.Colour.red(),
            description="[match (1~20) (Nickname)",
        )

        self.summonerNotFound = discord.Embed(
            title=":x: No summoner found",
            color=discord.Color.red(),
            description="Pls check the nickname!",
        )

    def rank_list(self, data_list: list[int]) -> list[int]:
        d = {n: i for i, n in enumerate(sorted(set(data_list), reverse=True), 1)}

        return [d[n] for n in data_list]

    def match_embed(
        self, ctx: commands.Context, data: MatchData, num: int
    ) -> tuple[discord.Embed, discord.ui.View]:  # Generate Match Embed by Dataset
        embed_list = []

        embed_init = discord.Embed(
            title=f"**:mag_right: {data.user_name}'s Match History ({num})**",
            color=discord.Color.green(),
            description=f"**{data.game_mode}** ({data.time})",
        )
        embed_init.set_footer(
            text=f"{ctx.author.name} | Disabled after 60 seconds of inactivity",
            icon_url=ctx.author.avatar,
        )

        team1 = ":tada: Win" if data.teams[0] else ":headstone: Lose"
        team2 = ":tada: Win" if data.teams[1] else ":headstone: Lose"
        embed_init.add_field(
            name=":blue_car: Blue Team", value=f"**{team1}**", inline=False
        )
        for i in range(0, 5):
            embed_init.add_field(
                name="_ _",
                value=f"{data.champ_emojis[i]} {data.names[i]} {data.perk_emojis[i]}\n**{data.kdas[i][0]} / {data.kdas[i][1]} / {data.kdas[i][2]}**\n"
                + f"{data.spell_emojis[i][0]} {data.spell_emojis[i][1]}\nDamage Dealt to Champions: **{data.dmg_to_ch[i]}**\n_ _",
                inline=True,
            )

        embed_init.add_field(
            name=":red_car: Red Team", value=f"**{team2}**", inline=False
        )
        for i in range(5, 10):
            embed_init.add_field(
                name="_ _",
                value=f"{data.champ_emojis[i]} {data.names[i]} {data.perk_emojis[i]}\n**{data.kdas[i][0]} / {data.kdas[i][1]} / {data.kdas[i][2]}**\n"
                + f"{data.spell_emojis[i][0]} {data.spell_emojis[i][1]}\nDamage Dealt to Champions: **{data.dmg_to_ch[i]}**\n_ _",
                inline=True,
            )

        embed_list.append(embed_init)

        dmg_to_ch_rank = self.rank_list(data.dmg_to_ch)
        dmg_taken_rank = self.rank_list(data.dmg_taken)
        gold_earned_rank = self.rank_list(data.gold_earned)

        team = 0
        for i in range(0, 10):
            if i > 4:
                team = 1

            color = discord.Color.green() if data.teams[team] else discord.Color.red()
            win_text = ":tada: Win" if data.teams[team] else ":headstone: Lose"

            embed = discord.Embed(
                title=f"**:mag_right: Player Details ({i+1}/10)**",
                color=color,
                description=f"**{data.game_mode}** ({data.time})\n**{win_text}**",
            )
            embed.set_footer(
                text=f"{ctx.author.name} | Disabled after 60 seconds of inactivity",
                icon_url=ctx.author.avatar,
            )

            embed.add_field(
                name="Info",
                value=f"{data.champ_emojis[i]} {data.names[i]} {data.perk_emojis[i]}\n**{data.kdas[i][0]} / {data.kdas[i][1]} / {data.kdas[i][2]}**\n"
                + f"{data.spell_emojis[i][0]} {data.spell_emojis[i][1]}",
            )
            embed.add_field(
                name="Items",
                value=f"{data.item_emojis[i][0]} {data.item_emojis[i][1]} {data.item_emojis[i][2]}  {data.item_emojis[i][6]} **Vision Score** - {data.vision_score[i]}\n"
                + f"{data.item_emojis[i][3]} {data.item_emojis[i][4]} {data.item_emojis[i][5]}",
            )

            embed.add_field(
                name="Stats",
                value=f"**:outbox_tray: Damage Dealt to Champions** - {data.dmg_to_ch[i]} (:medal: Rank: {dmg_to_ch_rank[i]})\n"
                + f"**:inbox_tray: Damage Taken** - {data.dmg_taken[i]} (:medal: Rank: {dmg_taken_rank[i]})\n"
                + f"**:coin: Gold Earned** - {data.gold_earned[i]} (:medal: Rank: {gold_earned_rank[i]})",
                inline=False,
            )

            embed_list.append(embed)

        return embed_init, Paginator(ctx.author.id, embed_list)

    @staticmethod
    def your_region(
        ctx: commands.Context, region: str
    ) -> discord.Embed:  # Returns your region
        embed = discord.Embed(
            title=f":mag_right: {ctx.author.name}'s region",
            color=discord.Colour.random(),
            description=f"Your region is currently **{region}**!",
        )
        embed.add_field(
            name=":question: [region Help",
            value="Use [region command to change your region.",
        )

        return embed

    @staticmethod
    def region_success(ctx: commands.Context, region: str) -> discord.Embed:
        embed = discord.Embed(
            title=f":white_check_mark: Region set successful",
            color=discord.Color.green(),
            description=f"Your region is now **{region}**! :earth_asia:",
        )

        return embed

    @staticmethod
    def emj_updated_embed(n: int, name: str) -> discord.Embed:
        embed = discord.Embed(
            title=":white_check_mark: Emoji is now updated!",
            color=discord.Color.green(),
            description=f"{n} emojis have been added to {name}.",
        )

        return embed
