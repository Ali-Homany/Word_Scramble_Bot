from telebot.types import User
from utils.lookups import number_to_emoji


class ScoreBoard:
    """
    This class is responsible for keeping up the scores of the game & saving each player progress
    Attributes:
        - scores (dict[int, int]): current points of each participating user
        - players (dict[int, User]): maps player_id to player object which saves all player details
    """
    def __init__(self):
        self.scores: dict[int, int] = {}
        self.players: dict[int, User] = {}

    def addPoints(self, points: int, player: User) -> None:
        """
        Args:
            points (int): number of points to be added
            player (User): the player who deserves the points. A telebot object which contains all details about him
        """
        if player.id not in self.scores.keys():
            self.scores[player.id] = points
            self.players[player.id] = player
        else:
            self.scores[player.id] += points

    def getWinner(self) -> str:
        """
        Returns:
            User object representing the player with the highest score from the scores attribute
        """
        if not self.scores:
            return None
        winner_id = max(self.scores, key=self.scores.get)
        winner = self.players[winner_id]
        winner_name = winner.username if winner.username else (winner.first_name + f' {winner.last_name}'*int(winner.last_name is not None))
        return winner_name

    def getMaxScore(self) -> int:
        return max(self.scores.values())

    def displayScores(self) -> str:
        """
        Returns:
            str: a string containing all the scores of the players
        """
        result = "Scoreboard:\n"
        for player_id, score in self.scores.items():
            player = self.players[player_id]
            # username & lastname might be empty, but firstname never is
            player_name = player.username if player.username else (player.first_name + f' {player.last_name}'*int(player.last_name is not None))
            result += f'\n{player_name}: {number_to_emoji(score)}'
        return result
