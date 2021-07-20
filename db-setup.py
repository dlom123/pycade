import sqlite3

con = sqlite3.connect('kca.db')
cur = con.cursor()

cur.execute('''CREATE TABLE accounts
               (id integer primary key, username varchar unique, password varchar)''')
cur.execute('''CREATE TABLE tokens
               (id integer primary key, account_id integer, amount integer)''')
cur.execute('''CREATE TABLE shop_items
               (id integer primary key, name varchar, value varchar, qty integer, cost integer)''')
cur.execute('''CREATE TABLE accounts_shop_items
               (id integer primary key, account_id integer, shop_item_id integer)''')

con.close()
