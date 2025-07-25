from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from encryption import encrypt, decrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecret')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize database
def init_db():
    if not os.path.exists("vault.db"):
        with sqlite3.connect("vault.db") as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

# Route: Home
@app.route("/")
def index():
    return render_template("index.html", credentials=None)

# Route: Add credentials
@app.route("/add", methods=["POST"])
def add():
    website = request.form["website"]
    username = request.form["username"]
    password = encrypt(request.form["password"])

    with sqlite3.connect("vault.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO credentials (website, username, password) VALUES (?, ?, ?)",
                  (website, username, password))
        conn.commit()
    return redirect(url_for("index"))

# Route: Get credentials by website
@app.route("/get", methods=["POST"])
def get():
    website = request.form["website"]

    with sqlite3.connect("vault.db") as conn:
        c = conn.cursor()
        c.execute("SELECT website, username, password FROM credentials WHERE website = ?", (website,))
        rows = c.fetchall()
        credentials = [(row[0], row[1], decrypt(row[2])) for row in rows]

    return render_template("index.html", credentials=credentials)

# Start app
if __name__ == "__main__":
    init_db()
