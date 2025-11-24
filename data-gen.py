import sqlite3
import os
import random

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_parts):
    """Generate test data for the parts table."""
    db = connect_db()
    
    sample_categories = ['Engine', 'Brakes', 'Wheels', 'Exhaust', 'Suspension']
    
    for i in range(num_parts):
        name = f'Test Part {i}'
        category = random.choice(sample_categories)
        quantity = random.randint(1, 100)
        price = round(random.uniform(5.0, 500.0), 2)
        description = f'Sample description for {name}'
        
        db.execute(
            'INSERT INTO parts (name, category, quantity, price, description) VALUES (?, ?, ?, ?, ?)',
            (name, category, quantity, price, description)
        )
    
    db.commit()
    print(f'{num_parts} test parts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test parts
