import os
import dotenv
from utils.bot import Bot


dotenv.load_dotenv()
if __name__ == "__main__":
    token = os.getenv('TOKEN')
    bot = Bot(token)
    bot.run()
