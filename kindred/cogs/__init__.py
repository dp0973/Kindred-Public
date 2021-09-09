from bot import Kindred


def load(bot: Kindred) -> None:
    cogs = ["events.error", "events.ready", "admin", "general"]

    for cog in cogs:
        bot.load_extension(f"cogs.{cog}")
