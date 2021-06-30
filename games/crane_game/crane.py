import curses
import os
from helpers import status_bar, update_tokens
import random


game_tokens = None
game_username = None
stdscr = None
window = None
prizes = []

def generate_prizes():
    prizes.clear()
    prizes.extend(random.sample(range(10, 100), 9))

def init():
    global stdscr, window
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    window = curses.newwin(15, 39, 0, 0)
    window.keypad(True)
    window.border()
    window.addch(1, 19, '|')
    window.addch(2, 19, '|')
    window.addch(3, 19, '|')
    window.addch(4, 19, '^')

def shutdown():
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

def refresh_screen():
    os.system('clear')
    status = status_bar(game_name="Deal Or No Deal", tokens=game_tokens)
    print(f"{status}\n")


def play(username, tokens):
    try:
        init()

        global game_tokens, game_username
        game_tokens = tokens
        game_username = username
        # refresh_screen()
        # window.addstr(0, 0, str(window.COLS))
        generate_prizes()
        window.refresh()
        window.getkey()
        shutdown()
    except Exception as e:
        shutdown()
        raise e
    finally:
        return game_tokens


if __name__ == '__main__':
    play('guest', 1000)
