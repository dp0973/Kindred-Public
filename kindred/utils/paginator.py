from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.ui.button import button
from discord.ui.view import View
from discord.embeds import Embed
from typing import Optional


class Paginator(View):
    def __init__(
        self, executor_id: int, embeds: list[Embed], timeout: Optional[float] = 60
    ):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.executor_id = executor_id
        self.index = 0

    @property
    def total(self):
        return len(self.embeds)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if user := interaction.user:
            if user.id == self.executor_id:
                return True

            await interaction.response.send_message(
                "You are not a command author!", ephemeral=True
            )

        return False

    @button(label="Previous", style=ButtonStyle.primary, emoji="◀")
    async def prev_page(self, _, interaction: Interaction):
        self.index -= 1

        if self.index < 0:
            self.index = self.total - 1

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @button(label="Next", style=ButtonStyle.primary, emoji="▶️")
    async def next_page(self, _, interaction: Interaction):
        self.index += 1

        if self.index >= self.total:
            self.index = 0

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @button(label="Close", style=ButtonStyle.danger, emoji="❌")
    async def close(self, _, interaction: Interaction):
        if message := interaction.message:
            self.stop()
            await message.delete()