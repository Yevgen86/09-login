from flask import Flask, render_template, request, redirect, url_for, make_response
from model import User, db
import hashlib
import uuid

app = Flask(__name__)
db.create_all() #creates new DB table


@app.route("/")
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None
    return render_template('index.html', user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name") # like in bind.param in PHP
    email = request.form.get("user-email") # like in bind.param in PHP
    password = request.form.get("user-password") # like in bind.param in PHP
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    #new Object from tpe User (model)
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, password=hashed_pw)
        db.add(user)
        db.commit()
    if hashed_pw != user.password:
        return "Wrong Password!!!"
    elif hashed_pw == user.password:
        session_token = str(uuid.uuid4()) # SESSION
        user.session_token = session_token
        db.add(user)
        db.commit()
        #Cookie
        response = make_response(redirect(url_for('index')))
        response.set_cookie('session_token', session_token, httponly=True, samesite='Strict')
        return response

if __name__ == '__main__':
    app.run()