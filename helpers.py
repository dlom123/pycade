import sqlite3

db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "kca.db")
con = sqlite3.connect(db_file)
cur = con.cursor()


def add_commas(n):
    """Returns a given string with commas inserted in a numeric format."""
    n = str(n)[::-1]
    groups = [n[x:x+3] for x in range(0, len(n), 3)]
    s = ",".join(groups)
    return s[::-1]


def status_bar(**kwargs):
    """Returns a string of status bar keys/values."""
    # do not display the key name for these
    value_only = ('game', 'username')
    status = ""
    for k, v in kwargs.items():
        if k not in value_only:
            title = k.replace('_', ' ').title()
            status += f"{title}: "
        status += f"{v}\t"
        if type(v) == str and (
            not len(v) % 6 or len(v) > 12
        ):
            status += "\t"
    return status


def update_tokens(username, tokens):
    """Writes the token amount to the tokens file for the given username."""
    # get the account id from the username
    cur.execute("""SELECT * FROM accounts
                   WHERE accounts.username = ?""", (username,))
    r = cur.fetchone()
    account_id = r[0]

    cur.execute("""UPDATE tokens
                   SET amount = ?
                   WHERE account_id = ?""", (tokens, account_id))
    con.commit()


def get_all_accounts():
    """Returns all accounts from the database along with token amounts."""
    cur.execute("""SELECT a.id, a.username, t.amount
                   FROM accounts a
                   INNER JOIN tokens AS t
                   ON t.account_id = a.id
                   ORDER BY t.amount DESC""")
    accounts = cur.fetchall()
    all_accounts = []
    for account in accounts:
        cur.execute("""SELECT si.value
                    FROM shop_items si
                    INNER JOIN accounts_shop_items AS asi
                    ON asi.shop_item_id = si.id
                    WHERE asi.account_id = ?
                    ORDER BY si.cost""", (account[0],))
        account_items = cur.fetchall()
        if len(account_items) > 0:
            account_items = [t[0] for t in account_items]
        all_accounts.append({
            'id': account[0],
            'username': account[1],
            'tokens': account[2],
            'items': account_items
        })
    return all_accounts


def get_account(username):
    """Returns data for an account from the database, given a username."""
    cur.execute("""SELECT a.id, a.username, t.amount
                   FROM accounts a
                   INNER JOIN tokens AS t
                   ON t.account_id = a.id
                   WHERE a.username = ?""", (username,))
    db_account = cur.fetchone()
    cur.execute("""SELECT si.value
                   FROM shop_items si
                   INNER JOIN accounts_shop_items AS asi
                   ON asi.shop_item_id = si.id
                   WHERE asi.account_id = ?
                   ORDER BY si.cost""", (db_account[0],))
    account_items = cur.fetchall()
    if len(account_items) > 0:
        account_items = [t[0] for t in account_items]
    account = {
        'id': db_account[0],
        'username': db_account[1],
        'tokens': db_account[2],
        'items': account_items
    }
    return account


def get_shop_items():
    """Returns all shop items from the database."""
    cur.execute("""SELECT *
                   FROM shop_items
                   ORDER BY cost""")
    r = cur.fetchall()
    return r


def buy_shop_item(username, item_id):
    """
    Attaches a shop item to the given username's account within the database.

    Returns the resulting account token amount.
    """
    cur.execute("""SELECT id, cost, qty FROM shop_items
                   WHERE id = ?""", (item_id,))
    shop_item_id, shop_item_cost, shop_item_qty = cur.fetchone()
    cur.execute("""SELECT a.id, t.amount
                   FROM accounts a
                   INNER JOIN tokens t
                   ON t.account_id = a.id
                   WHERE a.username = ?""", (username,))
    account = cur.fetchone()
    account_id, account_tokens = account
    cur.execute("""INSERT INTO accounts_shop_items
                   (account_id, shop_item_id)
                   VALUES (?, ?)""", (account_id, shop_item_id))
    con.commit()
    # Deduct the cost from the user's token amount
    new_token_amount = account_tokens - shop_item_cost
    cur.execute("""UPDATE tokens
                   SET amount = ?
                   WHERE account_id = ?""", (new_token_amount, account_id))
    con.commit()
    if shop_item_qty > 0:
        # This item does not have infinite supply -- reduce its supply
        cur.execute("""UPDATE shop_items
                    SET qty = ?
                    WHERE id = ?""", (shop_item_qty-1, shop_item_id))
        con.commit()
    return new_token_amount
