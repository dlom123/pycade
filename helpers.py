import sqlite3

con = sqlite3.connect('kca.db')
cur = con.cursor()


def status_bar(**kwargs):
    # do not display the key name for these
    value_only = ('game')
    status = ""
    for k, v in kwargs.items():
        if k not in value_only:
            title = k.replace('_', ' ').title()
            status += f"{title}: "
        status += f"{v}\t"
        if type(v) == str and len(v) > 12:
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
    cur.execute("""SELECT accounts.username, tokens.amount
                   FROM accounts
                   INNER JOIN tokens
                   ON tokens.account_id = accounts.id
                   ORDER BY tokens.amount DESC""")
    r = cur.fetchall()
    return r
