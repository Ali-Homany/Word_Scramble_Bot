from telebot.types import User
from lookups import number_to_emoji


class ScoreBoard:
    """
    This class is responsible for keeping up the scores of the game & saving each player progress
    Attributes:
        - scores (dict[User:int]): current points of each participating user
    """
    def __init__(self):
        self.scores: dict[User: int] = {}

    def addPoints(self, points: int, player: User) -> None:
        """
        Args:
            points (int): number of points to be added
            player (User): the player who deserves the points. A telebot object which contains all details about him
        """
        self.scores[player] += points

    def getWinner(self) -> User:
        """
        Returns:
            User object representing the player with the highest score from the scores attribute
        """
        winner, maxi = None, 0
        for player, score in self.scores.items():
            if score > maxi:
                winner, maxi = player, score
        return winner

    def displayScores(self) -> str:
        """
        Returns:
            str: a string containing all the scores of the players
        """
        result = "Scoreboard:\n"
        for player, score in self.scores.items():
            # username & lastname might be empty, but firstname never is
            player_name = player.username if player.username else player.first_name
            if player.last_name:
                player_name += ' ' + player.last_name
            result += f'\n{player_name}: {number_to_emoji(score)}'
        return result
