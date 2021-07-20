import sqlite3

con = sqlite3.connect('kca.db')
cur = con.cursor()


def add_commas(n):
    """Adds commas to a numeric string."""
    n = str(n)[::-1]
    groups = [n[x:x+3] for x in range(0, len(n), 3)]
    s = ",".join(groups)
    return s[::-1]


def status_bar(**kwargs):
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


def get_shop_items():
    cur.execute("""SELECT *
                   FROM shop_items
                   ORDER BY cost""")
    r = cur.fetchall()
    return r


def buy_shop_item(username, item_id):
    cur.execute("""SELECT id, qty FROM shop_items
                   WHERE id = ?""", (item_id,))
    shop_item_id, shop_item_qty = cur.fetchone()
    cur.execute("""SELECT id FROM accounts
                   WHERE username = ?""", (username,))
    account = cur.fetchone()
    cur.execute("""INSERT INTO accounts_shop_items
                   (account_id, shop_item_id)
                   VALUES (?, ?)""", (account[0], shop_item_id))
    con.commit()
    if shop_item_qty > 0:
        cur.execute("""UPDATE shop_items
                    SET qty = ?
                    WHERE id = ?""", (shop_item_qty-1, shop_item_id))
        con.commit()
