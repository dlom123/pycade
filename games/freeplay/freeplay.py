import helpers
import os
import random
from helpers import status_bar

INIT_REWARD = 5
still_playing = None
game_tokens = None
game_username = None


def init():
    global still_playing
    still_playing = True


def refresh_screen():
    os.system('clear')
    status = status_bar(game_name="Freeplay", tokens=game_tokens)
    print(f"{status}\n")


def play(username, tokens):
    init()

    global game_tokens, game_username
    game_tokens = tokens
    game_username = username
    while still_playing:
        refresh_screen()
        r = random.randint(1, 100)
        guess = int(input("Guess the number (1-100): "))
        distance = abs(r - guess)
        reward = INIT_REWARD - distance
        if reward > 0:
            game_tokens += reward
            helpers.update_tokens(game_username, game_tokens)
        else:
            reward = 0
        print(f"\nYou earned {reward} token(s).")
        choice = input("Would you like to play again? (y/n) ")
        if choice.lower() == "n":
            return game_tokens


if __name__ == '__main__':
    play()
