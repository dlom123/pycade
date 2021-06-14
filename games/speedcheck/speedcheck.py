"""
Speed Check:
    The subject is tested for speed and accuracy for their typing.
    if they are accurate enough they get rewarded (x2)
    if they are fast enough the tokens are returned to them (-1)
    if they are not fast enought the tokens are kept by the house.
 """
from datetime import datetime
import random
import helpers
exit_flag = None
game_tokens = None
game_username = None


def init():
    global still_playing, game_tokens, game_username
    still_playing = True


def input_continue_playing():
    """
    Make sure the player has enough tokens to continue playing, then ask them
    if they would like to continue playing, or walk away.
    Consider moving to helpers shared with other games.
    """
    global still_playing, game_tokens
    if game_tokens <= 0:
        still_playing = False
        print("Thank you for playing, you're broke now!")

    continue_playing = input("Would you like to keep playing? (y/n)")

    if continue_playing == "n":
        still_playing = False


def play(username, tokens):
    init()
    global game_tokens, game_username, still_playing
    game_tokens = tokens
    game_username = username
    words = []
    with open('games/speedcheck/longwords.txt', "r") as f:
        words = f.readlines()
    bet = 0
    while still_playing and game_tokens > 0:
        valid_bet = False
        while not valid_bet:
            bet = int(
                input(
                    f"You have: {game_tokens} tokens, how many will you bet(int):"))
            if bet <= game_tokens and bet >= 0:
                game_tokens -= bet
                helpers.update_tokens(game_username, game_tokens)
                print(f"You've bet {bet} tokens.")
                valid_bet = True
            else:
                print(f"something went wrong")
        print('countdown')  # needs animation
        time1 = datetime.now()
        secret_word = random.choice(words)
        time_to_beat = int(len(secret_word)/2)
        inputed_word = input(
            f"you have {time_to_beat} seconds to type: {secret_word}\n")
        time2 = datetime.now()
        reaction_speed = time2-time1
        print(str(reaction_speed)[-9:])
        # """if you are faster then x seconds you win"""
        if float(str(reaction_speed)[-9:]) < time_to_beat:
            print(f"Wow! {game_username} you are so fast")
            if inputed_word.lower().strip() == secret_word.lower().strip():
                # tiering the score 3x or 1.5x
                print(
                    f"and accurate too, you've earned {bet*2} tokens")
                game_tokens += bet*2
                helpers.update_tokens(game_username, game_tokens)
                input_continue_playing()
                continue
            print(
                f"but not very accurate \nThe word: {secret_word}\nYour word: {inputed_word}")  # noqa
            print(f"returned the balance{game_tokens}")
            # house always wins
            game_tokens += bet-1
            helpers.update_tokens(game_username, game_tokens)
            input_continue_playing()
        else:
            print("You're too slow.")
            print(f"The word: {secret_word}\nYour word: {inputed_word}")
            print(f"balance: {game_tokens}")
            input_continue_playing()
    return game_tokens
