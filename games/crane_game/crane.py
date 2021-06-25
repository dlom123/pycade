"""
TODO
  - fix bug with status bar not displaying
  - display instructions ("press spacebar to lower crane")
  - if the crane lands on a number when lowered, attach the
    number to the crane when it's raised
  - update tokens with crane reward
  - prompt the user to play again or quit
  - figure out a better character for the crane claw
"""

import curses
from helpers import status_bar, update_tokens
import random
import time

STATUS_WIDTH = 39
STATUS_HEIGHT = 2
WINDOW_WIDTH = 39
WINDOW_HEIGHT = 15
REFRESH_RATE = 0.2  # seconds
GAME_IDLE = 0
GAME_ACTIVE = 1
CRANE_X = 19
CRANE_CHAIN_LEN = 3
CRANE_MAX_LEN = WINDOW_HEIGHT - 4
CRANE_IDLE = 0
CRANE_LOWERING = 1
CRANE_RAISING = 2
PRIZES_Y = 13

still_playing = False
game_tokens = None
game_username = None
stdscr = None
status_window = None
window = None
game_state = None
crane = None
crane_state = None
prizes = []
prizes_offset = 0


def init():
    # window setup
    global stdscr, status_window, window
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    status_window = curses.newwin(STATUS_HEIGHT, STATUS_WIDTH, 0, 0)
    window = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 2, 0)
    window.nodelay(True)
    window.keypad(True)
    window.border()

    # game setup
    global still_playing, crane, crane_state, game_state
    still_playing = True
    game_state = GAME_ACTIVE
    crane = ["^"] + ["|"] * CRANE_CHAIN_LEN
    crane_state = CRANE_IDLE
    generate_prizes()


def draw_crane():
    for i, piece in enumerate(crane[::-1]):
        window.addch(i+1, CRANE_X, piece)


def lower_crane():
    crane.append("|")


def raise_crane():
    crane.pop()


def generate_prizes():
    prizes.clear()
    prizes.extend(random.sample(range(10, 100), 9))


def display_prizes():
    prize_str = "  ".join(map(str, prizes))
    window.addstr(PRIZES_Y, prizes_offset+1, prize_str)


def rotate_prizes():
    global prizes_offset
    if prizes_offset == 3:
        prizes.insert(0, prizes.pop())
    prizes_offset = (prizes_offset + 1) % 4


def shutdown():
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()


def display_status_bar():
    status = status_bar(game_name="Crane Game", tokens=game_tokens)
    status_window.addstr(0, 0, status)


def update_screen():
    window.clear()
    display_status_bar()  # TODO: this is not displaying
    window.border()
    draw_crane()
    rotate_prizes()
    display_prizes()
    window.refresh()


def play(username, tokens):
    global still_playing
    try:
        init()

        global game_tokens, game_username
        global game_state, crane_state
        game_tokens = tokens
        game_username = username
        while still_playing:
            if game_state == GAME_ACTIVE:
                update_screen()
                key = window.getch()
                if key == ord('q'):
                    # quit the game
                    still_playing = False
                elif key == 32:  # spacebar
                    # drop the crane!
                    crane_state = CRANE_LOWERING
                if crane_state == CRANE_LOWERING:
                    if len(crane) == CRANE_MAX_LEN:
                        game_state = GAME_IDLE
                        crane_state = CRANE_RAISING
                    lower_crane()
            else:
                if crane_state == CRANE_RAISING:
                    update_screen()
                    raise_crane()
                    if len(crane) == CRANE_CHAIN_LEN + 1:
                        update_screen()
                        crane_state = CRANE_IDLE
            time.sleep(REFRESH_RATE)
        shutdown()
    except Exception as e:
        shutdown()
        raise e
    finally:
        still_playing = False
        return game_tokens


if __name__ == '__main__':
    play('guest', 1000)
