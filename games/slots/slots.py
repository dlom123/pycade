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
roll_bet = None
last_roll = None
exit_flag = None


def init():
    global slots, game_tokens, roll_bet, last_roll, exit_flag
    slots = [None, None, None]
    game_tokens = 0
    roll_bet = 0
    last_roll = None
    exit_flag = False


def refresh_screen():
    os.system('clear')
    status = status_bar(game="Slots", tokens=game_tokens)
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
    global last_roll
    temp_slots = [None, None, None]
    for _ in range(rolls):
        refresh_screen()
        for index in range(len(temp_slots)):
            temp_slots[index] = random.choice(possibilities)
        last_roll = f"{temp_slots[0]} | {temp_slots[1]} | {temp_slots[2]}"
        print(last_roll)
        time.sleep(0.5)

    refresh_screen()
    print(f"{slots[0]} | {slots[1]} | {slots[2]}\n")


def input_roll_bet():
    """
    For each roll we ask the player to bet some tokens on that roll, then
    subtract that amount from the total amount of tokens put in
    """
    global roll_bet, game_tokens
    str_bet = input("How many tokens would you like to bet on this roll: ")

    if not str_bet.isnumeric():
        print("Please enter a number.")
        input_roll_bet()

    roll_bet = int(str_bet)

    if roll_bet > game_tokens:
        print(f"Max possible bet {game_tokens}")
        input_roll_bet()

    game_tokens -= roll_bet
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
        message = f"Winner, Winner, Chicken Dinner!! You won {roll_bet * 4} token(s)"
        game_tokens += roll_bet * 4
        update_tokens(game_username, game_tokens)
    elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
        message = f"Winner, Winner! You won {roll_bet * 3} token(s)"
        game_tokens += roll_bet * 3
        update_tokens(game_username, game_tokens)
    else:
        message = "You lose!"

    refresh_screen()
    print(f"{last_roll}\n")
    print(message)


def play(username, tokens):
    init()

    global game_tokens, game_username
    game_tokens = tokens
    game_username = username
    while not exit_flag:
        refresh_screen()
        # Ask how much they want to bet on a roll
        input_roll_bet()
        # Roll the slots
        roll()
        # check rewards
        # Modify amount of tokens the player has in the game
        check_rewards()
        # Check to see if the player can and wants to continue playing
        input_continue_playing()
    # TODO: reset globals to their initial values so that the next time
    #       this game is launched it is reinitialized

    return game_tokens


if __name__ == "__main__":
    play()
