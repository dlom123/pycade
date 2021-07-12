import random
import time
import os
from helpers import status_bar, update_tokens


# The list of all possibilities that each slot can land on
possibilities = ["🍉", "7", "🍇", "💎", "🍒", "🍊", "🔔", "🍋", "🍀", "🥇", "💖", "🧲", "BAR"]

# Slots to roll when we pull the lever
slots = None
game_tokens = None
game_username = None
current_bet = None
last_roll = None
exit_flag = None
errors = []


def init():
    global slots, game_tokens, current_bet, last_roll
    global exit_flag, errors
    slots = [None, None, None]
    current_bet = 0
    last_roll = None
    exit_flag = False
    errors = []


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Slots',
        'tokens': game_tokens
    }
    if current_bet:
        items['current_bet'] = current_bet
    status = status_bar(**items)
    print(f"{status}\n")


def roll():
    """
    Rolls each individual slot, then display a rolling animation in the terminal
    """
    for index in range(len(slots)):
        slots[index] = random.choice(possibilities)
    display_roll(5)


def display_roll(rolls):
    """
    Displays an animation by rolling temporary slots and displaying them
    temporarily before eventually showing what the actual selections were.

    The rolls variable is how many times we roll the temporary slots before
    displaying the actual rolls of each slot
    """
    global last_roll, current_bet
    temp_slots = [None, None, None]
    for _ in range(rolls):
        refresh_screen()
        for index in range(len(temp_slots)):
            temp_slots[index] = random.choice(possibilities)
        last_roll = f"{temp_slots[0]} | {temp_slots[1]} | {temp_slots[2]}"
        print(last_roll)
        time.sleep(0.5)

    current_bet = 0
    refresh_screen()
    print(f"{slots[0]} | {slots[1]} | {slots[2]}\n")


def input_bet():
    """
    For each roll we ask the player to bet some tokens on that roll, then
    subtract that amount from the total amount of tokens put in
    """
    global current_bet, game_tokens

    invalid_bet = True
    while invalid_bet:
        refresh_screen()
        if errors:
            print(f"{errors[0]}")
            errors.clear()
        try:
            tmp_bet = int(input("How many tokens would you like to bet on this roll: "))
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
    if current_bet > game_tokens:
        print(f"Max possible bet {game_tokens}")
        input_bet()

    game_tokens -= current_bet
    update_tokens(game_username, game_tokens)


def input_continue_playing():
    """
    Make sure the player has enough tokens to continue playing, then ask them
    if they would like to continue playing, or walk away.
    """
    global exit_flag
    if game_tokens <= 0:
        exit_flag = True
        print("Thank you for playing, youre broke now!")
        return

    continue_playing = input("Would you like to keep playing? (y/n) ")

    if continue_playing == "n":
        exit_flag = True
        return


def check_rewards():
    """
    Check how the slots were rolled to see if we should reward the player.
    Then display how many tokens they have in total
    """
    global game_tokens
    if slots[0] == slots[1] == slots[2]:
        message = f"Winner, Winner, Chicken Dinner!! You won {current_bet * 4} token(s)"
        game_tokens += current_bet * 4
        update_tokens(game_username, game_tokens)
    elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
        message = f"Winner, Winner! You won {current_bet * 3} token(s)"
        game_tokens += current_bet * 3
        update_tokens(game_username, game_tokens)
    else:
        message = "You lose!"
    print(message)


def play(username, tokens):
    init()

    global game_tokens, game_username, current_bet
    game_tokens = tokens
    game_username = username
    while not exit_flag:
        refresh_screen()
        # Ask how much they want to bet on a roll
        input_bet()
        # Roll the slots
        roll()
        # check rewards
        # Modify amount of tokens the player has in the game
        check_rewards()
        # Check to see if the player can and wants to continue playing
        input_continue_playing()
        current_bet = 0
    return game_tokens


if __name__ == "__main__":
    play()
