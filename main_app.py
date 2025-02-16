from flask import Flask, render_template, abort, redirect, url_for, request, session
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

if __name__ == "main":
    app.run()