import os
import random
from helpers import status_bar

# deck dictionary= "card": [number_of_cards, point_value]
DECK = {'A': [4, 1, 11], "2": [4, 2], "3": [4, 3], "4": [4, 4], "5": [4, 5],
        "6": [4, 6], "7": [4, 7], "8": [4, 8], "9": [4, 9], "10": [4, 10],
        "J": [4, 10], "Q": [4, 10], "K": [4, 10]}

still_playing = None
game_tokens = None
game_username = None
current_bet = None
errors = []


def init():
    global still_playing
    still_playing = True
    errors = []


def deal_one(one_hand, deal_deck):
    """Deals a single card"""
    # we can deal 5 of the same card
    one_hand.append(random.choice(list(deal_deck.keys())))
    deal_deck[one_hand[-1]][0] -= 1


def sum_hand(hand):
    """adds the value of all the cards"""
    # TODO: aces not accounted for"""
    score = 0
    for card in hand:
        score += DECK[card][-1]
    if score > 21 and "A" in hand:
        score = 0
        for card in hand:
            if card == "A":
                score += 1
            else:
                score += DECK[card][-1]
    return score


def deal_hands(player_hand, table_hand, table_deck):
    deal_one(player_hand, table_deck)
    deal_one(table_hand, table_deck)
    deal_one(player_hand, table_deck)
    deal_one(table_hand, table_deck)


def deal_new_hand(h, table_deck):
    deal_one(h, table_deck)
    deal_one(h, table_deck)


def draw_table_hand(table_hand, table_deck):
    # print(f"\tDealer: {','.join(table_hand)}", end="")
    while sum_hand(table_hand) < 17:
        deal_one(table_hand, table_deck)
    #     print(f",{table_hand[-1]}")
    # print()


# def winning(player_hand, table_hand):
#     """poorly named"""
#     print(f"Player's hand:{player_hand} score of {sum_hand(player_hand)}")
#     print(f"Dealer's hand:{table_hand} score of {sum_hand(table_hand)}")
#     # if d<p<=21:
#     if sum_hand(table_hand) < sum_hand(player_hand) <= 21:
#         print("winning")
#         return True
#     if len(player_hand) >= 5:
#         print("winning")
#         return True
#     print("lost")


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Blackjack',
        'tokens': game_tokens
    }
    if current_bet:
        items['current_bet'] = current_bet
    status = status_bar(**items)
    print(f"{status}\n")


def play(username, tokens):
    init()

    global game_tokens, game_username, still_playing
    global current_bet, errors
    game_tokens = tokens
    game_username = username

    """ runtime loop managing the game state """
    table_deck = DECK
    # shuffle the deck before dealing
    random.shuffle(list(table_deck.keys()))
    table_hand = []
    player_hand = []

    # game loop
    while still_playing and game_tokens > 0:
        # if the hand is empty deal 2 cards
        if not player_hand:
            invalid_bet = True
            while invalid_bet:
                refresh_screen()
                if errors:
                    print(f"{errors[0]}")
                    errors.clear()
                try:
                    tmp_bet = int(input("Enter bet: "))
                    if tmp_bet > game_tokens:
                        errors.append("Cannot bet more tokens than you have.")
                        continue
                    elif tmp_bet <= 0:
                        errors.append("Invalid bet.")
                        continue
                except Exception:
                    errors.append("Invalid bet.")
                    continue
                invalid_bet = False
                current_bet = tmp_bet
            refresh_screen()
            deal_hands(player_hand, table_hand, table_deck)
        if sum_hand(player_hand) <= 21:
            tmp_table_hand = ['?'] + table_hand[1:]
            print(
                f"Dealer's hand: {','.join(tmp_table_hand)}")
            print((
                "Player's hand: "
                f"{','.join(player_hand)} ({sum_hand(player_hand)})"
            ))
            print()
            player_said = input(
                "Would you like to hit or stay? (h/s) ")
            if player_said.lower() == "hit" or player_said.lower() == "h":
                deal_one(player_hand, table_deck)
                continue
            if player_said.lower() == "stay" or player_said.lower() == "s":
                """ go on with the loop """
                pass
            else:
                continue
        else:
            print('You broke!\n')

        draw_table_hand(table_hand, table_deck)

        # this part of the loop checks for wins or loses
        # then it waits for a responce to redeal or exit
        if sum_hand(table_hand) < sum_hand(player_hand) <= 21:
            winnings = current_bet * 2
            game_tokens += winnings
            current_bet = None
            refresh_screen()
            message = f"You won {winnings} token"
            if winnings != 1:
                message += 's'
            print(f"{message}! :)\n")
            print((
                "Dealer's hand: "
                f"{','.join(table_hand)} ({sum_hand(table_hand)})"
            ))
            print((
                "Player's hand: "
                f"{','.join(player_hand)} ({sum_hand(player_hand)})"
            ))
            player_said = input("\nPlay again? (y/n) ")
            player_hand.clear()
            table_hand.clear()
            if player_said.lower() == "no" or player_said.lower() == "n":
                still_playing = False
            continue
        elif sum_hand(table_hand) > 21 and sum_hand(player_hand) <= 21:
            winnings = current_bet * 2
            game_tokens += winnings
            current_bet = None
            refresh_screen()
            message = f"You won {winnings} token"
            if winnings != 1:
                message += 's'
            print(f"{message}! :)\n")
            print((
                "Dealer's hand: "
                f"{','.join(table_hand)} ({sum_hand(table_hand)})"
            ))
            print((
                "Player's hand: "
                f"{','.join(player_hand)} ({sum_hand(player_hand)})"
            ))
            player_said = input("\nPlay again? (y/n) ")
            player_hand.clear()
            table_hand.clear()
            if player_said.lower() == "no" or player_said.lower() == "n":
                still_playing = False
            continue
        elif len(player_hand) >= 5 and sum_hand(player_hand) <= 21:
            winnings = current_bet * 2
            game_tokens += winnings
            current_bet = None
            refresh_screen()
            message = f"You won {winnings} token"
            if winnings != 1:
                message += 's'
            print(f"{message}! :)\n")
            print((
                "Dealer's hand: "
                f"{','.join(table_hand)} ({sum_hand(table_hand)})"
            ))
            print((
                "Player's hand: "
                f"{','.join(player_hand)} ({sum_hand(player_hand)})"
            ))
            player_said = input("\nPlay again? (y/n) ")
            player_hand.clear()
            table_hand.clear()
            if player_said.lower() == "no" or player_said.lower() == "n":
                still_playing = False
            continue

        game_tokens -= current_bet
        current_bet = None
        refresh_screen()
        print("You lose :(\n")
        print((
            "Dealer's hand: "
            f"{','.join(table_hand)} ({sum_hand(table_hand)})"
        ))
        print((
            "Player's hand: "
            f"{','.join(player_hand)} ({sum_hand(player_hand)})"
        ))
        player_said = input("\nPlay again? (y/n) ")
        if player_said.lower() == "n":
            still_playing = False
        player_hand.clear()
        table_hand.clear()
    # TODO: reset globals to their initial values so that the next time
    #       this game is launched it is reinitialized

    return game_tokens


if __name__ == '__main__':
    play()


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
