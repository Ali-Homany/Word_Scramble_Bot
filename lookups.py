"""
This module contains all the lookups for the bot and other files
"""


class Messages:
    INTRO = lambda group_type: "Hello my friend" + 's' * int(group_type != "private") + "\nI can help you play and compete in Word Scramble Game. Whenever you wanna play, just hit /play."
    START_GAME = lambda letters: f"Game has started!\nTry to create words from those letters:\n{', '.join([l for l in letters])}"
    CORRECT_ANSWER = lambda points: f"Great !\nyou gained {number_to_emoji(points)} points"
    ALREADY_PLAYING = "you are already playing guys, you cannot play 2 games at the same time"


class Keys:
    TOKEN = "token"


def number_to_emoji(number: int) -> str:
    digits = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
    if number >= 10:
        return number_to_emoji(number // 10) + digits[number % 10]
    return digits[number % 10]


def choose_letters_combination() -> list[list]:
    """
    This function opens the json file and chooses a random combination of letters for the game
    Returns:
      list[list]: a list containing 2 elements, first is list of letters, second is list of correct answers
    """
    DATA_JSON = "data.json"
