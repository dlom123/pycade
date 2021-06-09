"""
place a message in the terminal
take x tokens
return x*score.

ready set (delay) random time (1 - 3 seconds)
  marking the time
post to terminal "go"
wait for input ()
  marking the time
calculate how long it took
    second time - first time = how long it took (par 2 seconds)

 """
import time
from datetime import datetime
import random
exit_flag = None
game_tokens = None
game_username = None


def init():
    global exit_flag, game_tokens, game_username, time
    exit_flag = False


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

    continue_playing = input("Would you like to keep playing? (y/n)")

    if continue_playing == "n":
        exit_flag = True
        return


def play(username, tokens):
    init()
    global game_tokens
    game_tokens = tokens
    game_username = username

    bet = 0
    while not exit_flag:
        bet = int(input("How many tokens will you bet?(int)"))
        # if bet <= game_tokens and bet >= 0:
        #     pass
        # helpers.update_tokens(game_username, game_tokens-bet)
        print('countdown')  # needs animation
        time.sleep(random.randint(1, 3))
        time1 = datetime.now()  # check the time
        input("go\n====\n")  # take input
        time2 = datetime.now()  # check the time
        print(f"time1:{time1} \ntime2: {time2}")
        reaction_speed = time2-time1
        print(str(reaction_speed)[-9:])
        if float(str(reaction_speed)[-9:]) < 2:
            print(f"wow {game_username} are so fast, you earned {bet} tokens")
            input_continue_playing()
            # reward tokens
            # update_token_amount = game_tokens + (bet*(2-reaction_speed))
            # helpers.update_tokens(game_username, updated_tokens_amount)
            # helper funtion updates 'database'
        else:
            print("you're too slow")
            input_continue_playing()
            # play again?
            # don't reward tokens.


play("marcus", 100)

# good

# 1 pachinko, racing, (pick a bucket and see if it wins )
# 2 hang-man  (get a word and guess it)
# 3 speed tester (randomly delay a post an time input) (how fast you type)


# probably not
# tic-tac-toe
# alphabet game.
# rps
# go
# chess
# uno
