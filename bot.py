import telebot
from telebot.types import Message
from lookups import Messages
from Game import Game, GameEndedException

"""This modules defines the telegram bot that will interact with players and manage different instanes of Game simultaneously"""


class Bot:
    def __init__(self, token: str):
        """
        When initiated, it creates a bot and defines its messages handlers

        Attributes:
            - bot (TeleBot) object defined using its token
            - games: dictionary of active group_chat_id:Game. A group is removed when its game ends
        """
        self.bot = telebot.TeleBot(token=token)
        self.games: dict[str: Game] = {}

        @self.bot.message_handler(commands=['start', 'help'])
        def introduce_bot(message: Message):
            """
            This method introduces the bot to new chats or those who requested help
            """
            self.bot.send_message(chat_id=message.chat.id, text=Messages.INTRO(message.chat.type))

        @self.bot.message_handler(commands=['play'])
        def handle_play(message):
            if message.chat.id not in self.games.keys():
                self.initiateGame(group_chat_id=message.chat.id)
            else:
                self.bot.send_message(message.chat.id, Messages.ALREADY_PLAYING)

        @self.bot.message_handler(commands=['endGame'])
        def handle_endGame(message):
            if message.chat.id in self.games.keys():
                self.endGame(group_id=message.chat.id)

        @self.bot.message_handler(function= lambda x: True)
        def handle_any(message):
            if message.chat.id in self.games.keys():
                self.checkAnswer(message=message)

    def run(self) -> None:
        """
        This function activates the bot (polling), so it is ready to handle any incoming messages and start games
        """
        self.bot.polling()

    def initiateGame(self, group_chat_id: str) -> None:
        """
        This function initiates a game for the group which requested.
        Args:
            - group_chat_id (int): the chat id of the group that requested a new game
        """
        new_game = Game()
        self.games[group_chat_id] = new_game
        self.bot.send_message(chat_id=group_chat_id, text=Messages.START_GAME(new_game.letters))

    def endGame(self, group_id) -> None:
        """
        This function is responsible for ending an ongoing game. This includes sending results, announcing winners, removing group from groups_details attribute. If the group is not even playing, do nothing

        Args:
            - group_id (int): chat_id of the group that just finished playing
        """
        self.bot.send_message(chat_id=group_id, text=self.games[group_id].displayGame())
        self.games.pop(group_id)

    def checkAnswer(self, message: Message) -> None:
        """
        This function is responsible for checking if the message is a correct answer to the game using Game.AddPoints. If yes, then it replies to the sender giving him points. Otherwise ignore. If the game is over, then it ends the game.

        Args:
            - message (Message): the message that was sent to the bot to be checked
        """
        chat_id = message.chat.id
        curr_game: Game = self.games[chat_id]
        points = curr_game.addPoints(player=message.from_user, answer=message.text)
        try:
            if points == 0:
                return
            if points == -1:
                self.bot.reply_to(message=message, text="Already answered word")
            else:
                self.bot.reply_to(message=message, text=Messages.CORRECT_ANSWER(points))
        except GameEndedException:
            self.endGame(group_id=chat_id)

