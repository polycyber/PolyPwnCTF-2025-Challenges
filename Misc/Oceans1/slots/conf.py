import sqlite3
import os
DATABASE = 'data.db'

def on_starting(_server):
    try:
        os.remove(DATABASE)
    except:
        pass

    db = sqlite3.connect(DATABASE)
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()