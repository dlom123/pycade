import curses
from helpers import status_bar, update_tokens
import random
import time

STATUS_WIDTH = 60
STATUS_HEIGHT = 3
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
prize = None


def init():
    # window setup
    global stdscr, status_window, window
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    status_window = curses.newwin(STATUS_HEIGHT, STATUS_WIDTH, 0, 0)
    window = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 3, 0)
    window.nodelay(True)
    window.keypad(True)
    window.border()

    # game setup
    global still_playing, crane, crane_state, game_state
    global prize
    still_playing = True
    game_state = GAME_ACTIVE
    crane = [chr(191)] + ["|"] * CRANE_CHAIN_LEN
    crane_state = CRANE_IDLE
    prize = None
    generate_prizes()


def draw_crane():
    for i, piece in enumerate(crane[::-1]):
        window.addch(i+1, CRANE_X, piece)
    if prize:
        # add the prize to the end of the crane claw
        prize_y = len(crane) + 1
        prize_x = CRANE_X
        if prize['offset'] == 1:
            prize_x -= 1
        window.addstr(prize_y, prize_x, str(prize['amount']))


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


def grab_prize():
    """Sets the prize to the value below the crane claw."""
    global prize
    if prizes_offset in (1, 2):
        # a prize was grabbed
        prize = {
            "amount": prizes[4],
            "offset": prizes_offset
        }
        prizes[4] = "  "


def apply_prize():
    global game_tokens
    if prize:
        game_tokens += prize['amount']
        update_tokens(game_username, game_tokens)


def shutdown():
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()


def display_status_bar():
    status = status_bar(
        game="Crane Game",
        tokens=game_tokens,
        username=game_username)
    status_window.addstr(0, 0, status)
    status_window.addstr(2, 0, "spacebar: lower crane, 'q': quit game")
    status_window.refresh()


def update_screen():
    window.clear()
    display_status_bar()
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
        global game_state, crane_state, prize
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
                    if len(crane) == CRANE_MAX_LEN + 1:
                        # crane has reached the bottom
                        game_state = GAME_IDLE
                        grab_prize()
                        crane_state = CRANE_RAISING
                    else:
                        lower_crane()
            else:
                if crane_state == CRANE_RAISING:
                    update_screen()
                    raise_crane()
                    if len(crane) == CRANE_CHAIN_LEN + 1:
                        update_screen()
                        crane_state = CRANE_IDLE
                        apply_prize()
                        update_screen()
                elif crane_state == CRANE_IDLE:
                    # end of round, continue playing?
                    window.nodelay(False)
                    window.addstr(7, 8, "Continue playing? (y/n)")
                    key = window.getch()
                    if key == ord('n'):
                        still_playing = False
                    else:
                        # restart the game
                        init()
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
