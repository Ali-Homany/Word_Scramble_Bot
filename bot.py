import telebot
from telebot.types import Message
from lookups import Messages
from Game import Game, GameEndedException

"""This modules defines the telegram bot that will interact with players and manage different instanes of Game simultaneously"""


class TelegramBot:
    def __init__(self, token: str):
        """
        When initiated, it creates a bot and defines its messages handlers

        Attributes:
            - bot (TeleBot) object defined using its token
            - games: dictionary of active group_chat_id:Game. A group is removed when its game ends
        """
        self.bot = telebot.TeleBot(token=token)
        self.games = {}

        @self.bot.message_handler(commands=['start', 'help'])
        def introduce_bot(message):
            """
            This method introduces the bot to new chats or those who requested help
            """
            pass

        @self.bot.message_handler(commands=['play'])
        def handle_play(message):
            if message.chat.id not in self.games.keys():
                self.initiateGame(message.chat.id)
            else:
                bot.send_message(message.chat.id, Messages.ALREADY_PLAYING)

        @self.bot.message_handler(commands=['endGame'])
        def handle_endGame(message):
            if message.chat.id in self.games.keys():
                self.endGame(message.chat.id)

        @self.bot.message_handler(function= lambda x: True)
        def handle_any(message):
            if message.chat.id in self.games.keys():
                self.checkAnswer(message)

    def run(self) -> None:
        """
        This function activates the bot (polling), so it is ready to handle any incoming messages and start games
        """
        pass

    def initiateGame(self, group_chat_id: str) -> None:
        """
        This function initiates a game for the group which requested.
        Args:
            - group_chat_id (int): the chat id of the group that requested a new game
        """
        pass

    def endGame(self, group_id) -> None:
        """
        This function is responsible for ending an ongoing game. This includes sending results, announcing winners, removing group from groups_details attribute. If the group is not even playing, do nothing

        Args:
            - group_id (int): chat_id of the group that just finished playing
        """
        pass

    def checkAnswer(message: Message) -> None:
        """
        This function is responsible for checking if the message is a correct answer to the game using Game.AddPoints. If yes, then it replies to the sender giving him points. Otherwise ignore. If the game is over, then it ends the game.

        Args:
            - message (Message): the message that was sent to the bot to be checked
        """
        pass
