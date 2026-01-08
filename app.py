import sqlite3
from flask import Flask, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash

counter = 0

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

connection = sqlite3.connect('database.db', check_same_thread=False)

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
    
        cursor.execute("SELECT password FROM user_info WHERE username = ?", (username,))

        #fetchone(): take the last sql line and transform it into a tuple, if there's no line, it returns None
        row = cursor.fetchone()

        if row is None:
            return render_template("apology.html")
        

        #em row[0], estamos acessando o 1 elemento da tupla (a sintaxe de tuplas é igual à de arrays)
        db_password = row[0]
        
        if check_password_hash(db_password, password) ==  True:
            return redirect("/")
        else:
            return render_template("apology.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_ok", methods=["GET", "POST"])
def register_ok():
    username = request.get("username")

    cursor.execute("SELECT username FROM user_info WHERE username = ?", (username))
    row = cursor.fetchone()

    #If the username doesnt exist yet
    if row is None:
        password = request.get("password")

        if not password:
            return render_template("apology.html") 
        password_hash = generate_password_hash(password, method='scrypt', salt_length=16)
        cursor.execute("INSERT INTO user_info(username, password, id) VALUES(?, ?, ?)", (username, password_hash, counter))
        counter += 1    
        return redirect("/")
    return render_template("apology.html")