# red = 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
# black = 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
import random
def num_col_combo():
    roll = {
        "red" : [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
        "black" : [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    }
    color = random.choice(list(roll.keys()))
    color_value = roll.get(color)
    number = random.choice(color_value)
    return color, number
def win_lose():
    user_input = input('Place your bets!: ')
    print(user_input)
    color, number = num_col_combo()
    if user_input == color:
        print(color, number, "YOU WIN!")
        return 'win'
    elif user_input == str(number):
        print(color, number, "YOU WIN!")
        return 'win big'
    else:
        print(color, number, "YOU LOSE!")
        return 'lose'
def currency():
    balance = 500
    while balance > 0:
        print(balance)
        bet = int(input('Enter your bet: '))
        result = win_lose()
        if result == 'win':    
            print(f"{balance} + {bet}") 
            # print("{} + {} = {}".format(balance, bet, balance + bet))
            # print(str(balance) + " + " + str(bet) + " = " + str(balance + bet))      
            balance += bet
        elif result == 'win big':
            print(f"{balance} + {bet * 35}") 
            balance += bet * 35
        else:
            print(f"{balance} - {bet}") 
            balance -= bet
    print("YOU BROKE!")
def main():
    # print('test')
    currency()
if __name__ == '__main__':
    main()
