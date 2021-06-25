"""
This file can be used as starter code for creating a
curses-based game -- i.e., "graphics for the terminal"
"""

import curses
# from helpers import status_bar, update_tokens

game_tokens = None
game_username = None
stdscr = None
prizes = []


def generate_prizes():
    pass


def init():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)


def shutdown():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def play(username, tokens):
    init()

    global game_tokens, game_username
    game_tokens = tokens
    game_username = username
    # refresh_screen()
    stdscr.addstr(0, 0, curses.COLS)
    stdscr.refresh()
    stdscr.getkey()
    shutdown()
    return game_tokens


if __name__ == '__main__':
    play('guest', 1000)
