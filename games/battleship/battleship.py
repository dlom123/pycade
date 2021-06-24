import random

still_playing = None
game_tokens = 20
game_username = "User"


def init():
    global still_playing
    still_playing = True


rows = "ABCDEFGHIJ"
column = list(range(1, 11))
game_board = {row: [f'{row}{number}' for number in column] for row in rows}
tracker_board = {row: [f'{row}{number}' for number in column] for row in rows}
row = [True, False]
checks = ' '.join([' '.join([f"{row}{number}"for number in column])
                   for row in rows]).split()
ship_dict = {"C": 5, "Bb": 4, "Gb": 3, "S": 3}
ship_name_dict = {"C": ["Carrier", 2],
                  "Bb": ["Battleship", 3],
                  "Gb": ["Gun Boat", 5],
                  "S": ["Ship", 5]}
ships = [2, 3, 3, 4, 5]


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


def play(username, tokens):
    init()

    global game_tokens, game_username, still_playing, checks
    global ship_name_dict, game_board, column, rows, ship_dict
    game_tokens = tokens
    game_username = username
    sunken_ships = []
    guess_list = []
    position = enemy_placement()
    print(f"Battleship\tTokens: {game_tokens}\n")
    print("Welcome to Battleship! Run out of guesses and good-bye fleet.")
    decision = input("Would you like to play?[y/n] ")
    if decision.lower() == "y":
        tries = input("Please submit the amount of tokens (5 guesses per token) ") # noqa
        while tries:
            try:
                int(tries)
                break
            except Exception:
                tries = input("Please submit an integer")
        n = 5*int(tries)
        game_tokens -= int(tries)
        print(f"You have {n} guesses")
        choices = [[f"{row}{number}" for number in column]for row in rows]
        while n or len(sunken_ships) == len(ship_dict.keys()):
            hit = False
            for letter in choices:
                for number in letter:
                    print(f'{number}', end=" ")
                print("\n")
            print(f'You have {n} guesses left')
            if guess_list:
                print("Here are your guesses:")
                [print(previous_guess, end=" ") for previous_guess in guess_list] # noqa
                print("\n")
                if not hit:
                    print("MISS")
                elif hit:
                    print("HIT!!")
                for ship_type in position.keys():
                    if position[ship_type] == [] and ship_type not in sunken_ships: # noqa
                        print(f"You sunk my {ship_name_dict[ship_type][0]}!!!")
                        sunken_ships.append(ship_type)
                print('\n')
            guess = input("Here are your selections. What square do you guess?").upper() # noqa
            while guess not in checks:
                guess = input("Sorry, that is not on the board.Try again. What square do you guess?") # noqa
            guess_list.append(guess)
            for enemy_ship_positions in position.values():
                for index, single_ship_position in enumerate(enemy_ship_positions): # noqa
                    if guess == single_ship_position:
                        hit = True
                        enemy_ship_positions.pop(index)
                        break
                if hit:
                    break
            n -= 1
            choices = [[f"{cells}" if guess != cells else (" O" if cells == guess and hit else " X") for cells in rows]for rows in choices] # noqa
        if len(sunken_ships) == len(ship_dict.keys()):
            print("You win!")
        elif n == 0:
            print(f"You lose. Nice Try Admiral {username}")
        winnings = sum([ship_name_dict[ship][1] for ship in sunken_ships])
        game_tokens += winnings
        print(f"You won {winnings} tokens")
        again = input("Would you like to play again?][y/n] ")
        if again.lower() == 'y':
            return play(username, game_tokens)
        print("See you again!")
        return game_tokens


if __name__ == '__main__':
    play(game_username, game_tokens)
