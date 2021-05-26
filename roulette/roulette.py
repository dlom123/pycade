# red = 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
# black = 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
import random
exit_flag = False
bet_types = {
    "outside": [
        "red/black",
        "odd/even",
        "high/low",
        "columns",
        "dozens"
    ]
}
columns = {
    "1": [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
    "2": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    "3": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
}
dozens = {
    "1": list(range(1, 13)),
    "2": list(range(13, 25)),
    "3": list(range(25, 37))
}
# This is EU roulette, Metric system > Imperial system
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
             - High or low (e.g. if you expect the number to be above 18 bet high)
             - column (to make a column bet)
             - Dozens (to make a dozens bet)
        please visit this link for more in depth inforamtion: https://www.gamblingsites.com/online-casino/games/roulette/bets/
        """  # noqa E501
    ).lower()
    if outcome == "column":
        column = input(
            f"""
            Please enter a column number:
            Columns:
            1: {columns["1"]}
            2: {columns["2"]}
            3: {columns["3"]}
            """
        )
        return f"c{column}"
    elif outcome == "dozens":
        dozen = input(
            f"""
            Please enter a dozens number:
            Dozens:
            1: {dozens["1"]}
            2: {dozens["2"]}
            3: {dozens["3"]}
            """
        )
        return f"d{dozen}"
    else:
        return outcome
def win_lose(balance, bet):
    user_input = get_outcome_bet()
    user_input = user_input.lower()
    color, number = num_col_combo()
    if user_input == color:
        print(color, number, "YOU WIN!")
        balance += bet
    elif user_input == str(number):
        print(color, number, "YOU WIN!")
        balance += (bet * 35)
    elif user_input == "odd" and number % 2:
        print(color, number, "YOU WIN!")
        balance += bet
    elif user_input == "even" and not number % 2:
        print(color, number, "YOU WIN!")
        balance += bet
    elif user_input == "high" and number > 18:
        print(color, number, "YOU WIN!")
        balance += bet
    elif user_input == "low" and 0 < number < 19:
        print(color, number, "YOU WIN!")
        balance += bet
    elif user_input[0] == "c" and number in columns[user_input[1]]:
        print(color, number, "YOU WIN!")
        balance += bet * 2
    elif user_input[0] == "d" and number in dozens[user_input[1]]:
        print(color, number, "YOU WIN!")
        balance += bet * 2
    else:
        print(color, number, "YOU LOSE!")
        balance -= bet
    return balance
def get_bet(balance):
    str_bet = input("How much Kenzie coin are you betting on this roll: ")
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
def get_deposit_balance():
    """
    Get amount of kenzie coin user would like to input to make
    bets against. Make sure to check for a valid input.
    """
    str_bal = input("How much Kenzie coin would you like to place in the betting pool: ")  # noqa: E501
    if not str_bal.isnumeric():
        print("Please enter a numeric amount greater than 0")
        return get_deposit_balance()
    balance = int(str_bal)
    if balance <= 0:
        print("Please enter a numeric amount greater than 0")
        return get_deposit_balance()
    return balance
def get_continue_playing():
    keep_playing = input("Do you want to continue playing? (y/n)")
    keep_playing = keep_playing.lower()
    return keep_playing != "n"
def main():
    balance = get_deposit_balance()
    global exit_flag
    while not exit_flag:
        bet = get_bet(balance)
        balance = win_lose(balance, bet)
        print(f"Your current balance is: {balance}")
        if balance <= 0 or not get_continue_playing():
            exit_flag = True
if __name__ == '__main__':
    main()
