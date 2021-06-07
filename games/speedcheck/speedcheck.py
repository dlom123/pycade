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
    game_tokens = 0
    exix_flag = False


def play(username, tokens):
    init()
    game_tokens = tokens
    game_username = username

    while not exit_flag:
        print('countdown')
        time.sleep(random.randint(1, 3))
        time1 = datetime.now()
        input("go")
        time2 = datetime.now()
        print(f"time1:{time1} \ntime2: {time2}")
        reaction_speed = time2-time1
        print(str(reaction_speed)[-9:])
        if float(str(reaction_speed)[-9:]) < 2:
            print("wow you are so fast, you need some tokens")
            # play again
            # reward tokens
        else:
            print("you're too slow")
            # play again?
            # don't reward tokens.
        # ready set (delay) random time (1 - 3 seconds)
        # marking the time it posts
        # wait for input.
        # calculate how long it took

    pass


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
