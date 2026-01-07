import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor.execute("INSERT INTO user(username TXT UNIQUE, password TXT) VALUES(?, ?)", username, password)
        return render_template("index.html")        