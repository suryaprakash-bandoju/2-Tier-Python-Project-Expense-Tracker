from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "expenses.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    category = request.args.get("category", "")

    connection = get_db_connection()

    if category:
        expenses = connection.execute(
            """
            SELECT * FROM expenses
            WHERE category = ?
            ORDER BY expense_date DESC, id DESC
            """,
            (category,),
        ).fetchall()
    else:
        expenses = connection.execute("""
            SELECT * FROM expenses
            ORDER BY expense_date DESC, id DESC
            """).fetchall()

    total = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()[0]

    categories = connection.execute(
        "SELECT DISTINCT category FROM expenses ORDER BY category"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=categories,
        selected_category=category,
    )


@app.route("/add", methods=["POST"])
def add_expense():
    description = request.form["description"]
    category = request.form["category"]
    amount = request.form["amount"]
    expense_date = request.form["expense_date"]

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO expenses
        (description, category, amount, expense_date)
        VALUES (?, ?, ?, ?)
        """,
        (description, category, amount, expense_date),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    connection = get_db_connection()

    connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    initialize_database()

    app.run(host="0.0.0.0", port=5000, debug=False)
