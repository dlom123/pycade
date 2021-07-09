import sqlite3

con = sqlite3.connect('kca.db')
cur = con.cursor()

cur.execute('''CREATE TABLE accounts
               (id integer primary key, username varchar unique, password varchar)''')
cur.execute('''CREATE TABLE tokens
               (id integer primary key, account_id integer, amount integer)''')

con.close()
