#!/usr/bin/env python3
import sqlite3
import os
import sys

# ===========================
# Database location
# ===========================
DATABASE = "/nfs/demo.db"

# ===========================
# Connect to the database
# ===========================
def connect_db():
    # Ensure the folder exists
    db_dir = os.path.dirname(DATABASE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    return sqlite3.connect(DATABASE)

# ===========================
# Initialize table if missing
# ===========================
def init_db():
    db = connect_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS warhammer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            faction TEXT NOT NULL,
            painted INTEGER NOT NULL,
            models_owned INTEGER NOT NULL
        );
    """)
    db.commit()
    db.close()

# ===========================
# Generate test data
# ===========================
def generate_test_data(num_records=10):
    db = connect_db()
    print("\n⚔️ Generating test models for Selenium…\n")

    for i in range(num_records):
        model = f"Test Model {i}"
        faction = f"Faction {i}"
        painted = 1  # Always painted for simplicity
        owned = 10   # Arbitrary number

        db.execute(
            "INSERT INTO warhammer (model_name, faction, painted, models_owned) VALUES (?, ?, ?, ?)",
            (model, faction, painted, owned)
        )

        print(f"  ✔ Added {model} ({faction}) — Painted: {painted}, Owned: {owned}")

    db.commit()
    db.close()
    print(f"\n🛡️ Test data generation complete — {num_records} entries added.\n")

# ===========================
# Main execution
# ===========================
if __name__ == "__main__":
    try:
        init_db()
        # Optional: allow specifying number of records via command line
        num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        generate_test_data(num_records)
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        sys.exit(1)
