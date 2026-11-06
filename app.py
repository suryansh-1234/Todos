from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "todos.db"


# Connect to database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# Homepage
@app.route("/")
def home():
    conn = get_db()
    todos = conn.execute(
        "SELECT * FROM todos ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", todos=todos)


# Add task
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()

    if task:
        conn = get_db()
        conn.execute(
            "INSERT INTO todos (task) VALUES (?)",
            (task,)
        )
        conn.commit()
        conn.close()

    return redirect("/")


# Complete task
@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = get_db()

    conn.execute(
        "UPDATE todos SET completed = NOT completed WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Delete task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM todos WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
