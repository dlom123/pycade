import random

# deck dictionary= "card": [number_of_cards, point_value]
deck = {'A': [4, 1, 11], "2": [4, 2], "3": [4, 3], "4": [4, 4], "5": [4, 5],
        "6": [4, 6], "7": [4, 7], "8": [4, 8], "9": [4, 9], "10": [4, 10],
        "J": [4, 10], "Q": [4, 10], "K": [4, 10]}


def deal_one(one_hand, deal_deck):
    """Deals a single card"""
    one_hand.append(random.choice(list(deal_deck.keys())))
    deal_deck[one_hand[-1]][0] -= 1


def sum_hand(hand):
    """adds the value of all the cards"""
    # TODO: aces not accounted for"""
    return sum([deck[card][-1] for card in hand])


def deal_hands(player_hand, table_hand, table_deck):
    deal_one(player_hand, table_deck)
    deal_one(table_hand, table_deck)
    deal_one(player_hand, table_deck)
    deal_one(table_hand, table_deck)


def deal_new_hand(h, table_deck):
    deal_one(h, table_deck)
    deal_one(h, table_deck)


def draw_table_hand(table_hand, table_deck):
    while sum_hand(table_hand) < 17:
        deal_one(table_hand, table_deck)
        print(f"      Dealer: {sum_hand(table_hand)} {table_hand}")


def winning(player_hand, table_hand):
    """poorly named"""
    print(f"Player's hand:{player_hand} score of {sum_hand(player_hand)}")
    print(f"Dealer's hand:{table_hand} score of {sum_hand(table_hand)}")
    # if d<p<=21:
    if sum_hand(table_hand) < sum_hand(player_hand) <= 21:
        print("winning")
    else:
        print("lost")


def black_jack():
    """ runtime loop managing the game state """
    table_deck = deck
    # shuffle the deck before dealing
    random.shuffle(list(table_deck.keys()))
    table_hand = []
    player_hand = []
    balance = 500


    # game loop
    still_playing = True
    while still_playing and balance > 0:
        # if the hand is empty deal 2 cards
        if not player_hand:
            print(f"Balance: {balance}")
            bet = int(input("Enter bet: "))
            print(f"Current bet: {bet}")
            deal_hands(player_hand, table_hand, table_deck)
            # deal_new_hand(player_hand, table_deck)
        # deal/bet loop/check hand
        if sum_hand(player_hand) <= 21:
            print(f"   Dealer: {['?', table_hand[1]]}")
            print(f"Your hand: {player_hand}")
            player_said = input(
                "Would you like to hit or stay? (hit or h, stay or s) ")
            if player_said.lower() == "hit" or player_said.lower() == "h":
                deal_one(player_hand, table_deck)
                continue
            if player_said.lower() == "stay" or player_said.lower() == "s":
                """ go on with the loop """
                pass
            else:
                continue
                # win_checking?  and reseting the game
        else:
            print('you broke')

        draw_table_hand(table_hand, table_deck)

        # this part of the loop checks for wins or loses
        # then it waits for a responce to redeal or exit
        if sum_hand(table_hand) < sum_hand(player_hand) <= 21:
            balance += bet
            print(
                f"Player's hand: {sum(player_hand)} {player_hand} score of {sum_hand(player_hand)}")
            print(
                f"Dealer's hand: {sum(table_hand)} {table_hand} score of {sum_hand(table_hand)}")
            player_said = input(
                "You Win! \nplay again? (say \"n\" to exit) ")
            player_hand.clear()
            table_hand.clear()
            if player_said.lower() == "no" or player_said.lower() == "n":
                still_playing = False
            continue
        else:
            balance -= bet
            print(
                f"Player's hand:{player_hand} score of {sum_hand(player_hand)}")
            print(
                f"Dealer's hand:{table_hand} score of {sum_hand(table_hand)}")
            player_said = input(
                "You Lose :( \nplay again? (say \"n\" to exit) ")
            if player_said.lower() == "no" or player_said.lower() == "n":
                still_playing = False
            player_hand.clear()


black_jack()


# win conditions
# does it beat the dealers hand.
# does it break 21
# high suit?
# 5 cards

# exceptiong handling around Aces.
# one or 11
# deal in a pair?

# rules for dealer
# always hits unless 17
# 16 is soft
# wins ties

# betting
# split doubles
# split bets again
# multiplayer?
# tokens?
#
