import sqlite3
import os
import random

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_models):
    """Generate test Warhammer hobby data."""
    db = connect_db()
    
    factions = [
        'Adeptus Astartes',
        'Chaos Space Marines',
        'Adeptus Mechanicus',
        'Orks',
        'T’au Empire',
        'Necrons',
        'Astra Militarum',
        'Drukhari',
        'Tyranids',
        'Craftworld Aeldari'
    ]

    unit_names = [
        'Tactical Squad',
        'Terminator Squad',
        'Strike Team',
        'Boyz Mob',
        'Immortals',
        'Leman Russ Battle Tank',
        'Hormagaunts',
        'Wych Cult Fighters',
        'Rangers',
        'Intercessors'
    ]
    
    for i in range(num_models):
        model_name = random.choice(unit_names)
        faction = random.choice(factions)
        
        models_owned = random.randint(3, 60)
        painted = random.randint(0, models_owned)

        db.execute(
            '''
            INSERT INTO models (model_name, faction, paint_status, models_owned)
            VALUES (?, ?, ?, ?)
            ''',
            (model_name, faction, painted, models_owned)
        )
    
    db.commit()
    print(f'{num_models} mighty regiments have bolstered the Hobby Crusade!')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test models
