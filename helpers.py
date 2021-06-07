import re


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
