import helpers
import os
import random
from helpers import status_bar

NAME = 'Freeplay'
COST = 0
INIT_REWARD = 5
MAX_NUM = 100

still_playing = None
game_tokens = None
game_username = None
errors = []


def init():
    global still_playing, errors
    still_playing = True
    errors = []


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Freeplay',
        'tokens': game_tokens
    }
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


def play(username, tokens):
    init()

    global game_tokens, game_username
    game_tokens = tokens
    game_username = username
    while still_playing:
        r = random.randint(1, MAX_NUM)
        invalid_guess = True
        while invalid_guess:
            refresh_screen()
            if errors:
                print(f"{errors[0]}")
                errors.clear()
            try:
                guess = int(input(f"Guess the number (1-{MAX_NUM}): "))
                if guess < 1 or guess > MAX_NUM:
                    errors.append("Invalid guess.")
                    continue
                invalid_guess = False
            except Exception:
                errors.append("Invalid guess.")
                continue

        distance = abs(r - guess)
        reward = INIT_REWARD - distance
        if reward > 0:
            game_tokens += reward
            helpers.update_tokens(game_username, game_tokens)
        else:
            reward = 0
        refresh_screen()
        print(f"Your guess: {guess}")
        print(f"The number: {r}")
        print(f"\nYou earned {reward} token(s).")
        choice = input("Would you like to play again? (y/n) ")
        if choice.lower() == "n":
            return game_tokens


if __name__ == '__main__':
    play()
