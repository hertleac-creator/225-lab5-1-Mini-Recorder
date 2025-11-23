#!/usr/bin/env python3
import sqlite3
import os

DATABASE = "/nfs/demo.db"

def connect():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    return sqlite3.connect(DATABASE)

def init():
    db = connect()
    db.execute("""
        CREATE TABLE IF NOT EXISTS warhammer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            faction TEXT NOT NULL,
            painted INTEGER NOT NULL,
            models_owned INTEGER NOT NULL
        )
    """)
    db.commit()
    db.close()

def clear():
    db = connect()
    db.execute("DELETE FROM warhammer")
    db.commit()
    db.close()

def generate():
    db = connect()
    for i in range(10):
        db.execute(
            "INSERT INTO warhammer (model_name, faction, painted, models_owned) VALUES (?, ?, ?, ?)",
            (f"Test Model {i}", f"Faction {i}", 1, 10)
        )
    db.commit()
    db.close()
    print("Generated 10 fresh test models.")

if __name__ == "__main__":
    init()
    clear()
    generate()
