import os
import random
from helpers import status_bar

game_tokens = None
game_username = None
user_suitcase = {}
remaining_cases = None
suit_cases_values = [
    0,
    1,
    5,
    10,
    25,
    50,
    75,
    100,
    200,
    300,
    400,
    500,
    750,
    1_000,
    5_000,
    10_000,
    25_000,
    50_000,
    75_000,
    100_000,
    200_000,
    300_000,
    400_000,
    500_000,
    750_000,
    1_000_000
]
errors = []


def init():
    global game_tokens, user_suitcase, remaining_cases
    global errors
    game_tokens = 0
    user_suitcase = {}
    shuffled_values = random.sample(suit_cases_values, len(suit_cases_values))
    remaining_cases = {
        k+1: v
        for k, v in enumerate(shuffled_values)
    }
    errors = []


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Deal Or No Deal',
        'tokens': game_tokens
    }
    status = status_bar(**items)
    print(f"{status}\n")


def play(username, tokens):
    init()

    global game_tokens, game_username, user_suitcase
    global errors
    game_tokens = tokens
    game_username = username
    # if tokens < 1000:
    #     print("You need at least 1000 tokens to play!")
    #     return game_tokens
    invalid_suitcase = True
    while invalid_suitcase:
        refresh_screen()
        show_remaining_cases()
        if errors:
            print(f"{errors[0]}")
            errors.clear()
        try:
            choice = int(input("Choose a suitcase [1-26]: "))
            if choice < 1 or choice > len(suit_cases_values):
                errors.append("Invalid suitcase.")
                continue
            invalid_suitcase = False
        except Exception:
            errors.append("Invalid suitcase.")
            continue

    popped = remaining_cases.pop(choice)
    user_suitcase[choice] = popped

    refresh_screen()
    show_remaining_cases()
    # 1. pick a case to reveal
    choice = int(input("Open a suitcase: "))
    # 2. reveal that case
    # 3. banker makes an offer
        # user chooses to "deal" or "no deal"
        # "no deal" - repeat from step 1
        # "deal" - player earns the amount of tokens offered by the banker
            # reveal their chosen suitcase

    return game_tokens


def show_remaining_cases():
    row_sizes = (6, 7, 7, 6)
    for row, width in enumerate(row_sizes):
        offset = sum(row_sizes[0:row+1])  # 6, 13, 20, 26
        start = 27 - offset
        row_string = ""
        for col in range(start, start+width):
            # i = 27 - (col + offset + 1)
            if col in remaining_cases:
                row_string += f"{col:>4}"
            else:
                row_string += '  '
        print(f"{row_string:^28}")
    print()



if __name__ == '__main__':
    play('guest', 1000)
