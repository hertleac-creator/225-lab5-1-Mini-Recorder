from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os
import math
import random

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DATABASE = '/nfs/demo.db'
PER_PAGE_DEFAULT = 10

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with Warhammer minis table."""
    with app.app_context():
        db = get_db()

        # Drop old table if it exists
        db.execute("DROP TABLE IF EXISTS parts")

        # Create the new parts table
        db.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0.0,
                description TEXT
            );
        ''')

        # Generate sample Warhammer minis
        factions = ['Space Marines', 'Orks', 'Eldar', 'Chaos', 'Necrons', 'Tyranids']
        detachments = ['Battle Company', 'Kill Team', 'Strike Force', 'Vanguard', 'Patrol']
        minis = []

        for i in range(10):
            name = f'Mini {i}'
            category = random.choice(factions)
            quantity = random.randint(1, 20)  # points
            price = round(random.uniform(10.0, 100.0), 2)  # cost
            description = random.choice(detachments)
            minis.append((name, category, quantity, price, description))

        db.executemany(
            "INSERT INTO parts (name, category, quantity, price, description) VALUES (?, ?, ?, ?, ?)",
            minis
        )

        db.commit()
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    # ---------------------------
    # POST (Add, Update, Delete)
    # ---------------------------
    if request.method == 'POST':
        action = request.form.get('action')

        # DELETE PART
        if action == 'delete':
            part_id = request.form.get('part_id')
            if part_id:
                db = get_db()
                db.execute('DELETE FROM parts WHERE id = ?', (part_id,))
                db.commit(); db.close()
                flash('Mini deleted successfully.', 'success')
            else:
                flash('Missing mini id.', 'danger')
            return redirect(url_for('index'))

        # UPDATE PART
        if action == 'update':
            part_id = request.form.get('part_id')
            name = request.form.get('name')
            category = request.form.get('category')
            quantity = request.form.get('quantity')
            price = request.form.get('price')
            description = request.form.get('description')

            if part_id and name:
                db = get_db()
                db.execute('''
                    UPDATE parts
                    SET name=?, category=?, quantity=?, price=?, description=?
                    WHERE id=?
                ''', (name, category, quantity, price, description, part_id))
                db.commit(); db.close()
                flash('Mini updated.', 'success')
            else:
                flash('Missing required fields for update.', 'danger')
            return redirect(url_for('index'))

        # ADD NEW MINI
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        description = request.form.get('description')

        if name:
            db = get_db()
            db.execute('''
                INSERT INTO parts (name, category, quantity, price, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, category, quantity, price, description))
            db.commit(); db.close()
            flash('Mini added successfully.', 'success')
        else:
            flash('Name is required.', 'danger')

        return redirect(url_for('index'))

    # ---------------------------
    # GET (Pagination)
    # ---------------------------
    try:
        page = max(int(request.args.get('page', 1)), 1)
    except ValueError:
        page = 1
    try:
        per_page = max(int(request.args.get('per', PER_PAGE_DEFAULT)), 1)
    except ValueError:
        per_page = PER_PAGE_DEFAULT

    offset = (page - 1) * per_page

    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM parts').fetchone()[0]
    parts = db.execute(
        'SELECT * FROM parts ORDER BY id DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    db.close()

    pages = max(1, math.ceil(total / per_page))
    has_prev = page > 1
    has_next = page < pages
    start_page = max(1, page - 2)
    end_page = min(pages, page + 2)

    return render_template(
        'index.html',
        parts=parts,
        page=page, pages=pages, per_page=per_page,
        has_prev=has_prev, has_next=has_next, total=total,
        start_page=start_page, end_page=end_page
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
