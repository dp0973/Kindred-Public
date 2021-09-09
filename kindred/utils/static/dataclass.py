from dataclasses import dataclass


@dataclass
class MatchData:
    time: str
    game_mode: str
    names: list[str]
    user_name: str
    teams: list[bool]
    kdas: list[list[int]]
    dmg_to_ch: list[int]
    dmg_taken: list[int]
    gold_earned: list[int]
    vision_score: list[int]
    champ_names: list[str]
    champ_emojis: list[str]
    perk_emojis: list[str]
    spell_emojis: list[str]
    item_emojis: list[list[str]]