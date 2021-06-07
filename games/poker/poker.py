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

#player and table tokens
game_tokens = 0
player_tokens = 1000
table_tokens = 1000
# win conditions in order of importance
# s_flush: five cards of the same suit in sequence
# four_kind: Four cards of the same rank (e.g. A♣, A♠, A♥, A◆)
# full_house: three cards of one rank and two cards of another rank
# flush: Five cards of the same suit.
# straight: Five cards of mixed suits in sequence
# three_kind: Three cards of the same rank plus two unequal cards
# two_pairs: two cards of equal rank
# 

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
    global player_tokens
    global table_tokens
    random_deck = build_deck()
    random.shuffle(random_deck)
    player_hand = []
    # deal the hands"
    computer_hand = []
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
    place_bets = input("starting bet is 10 tokens.  Do you wish to proceed?")
    if place_bets.lower() == "yes" or place_bets.lower() == "y":
        player_tokens -= 10
        table_pot += 10
        while loop < 3:
            print(f"Current pot: {table_pot}")
            print(
                f"""here is your hand of {5} cards: {player_hand} \n computerhand: {[ "**" for _ in computer_hand]}""")
            mulligan_choices = input(
                "what are the indices of the cards you want to mulligan in a csv or 'n': ")
            if mulligan_choices == "n":
                print("ok you can keep those cards")
                continue
            else:
                for choice in mulligan_choices.split(","):
                    player_hand[int(choice)] = random_deck.pop()
                print(player_hand)
                fold_or_stay = input("Fold or stay?: ")
                if fold_or_stay.lower() == "fold" or fold_or_stay[0].lower() == "f":
                    break
                raised_or_call = input("Are you going to raise or call? ")
                if raised_or_call.lower() == "r" or raised_or_call.lower() == "raise":
                    auntie = input("Up your ante: ")
                    while auntie:
                        try:
                            while int(auntie) > player_tokens:
                                auntie = input("Too big for your britches.  Bet in your range: ")
                            player_tokens -= int(auntie)
                            table_pot += int(auntie)
                            break
                        except (ValueError):
                            auntie = input("That's not a number.  What's your ante?: ")
                else:
                    player_tokens -= auntie
                    table_pot += auntie
            loop += 1
    # fix the computer hand for printing
    # computer_hand.clear()
    # may need to be sooner.
    # while len(computer_hand) < num:
    #     computer_hand.append(random_deck.pop())
        print(
            f"here is your hand of {5} cards: {player_hand} \n computerhand: {computer_hand}")
    print("Come back when you have the tokens")


def play(username, tokens):
    """Main program code."""
    global game_tokens
    game_tokens = tokens
    pokerdealer()
    # TODO: reset globals to their initial values so that the next time
    #       this game is launched it is reinitialized

    return game_tokens

if __name__ == '__main__':
    play()
