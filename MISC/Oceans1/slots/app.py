from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    g,
    redirect,
    url_for,
    session,
)
import random
import sqlite3
import os
import traceback
import uuid
import hashlib
import time
import http
from conf import DATABASE

SALT = b"Salt&PepperPls$$"

http.server.BaseHTTPRequestHandler.version_string = (
    lambda _: "Polypwn Grand httpd 7.7.7"
)

app = Flask(__name__)

app.secret_key = b"CasinoDingDingDingYouWin"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    conn.close()


def password_hash(password: str) -> str:
    return hashlib.sha256(password.encode() + SALT).hexdigest()


####


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/play", methods=["GET", "POST"])
def play():
    if "id" not in session:
        return redirect(url_for("login"))

    balance = query_db(
        f"SELECT balance FROM users WHERE id = ?", [session["id"]], one=True
    )[0]

    if request.method == "GET":
        return render_template("play.html", balance=balance)

    values = {"🍎": 50, "🍍": 70, "🍌": 100, "🍇": 150, "🍒": 400}

    slots = [random.choice(list(values.keys())) for _ in range(3)]
    gains = -10
    now = time.time()

    if now < session.get("last_spin", 0) + 2:  # 2 second intervals
        slots = [":("] * 3
    elif len(set(slots)) == 1:
        gains = values[slots[0]]

    session["last_spin"] = now
    balance += gains

    insert_db("UPDATE users SET balance = ? WHERE id = ?", [balance, session["id"]])

    return jsonify({"slots": slots, "gains": gains, "balance": balance})


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "id" in session:
        return redirect(url_for("home"))

    error_msg = None
    stack_trace = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        try:
            if not username or not password:
                error_msg = "All fields are required"
            elif password != password_confirmation:
                error_msg = "Passwords do not match"
            else:
                u = query_db(
                    f'SELECT username FROM users WHERE username = "{username}"'
                )
                if len(u) == 0:
                    id = str(uuid.uuid4())
                    insert_db(
                        "INSERT INTO users VALUES (?, ?, ?, ?)",
                        [id, str(username), password_hash(password), 100.0],
                    )
                    session["id"] = id
                    return redirect(url_for("play"))
                else:
                    error_msg = f"User {u[0][0]} already exists"
        except Exception as ex:
            error_msg = "An error occured"
            stack_trace = ''.join(traceback.format_exception(ex))

    return render_template("signup.html", error_msg=error_msg, stack_trace=stack_trace)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "id" in session:
        return redirect(url_for("home"))

    error_msg = None

    if request.method == "POST":
        error_msg = "Invalid username or password"
        username = request.form.get("username")
        password = request.form.get("password")

        u = query_db(
            f"SELECT id FROM users WHERE username = ? AND password_hash = ?",
            [str(username), password_hash(str(password))],
            one=True,
        )

        if u is not None:
            session["id"] = u[0]
            return redirect(url_for("play"))

    return render_template("login.html", error_msg=error_msg)


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    entries = query_db(
        "SELECT username, balance FROM users NATURAL JOIN balance ORDER BY balance DESC"
    )
    return jsonify(entries)


if __name__ == "__main__":
    import conf

    conf.on_starting()
    app.run(debug=False)
