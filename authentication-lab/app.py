from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDKWIOQOnWH8BAiHUA2YN36ijcn7WB8wzI",
  "authDomain": "cs-gropf.firebaseapp.com",
  "projectId": "cs-gropf",
  "storageBucket": "cs-gropf.appspot.com",
  "messagingSenderId": "997403894075",
  "appId": "1:997403894075:web:b3deabf2b7b838fff2d71e",
  "measurementId": "G-N29PHVT4RC",
  "databaseURL" : "https://cs-gropf-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        bio= request.form['bio']
        try:


            login_session['user'] = auth.create_user_with_email_and_password(email, password)
           
            user = {"name": name, "email": email, "password":password,"username":username,"bio":bio}
            db.child("Users").child(login_session['user']['localId']).set(user)



            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
    else:
        return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    else: 
        return render_template("signin.html")

    


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        try:
            title = request.form['title']
            tweet = request.form['tweet']
            tweets={'title': title,'tweet': tweet}
            db.child("tweets").push(tweet)
            return redirect(url_for('signup'))

        except:
            error="sorry! couldn't post the tweet"
            return render_template("add_tweet.html")

    else:
        error="got to GET method"
        return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)