# Word_Scramble_Bot
Telegram bot that helps a group of friends to play word scramble game

Word scramble is a simple multiplayer game where given a list of letters, the person to find most words in the specified time wins!

## Project Structure
[main.py](./main.py) is the entry point to this project, which initializes the bot instance and runs it.

[Utils folder](./utils/) contains all modules needed for the project:
- [bot.py](./utils/bot.py): defines the telegram bot that will interact with players and manage different instanes of Game simultaneously.
- [Game.py](./utils/Game.py): The Game class wraps a game instance in a group, it is responsible for storing and managing all its variables and progress.
- [scoreboard.py](./utils/scoreboard.py): This class is responsible for keeping up the scores of the game & saving each player progress. It is used inside a Game object.
- [lookups.py](./utils/lookups.py): contains all the lookups for the bot and other files + some helper methods.

## How to play?
- Add the bot to your telegram group
- Give the bot access to read the chat & send messages (preferrably make it admin)
- send /play

That's it! the bot then will send a list of letters and start a timer. Send as many words as you can find from those letters, try to beat your friends!
The bot will count points as you're playing, and finally send the final results when time's up!
