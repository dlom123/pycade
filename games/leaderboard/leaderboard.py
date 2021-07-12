import os
from helpers import status_bar, get_all_accounts

game_username = None
game_tokens = None
rank = None


def show(username, tokens):
    global game_tokens, game_username, rank
    game_tokens = tokens
    game_username = username
    accounts = get_all_accounts()
    board = []
    for i, account in enumerate(accounts, start=1):
        account_username, account_tokens = account
        if account_username == game_username:
            rank = i
            if i > 10:
                break
        if i <= 10:
            board.append(f"{i:>2}. {account_username:<12} {account_tokens}")
    refresh_screen()
    print("\n".join(board))
    input("\nPress Enter to return to the main menu.")
    return game_tokens


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Leaderboard',
        'tokens': game_tokens,
        'rank': rank
    }
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


if __name__ == '__main__':
    show()
