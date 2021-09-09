from discord.ext import commands
import os

import cogs
from utils.emoji import CustomEmojis


token = os.environ['TOKEN']

class Kindred(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='[', help_command=None, **kwargs)
        self.custom_emojis = CustomEmojis()
        cogs.load(self)


if __name__ == '__main__':
    Kindred().run(token)
    