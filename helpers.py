import re


def status_bar(game_name=None, tokens=None, current_bet=None):
    status = ""
    if game_name:
        status += game_name
    if tokens:
        if status:
            status += "\t"
            if len(game_name) > 12:
                status += "\t"
        status += f"Tokens: {tokens}"
    if current_bet:
        if status:
            status += "\t"
        status += f"\tCurrent bet: {current_bet}"
    return status


def update_tokens(username, tokens):
    """Writes the token amount to the tokens file for the given username."""
    with open("data/tokens.txt") as f:
        contents = f.read()

    new_contents = re.sub(
        rf"{username}:\d+",
        f"{username}:{tokens}",
        contents)

    with open("data/tokens.txt", "w") as f:
        f.write(new_contents)
