#!/usr/bin/env python3
import sqlite3
import os
import sys

DATABASE = "/nfs/demo.db"

def connect_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    return sqlite3.connect(DATABASE)

def init_db():
    db = connect_db()
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

def clear_table():
    db = connect_db()
    db.execute("DELETE FROM warhammer")
    db.commit()
    db.close()

def generate_test_data(num_records=10):
    db = connect_db()
    for i in range(num_records):
        model = f"Test Model {i}"
        faction = f"Faction {i}"
        painted = 1
        owned = 10
        db.execute(
            "INSERT INTO warhammer (model_name, faction, painted, models_owned) VALUES (?, ?, ?, ?)",
            (model, faction, painted, owned)
        )
    db.commit()
    db.close()
    print(f"Inserted {num_records} test models")

if __name__ == "__main__":
    try:
        init_db()
        clear_table()
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        generate_test_data(n)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
