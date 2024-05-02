from telebot.types import User
from scoreboard import ScoreBoard
from lookups import choose_letters_combination, number_to_emoji
import time


class GameEndedException(RuntimeError):
    pass


class Game:
    def __init__(self):
        self.scores = ScoreBoard()
        self.letters, self.correct_answers = choose_letters_combination()
        self.prev_answers = []
        self.start_time = time.time()

    def addPoints(self, player, answer):
        """
        Add points to the player based on the correctness of the answer.

        Args:
            player (str): The player's name.
            answer (str): The answer provided by the player.

        Returns:
            int: The points awarded to the player.

        Raises:
            GameEndedException: If the game has already ended.

        """
        if len(self.prev_answers) == len(self.correct_answers):
            raise GameEndedException("Game already ended! No more correct answers exist")

        if answer in self.prev_answers:
            return 0

        if not self.wordLettersSubset(answer) or answer not in self.correct_answers:
            return -1

        if 2 <= len(answer) <= len(self.letters) - 2:
            points = 1
        elif len(answer) <= len(self.letters) - 1:
            points = 2
        else:
            points = 3

        self.prev_answers.append(answer)

        self.scores.addPoints(points, player)
        return points

    def wordLettersSubset(self, answer):
        """
        Check if all the letters of a word are a subset of the letters available.

        Args:
            answer (str): The word to check.

        Returns:
            bool: True if all the letters of the word are a subset of the available letters, False otherwise.

        """
        # Convert both strings to sets of characters
        # note : we can do this word set conversion from start, better than converting it
        word_set = set(answer)
        letters_set = set(self.letters)

        # Check if the set of characters of 'word' is a subset of the set of characters of 'letters'
        return word_set.issubset(letters_set)


    def displayGame(self) -> str:
        """
        Returns:
            str: The results of the game when it ends, including the final scoreboard, the winner, and the time it took to complete the game.
        """
        # Calculate the time taken to complete the game
        end_time = time.time()
        total_time = end_time - self.start_time

        winner = self.scores.getWinner()
        scoreboard = self.scores.displayScores()

        results = f"Game Over!\n\n"
        results += f"{scoreboard}\n\n"
        results += f"Winner: {winner}\n\n"
        results += f"Time taken: {total_time:.2f} seconds"

        return results
