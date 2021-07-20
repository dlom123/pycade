# red = 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
# black = 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
import random
import helpers
import os
from helpers import status_bar, add_commas

NAME = 'Roulette'
COST = 0
COLUMNS = {
    "1": [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
    "2": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    "3": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
}
DOZENS = {
    "1": list(range(1, 13)),
    "2": list(range(13, 25)),
    "3": list(range(25, 37))
}
# This is EU roulette, Metric system > Imperial system

exit_flag = None
game_tokens = 0
game_username = None
current_bet = 0

possible_bets = [
    'red',
    'black',
    'c1',
    'c2',
    'c3',
    'd1',
    'd2',
    'd3',
    'high',
    'low',
    'odd',
    'even'
] + [str(i) for i in range(37)]


def init():
    global exit_flag
    exit_flag = False


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Roulette',
        'tokens': add_commas(game_tokens)
    }
    if current_bet:
        items['current_bet'] = current_bet
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


def num_col_combo():
    roll = {
        "red": [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],  # noqa: E501
        "black": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],  # noqa: E501
        "green": [0]
    }
    number = random.choice(range(0, 37))
    color = ""
    for c in roll:
        if number in roll[c]:
            color = c
    return color, number


def get_outcome_bet():
    """
    This function explains how a user can place a bet, and returns the bet
    the user places
    """
    refresh_screen()
    print((
        "To place a bet you can enter:\n"
        "\t- a color (e.g. 'red' or 'black')\n"
        "\t- a number (e.g. '1' or '16')\n"
        "\t- odd or even (e.g. if a number is a multiple of 2 or not)\n"
        "\t- high or low (e.g. low: 1-18, high: 19-36)\n"
        "\t- column (to make a column bet)\n"
        "\t- dozens (to make a dozens bet)\n"
        "please visit this link for more in depth information: "
        "https://www.gamblingsites.com/online-casino/games/roulette/bets"
        "\n"
    ))
    outcome = input("Choose a bet: ").lower()
    if outcome == "column":
        refresh_screen()
        print((
            "Please enter a column number (or 'x' to go back):\n"
            "\tColumns:\n"
            f"\t1: {COLUMNS['1']}\n"
            f"\t2: {COLUMNS['2']}\n"
            f"\t3: {COLUMNS['3']}\n"
        ))
        column = input("Choose a column (1-3): ")
        return f"c{column}"
    elif outcome == "dozens":
        refresh_screen()
        print((
            "Please enter a dozens number (or 'x' to go back):\n"
            "\tDozens:\n"
            f"\t1: {DOZENS['1']}\n"
            f"\t2: {DOZENS['2']}\n"
            f"\t3: {DOZENS['3']}\n"
        ))
        dozen = input("Choose a dozen (1-3): ")
        return f"d{dozen}"
    else:
        return outcome


def print_outcome(color, number, message):
    result = f"{color} {number}"
    print(f"\t{'=' * 12}")
    print(f"\t|{message:^10}|")
    print(f"\t{'-' * 12}")
    print(f"\t|{result:^10}|")
    print(f"\t{'=' * 12}")


def win_lose(balance, bet):
    global current_bet, game_tokens
    current_bet = 0
    while True:
        user_input = get_outcome_bet()
        user_input = user_input.lower()
        color, number = num_col_combo()
        if user_input in possible_bets:
            if user_input == color:
                balance += bet
                break
            elif user_input == str(number):
                balance += (bet * 35)
                break
            elif user_input == "odd" and number % 2:
                balance += bet
                break
            elif user_input == "even" and not number % 2:
                balance += bet
                break
            elif user_input == "high" and number > 18:
                balance += bet
                break
            elif user_input == "low" and 0 < number < 19:
                balance += bet
                break
            elif user_input[0] == "c" and number in COLUMNS[user_input[1]]:
                balance += bet * 2
                break
            elif user_input[0] == "d" and number in DOZENS[user_input[1]]:
                balance += bet * 2
                break
            else:
                balance -= bet
                break
        elif user_input != 'cx' and user_input != 'dx':
            refresh_screen()
            print("Please enter a valid option")

    message = "YOU WIN!" if balance > game_tokens else "YOU LOSE"
    game_tokens = balance
    refresh_screen()
    print_outcome(color, number, message)
    print()
    helpers.update_tokens(game_username, balance)


def get_bet(balance):
    global current_bet
    str_bet = input("How many tokens are you betting on this roll: ")
    refresh_screen()
    if not str_bet.isnumeric():
        print("Please enter a numeric amount")
        return get_bet(balance)
    current_bet = int(str_bet)
    if current_bet <= 0:
        print("please enter a bet that is greater than 0")
        return get_bet(balance)
    if current_bet > balance:
        print("Please enter a bet less than your total balance")
        return get_bet(balance)
    return current_bet


def get_continue_playing():
    while True:
        keep_playing = input("Do you want to continue playing? (y/n) ")
        keep_playing = keep_playing.lower()
        refresh_screen()
        if keep_playing == 'y' or keep_playing == 'n':
            break
        else:
            print("Please enter a valid option")

    return keep_playing != "n"


def play(username, tokens):
    init()

    global game_tokens, game_username
    global exit_flag
    game_tokens = tokens
    game_username = username
    while not exit_flag:
        refresh_screen()
        bet = get_bet(game_tokens)
        win_lose(game_tokens, bet)
        if game_tokens <= 0:
            exit_flag = True
            print('You are out of tokens!')
        elif not get_continue_playing():
            exit_flag = True
    input('Thanks for playing! Press any key to return to menu.')

    return game_tokens


if __name__ == '__main__':
    play()
