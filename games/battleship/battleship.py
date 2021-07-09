import os
import random
from helpers import status_bar, update_tokens

still_playing = None
game_tokens = None
game_username = None

rows = "ABCDEFGHIJ"
column = list(range(1, 11))
game_board = {row: [f'{row}{number}' for number in column] for row in rows}
tracker_board = {row: [f'{row}{number}' for number in column] for row in rows}
row = [True, False]
checks = ' '.join([' '.join([f"{row}{number}" for number in column])
                   for row in rows]).split()
ship_dict = {"C": 5, "Bb": 4, "Gb": 3, "S": 3}
ship_name_dict = {"C": ["Carrier", 2],
                  "Bb": ["Battleship", 3],
                  "Gb": ["Gun Boat", 5],
                  "S": ["Ship", 5]}
ships = [2, 3, 3, 4, 5]
guesses = None
errors = []
sunken_ships = None
guess_list = None


def init():
    global still_playing, guesses, errors
    global sunken_ships, guess_list
    still_playing = True
    guesses = 0
    errors = []
    sunken_ships = []
    guess_list = []


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Battleship',
        'tokens': game_tokens
    }
    if guesses:
        items['guesses'] = guesses
    status = status_bar(**items)
    print(f"{status}\n")


def enemy_placement(ship_locale={}):
    for ship in ship_dict:
        ship_pos = []
        if ship not in ship_locale:
            orientation = random.choice(row)
            rand_row = random.choice(list(tracker_board.keys()))
            start = random.choice(tracker_board[rand_row])
            if start == "X":
                return enemy_placement(ship_locale=ship_locale)
            elif orientation and int(start[1:]) > ship_dict[ship]+1:
                start = start[0] + str(10-ship_dict[ship]+1)
            elif not orientation and rows.find(rand_row) + 1 > ship_dict[ship]:
                start = f"{rows[len(tracker_board[rand_row])-ship_dict[ship]]}{start[1:]}" # noqa
            if start == "X":
                return enemy_placement(ship_locale=ship_locale)
            ship_pos.append(start)
            for _ in range(ship_dict[ship]-1):
                if orientation:
                    new_col = int(start[1:])
                    new_col_pos = tracker_board[rand_row][new_col]
                    if new_col_pos == "X":
                        return enemy_placement(ship_locale=ship_locale)
                    ship_pos.append(new_col_pos)
                    start = new_col_pos
                else:
                    new_row = rows[rows.find(start[0])+1]
                    next_pos = tracker_board[new_row][int(start[1:])-1]
                    if next_pos == "X":
                        return enemy_placement(ship_locale=ship_locale)
                    ship_pos.append(next_pos)
                    start = f"{next_pos[0]}{start[1:]}"
            for pos in ship_pos:
                track_row = tracker_board[pos[0]]
                if pos not in track_row:
                    return enemy_placement(ship_locale=ship_locale)
                index = track_row.index(pos)
                track_row[index] = "X"
            ship_locale[ship] = ship_pos
    return ship_locale


def display_board(squares):
    for letter in squares:
        for number in letter:
            print(f'{number}', end=" ")
        print()


def play(username, tokens, replay=False):
    init()

    global game_tokens, game_username, still_playing, checks
    global ship_name_dict, game_board, column, rows, ship_dict
    global guesses, errors
    game_tokens = tokens
    game_username = username
    position = enemy_placement()
    hit = False

    if not replay:
        refresh_screen()
        print(
            "Welcome to Battleship! Run out of guesses and good-bye fleet!\n"
        )
        decision = input("Would you like to play? [y/n] ")
    if replay or decision.lower() == "y":
        invalid_input = True
        while invalid_input:
            refresh_screen()
            tries = input("How many tokens will you spend (5 guesses per token)? ")
            try:
                tries = int(tries)
                if tries > 0:
                    invalid_input = False
                else:
                    continue
            except Exception:
                continue
        guesses = 5 * int(tries)
        game_tokens -= int(tries)
        update_tokens(game_username, game_tokens)

        squares = [[f"{row}{number}" for number in column] for row in rows]
        while guesses or len(sunken_ships) == len(ship_dict.keys()):
            refresh_screen()
            display_board(squares)
            if guess_list:
                message = ""
                if not hit:
                    message += f"\n{'-' * 10:^30}\n"
                    message += f"{'|  MISS  |':^30}\n"
                    message += f"{'-' * 10:^30}\n"
                elif hit:
                    message += f"\n{'-' * 10:^30}\n"
                    message += f"{'| HIT!!! |':^30}\n"
                    message += f"{'-' * 10:^30}\n"
                for ship_type in position.keys():
                    if position[ship_type] == [] and ship_type not in sunken_ships:  # noqa
                        ship_name = ship_name_dict[ship_type][0]
                        msg_sunk = f'You sunk my {ship_name}!!!'
                        message += f"\n{msg_sunk:^30}\n"
                        sunken_ships.append(ship_type)
                print(message)
                print("Your guesses:")
                for i, previous_guess in enumerate(guess_list):
                    if not i % 10:
                        print()
                    print(previous_guess, end=" ")
                print()
            hit = False
            if errors:
                print(f"\n{errors[0]}.", end="")
            guess = input("\nWhich square do you guess? ").upper()
            if guess not in checks:
                errors.append("Invalid guess.")
                continue
            elif guess in guess_list:
                errors.append(f"{guess} has already been guessed. Try again.")
                continue
            errors = []
            guess_list.append(guess)
            for enemy_ship_positions in position.values():
                for index, single_ship_position in enumerate(enemy_ship_positions): # noqa
                    if guess == single_ship_position:
                        hit = True
                        enemy_ship_positions.pop(index)
                        break
                if hit:
                    break
            if not hit:
                guesses -= 1
            squares = [[f"{cells}" if guess != cells else (" O" if cells == guess and hit else " X") for cells in rows] for rows in squares] # noqa

        # end of game
        refresh_screen()
        display_board(squares)
        if len(sunken_ships) == len(ship_dict.keys()):
            winnings = sum([ship_name_dict[ship][1] for ship in sunken_ships])
            msg_win = f"You win! (+{winnings} tokens)"
            print(f"\n{msg_win:^30}\n")
            game_tokens += winnings
            update_tokens(game_username, game_tokens)
        elif guesses == 0:
            print(f"\n{'GAME OVER':^30}")
            msg_nice_try = f"Nice Try, Admiral {username.title()}."
            print(f"{msg_nice_try:^30}\n")
        if game_tokens:
            again = input("Would you like to play again? [y/n] ")
            if again.lower() == 'y':
                return play(username, game_tokens, replay=True)
        else:
            input((
                "You are out of tokens.\n"
                "Press a key to return to the main menu."
            ))
    return game_tokens


if __name__ == '__main__':
    play(game_username, game_tokens)
