import re


def status_bar(**kwargs):
    # do not display the key name for these
    value_only = ('game')
    status = ""
    for k, v in kwargs.items():
        if k not in value_only:
            title = k.replace('_', ' ').title()
            status += f"{title}: "
        status += f"{v}\t"
        if type(v) == str and len(v) > 12:
            status += "\t"
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
