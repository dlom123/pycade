import random
import time
from string import ascii_lowercase as al
still_playing = None
game_tokens = 30
game_username = "user"


def init():
    global still_playing
    still_playing = True


def get_words(number):
    with open('games/speedcheck/longwords.txt') as f:
        selections = [word for word in f.read().split() if len(word) > 1]
    result_selection = []
    while len(result_selection) < number:
        result_selection.append(random.choice(selections))
    return result_selection


def blank_it(word_selection):
    return " ".join(["".join(["█" for _ in word]) for word in word_selection])


def play(username, tokens):
    global game_tokens, game_username, still_playing
    attempted_letters = [" "]
    game_tokens = tokens
    game_username = username
    init()
    print(f"Wheel of Python\tTokens: {game_tokens}\n")
    print("WHEEL")
    time.sleep(1)
    print("OF")
    time.sleep(1)
    print("PYTHON!")
    time.sleep(2)
    print('')
    print("Play against Rebecca Alice Ingenia")
    print("The entry fee is 7 tokens. ", end="")
    decision = input("Would you like to play?[y/n] ")
    if decision.lower() == "y":
        tokens -= 7
        num_words = input("How many words would you like to queue? ")
        while num_words:
            try:
                int(num_words) >= 1
                break
            except Exception:
                num_words = input("Please submit an positive integer")
        num_words = int(num_words)
        selection = get_words(num_words)
        redacted = blank_it(selection)
        switch = False
        print("HERE WE GO!")
        while redacted != " ".join(selection).upper():
            [print(redact, end='') for redact in redacted]
            print()
            if attempted_letters:
                print("Here are the letters that have tried:")
                [print(letter.upper(), end=" ")
                 for letter in attempted_letters]
                print()
            if not switch:
                letter_guess = input("What letter do you guess? ")
            else:
                letter_guess = random.choice(list(al))
            letter_guess = letter_guess.lower()
            is_found = False
            adjusted = list(redacted)
            count = 0
            for index, letter in enumerate(list(" ".join(selection))):
                if letter_guess == letter:
                    adjusted[index] = letter_guess.upper()
                    is_found = True
                    count += 1
            time.sleep(.5)
            redacted = "".join(adjusted)
            if is_found:
                if letter_guess in attempted_letters:
                    print(f"{letter_guess} has already been used!")
                    switch = not switch
                elif count == 1:
                    print(f"There is {count} {letter_guess.upper()}")
                    attempted_letters.append(letter_guess)
                else:
                    print(f"There are {count} {letter_guess.upper()}s")
                    attempted_letters.append(letter_guess)
                tokens += 1
                time.sleep(1)
            else:
                if letter_guess in attempted_letters:
                    print("That letter has already been used!")
                else:
                    print("Too bad, so sad!")
                    attempted_letters.append(letter_guess)
                switch = not switch
                time.sleep(1)
        print()
        print(redacted)
        if not switch:
            print("YOU'VE WON! WHEEL")
        else:
            print("Ingenia has won! Thank you for playing WHEEL")
        time.sleep(1)
        print("OF")
        time.sleep(1)
        print("PYTHON!")
        time.sleep(2)
        print(f"You've won {tokens-game_tokens} tokens")
        again = input("Would you like to play again?[y/n] ")
        if again.lower() == "y":
            play(game_username, game_tokens)
    print("See you soon!")


if __name__ == '__main__':
    play(game_username, game_tokens)