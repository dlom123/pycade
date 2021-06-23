# 1. Display a numbered list of available games and token total
# 2. Choose a game
# 3. Play that game
#       - exit at any time by entering "exit"
import hashlib
import os
import time

from games.battleship import battleship
from games.blackjack import blackjack
from games.deal_or_no_deal import dealornodeal
from games.freeplay import freeplay
from games.poker import poker
from games.roulette import roulette
from games.slots import slots
from games.speedcheck import speedcheck
from helpers import status_bar

START_TOKENS = 100
available_games = sorted(os.listdir('games'))
tokens = 0
username = None


def main():
    # if a 'data' directory does not exist, create it
    if not os.path.exists('data'):
        os.mkdir('data')
    os.system('clear')
    choice = show_main_menu()
    make_choice(main_menu_choices, choice)


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
            print(f"Thanks for playing, {username}!")
            time.sleep(2)
            return
        error = "Invalid choice. Please enter a valid number."

    play_game(int(choice))


def make_choice(choices: dict, choice: str):
    os.system('clear')
    choices[choice]()


def login(error: str = ""):
    os.system('clear')
    if error:
        print(f"{error}\n")
    print_banner("Log In")
    input_username = input("Username: ")
    input_password = input("Password: ")
    # open the accounts file
    found = False
    with open("data/accounts.txt") as f:
        for line in f:
            stored_username, stored_password = line.strip().split(':')
            if input_username == stored_username:
                found = True
                break
    if not found:
        login(error="Invalid login")

    # found a valid username match
    global username
    username = input_username
    encrypted_password = encrypt_password(input_password)
    if encrypted_password != stored_password:
        login(error="Invalid login")
    print("Welcome!")

    # retrieve the user's stored tokens
    global tokens
    with open("data/tokens.txt") as f:
        # find this user's line
        for line in f:
            f_username, num_tokens = line.strip().split(':')
            if f_username == input_username:
                tokens = int(num_tokens)
                break
    show_game_menu()


def create_account():
    print_banner("Create Account")
    username = input("Username: ")
    password = input("Password: ")
    encrypted_password = encrypt_password(password)
    with open("data/accounts.txt", "a") as f:
        f.write(f"{username}:{encrypted_password}\n")

    with open("data/tokens.txt", "a") as f:
        f.write(f"{username}:{START_TOKENS}\n")
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

    show_game_menu()


main_menu_choices = {
    1: login,
    2: create_account
}


if __name__ == '__main__':
    main()
