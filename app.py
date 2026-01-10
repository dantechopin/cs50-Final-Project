import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from datetime import timedelta



app = Flask(__name__)

app.config.update(
    SESSION_PERMANENT=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # True se HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

connection = sqlite3.connect('database.db', check_same_thread=False)

cursor = connection.cursor()

@app.context_processor
def inject_user():
    return {
        'autenticado': session.get('autenticado', False),
        'username': session.get('username')
    }

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
        #TODO: make so that the username and password, if invalid redirect you to this page 
    
        cursor.execute("SELECT password FROM user_info WHERE username = ?", (username,))


        #fetchone(): take the last sql line and transform it into a tuple, if there's no line, it returns None
        row = cursor.fetchone()

        if row is None:
            return render_template("apology.html")

        cursor.execute("SELECT id FROM user_info WHERE username = ?", (username,))
        ids = cursor.fetchone()

        #em row[0], estamos acessando o 1 elemento da tupla (a sintaxe de tuplas é igual à de arrays)
        db_password = row[0]
        id_ = ids[0]
        
        if check_password_hash(db_password, password) ==  True:
            session.clear()
            session["autenticado"] = True
            session["username"] = username
            session["id"] = id_
            return redirect("/")
        else:
            return render_template("apology.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_ok", methods=["GET", "POST"])
def register_ok():
    username = request.form.get("username")

    cursor.execute("SELECT username FROM user_info WHERE username = ?", (username,))
    row = cursor.fetchone()

    #If the username doesnt exist yet
    if row is None:
        password = request.form.get("password")

        if not password:
            return render_template("apology.html") 

        password_hash = generate_password_hash(password, method='scrypt', salt_length=16)
        cursor.execute("INSERT INTO user_info(username, password) VALUES(?, ?)", (username, password_hash))
        connection.commit()

        return render_template("register_ok.html")

    return render_template("apology.html")