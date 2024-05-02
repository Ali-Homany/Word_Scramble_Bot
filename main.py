from bot import Bot
from lookups import Keys


if __name__ == "__main__":
    bot = Bot(Keys.TOKEN)
    bot.run()