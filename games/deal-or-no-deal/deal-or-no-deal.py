import os
import random
from helpers import status_bar, update_tokens
import math
import time

NAME = 'Deal Or No Deal'
COST = 5

game_tokens = None
game_username = None
user_suitcase = {}
remaining_cases = None
still_playing = True
suit_cases_values = [
    0,
    1,
    2,
    4,
    6,
    8,
    16,
    24,
    32,
    40,
    48,
    56,
    64,
    128,
    192,
    256,
    320,
    384,
    385,
    400,
    404,
    418,  # teapot
    420,
    500,
    512,
    1337
]
errors = []
current_round = None


def init():
    global game_tokens, user_suitcase, remaining_cases, still_playing
    global errors, current_round
    game_tokens = 0
    still_playing = True
    user_suitcase = {}
    shuffled_values = random.sample(suit_cases_values, len(suit_cases_values))
    remaining_cases = {
        k+1: v
        for k, v in enumerate(shuffled_values)
    }
    errors = []
    current_round = 0


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Deal Or No Deal',
        'tokens': game_tokens
    }
    if user_suitcase:
        items['your_suitcase'] = list(user_suitcase.keys())[0]
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


def get_bankers_offer():
    """
    you take each remaining value and square it. Then you sum up all of these
    squared terms, divide by how many cases are left, then take the square
    root of the whole thing
    """
    global remaining_cases
    sqd_sum = sum([remaining_cases[val] ** 2 for val in remaining_cases])
    return math.floor(((sqd_sum / len(remaining_cases)) ** .5))


def make_bankers_offer():
    """
    gets the bankers offer and then offers it to the player.
    """
    global game_tokens, still_playing
    offer = get_bankers_offer()
    refresh_screen()
    show_remaining_cases(current_round, 0)
    print(f"The banker would like to offer you {offer} to walk away")
    prompt = input("Deal or No Deal!\n")

    if prompt.lower() == "deal":
        still_playing = False
        num = list(user_suitcase.keys())[0]
        val = user_suitcase[num]
        for i in range(1, 4):
            refresh_screen()
            print(f"You chose case: {num}, which contained{'.' * i}")
        print(f"{val} tokens!")
        game_tokens += offer
        input("")


def play(username, tokens):
    """
    This is the main loop of the game
    """
    init()

    global game_tokens, game_username, user_suitcase, still_playing
    global errors, current_round, remaining_cases
    game_tokens = tokens
    game_username = username
    invalid_suitcase = True
    while invalid_suitcase:
        refresh_screen()
        show_remaining_cases(0, 1)
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
    while still_playing:
        current_round += 1
        for case in range(max(6-current_round+1, 1)):
            invalid_suitcase = True
            while invalid_suitcase:
                refresh_screen()
                show_remaining_cases(
                    current_round,
                    max(6 - (current_round - 1) - case, 1))
                if errors:
                    print(f"{errors[0]}")
                    errors.clear()
                try:
                    choice = int(input("Open a suitcase: "))
                    if choice < 1 or choice > len(suit_cases_values):
                        errors.append("Invalid suitcase.")
                        continue
                    elif choice not in remaining_cases:
                        errors.append(f"Suitcase {choice} is not available.")
                        continue
                    invalid_suitcase = False
                except Exception:
                    errors.append("Invalid suitcase.")
                    continue
            popped = remaining_cases.pop(choice)
            print(f"Suitcase {choice} contained {popped}")
            time.sleep(2)

        if len(remaining_cases) > 1:
            make_bankers_offer()
        else:
            still_playing = False

    current_round += 1
    refresh_screen()
    show_remaining_cases(current_round, 0)
    last_case = list(remaining_cases.keys())[0]
    choice_swap = input(
        f"Would you like to swap your case for case #{last_case}? (y/n) ")
    if choice_swap.lower() == 'y':
        user_suitcase, remaining_cases = remaining_cases, user_suitcase
    winnings = list(user_suitcase.values())[0]
    game_tokens += winnings
    other_tokens = list(remaining_cases.values())[0]
    refresh_screen()
    print(f"{'=' * 13:^20}{'=' * 14:^16}")
    print(f"{'|  Your Case  |':^20}{'|  Other Case  |':^15}")
    print(f"{'-' * 13:^20}{'-' * 14:^16}")
    display_your_case = f'|{winnings:^13}|'
    display_other_case = f'|{other_tokens:^14}|'
    print(f"{display_your_case:^20}{display_other_case:^15}")
    print(f"{'=' * 13:^20}{'=' * 14:^16}\n")
    update_tokens(game_username, game_tokens)
    print(f"You won {winnings} tokens!")
    input("\nThanks for playing! Press Enter to return to the main menu.")
    return game_tokens


def show_remaining_cases(round, cases_left_in_round):
    """
    Displays the current game state to the user
    """
    refresh_screen()
    if user_suitcase:
        remaining_values = [v for v in remaining_cases.values()]
        remaining_values += user_suitcase.values()
        remaining_values.sort(reverse=True)
        print("Remaining Suitcase Values:")
        for i in range(len(remaining_values)//10+1):
            print(", ".join([str(v) for v in remaining_values[i*10:i*10+10]]))
    print()
    print(f"Round {round}")
    print(f"Cases Left To Pick: {cases_left_in_round}\n")
    row_sizes = (6, 7, 7, 6)
    for row, width in enumerate(row_sizes):
        offset = sum(row_sizes[0:row+1])
        start = 27 - offset
        row_string = ""
        for col in range(start, start+width):
            if col in remaining_cases:
                row_string += f"{col:>4}"
            else:
                row_string += '    '
        print(f"{row_string:^28}")
    print()


if __name__ == '__main__':
    play('guest', 1000)
