import time
from telebot.types import User
from utils.scoreboard import ScoreBoard
from utils.lookups import choose_letters_combination, convert_time, MAX_DURATION


class GameEndedException (RuntimeError):
    pass


class Game:
    def __init__(self, is_single_player: bool=False):
        self.scores = ScoreBoard()
        self.letters, self.correct_answers = choose_letters_combination()
        self.prev_answers = []
        self.start_time = time.time()
        self.active = True
        self.is_single_player = is_single_player

    def addPoints(self, player: User, answer: str) -> int:
        """
        This function adds points to the player based on the validity of the answer.

        Args:
            - player (User): The player's name.
            - answer (str): The answer provided by the player.

        Returns:
            int: The points awarded to the player.

        Raises:
            GameEndedException: If the game has already ended.
        """
        if time.time() - self.start_time >= MAX_DURATION:
            self.active = False
            raise GameEndedException("Game maximum duration has ended")

        if answer in self.prev_answers:
            return 0

        if answer not in self.correct_answers or len(answer) < 3:
            return -1

        points = len(answer) - 3 + int(len(answer) == 3)

        self.prev_answers.append(answer)
        self.scores.addPoints(points, player)
        if len(self.prev_answers) == len(self.correct_answers):
            self.active = False
            raise GameEndedException("Game already ended! No more correct answers exist")

        return points

    def displayGame(self) -> str:
        """
        Returns the game results, including the final scoreboard, winner, and time taken to complete the game.
        In single-player mode, returns a simplified message with only the final score.
        """
        if self.is_single_player:
            return f'Game Over\nYou scored {self.scores.getMaxScore()}'
        if not self.scores.scores:
            return "Game Over! There is no winner"

        # calculate the time taken to complete the game
        total_time = time.time() - self.start_time

        winner = self.scores.getWinner()
        scoreboard = self.scores.displayScores()

        results = f"Game Over!\n\n"
        results += f"{scoreboard}\n\n"
        results += f"Winner: {winner}\n\n"
        results += f"Time taken: {convert_time(total_time)}"

        return results
