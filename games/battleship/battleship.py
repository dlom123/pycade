import random

still_playing = None
game_tokens = None
game_username = None


def init():
    global still_playing
    still_playing = True


rows = "ABCDEFGHIJ"
column = list(range(1, 11))
game_board = {row: [f'{row}{number}' for number in column] for row in rows}

ship_dict = {"C": 5, "Bb": 4, "Gb": 3, "S": 3}
ship_name_dict = {"C": ["Carrier", 2],
                  "Bb": ["Battleship", 3],
                  "Gb": ["Gun Boat", 5],
                  "S": ["Ship", 5]}
ships = [2, 3, 3, 4, 5]


def enemy_placement():
    ship_locale = {}
    row = [True, False]
    tracker_board = {row: [f'{row}{number}' for number in column] for row in rows} # noqa
    for ship in ship_dict:
        ship_pos = []
        orientation = random.choice(row)
        rand_row = random.choice(list(tracker_board.keys()))
        start = random.choice(tracker_board[rand_row])
        if orientation and int(start[1:]) > ship_dict[ship]+1:
            start = start[0] + str(10-ship_dict[ship]+1)
        elif not orientation and rows.find(rand_row) + 1 > ship_dict[ship]:
            start = f"""{rows[len(tracker_board[rand_row])-ship_dict[ship]]}
            {start[1:]}"""
        ship_pos.append(start)
        for _ in range(ship_dict[ship]-1):
            if orientation:
                new_col = int(start[1:])
                new_col_pos = tracker_board[rand_row][new_col]
                ship_pos.append(new_col_pos)
                start = new_col_pos
            else:
                new_row = rows[rows.find(start[0])+1]
                next_pos = tracker_board[new_row][int(start[1:])-1]
                ship_pos.append(next_pos)
                start = f"{next_pos[0]}{start[1:]}"
        for pos in ship_pos:
            tracker_board[pos[0]].pop(tracker_board[pos[0]].index(pos))
        ship_locale[ship] = ship_pos
    return ship_locale


def play(username, tokens):
    init()

    global game_tokens, game_username, still_playing
    global ship_name_dict, game_board, column, rows, ship_dict
    game_tokens = tokens
    game_username = username
    sunken_ships = []
    guess_list = []

    print(f"Battleship\tTokens: {game_tokens}\n")

    try:
        position = enemy_placement()
    except Exception:
        play(username, tokens)
    print(f"You have {game_tokens} tokens")
    print("Welcome to Battleship! Run out of guesses and good-bye fleet.")
    decision = input("Would you like to play?[y/n] ")
    if decision.lower() == "y":
        tries = input("Please submit the amount of tokens (5 guesses per token) ") # noqa
        n = 5*int(tries)
        game_tokens -= int(tries)
        print(f"You have {n} guesses")
        guesses = 0
        choices = [[f"{row}{number}" for number in column]for row in rows]
        while guesses < n or len(sunken_ships) == len(ship_dict.keys()):
            for letter in choices:
                for number in letter:
                    print(f'{number}', end=" ")
                print("\n")
            print(f'You have {n-guesses} guesses left')
            if guess_list:
                print("Here are your guesses:")
                [print(previous_guess, end=" ") for previous_guess in guess_list] # noqa
                print("\n")
            guess = input("Here are your selections. What square do you guess?").upper() # noqa
            guess_list.append(guess)
            hit = False
            for enemy_ship_positions in position.values():
                for index, single_ship_position in enumerate(enemy_ship_positions): # noqa
                    if guess == single_ship_position:
                        print("HIT!")
                        hit = True
                        enemy_ship_positions.pop(index)
                        break
                if hit:
                    break
            if not hit:
                print("MISS")
                guesses += 1
            choices = [[f"{cells}" if guess != cells else (" O" if cells == guess and hit else " X") for cells in rows]for rows in choices] # noqa
            for ship_type in position.keys():
                if position[ship_type] == [] and ship_type not in sunken_ships:
                    print(f"You sunk my {ship_name_dict[ship_type][0]}!!!")
                    sunken_ships.append(ship_type)
        if len(sunken_ships) == len(ship_dict.keys()):
            print("You win!")
        else:
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
    play()
