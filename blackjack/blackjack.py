import random
# dictionary = {"key": value}

# dictionary["key"] = value

# deck dictionary= "card": [number_of_cards, point_value]
deck = {'A': [4, 1, 11], "2": [4, 2], "3": [4, 3], "4": [4, 4], "5": [4, 5],
        "6": [4, 6], "7": [4, 7], "8": [4, 8], "9": [4, 9], "10": [4, 10],
        "J": [4, 10], "Q": [4, 10], "K": [4, 10]}


def deal(one_hand, deal_deck):
    one_hand.append(random.choice(list(deal_deck.keys())))
    deal_deck[one_hand[-1]][0] -= 1


def sum_hand(hand):
    return sum([deck[card][-1] for card in hand])


def black_jack():
    table_deck = deck
    random.shuffle(list(table_deck.keys()))
    table_hand = []
    player_hand = []
    deal(player_hand, table_deck)
    deal(table_hand, table_deck)
    deal(player_hand, table_deck)
    deal(table_hand, table_deck)
    while sum_hand(player_hand) < 21:
        sum_hand(player_hand)
        print(f"Current hand:{player_hand}")
        player_said = input("Would you like to hit or stay?")
        if player_said.lower() == "hit" or player_said.upper() == "H":
            deal(player_hand, table_deck)
        print(f"broke: {sum_hand(player_hand)}, {player_hand}")


black_jack()
