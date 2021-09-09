from discord import Emoji

from utils.static.data import emoji_servers


class CustomEmojis:
    @staticmethod
    def update_dict(emojis: list[Emoji]) -> dict[str, str]:
        emoji_dict = {}

        for emoji in emojis:
            if emoji.guild.id in emoji_servers:
                emoji_dict[emoji.name] = f'<:{emoji.name}:{emoji.id}>'

        return emoji_dict

    def init(self, emojis: list[Emoji]):
        self.__dict = self.update_dict(emojis)

    @property
    def dict(self):
        return self.__dict

    @dict.setter
    def dict(self, emojis: list[Emoji]):
        self.__dict = self.update_dict(emojis)

    def id_to_emoji(self, id: str) -> str:
        if id in self.dict.keys():
            return self.dict[id]
        
        return ':black_large_square:'
