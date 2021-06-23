import curses
import os
from helpers import status_bar, update_tokens

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

def refresh_screen():
    os.system('clear')
    status = status_bar(game_name="Deal Or No Deal", tokens=game_tokens)
    print(f"{status}\n")


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
