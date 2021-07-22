"""
Initialize the database with all necessary tables.
Also populates the gift shop.

Note: Prone to errors and duplicating data since existing tables
      and data are NOT taken into account.
"""

import sqlite3

con = sqlite3.connect('kca.db')
cur = con.cursor()

# Create necessary tables
cur.execute('''CREATE TABLE accounts
               (
                   id integer primary key,
                   username varchar unique,
                   password varchar
               )''')
cur.execute('''CREATE TABLE tokens
               (
                   id integer primary key,
                   account_id integer,
                   amount integer
               )''')
cur.execute('''CREATE TABLE shop_items
               (
                   id integer primary key,
                   name varchar,
                   value varchar,
                   qty integer,
                   cost integer
               )''')
cur.execute('''CREATE TABLE accounts_shop_items
               (
                   id integer primary key,
                   account_id integer,
                   shop_item_id integer
               )''')

# Populate the gift shop
shop_items = [
    ("star-power", "🤩", 25, -1),
    ("donut", "🍩", 200, 12),
    ("brain", "🧠", 10000, -1),
    ("zombie", "🧟", 15000, -1),
    ("robo-arm", "🦾", 42000, 42),
    ("shooting-star", "🌠", 50000, 10),
    ("one-hundred", "💯", 100000, 100),
    ("superhero", "🦸", 250000, 4),
    ("supervillain", "🦹", 300000, 5),
    ("merperson", "🧜", 3000000, 2),
    ("rainbow", "🌈", 500000000, 3),
    ("unicorn", "🦄", 1000000000, 1),
]
for item in shop_items:
    cur.execute('''INSERT INTO shop_items
                   (name, value, cost, qty)
                   VALUES (?, ?, ?, ?)''', (*item,))
con.commit()
con.close()
