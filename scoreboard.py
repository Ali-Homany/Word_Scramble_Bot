from telebot.types import User
from lookups import number_to_emoji


class ScoreBoard:
    """
    This class is responsible for keeping up the scores of the game & saving each player progress
    Attributes:
        - scores (dict[User:int]): current points of each participating user
    """
    def __init__(self):
        self.scores: dict[User, int] = {}

    def addPoints(self, points: int, player: User) -> None:
        """
        Args:
            points (int): number of points to be added
            player (User): the player who deserves the points. A telebot object which contains all details about him
        """
        if player.id not in [p.id for p in self.scores.keys()]:
            self.scores[player] = points
        else:
            player = [player for player in self.scores.keys() if player.id == player.id][0]
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

        winner_name = winner.username if winner.username else (winner.first_name + f' {winner.last_name}'*int(winner.last_name is not None))
        return winner_name

    def displayScores(self) -> str:
        """
        Returns:
            str: a string containing all the scores of the players
        """
        result = "Scoreboard:\n"
        for player, score in self.scores.items():
            # username & lastname might be empty, but firstname never is
            player_name = player.username if player.username else (player.first_name + f' {player.last_name}'*int(player.last_name is not None))
            result += f'\n{player_name}: {number_to_emoji(score)}'
        return result
