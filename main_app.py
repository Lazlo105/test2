from flask import Flask, render_template, abort, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "WAD"
app.config["MONGO_URI"] = "mongodb://localhost:27017/auth_db"
mongo = PyMongo(app)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user.get('password'), password):
            session["username"] = username
            return render_template('profile.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/profile")
def render_profile():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("profile.html", username=session["username"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        # Проверка, существует ли уже пользователь с таким именем
        if mongo.db.users.find_one({"username": username}):
            flash("Username already exists", "danger")
            return redirect(url_for("register"))

        # Хешируем пароль
        hashed_password = generate_password_hash(password)

        # Добавляем пользователя в базу данных
        mongo.db.users.insert_one({
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": hashed_password
        })

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)