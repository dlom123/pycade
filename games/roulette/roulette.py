# red = 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
# black = 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
import random
import helpers
import os


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
game_tokens = None
game_username = None

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
    outcome = input(
        """
        To place a bet you can enter:
             - a color (e.g. 'red' or 'black')
             - a number (e.g. '1' or '16')
             - odd or even (e.g. if a number is a multiple of 2 or not)
             - high or low (e.g. if you expect the number to be above 18 bet high)
             - column (to make a column bet)
             - dozens (to make a dozens bet)
        please visit this link for more in depth information: https://www.gamblingsites.com/online-casino/games/roulette/bets/
        """  # noqa E501
    ).lower()
    if outcome == "column":
        os.system('clear')
        column = input(
            f"""
            Please enter a column number (or 'x' to go back):
            Columns:
            1: {COLUMNS["1"]}
            2: {COLUMNS["2"]}
            3: {COLUMNS["3"]}

            """
        )
        return f"c{column}"
    elif outcome == "dozens":
        os.system('clear')
        dozen = input(
            f"""
            Please enter a dozens number (or 'x' to go back):
            Dozens:
            1: {DOZENS["1"]}
            2: {DOZENS["2"]}
            3: {DOZENS["3"]}
            """
        )
        return f"d{dozen}"
    else:
        return outcome


def win_lose(balance, bet):
    
    while True:
        user_input = get_outcome_bet()
        user_input = user_input.lower()
        color, number = num_col_combo()
        os.system('clear')
        if user_input in possible_bets:
            if user_input == color:
                print(color, number, "YOU WIN!")
                balance += bet
                break
            elif user_input == str(number):
                print(color, number, "YOU WIN!")
                balance += (bet * 35)
                break
            elif user_input == "odd" and number % 2:
                print(color, number, "YOU WIN!")
                balance += bet
                break
            elif user_input == "even" and not number % 2:
                print(color, number, "YOU WIN!")
                balance += bet
                break
            elif user_input == "high" and number > 18:
                print(color, number, "YOU WIN!")
                balance += bet
                break
            elif user_input == "low" and 0 < number < 19:
                print(color, number, "YOU WIN!")
                balance += bet
                break
            elif user_input[0] == "c" and number in COLUMNS[user_input[1]]:
                print(color, number, "YOU WIN!")
                balance += bet * 2
                break
            elif user_input[0] == "d" and number in DOZENS[user_input[1]]:
                print(color, number, "YOU WIN!")
                balance += bet * 2
                break
            else:
                print(color, number, "YOU LOSE!")
                balance -= bet
                break
        elif user_input != 'cx' and user_input != 'dx':
            print("Please enter a valid option")
            
    helpers.update_tokens(game_username, balance)
    return balance


def get_bet(balance):
    print(f"Tokens: {game_tokens}\n")
    str_bet = input("How many tokens are you betting on this roll: ")
    os.system('clear')
    if not str_bet.isnumeric():
        print("Please enter a numeric amount")
        return get_bet(balance)
    bet = int(str_bet)
    if bet <= 0:
        print("please enter a bet that is greater than 0")
        return get_bet(balance)
    if bet > balance:
        print("Please enter a bet less than your total balance")
        return get_bet(balance)
    return bet


def get_continue_playing():
    while True:
        keep_playing = input("Do you want to continue playing? (y/n)")
        keep_playing = keep_playing.lower()
        os.system('clear')
        if keep_playing == 'y' or keep_playing == 'n':
            break
        else:
            print("Please enter a valid option")

    return keep_playing != "n"


def play(username, tokens):
    init()

    global game_tokens, game_username
    game_tokens = tokens
    game_username = username
    global exit_flag
    while not exit_flag:
        bet = get_bet(game_tokens)
        game_tokens = win_lose(game_tokens, bet)
        print(f"Tokens: {game_tokens}\n")
        if game_tokens <= 0:
            exit_flag = True
            print('You are out of tokens!')
        elif not get_continue_playing():
            exit_flag = True
    input('Thanks for playing! Press any key to return to menu.')  

    return game_tokens


if __name__ == '__main__':
    play()
