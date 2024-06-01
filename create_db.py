import sqlite3

conn = sqlite3.connect("expenses.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS expenses
(id INTEGER PRIMARY KEY ,
Date DATE ,
category TEXT,
description TEXT ,
total_members INTEGER,
amount_for_each_member REAL,
actual_price  REAL,
total_price_with_tip REAL)""")

conn.commit()
conn.close()