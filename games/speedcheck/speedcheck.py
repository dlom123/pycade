"""
Speed Check:
    The subject is tested for speed and accuracy for their typing.
    if they are accurate enough they get rewarded (x2)
    if they are fast enough the tokens are returned to them (-1)
    if they are not fast enought the tokens are kept by the house.
 """
from datetime import datetime
import os
import random
from helpers import status_bar, update_tokens

exit_flag = None
game_tokens = None
game_username = None
current_bet = None
errors = []


def init():
    global still_playing, game_tokens, game_username
    global errors, current_bet
    still_playing = True
    current_bet = 0
    errors = []


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Speedcheck',
        'tokens': game_tokens
    }
    if current_bet:
        items['current_bet'] = current_bet
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


def input_continue_playing():
    """
    Make sure the player has enough tokens to continue playing, then ask them
    if they would like to continue playing, or walk away.
    Consider moving to helpers shared with other games.
    """
    global still_playing, game_tokens
    if game_tokens <= 0:
        still_playing = False
        print("Thank you for playing, you're broke now!")

    continue_playing = input("Would you like to keep playing? (y/n) ")

    if continue_playing == "n":
        still_playing = False


def play(username, tokens):
    init()

    global game_tokens, game_username, still_playing
    global errors, current_bet
    game_tokens = tokens
    game_username = username
    words = []
    with open('games/speedcheck/longwords.txt', "r") as f:
        words = f.readlines()
    while still_playing and game_tokens > 0:
        invalid_bet = True
        while invalid_bet:
            refresh_screen()
            if errors:
                print(f"{errors[0]}")
                errors.clear()
            try:
                tmp_bet = int(input("How many tokens will you bet? "))
                if tmp_bet <= 0:
                    errors.append("Invalid bet.")
                    continue
                elif tmp_bet > game_tokens:
                    errors.append("Cannot bet more tokens than you have.")
                    continue
                invalid_bet = False
            except Exception:
                errors.append("Invalid bet.")
                continue
        current_bet = tmp_bet
        game_tokens -= current_bet
        update_tokens(game_username, game_tokens)
        time1 = datetime.now()
        secret_word = random.choice(words)
        time_to_beat = int(len(secret_word) / 2)
        refresh_screen()
        inputed_word = input(
            f"You have {time_to_beat} seconds to type: {secret_word}\n")
        time2 = datetime.now()
        reaction_speed = time2 - time1
        display_speed = str(reaction_speed)[-9:]
        message = (
            f"{'The word':>14}: {secret_word}"
            f"{'You typed':>14}: {inputed_word}\n"
        )
        # """if you are faster then x seconds you win"""
        if float(display_speed) < time_to_beat:
            message += (
                f"\nWow, {game_username}!"
                f" You are so fast! ({display_speed}s)"
            )
            if inputed_word.lower().strip() == secret_word.lower().strip():
                # tiering the score 3x or 1.5x
                message += (
                    "\n...and accurate too!"
                    f" (+{current_bet*2} tokens)\n"
                )
                game_tokens += current_bet * 2
                update_tokens(game_username, game_tokens)
            else:
                message += (
                    "\n...but not very accurate!"
                    f" (+{current_bet-1} tokens)\n"
                )
                # house always wins
                game_tokens += current_bet - 1
                update_tokens(game_username, game_tokens)
        else:
            message += f"\nToo slow! ({display_speed}s)\n"
        current_bet = 0
        refresh_screen()
        print(message)
        input_continue_playing()
    return game_tokens
