import time
import telebot
import threading
from telebot.types import Message, Chat
from utils.lookups import Messages, MAX_DURATION
from utils.Game import Game, GameEndedException

"""
This modules defines the telegram bot that will interact with players and manage different instanes of Game simultaneously
"""


class Bot:
    """
    When initiated, it creates a bot and defines its message handlers

    Attributes:
        - bot (TeleBot) object defined using its token
        - games: dictionary of active chat_id:Game. A group is removed when its game ends
    """
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token=token)
        self.games: dict[int, Game] = {}
        # this variable is created to avoid race condition between threads, because they may access/modify shared variables
        # a context manager will be used to enable this lock, in each method that accesses games attribute (shared variable)
        self.games_lock = threading.RLock()

        @self.bot.message_handler(commands=['start', 'help'])
        def introduce_bot(message):
            """
            This method introduces the bot to new chats or those who requested help
            """
            self.bot.send_message(chat_id=message.chat.id, text=Messages.INTRO(message.chat.type))

        @self.bot.message_handler(commands=['play'])
        def handle_play(message):
            with self.games_lock:
                if message.chat.id in self.games.keys():
                    self.bot.send_message(message.chat.id, Messages.ALREADY_PLAYING)
                    return
            self.initiateGame(chat=message.chat)

        @self.bot.message_handler(commands=['endGame'])
        def handle_endGame(message):
            with self.games_lock:
                if message.chat.id not in self.games.keys():
                    return
            self.endGame(group_id=message.chat.id)
        
        @self.bot.message_handler(content_types=['new_chat_members'])
        def new_chat_member(message):
            chat_id = message.chat.id
            new_members = message.new_chat_members

            for member in new_members:
                if member.id == self.bot.get_me().id:
                    # The bot itself was added to the group
                    introduce_bot(message)
                else:
                    # Other members were added to the group
                    self.bot.send_message(chat_id, "اهلين ب " + member.full_name)

        @self.bot.message_handler(func= lambda message: True)
        def handle_any(message):
            if all(char not in message.text for char in ' !@#$%^&*( )_+-=[]{}|;:,.<>?/\\0123456789'):
                self.checkAnswer(message=message)
        

    def run(self) -> None:
        """
        This function activates the bot (polling), so it is ready to handle any incoming messages and start games
        """
        self.bot.polling()

    def initiateGame(self, chat: Chat) -> None:
        """
        This function initiates a game for the group which requested.
        Args:
            - chat_id (int): the chat id of the group that requested a new game
        """
        # this context manager uses the lock automatically, rather than manually calling lock.acquire() and .release()
        with self.games_lock:
            chat_id = chat.id
            if chat.type == 'private':
                new_game = Game(is_single_player=True)
            else:
                new_game = Game()
            self.games[chat_id] = new_game
        self.bot.send_message(chat_id=chat_id, text=Messages.START_GAME(new_game.letters))
        letters_message = self.bot.send_message(chat_id=chat_id, text='  '.join(new_game.letters))
        self.bot.unpin_all_chat_messages(chat_id=chat_id)
        self.bot.pin_chat_message(
                chat_id=chat_id,
                message_id=letters_message.message_id
        )
        threading.Thread(target=self.checkGameDuration, args=(chat_id,), daemon=True).start()

    def endGame(self, group_id) -> None:
        """
        This function is responsible for ending an ongoing game. This includes sending results, announcing winners, removing group from groups_details attribute. If the group is not even playing, do nothing

        Args:
            - group_id (int): chat_id of the group that just finished playing
        """
        with self.games_lock:
            if group_id in self.games:
                self.games[group_id].active = False
                self.bot.send_message(chat_id=group_id, text=self.games[group_id].displayGame())
                self.games.pop(group_id)

    def checkAnswer(self, message: Message) -> None:
        """
        This function is responsible for checking if the message is a correct answer to the game using Game.AddPoints. If yes, then it replies to the sender giving him points. Otherwise ignore. If the game is over, then it ends the game.

        Args:
            - message (Message): the message that was sent to the bot to be checked
        """
        with self.games_lock:
            chat_id = message.chat.id
            if chat_id not in self.games:
                return
            curr_game = self.games[chat_id]
            if time.time() - curr_game.start_time >= MAX_DURATION:
                self.bot.send_message(chat_id=chat_id, text="Time is up! Ending the game...")
            try:
                points = curr_game.addPoints(player=message.from_user, answer=message.text.lower())
                if points == -1:
                    return
                if points == 0:
                    self.bot.reply_to(message=message, text="Already answered word")
                else:
                    self.bot.reply_to(message=message, text=Messages.CORRECT_ANSWER(points))
            except GameEndedException:
                self.endGame(group_id=chat_id)

    def checkGameDuration(self, chat_id: str) -> None:
        """
        This function runs in a background thread to periodically check if the game's duration has exceeded MAX_DURATION.
        If the duration is exceeded, the game ends and a notification is sent.

        Args:
            - chat_id (str): the chat id of the group to check the game duration for
        """
        stop = False
        with self.games_lock:
            # check if key exists before accessing it, maybe it was removed by another thread
            if chat_id in self.games.keys():
                game = self.games[chat_id]
                if not game.active or time.time() - game.start_time >= MAX_DURATION:
                    stop = True
        # stop variable is created to avoid calling the methods inside the context manager
        if stop:
            self.endGame(group_id=chat_id)
        # recursion is used instead of a while because a while loop would actually own the lock until the game ends
        # this way however time.sleep is outside the context manager so the lock is released during this time
        else:
            time.sleep(.5)
            self.checkGameDuration(chat_id=chat_id)
