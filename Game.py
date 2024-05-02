from telebot.types import User
from scoreboard import ScoreBoard
from lookups import choose_letters_combination, convert_time
import time


class GameEndedException (RuntimeError):
    pass


class Game:
    def __init__(self):
        self.scores = ScoreBoard()
        self.letters, self.correct_answers = choose_letters_combination()
        self.prev_answers = []
        self.start_time = time.time()

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
      if len(self.prev_answers) == len(self.correct_answers):
          raise GameEndedException("Game already ended! No more correct answers exist")
  
      if answer in self.prev_answers:
          return 0
  
      if answer not in self.correct_answers:
          return -1
  
      if 2 <= len(answer) <= len(self.letters) - 2:
          points = 1
      else:
          points = 2 + int(len(answer) >= len(self.letters))

      self.prev_answers.append(answer)
      self.scores.addPoints(points, player)
      return points

    def displayGame(self) -> str:
      """
      Returns:
          str: The results of the game when it ends, including the final scoreboard, the winner, and the time it took to complete the game.
      """
      if not self.scoreboard.scores:
        return "There is no winner coz no one played"
      
      # calculate the time taken to complete the game
      total_time = convert_time(time.time() - self.start_time)
  
      winner = self.scores.getWinner()
      scoreboard = self.scores.displayScores()
  
      results = f"Game Over!\n\n"
      results += f"{scoreboard}\n\n"
      results += f"Winner: {winner}\n\n"
      results += f"Time taken: {total_time:.2f}"
  
      return results
  