import os
from helpers import status_bar, get_all_accounts

game_tokens = None
rank = None


def show(username, tokens):
    global game_tokens, rank
    game_tokens = tokens
    accounts = get_all_accounts()
    board = []
    for i, account in enumerate(accounts, start=1):
        account_username, account_tokens = account
        if account_username == username:
            rank = i
            if i > 10:
                break
        if i <= 10:
            board.append(f"{i:>2}. {account_username:<12} {account_tokens}")
    refresh_screen()
    print("\n".join(board))
    input("\nPress Enter to return to the main menu.")


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Leaderboard',
        'tokens': game_tokens,
        'rank': rank
    }
    status = status_bar(**items)
    print(f"{status}\n")


if __name__ == '__main__':
    show()
