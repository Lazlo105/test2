from flask import Flask, render_template, abort, redirect, url_for, request
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/auth_db"
mongo = PyMongo(app)

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(password)
        user = mongo.db.users.find_one({'username': username})
        print((hash_password(password)))
        print(user.get('password'))
        if user and (hash_password(password) == user.get('password')):
            print('YES')
        else:
            print('NO')
    return render_template('login.html')

@app.route("/profile")
def index():
    return render_template('profile.html')

if __name__ == "main":

    app.run()