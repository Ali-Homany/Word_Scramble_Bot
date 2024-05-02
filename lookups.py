"""
This module contains all the lookups for the bot and other files
"""


class Messages:
    INTRO = "Hello guys how are you"


class Keys:
    TOKEN = "token"


def choose_letters_combination() -> list[list]:
    """
    This function opens the json file and chooses a random combination of letters for the game
    Returns:
      list[list]: a list containing 2 elements, first is list of letters, second is list of correct answers
    """
    DATA_JSON = "data.json"
