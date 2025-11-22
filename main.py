from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os
import math

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DATABASE = "/nfs/demo.db"
PER_PAGE_DEFAULT = 10


# ------------------------------
# DATABASE HELPERS
# ------------------------------
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Create Warhammer models database table."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS warhammer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                faction TEXT NOT NULL,
                painted INTEGER NOT NULL,
                models_owned INTEGER NOT NULL
            );
            """
        )
        db.commit()
        db.close()


# ------------------------------
# ROUTES
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # ---------- POST actions (Add / Update / Delete) ----------
    if request.method == "POST":
        action = request.form.get("action")

        # DELETE
        if action == "delete":
            model_id = request.form.get("model_id")
            if model_id:
                db = get_db()
                db.execute("DELETE FROM warhammer WHERE id = ?", (model_id,))
                db.commit()
                db.close()
                flash("Model deleted.", "success")
            else:
                flash("Missing model ID.", "danger")

            return redirect(url_for("index"))

        # UPDATE
        if action == "update":
            model_id = request.form.get("model_id")
            model_name = request.form.get("model_name")
            faction = request.form.get("faction")
            painted = request.form.get("painted", 0)
            models_owned = request.form.get("models_owned")

            if model_id and model_name and faction and models_owned:
                db = get_db()
                db.execute(
                    """
                    UPDATE warhammer 
                    SET model_name=?, faction=?, painted=?, models_owned=?
                    WHERE id=?
                    """,
                    (model_name, faction, painted, models_owned, model_id),
                )
                db.commit()
                db.close()
                flash("Model updated.", "success")
            else:
                flash("Missing fields for update.", "danger")

            return redirect(url_for("index"))

        # ADD
        model_name = request.form.get("model_name")
        faction = request.form.get("faction")
        painted = request.form.get("painted", 0)
        models_owned = request.form.get("models_owned")

        if model_name and faction and models_owned:
            db = get_db()
            db.execute(
                """
                INSERT INTO warhammer (model_name, faction, painted, models_owned) 
                VALUES (?, ?, ?, ?)
                """,
                (model_name, faction, painted, models_owned),
            )
            db.commit()
            db.close()
            flash("Model added.", "success")
        else:
            flash("Missing required fields.", "danger")

        return redirect(url_for("index"))

    # ---------- GET (Display with pagination) ----------
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1

    try:
        per_page = max(int(request.args.get("per", PER_PAGE_DEFAULT)), 1)
    except ValueError:
        per_page = PER_PAGE_DEFAULT

    offset = (page - 1) * per_page

    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM warhammer").fetchone()[0]

    rows = db.execute(
        """
        SELECT * FROM warhammer 
        ORDER BY id DESC 
        LIMIT ? OFFSET ?
        """,
        (per_page, offset),
    ).fetchall()

    db.close()

    pages = max(1, math.ceil(total / per_page))
    has_prev = page > 1
    has_next = page < pages
    start_page = max(1, page - 2)
    end_page = min(pages, page + 2)

    return render_template(
        "index.html",
        models=rows,
        page=page,
        pages=pages,
        per_page=per_page,
        has_prev=has_prev,
        has_next=has_next,
        total=total,
        start_page=start_page,
        end_page=end_page,
    )


# ------------------------------
# BOOTSTRAP
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host="0.0.0.0", port=port)
