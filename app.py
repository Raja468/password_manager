from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from encryption import encrypt, decrypt
from dotenv import load_dotenv
import os

# Load secret key from .env file
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Ensure the database exists and table is created
def init_db():
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

# Add credentials
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

# Retrieve credentials by website name
@app.route("/get", methods=["POST"])
def get():
    website = request.form["website"]
    with sqlite3.connect("vault.db") as conn:
        c = conn.cursor()
        c.execute("SELECT website, username, password FROM credentials WHERE website = ?", (website,))
        rows = c.fetchall()
        credentials = [(row[0], row[1], decrypt(row[2])) for row in rows]
    return render_template("index.html", credentials=credentials)

# Main page
@app.route("/")
def index():
    return render_template("index.html", credentials=None)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

