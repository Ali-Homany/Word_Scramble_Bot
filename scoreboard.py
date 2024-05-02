from telebot.types import User


class ScoreBoard:
    def __init__(self):
        """
        This class is responsible for keeping up the scores of the game & saving each player progress
        Attributes:
            - scores (dict[User:int]): current points of each participating user
        """
        self.scores: dict[User: int] = {}

    def addPoints(self, points: int, player: User) -> None:
        """
        Args:
            points (int): number of points to be added
            player (User): the player who deserves the points. A telebot object which contains all details about him
        """
        pass

    def getWinner(self) -> User:
        """
        Returns:
            User object representing the player with the highest score from the scores attribute
        """
        pass

    def displayScores(self) -> str:
        """
        Returns:
            str: a string containing all the scores of the players
        """
        pass
