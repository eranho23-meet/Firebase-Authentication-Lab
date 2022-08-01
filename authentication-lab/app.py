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
  "databaseURL": "https://cool-project-d10a3-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        mail = request.form['email']
        word = request.form['password']
        full_name = request.form['namename']
        username = request.form['username']
        bio = request.form['bio']
        user = {'mail':mail, 'password':word, 'full_name':full_name, 'username':username, 'bio':bio}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(mail, word)
            db.child('Users').child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            print('error bad')
    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        mail = request.form['email']
        word = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(mail, word)
            return redirect(url_for('add_tweet'))
        except:
            print('ERRORROROROROROROR bad')
    return render_template("signin.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        if request.args.get('f') == 'f1':
            return redirect(url_for('signout'))
        elif request.args.get('f') == 'f2':
            return redirect(url_for('all_tweets'))
        tweet = {'title':request.form['title'], 'content':request.form['con'], 'uid':login_session['user']['localId']}
        try:
           db.child('Articles').push(tweet)

        except:
            print('nononoonoononononono!')

    return render_template("add_tweet.html")


@app.route('/all_tweets')
def all_tweets():
    return render_template('all_tweets.html', twitts = db.child('Articles').get().val())






@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



if __name__ == '__main__':
    app.run(debug=True)