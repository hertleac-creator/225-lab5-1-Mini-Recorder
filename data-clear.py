import sqlite3
import os
import sys

# ======================================================
# CONFIGURATION
# ======================================================
DATABASE = '/nfs/demo.db'
TEST_DATA_PATTERN = 'Test Part %'   # Change if needed


# ======================================================
# DATABASE UTIL
# ======================================================
def connect_db():
    """Return a SQLite DB connection, fail clearly if missing."""
    if not os.path.exists(DATABASE):
        print(f"[ERROR] Database not found: {DATABASE}")
        sys.exit(1)
    return sqlite3.connect(DATABASE)


def table_exists(db, table_name):
    """Check that the expected table exists."""
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name=?
        """,
        (table_name,)
    )
    return cursor.fetchone() is not None


# ======================================================
# CLEANUP OPERATION
# ======================================================
def clear_test_parts():
    print("\n=== TEST DATA CLEANUP TOOL ===")
    print(f"Target DB: {DATABASE}")

    db = connect_db()

    if not table_exists(db, "parts"):
        print("[ERROR] Table 'parts' does not exist in this database!")
        db.close()
        sys.exit(1)

    cursor = db.cursor()

    # Count before delete
    cursor.execute("SELECT COUNT(*) FROM parts")
    total_before = cursor.fetchone()[0]

    print(f"Total rows before delete: {total_before}")

    # Delete targeted rows
    cursor.execute(
        "DELETE FROM parts WHERE name LIKE ?",
        (TEST_DATA_PATTERN,)
    )
    db.commit()

    # Count after delete
    cursor.execute("SELECT COUNT(*) FROM parts")
    total_after = cursor.fetchone()[0]

    deleted = total_before - total_after

    print(f"Rows deleted: {deleted}")
    print(f"Rows remaining: {total_after}")
    print("Cleanup complete.\n")

    db.close()


# ======================================================
# MAIN EXECUTION
# ======================================================
if __name__ == "__main__":
    clear_test_parts()
