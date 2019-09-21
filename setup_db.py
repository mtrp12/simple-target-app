#!/usr/bin/env python3

import sqlite3

with open("setup_db.sql", "r") as file:
    script = file.read()

conn = sqlite3.connect("user_data.db")
conn.executescript(script)
conn.commit()
conn.close()
