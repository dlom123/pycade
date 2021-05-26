import random
import time
import os

# The list of all possibilities that each slot can land on
possibilities = ["🍉", "7", "🍇", "💎", "🍒", "🍊", "🔔", "🍋", "🍀", "🥇", "💖", "🧲", "BAR"]

# Slots to roll when we pull the lever
slots = [None, None, None]
money = 0
roll_bet = 0
exit_flag = False


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
    temp_slots = [None, None, None]
    for _ in range(rolls):
        os.system('clear')
        for index in range(len(temp_slots)):
            temp_slots[index] = random.choice(possibilities)
        print(f"{temp_slots[0]} | {temp_slots[1]} | {temp_slots[2]}")
        time.sleep(.5)

    os.system('clear')
    print(f"{slots[0]} | {slots[1]} | {slots[2]}")


def input_money():
    """
    Get the users input for how much money they are going to have in total
    to begin placing bets on each roll

    we do some checks to make sure they input an actual numeric string, and
    that the amount of money they put in is greater than 0
    """
    global money
    str_money = input("How much money would you like to deposit: ")

    if str_money.isnumeric():
        money = int(str_money)
        if money <= 0:
            print("Please enter a number greater than 0 to begin playing")
            input_money()
    else:
        print("Please enter a numeric string")
        input_money()


def input_roll_bet():
    """
    For each roll we ask the player to bet some money on that roll, then
    subtract that amount from the total amount of money put in
    """
    global roll_bet, money
    str_bet = input("How much money would you like to bet on this roll: ")

    if not str_bet.isnumeric():
        print("Please enter a numeric string")
        input_roll_bet()

    roll_bet = int(str_bet)

    if roll_bet > money:
        print(f"Max possible bet {money}")
        input_roll_bet()

    money -= roll_bet


def input_continue_playing():
    """
    Make sure the player has enough money to continue playing, then ask them
    if they would like to continue playing, or walk away.
    """
    global exit_flag
    if money <= 0:
        exit_flag = True
        print("Thank you for playing, youre broke now!")
        return

    continue_playing = input("Would you like to keep playing? (y/n)")

    if continue_playing == "n":
        exit_flag = True
        return


def check_rewards():
    """
    Check how the slots were rolled to see if we should reward the player.
    Then display how much money they have in total
    """
    global money
    if slots[0] == slots[1] == slots[2]:
        print(f"Winner, Winner, Chicken Dinner!! You won {roll_bet * 4}")
        money += roll_bet * 4
    elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
        print(f"Winner, Winner! You won {roll_bet * 3}")
        money += roll_bet * 3

    print(f"You now have {money} in total!")


def main():
    input_money()

    while not exit_flag:
        # Ask how much they want to bet on a roll
        input_roll_bet()
        # Roll the slots
        roll()
        # check rewards
        # Modify amount of money the player has in the game
        check_rewards()
        # Check to see if the player can and wants to continue playing
        input_continue_playing()


if __name__ == "__main__":
    main()
