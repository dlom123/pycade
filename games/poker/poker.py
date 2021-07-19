import os
import random
import sys
from helpers import status_bar
# imported random and used it. check
# mulligan? types of poker holdem,
# 5 card etc
# holdem river
# deck of cards 4 suits with 13 cards. check
# betting
# mulligans
# num-of-players
# copy ?

NAME = 'Poker'
COST = 0

#player and table tokens
game_tokens = None
game_username = None
player_tokens = 1000
table_tokens = 1000
still_playing = False
player_hand = []
computer_hand = []
table_pot = 0

# win conditions in order of importance
# s_flush: five cards of the same suit in sequence
# four_kind: Four cards of the same rank (e.g. A♣, A♠, A♥, A◆)
# full_house: three cards of one rank and two cards of another rank
# flush: Five cards of the same suit.
# straight: Five cards of mixed suits in sequence
# three_kind: Three cards of the same rank plus two unequal cards
# two_pairs: two cards of equal rank
# 

def init():
    global still_playing, player_hand, computer_hand
    still_playing = True
    player_hand = []
    computer_hand = []


def build_deck():
    """build an ordered deck using list comprehensions (thanks"""
    suits = ['♣', '♠', '♥', '◆']
    numbers = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    deck = [[str(num) + str(suit.upper()) for num in numbers]
            for suit in suits]
    new_deck = []
    for suit in deck:
        new_deck += suit
    return new_deck


def pokerdealer():
    """deal a random hand of num cards"""
    global player_tokens, table_tokens, table_pot
    random_deck = build_deck()
    random.shuffle(random_deck)
    # deal the hands"
    while len(computer_hand) < 5:
        player_hand.append(random_deck.pop())
        computer_hand.append(random_deck.pop())

    # while len(computer_hand) < num:
        # computer_hand.append(random_deck.pop())
        # not removing card from the deck
        # computer_hand.append("**")
        # suggestion: actually append card here, display ** in print


# unneccessary for loop? resolved on line 50
    # for card in computer_hand:
    #     card.append("**")
    loop = 0
    table_pot = 10
    auntie = 2
    place_bets = input("Starting bet is 10 tokens. Do you wish to proceed? (y/n) ")
    if place_bets.lower().startswith("y"):
        player_tokens -= 10
        table_pot += 10
        while loop < 3:
            display_table()
            mulligan_choices = input(
                "Which card(s) would you like to mulligan? ('n' or card position(s) e.g. 2,4,5): ")
            if mulligan_choices == "n":
                continue
            else:
                for choice in mulligan_choices.split(","):
                    player_hand[int(choice)-1] = random_deck.pop()
                display_table()
                fold_or_stay = input("Fold or stay? (f/s) ")
                if fold_or_stay.lower().startswith("f"):
                    break
                display_table()
                raised_or_call = input("Are you going to raise or call? (r/c) ")
                if raised_or_call.lower().startswith("r"):
                    auntie = input("Up your ante: ")
                    while auntie:
                        try:
                            while int(auntie) > player_tokens:
                                display_table()
                                auntie = input("Too big for your britches. Bet within your available token amount: ")
                            player_tokens -= int(auntie)
                            table_pot += int(auntie)
                            break
                        except (ValueError):
                            display_table()
                            auntie = input("That's not a number. What's your ante?: ")
                else:
                    player_tokens -= auntie
                    table_pot += auntie
            loop += 1
    # fix the computer hand for printing
    # computer_hand.clear()
    # may need to be sooner.
    # while len(computer_hand) < num:
    #     computer_hand.append(random_deck.pop())
        display_table()
    print("Come back when you have the tokens!")


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Poker',
        'tokens': game_tokens
    }
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


def display_table():
    refresh_screen()
    print(f"Current pot: {table_pot}\n")
    print((
        f"Player's hand: {player_hand}\n"
        f"Dealer's hand: {[ '**' for _ in computer_hand]}\n"
    ))


def play(username, tokens):
    """Main program code."""
    init()

    global game_tokens, game_username
    game_tokens = tokens
    game_username = username
    refresh_screen()
    pokerdealer()

    return game_tokens

if __name__ == '__main__':
    play()
