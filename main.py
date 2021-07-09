# 1. Display a numbered list of available games and token total
# 2. Choose a game
# 3. Play that game
#       - exit at any time by entering "exit"

"""
TODO
- display cost of each game along right side of game menu
"""

import hashlib
import os
import time

from games.battleship import battleship
from games.blackjack import blackjack
from games.crane_game import crane
from games.deal_or_no_deal import dealornodeal
from games.freeplay import freeplay
from games.poker import poker
from games.roulette import roulette
from games.slots import slots
from games.speedcheck import speedcheck
from games.wheel_of_python import wheel
from helpers import con, cur, status_bar

START_TOKENS = 100
DISABLED = ['poker']
available_games = sorted(
    [game for game in os.listdir('games') if game not in DISABLED]
)
tokens = 0
username = None
errors = []


def main():
    os.system('clear')
    choice = show_main_menu()
    make_choice(main_menu_choices, choice)
    con.close()


def show_main_menu():
    os.system('clear')
    print_banner("Main Menu")
    print("1. Log in")
    print("2. Create account")
    print()
    choice = int(input("Choose an option: "))

    return choice


def show_game_menu():
    error = None
    while True:
        os.system('clear')
        if error:
            print(f"{error}\n")
        print(f"{status_bar(tokens=tokens)}\n")
        print_banner("Games")
        for i, game in enumerate(available_games):
            game_title = game.replace("_", " ").title()
            print(f"{i+1}. {game_title}")
        print()
        choice = input(
            f"Choose a game (1-{len(available_games)} or 'q' to quit): ")
        if choice.isdigit() and 0 < int(choice) <= len(available_games):
            break
        elif choice.lower() == 'q':
            print(f"\nThanks for playing, {username}!")
            time.sleep(2)
            return
        error = "Invalid choice. Please enter a valid number."

    play_game(int(choice))


def make_choice(choices: dict, choice: str):
    os.system('clear')
    choices[choice]()


def login(error: str = ""):
    valid_login = False
    while not valid_login:
        os.system('clear')
        if errors:
            print(f"{errors[0]}\n")
            errors.clear()
        print_banner("Log In")

        input_username = input("Username: ")
        input_password = input("Password: ")
        encrypted_password = encrypt_password(input_password)
        cur.execute("""SELECT * FROM accounts
                    WHERE username = ? AND password = ?""",
                    (input_username, encrypted_password))
        account = cur.fetchone()
        if account:
            valid_login = True
        else:
            errors.append("Invalid login")

    account_id = account[0]
    # user has logged in
    global username
    username = input_username

    # retrieve the user's stored tokens
    global tokens
    cur.execute("""SELECT * FROM tokens WHERE account_id = ?""",
                (account_id,))
    r_tokens = cur.fetchone()
    tokens_id, tokens_account_id, tokens_amount = r_tokens
    tokens = tokens_amount
    show_game_menu()


def create_account():
    print_banner("Create Account")
    username = input("Username: ")
    password = input("Password: ")
    encrypted_password = encrypt_password(password)
    cur.execute("""INSERT INTO accounts(username, password) VALUES (?, ?)""",
                (username, encrypted_password))
    con.commit()
    cur.execute("""INSERT INTO tokens(account_id, amount) VALUES (?, ?)""",
                (cur.lastrowid, START_TOKENS))
    con.commit()
    show_main_menu()


def encrypt_password(password):
    encoded = password.encode()
    return hashlib.sha256(encoded).hexdigest()


def print_banner(message):
    print("-" * len(message))
    print(message)
    print("-" * len(message))


def play_game(game_number):
    global tokens, username
    os.system('clear')
    game = available_games[game_number-1]

    if game == "battleship":
        tokens = battleship.play(username, tokens)
    elif game == "blackjack":
        tokens = blackjack.play(username, tokens)
    elif game == "crane_game":
        tokens = crane.play(username, tokens)
    elif game == "deal_or_no_deal":
        tokens = dealornodeal.play(username, tokens)
    elif game == "freeplay":
        tokens = freeplay.play(username, tokens)
    elif game == "poker":
        tokens = poker.play(username, tokens)
    elif game == "roulette":
        tokens = roulette.play(username, tokens)
    elif game == "slots":
        tokens = slots.play(username, tokens)
    elif game == "speedcheck":
        tokens = speedcheck.play(username, tokens)
    elif game == "wheel_of_python":
        tokens = wheel.play(username, tokens)

    show_game_menu()


main_menu_choices = {
    1: login,
    2: create_account
}


if __name__ == '__main__':
    main()
