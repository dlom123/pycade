# 1. Display a numbered list of available games and token total
# 2. Choose a game
# 3. Play that game
#       - exit at any time by entering "exit"

import hashlib
import importlib
import os

from helpers import con, cur, status_bar

START_TOKENS = 100
DISABLED = ['poker', 'wheel-of-python']
available_games = sorted(
    [game for game in os.listdir('games')
     if game not in DISABLED
        and game != 'leaderboard']
)
available_games.append('leaderboard')
games = {}
for game_name in available_games:
    mod = importlib.import_module(f"games.{game_name}.{game_name}")
    games[mod] = {
        'name': mod.NAME,
        'cost': mod.COST
    }
tokens = 0
username = None
errors = []


def main():
    while True:
        os.system('clear')
        choice = show_main_menu()
        if choice.lower() == 'q':
            break
        main_menu_choices[int(choice)]()
    con.close()


def show_main_menu():
    os.system('clear')
    print_banner("Main Menu")
    print("1. Log in")
    print("2. Create account")
    print()
    choice = input("Choose an option ('q' to quit): ")

    return choice


def show_game_menu():
    error = None
    while True:
        os.system('clear')
        if error:
            print(f"{error}\n")
        print(f"{status_bar(tokens=tokens, username=username)}\n")
        print_banner("Games")
        for i, game in enumerate(games.values()):
            name, cost = game['name'], game['cost']
            name_string = f"{i+1:>2}. {name}"
            cost_string = "FREE to play" if not cost else f"({cost} tokens to play)"
            game_string = f"{name_string:<20} {cost_string}"
            print(game_string)
        print()
        choice = input(
            f"Choose a game (1-{len(games)} or 'q' to quit): ")
        if choice.isdigit() and 0 < int(choice) <= len(games):
            break
        elif choice.lower() == 'q':
            return
        error = "Invalid choice. Please enter a valid number."

    play_game(int(choice))


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
    os.system('clear')
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
    game_choice = available_games[game_number-1]
    for mod, game in games.items():
        game_choice = game_choice.replace("-", " ").replace("_", " ")
        if game_choice.lower() == game['name'].lower():
            tokens = mod.play(username, tokens)

    show_game_menu()


main_menu_choices = {
    1: login,
    2: create_account
}


if __name__ == '__main__':
    main()
