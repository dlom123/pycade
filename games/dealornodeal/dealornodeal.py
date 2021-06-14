import os
import random
import math
import time
# import helpers

game_tokens = None
game_username = None
user_suitcase = {}
remaining_cases = None
still_playing = True
suit_cases_values = [
    0,
    1,
    2,
    4,
    6,
    8,
    16,
    24,
    32,
    40,
    48,
    56,
    64,
    128,
    192,
    256,
    320,
    384,
    385,
    400,
    404,
    418,  # teapot
    420,
    500,
    512,
    1337
]


def init():
    global game_tokens, user_suitcase, remaining_cases, still_playing
    game_tokens = 0
    still_playing = True
    user_suitcase = {}
    shuffled_values = random.sample(suit_cases_values, len(suit_cases_values))
    remaining_cases = {
        k+1: v
        for k, v in enumerate(shuffled_values)
    }


def get_bankers_offer():
    """
    you take each remaining value and square it. Then you sum up all of these
    squared terms, divide by how many cases are left, then take the square
    root of the whole thing
    """
    global remaining_cases
    sqd_sum = sum([remaining_cases[val] ** 2 for val in remaining_cases])
    return math.floor(((sqd_sum / len(remaining_cases)) ** .5))


def make_bankers_offer():
    global game_tokens, still_playing
    offer = get_bankers_offer()
    print(f"The banker would like to offer you {offer} to walk away")
    prompt = input("Deal or No Deal!\n")

    if prompt.lower() == "deal":
        still_playing = False
        num = list(user_suitcase.keys())[0]
        val = user_suitcase[num]
        for i in range(1, 4):
            os.system("clear")
            print(f"You chose case: {num}, which contained{'.' * i}")
            time.sleep(1)
        print(f"{val} tokens!")
        game_tokens += offer


def play(username, tokens):
    init()

    global game_tokens, game_username, user_suitcase, still_playing
    game_tokens = tokens
    game_username = username
    if tokens < 1000:
        print("You need at least 1000 tokens to play!")
        return game_tokens

    show_remaining_cases(0, 1)
    choice = int(input("Choose a suitcase [1-26]: "))
    popped = remaining_cases.pop(choice)
    user_suitcase[choice] = popped

    cur_round = 0
    while still_playing:
        for case in range(max(6-cur_round, 1)):
            show_remaining_cases(cur_round + 1, max(6-cur_round, 1) - case)
            choice = int(input("Open a suitcase: "))
            popped = remaining_cases.pop(choice)
            print(f"That case contained {popped}")
            time.sleep(1)

        make_bankers_offer()
        cur_round += 1
        if len(remaining_cases) <= 1:
            still_playing = False
        # 1. pick a case to reveal
        # 2. reveal that case
        # 3. banker makes an offer
        #     user chooses to "deal" or "no deal"
        #     "no deal" - repeat from step 1
        #     "deal" - player earns the amount of tokens offered by the banker
        #         reveal their chosen suitcase

    print(game_tokens)
    return game_tokens


def show_remaining_cases(round, cases_left_in_round):
    os.system('clear')
    print(f"Round: {round}, Cases Left To Pick: {cases_left_in_round}\n")
    row_sizes = (6, 7, 7, 6)
    for row, width in enumerate(row_sizes):
        offset = sum(row_sizes[0:row+1])
        start = 27 - offset
        row_string = ""
        for col in range(start, start+width):
            if col in remaining_cases:
                row_string += f"{col:>4}"
            else:
                row_string += '    '
        print(f"{row_string:^28}")
    print()


if __name__ == '__main__':
    play('guest', 1000)
