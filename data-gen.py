import sqlite3
import os
import random

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_minis):
    """Generate Warhammer mini test data for the parts table."""
    db = connect_db()
    
    factions = ['Space Marines', 'Orks', 'Eldar', 'Chaos', 'Necrons', 'Tyranids']
    detachments = ['Battle Company', 'Kill Team', 'Strike Force', 'Vanguard', 'Patrol']

    for i in range(num_minis):
        name = f'Mini {i}'
        category = random.choice(factions)
        quantity = random.randint(1, 20)  # Points
        price = round(random.uniform(10.0, 100.0), 2)  # Cost
        description = random.choice(detachments)
        
        db.execute(
            'INSERT INTO parts (name, category, quantity, price, description) VALUES (?, ?, ?, ?, ?)',
            (name, category, quantity, price, description)
        )
    
    db.commit()
    print(f'{num_minis} Warhammer minis added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 Warhammer minis
