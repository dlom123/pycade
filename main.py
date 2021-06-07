# 1. Display a numbered list of available games and token total
# 2. Choose a game
# 3. Play that game
#       - exit at any time by entering "exit"
import hashlib
import os

from games.blackjack import blackjack
from games.freeplay import freeplay
from games.poker import poker
from games.roulette import roulette
from games.slots import slots

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
    print_banner("Main Menu")
    print("1. Log in")
    print("2. Create account")
    choice = int(input("Choose an option: "))

    return choice


def show_game_menu():
    os.system('clear')
    print_banner("Games")
    print_tokens()
    for i, game in enumerate(available_games):
        print(f"{i+1}. {game.title()}")
    choice = int(input("Choose a game: "))
    play_game(choice)


def make_choice(choices: dict, choice: str):
    os.system('clear')
    choices[choice]()


def login(error: str = ""):
    os.system('clear')
    if error:
        print(error)
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
    login()


def encrypt_password(password):
    encoded = password.encode()
    return hashlib.sha256(encoded).hexdigest()


def print_banner(message):
    print(message)
    print("-" * len(message))


def print_tokens():
    print(f"Tokens: {tokens}\n")


def play_game(game_number):
    global tokens, username
    os.system('clear')
    game = available_games[game_number-1]

    if game == "blackjack":
        tokens = blackjack.play(username, tokens)
    elif game == "freeplay":
        tokens = freeplay.play(username, tokens)
    elif game == "poker":
        tokens = poker.play(username, tokens)
    elif game == "roulette":
        tokens = roulette.play(username, tokens)
    elif game == "slots":
        tokens = slots.play(username, tokens)

    show_game_menu()


main_menu_choices = {
    1: login,
    2: create_account
}


if __name__ == '__main__':
    main()
