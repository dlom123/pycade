import random
import os
import time
from string import ascii_uppercase as au

still_playing = None
game_tokens = 30
game_username = "user"


def init():
    global still_playing
    still_playing = True


def get_words(number):
    with open(os.path.abspath('games/speedcheck/longwords.txt')) as f:
        selections = [word for word in f.read().split() if len(word) > 1]
    result_selection = []
    while len(result_selection) < number:
        result_selection.append(random.choice(selections))
    return result_selection


def blank_it(word_selection):
    return " ".join(["".join(["█" for _ in word]) for word in word_selection])


def play(username, tokens):
    global game_tokens, game_username, still_playing
    first_level = list(au[:13])
    second_level = list(au[13:])
    game_tokens = tokens
    game_username = username
    init()
    print(f"Wheel of Fortune\tTokens: {game_tokens}\n")
    print("WHEEL")
    time.sleep(1)
    print("OF")
    time.sleep(1)
    print("FORTUNE!")
    time.sleep(2)
    print("\n")
    decision = input("Would you like to play?[y/n] ")
    if decision.lower() == "y":
        tries = input("Please submit the amount of tokens (7 guesses per token) ")
        while tries:
            try:
                int(tries)
                break
            except Exception:
                tries = input("Please submit an integer")
        n = int(tries)*7
        game_tokens -= int(tries)
        num_words = input("How many words would you like to queue?")
        while num_words:
            try:
                int(num_words) >= 1
                break
            except Exception:
                num_words = input("Please submit an integer")
        num_words = int(num_words)
        selection = get_words(num_words)
        redacted = blank_it(selection)
        while n > 0:
            print("Here are your letters")
            [print(letter, end=" ") for letter in first_level]
            print("")
            print(" ", end="")
            [print(letter, end=" ") for letter in second_level]
            print('')
            print("What  ?")
            [print(redact, end='') for redact in redacted]


if __name__ == '__main__':
    play(game_username, game_tokens)