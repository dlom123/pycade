import sys
import random
# imported random and used it. check
# mulligan? types of poker holdem,
# 5 card etc
# holdem river
# deck of cards 4 suits with 13 cards. check
# betting
# mulligans
# num-of-players
# copy ?


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


def pokerdealer(num):
    """deal a random hand of num cards"""
    random_deck = build_deck()
    random.shuffle(random_deck)
    player_hand = []
    # deal the hands"
    computer_hand = []
    while len(player_hand) < num:
        player_hand.append(random_deck.pop())

    while len(computer_hand) < num:
        computer_hand.append("**")

    for card in computer_hand:
        # hide_it
        pass
    loop = 0
    while loop < 3:
        print(
            f"here is your hand of {num} cards: {random_deck[-num:]} \n computerhand: {computer_hand}")
        mulligan_choices = input(
            "what are the indices of the cards you want to mulligan in a csv or 'n':")
        if mulligan_choices == "n":
            loop = 3
            print("ok you can keep those cards")
            continue
        for choice in mulligan_choices.split(","):
            player_hand[int(choice)] = random_deck.pop()
        loop += 1
    # fix the computer hand for printing
    computer_hand.clear()
    while len(computer_hand) < num:
        computer_hand.append(random_deck.pop())
    print(
        f"here is your hand of {num} cards: {random_deck[-num:]} \n computerhand: {computer_hand}")


def main(args):
    """Main program code."""
    if len(args) != 1:
        print('usage: python pokerhands.py num_of_cards')
        sys.exit(1)

    num = sys.argv[1]
    pokerdealer(int(num))


if __name__ == '__main__':
    main(sys.argv[1:])
