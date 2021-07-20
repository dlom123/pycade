import html
import os
from helpers import status_bar, get_shop_items, buy_shop_item, add_commas

NAME = "Gift Shop"
COST = 0

game_username = None
game_tokens = None
items = {}
errors = []


def play(username, tokens):
    global game_tokens, game_username, rank, errors
    game_tokens = tokens
    game_username = username
    errors = []
    is_shopping = True
    while is_shopping:
        shop_items = get_shop_items()
        for i, item in enumerate(shop_items):
            id_, name, value, qty, cost = item
            items[i+1] = {
                'id': id_,
                'name': name,
                'value': value,
                'qty': qty,
                'cost': cost
            }
        valid_choice = False
        while not valid_choice:
            refresh_screen()
            display_items()
            if errors:
                print(f"{errors[0]}")
                errors.clear()
            try:
                choice = input(
                    "Enter an item number to purchase ('q' to quit): ")
                if choice.lower() == 'q':
                    is_shopping = False
                    break
                elif int(choice) < 1 or int(choice) > len(shop_items):
                    errors.append("Invalid choice")
                elif items[int(choice)]['qty'] == 0:
                    my_choice = items[int(choice)]
                    errors.append((
                        "Sorry, all out of "
                        f"{format_item_name(my_choice['name'])}."
                    ))
                elif items[int(choice)]['cost'] > game_tokens:
                    my_choice = items[int(choice)]
                    errors.append((
                        "Not enough tokens to buy a "
                        f"{format_item_name(my_choice['name'])}!"
                    ))
                else:
                    valid_choice = True
            except Exception:
                errors.append("Invalid choice")
        if is_shopping:
            buy_shop_item(game_username, items[int(choice)]['id'])
            errors.append((
                "Congratulations on your brand new "
                f"{format_item_name(items[int(choice)]['name'])}!"
            ))
    return game_tokens


def display_items():
    print(f"{'=' * 58}")
    print(f"| {'#':>2}  {'Item':<15}   {'Cost':<23}{'Available':<10}|")
    print(f"{'=' * 58}")
    for i, t in enumerate(items.items()):
        n, item = t
        if i > 0:
            print(f"{'-' * 58}")
        item_name = format_item_name(item['name'])
        if item['qty'] == -1:
            item['qty'] = html.unescape("&infin;")
        cost_str = f"{add_commas(item['cost'])} tokens"
        print(f"| {n:>2}. {item_name:<13} ", end="")
        print(f"{item['value']:<2} {cost_str:<22} {item['qty']:<10}|")
    print(f"{'-' * 58}")
    print()


def format_item_name(item_name):
    return item_name.replace('-', ' ').title()


def refresh_screen():
    os.system('clear')
    items = {
        'game': 'Gift Shop',
        'tokens': add_commas(game_tokens)
    }
    items['username'] = game_username
    status = status_bar(**items)
    print(f"{status}\n")


if __name__ == '__main__':
    play()
