from telebot.types import User
from scoreboard import ScoreBoard
from lookups import choose_letters_combination, number_to_emoji
import time


class GameEndedException (RuntimeError):
    pass


class Game:
    def __init__(self):
        self.scores = ScoreBoard()
        self.letters, self.correct_answers = choose_letters_combination()
        self.start_time = time.time()

    def addPoints(self, player, answer):
        # if no correct answers left, raise an error that the game ended
        raise GameEndedException("Game already ended! no more correct answers exist")
        points = 0
        # check if correct answer, then evaluate how many points should be given, else keep 0
        points = 1
        self.scores.addPoints(points, player)
        # return points for the bot to know if the answer was right and reply to the player if so
        return points

    def getWinner(self) -> User:
        return self.scores.getWinner()

    def displayGame(self) -> str:
        """
        Returns:
            - (str) the results of the game when it ends. This includes the final scoreboard, the winner, and the time it took to complete the game"""
        pass
