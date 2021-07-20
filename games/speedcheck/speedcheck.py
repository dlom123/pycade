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
from helpers import status_bar, update_tokens, add_commas

NAME = 'Speedcheck'
COST = 2
WINS_PER_LEVEL = 5

exit_flag = None
game_tokens = None
game_username = None
errors = []
level = 0
wins = 0


def init():
    global still_playing, game_tokens, game_username
    global errors, level, wins
    still_playing = True
    errors = []
    level = 0
    wins = 0


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Speedcheck',
        'tokens': add_commas(game_tokens),
        'level': level
    }
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


def get_accuracy(typed_word, secret_word):
    correct = 0
    for t, s in zip(typed_word, secret_word):
        if t == s:
            correct += 1
    extra_letters = max(len(typed_word) - len(secret_word), 0)
    accuracy = max(correct - extra_letters, 0) / len(secret_word)
    return accuracy


def display_substatus():
    progress = wins / WINS_PER_LEVEL
    substatus = (
        f"Level {level} Progress: " +
        f"[{'=' * wins}{' ' * (WINS_PER_LEVEL - wins)}] " +
        f"{int(progress * 100)}%\n"
    )
    print(substatus)


def play(username, tokens):
    init()

    global game_tokens, game_username, still_playing
    global errors, level, wins
    game_tokens = tokens
    game_username = username
    words = {}
    with open('games/speedcheck/longwords.txt', "r") as f:
        for word in f:
            words.setdefault(len(word), [])
            words[len(word)].append(word.strip())
    while still_playing and game_tokens > 0:
        game_tokens -= COST
        update_tokens(game_username, game_tokens)
        word_lengths = sorted(words.keys())[level]
        level_words = words[word_lengths % len(words.keys())]
        time1 = datetime.now()
        secret_word = random.choice(level_words).strip().lower()
        time_to_beat = int(len(secret_word) / 2)
        refresh_screen()
        display_substatus()
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
            accuracy = get_accuracy(
                inputed_word.lower().strip(),
                secret_word
            )
            wins = wins + 1 if accuracy == 1 else 0
            if wins == 5:
                level += 1
                wins = 0
            display_accuracy = round(accuracy * 100, 2)
            reward = int(COST * 2 * accuracy)
            if int(accuracy) == 1:
                message += (
                    f"\n...and accurate too!"
                    f" ({display_accuracy}% accuracy, +{reward} tokens)\n"
                )
            else:
                message += (
                    "\n...but not very accurate!"
                    f" ({display_accuracy}% accuracy, +{reward} tokens)\n"
                )
            game_tokens += reward
            update_tokens(game_username, game_tokens)
        else:
            message += f"\nToo slow! ({display_speed}s)\n"
        refresh_screen()
        display_substatus()
        print(message)
        input_continue_playing()
    return game_tokens
