#!/usr/bin/env python3
import sqlite3, os, sys
DATABASE = "/nfs/demo.db"

def connect_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    return sqlite3.connect(DATABASE)

def clear_warhammer():
    db = connect_db()
    cur = db.cursor()
    cur.execute("DELETE FROM warhammer")
    db.commit()
    db.close()
    print("Cleared warhammer table")

if __name__ == "__main__":
    clear_warhammer()
