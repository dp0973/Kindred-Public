from datetime import datetime

from utils.emoji import CustomEmojis
from utils.static.dataclass import MatchData
from utils.request import RiotRequest


class LolExt:
    def __init__(self, custom_emojis: CustomEmojis):
        self.custom_emojis = custom_emojis
        self.r_request = RiotRequest()

    @staticmethod
    def replace_mode(game_mode: str) -> str:
        game_mode_dict = {
            "CLASSIC": "Classic",
            "ARAM": "ARAM",
            "TEAM_BUILDER": "Team Builder",
            "ONEFORALL": "One for All",
            "FIRSTBLOOD": "Snowdown Showdown",
            "ASCENSION": "Ascension",
            "KING_PORO": "King Poro",
            "COUNTER_PICK": "Nexus",
            "BILGEWATER": "Black Market Brawlers",
        }
        try:
            return game_mode_dict[game_mode]
        except KeyError:
            return "Unknown"

    async def parse_match(self, match: dict, user_name: str) -> MatchData:
        timestamp = str(match["gameCreation"])
        time = str(datetime.fromtimestamp(int(timestamp[:10])))

        game_mode = self.replace_mode(match["gameMode"])

        names = [
            match["participantIdentities"][i]["player"]["summonerName"]
            for i in range(0, 10)
        ]

        teams = [True, False]
        if match["teams"][1]["win"] == "Win":
            teams.reverse()

        champ_names = [
            self.r_request.get_name_by_key(
                match["participants"][i]["championId"], "champion"
            )
            for i in range(0, 10)
        ]

        champ_emojis = [
            self.custom_emojis.id_to_emoji(
                self.r_request.get_id_by_key(
                    match["participants"][i]["championId"], "champion"
                )
            )
            for i in range(0, 10)
        ]

        spell_emojis = [
            [
                self.custom_emojis.id_to_emoji(
                    self.r_request.get_id_by_key(
                        match["participants"][i]["spell1Id"], "spell"
                    )
                ),
                self.custom_emojis.id_to_emoji(
                    self.r_request.get_id_by_key(
                        match["participants"][i]["spell2Id"], "spell"
                    )
                ),
            ]
            for i in range(0, 10)
        ]

        perk_emojis = [
            self.custom_emojis.id_to_emoji(
                str(match["participants"][i]["stats"]["perk0"])
            )
            for i in range(0, 10)
        ]

        item_emojis = []
        for i in range(0, 10):
            items = []
            for j in range(0, 7):
                items.append(
                    self.custom_emojis.id_to_emoji(
                        str(match["participants"][i]["stats"][f"item{j}"])
                    )
                )
            item_emojis.append(items)

        kdas = [
            [
                match["participants"][i]["stats"]["kills"],
                match["participants"][i]["stats"]["deaths"],
                match["participants"][i]["stats"]["assists"],
            ]
            for i in range(0, 10)
        ]

        dmg_to_ch = [
            match["participants"][i]["stats"]["totalDamageDealtToChampions"]
            for i in range(0, 10)
        ]

        dmg_taken = [
            match["participants"][i]["stats"]["totalDamageTaken"] for i in range(0, 10)
        ]

        gold_earned = [
            match["participants"][i]["stats"]["goldEarned"] for i in range(0, 10)
        ]

        vision_score = [
            match["participants"][i]["stats"]["visionScore"] for i in range(0, 10)
        ]

        match_data = MatchData(
            time,
            game_mode,
            names,
            user_name,
            teams,
            kdas,
            dmg_to_ch,
            dmg_taken,
            gold_earned,
            vision_score,
            champ_names,
            champ_emojis,
            perk_emojis,
            spell_emojis,
            item_emojis,
        )

        return match_data
