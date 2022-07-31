from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyAn29lPw7NBYnhAZ-XLRQHGb7fYoS7fuZE",
  "authDomain": "cool-project-d10a3.firebaseapp.com",
  "projectId": "cool-project-d10a3",
  "storageBucket": "cool-project-d10a3.appspot.com",
  "messagingSenderId": "285222370726",
  "appId": "1:285222370726:web:03d7cce950a51ff7de6367",
  "measurementId": "G-LPVLYQNTK9",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        mail = request.form('email')
        word = request.form('password')
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(mail, word)
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)