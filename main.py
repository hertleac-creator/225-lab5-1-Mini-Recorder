from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os
import math

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DATABASE = '/nfs/demo.db'
PER_PAGE_DEFAULT = 10

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with a motorcycle parts table."""
    with app.app_context():
        db = get_db()

        # Drop old contacts table if it exists
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

        # Optional sample data
        sample_parts = [
            ("Brake Pad", "Brakes", 50, 25.99, "High performance front brake pad"),
            ("Oil Filter", "Engine", 100, 7.50, "OEM replacement oil filter"),
            ("Tire", "Wheels", 20, 120.00, "Sport rear tire 180/55ZR17")
        ]
        db.executemany(
            "INSERT INTO parts (name, category, quantity, price, description) VALUES (?, ?, ?, ?, ?)",
            sample_parts
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
                flash('Part deleted successfully.', 'success')
            else:
                flash('Missing part id.', 'danger')
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
                flash('Part updated.', 'success')
            else:
                flash('Missing required fields for update.', 'danger')
            return redirect(url_for('index'))

        # ADD NEW PART
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
            flash('Part added successfully.', 'success')
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
