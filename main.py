from flask import Flask, request, redirect, url_for, session, flash, jsonify
import socket, json, os, hashlib, threading
#import yfinance as yf
from flask_socketio import SocketIO, emit, join_room, send
from threading import Lock
#from flask_sqlalchemy import SQLAlchemy

'''db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = es,db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    friends = db.relationship('Friend', backref='user', lazy=True)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_name = db.Column(db.String(50), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10))  # Deposit, Withdraw, Transfer
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
class CreatorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    profile_pic = db.Column(db.String(200), nullable=True)  # Store image path
    projects = db.Column(db.Text, nullable=True)  # List of projects
    social_links = db.Column(db.Text, nullable=True)  # JSON for links

# Add your profile data manually for now
def create_creator_profile():
    creator = CreatorProfile.query.first()
    if not creator:
        new_creator = CreatorProfile(
            name="Divyanshu Sinha",
            bio="Python developer, AI enthusiast, and creator of DBOI Bank System.",
            profile_pic="static/images/creator.jpg",
            projects="Bank Of Divyanshu",
            social_links='{"GitHub": "https://github.com/pirate_136k", "LinkedIn": "https://linkedin.com/in/yourprofile"}'
        )
        db.session.add(new_creator)
        db.session.commit()
'''
app = Flask(__name__)
'''app.config['SECRET_KEY'] = '41fe694da0be136feb87fb96c846c907788b56aeb6b001c7ca0e6f5267f33415'
app.config.from_object('config')
db.init_app(app)

with app.app_context():
    db.create_all()'''
app.secret_key = '41fe694da0be136feb87fb96c846c907788b56aeb6b001c7ca0e6f5267f33415'  # Needed for session management
#db.init_app(app)

'''@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto', 'http') == 'http':
        return redirect(request.url.replace("http://", "https://"))'''

socketio = SocketIO(app, cors_allowed_origins="*")
thread_lock = Lock()

def hash_password(password: str = any) -> str:
    # Create a new SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the text
    hash_object.update(password.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    return hex_dig

class BOD:
    def __init__(self) -> None:
        self.data = {}

    def create(self, name: str= any, email: str= any, password: str= any) -> bool:
        if name in self.data and email in self.data:
            return False

        self.data[hash_password(password)] = {'Name': name, 'Email': email, 'Password': password}
        # Save the data to a file
        self.save()
        return True

    def login(self, name: str= any, email: str= any, password: str= any) -> bool:
        if hash_password(password) in self.data and email == self.data[hash_password(password)]['Email'] and name == self.data[hash_password(password)]['Name']:
            return True

        return False

    def save(self) -> None:
        with open('db.json', 'w') as save:
            json.dump(self.data, save)

    def load(self) -> None:
        if os.path.exists('db.json'):
            with open('db.json', 'r') as load:
                self.data = json.load(load)

bod = BOD()
bod.load()

@app.route('/', methods=['GET'])
def login_page():
    """if 'username' in session:
        return dashboard()"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank Of Divyanshu Login Page</title>
    <style>
        *{
            padding: 0;
            margin: 0;
        }

        body{
            background-color: beige;
        }

        .text-bank {
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            color: rgb(156, 134, 235);
            font-size: 30px;
            font-weight: bolder;
            margin: 20px 0;
        }

        .cursor {
            display: inline-block;
            color: black;
            animation: blink 0.7s steps(1) infinite;
        }

        @keyframes blink {
            50% {
                opacity: 0;
            }
        }


        .container{
            width: 75%;
            height: 100%;
            padding: 20px 20px;
            right: 2px;
            left: 2px;
            bottom: 2px;
            top: 4px;
            transition: 0.3s ease;
            background-color: rgb(205, 192, 253);
            position: absolute;
            backdrop-filter: blur(10px);
            border-radius: 10px;
            outline: none;
            border: 2px solid transparent;
            top: 20%;
            left: 10%;
            bottom: 10px;
            transition: 0.3s;
            overflow: hidden;
        }

        .container:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container:hover{
            /* transform: scale(1.1);*/
            transition: 2s;
            box-shadow: 0px 10px 10px #9f9fa0;
        }

        .container .username{
            padding-left: 6px;
            margin: 0 10%;
            outline: none;
            border: 2px solid transparent;
            border-radius: 5px;
            height: 8%;
            width: 50%;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
        }

        .container .email{
            padding-left: 6px;
            margin: 0 30%;
            outline: none;
            border: 2px solid transparent;
            border-radius: 5px;
            height: 8%;
            width: 50%;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
        }

        .container .password{
            padding-left: 6px;
            margin: 0 10%;
            outline: none;
            border: 2px solid transparent;
            border-radius: 5px;
            height: 8%;
            width: 50%;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
        }

        .container .username{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .username:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .email{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .email:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .password{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .password:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .login{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
            margin: 0 23%;
            width: 35%;
            height: 8%;
            outline: none;
            border-radius: 5px;
            border: 2px solid transparent;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
            cursor: pointer;
        }

        .container .login:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .toggle-password{
            border-radius: 20px;
            transition: 0.3s;
        }

        .container .toggle-password:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .bigger-circle{
            height: 300px;
            width: 300px;
            border-radius: 50%;
            margin: 0 25%;
        }

        .container .bigger-circle .circle{
            width: 200px;
            height: 200px;
            background-color: rgb(160, 146, 241);
            border-radius: 50%;
            margin: 0 25%;
            background-image: url('clickedImage.jpg');
            background-position: center;
        }

        .container .bigger-circle .circle:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .bigger-circle .add{
            height: 60px;
            width: 60px;
            border-radius: 50%;
            background-color: rgb(144, 128, 233);
            text-align: center;
            justify-content: center;
            color: beige;
            font-size: 50px;
            font-weight: bolder;
            position: absolute;
            left: 47%;
            bottom: 70%;
            cursor: pointer;
        }

        .container .bigger-circle .add:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }
    </style>
</head>
<body>
    <form action="/login" method="post">
        <h1 class="text-bank">
            Welcome in <span id="typed-text"></span><span class="cursor">|</span>
        </h1>

        <div class="container">
            <div class="bigger-circle">
                <div class="circle"></div><br>
                <div class="add" onclick="message()">+
                    <video src=""></video>
                </div><br>
            </div>
            <input type="text" name="username" placeholder="User Name" class="username"><br><br>
            <input type="email" name="email" placeholder="Email" class="email"><br><br>
            <input type="password" name="password" placeholder="Password" class="password" id="password-dispaly">
            <span class="toggle-password" onclick="togglePassword()" style="cursor: pointer;margin-left: 5px; color: rgb(24, 25, 26); font-size: 25px;">👁</span><br><br>
            <input type="submit" value="Login" class="login"><br><br><br>
            <p style="font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; margin: 7px 20%;">Don't have an  account?<a style="outline: none; border: 2px solid transparent; background: transparent; font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; color: blue; cursor: pointer;" href="create.html">Create Account</a></span></p>
        </div>
    </form>

    <form action="/create-account" method="post">
        <canvas class="create">
            <div>
                <p style="font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; margin: 7px 20%;">Don't have an  account?<input type="submit" value="Create Account" style="outline: none; border: 2px solid transparent; background: transparent; font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; color: blue; cursor: pointer;"></span></p>
            </div>
        </canvas>
    </form>
    <script>
    const phrases = ["Bank Of Divyanshu.", "BOD.", "Bank Platform."];
    let i = 0;
    let j = 0;
    let currentPhrase = [];
    let isDeleting = false;
    let isEnd = false;

    function loop() {
        const typedText = document.getElementById('typed-text');

        isEnd = false;
        typedText.innerHTML = currentPhrase.join('');

        if (i < phrases.length) {

            if (!isDeleting && j <= phrases[i].length) {
                currentPhrase.push(phrases[i][j]);
                j++;
            }

            if (isDeleting && j <= phrases[i].length) {
                currentPhrase.pop();
                j--;
            }

            if (j === phrases[i].length) {
                isEnd = true;
                isDeleting = true;
            }

            if (isDeleting && j === 0) {
                currentPhrase = [];
                isDeleting = false;
                i++;
                if (i === phrases.length) {
                    i = 0;
                }
            }
        }

        const speed = isEnd ? 1000 : isDeleting ? 50 : 100;
        setTimeout(loop, speed);
    }

    loop();

        function togglePassword(){
        let passwordField = document.getElementById("password-dispaly");
        passwordField.type = passwordField.type === "password"?"text":"password";
    }

    function message(){
        alert('Button Clicked');
        console.log('Button Clicked')
    }
    </script>
</body>
</html>
'''

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if password == "" or password == " " or password == "   " or password == "\t":
            return '<script>alert("Give Password")</script>'

        else:
            if bod.login(name= username, email= email, password= password):
                session['username'] = username
                '''return redirect(url_for('login_page'))'''
                return dashboard()

            else:
                flash("Invalid Credentials. Try again.")
                return redirect(url_for('login'))

            #'<p>Something going worng! :-( </p>'

@app.route('/create.html', methods= ['GET'])
def create_account_page():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank Of Divyanshu Login Page</title>
    <style>
        *{
            padding: 0;
            margin: 0;
        }

        body{
            background-color: beige;
        }

        .text-bank {
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            color: rgb(156, 134, 235);
            font-size: 30px;
            font-weight: bolder;
            margin: 20px 0;
        }

        .cursor {
            display: inline-block;
            color: black;
            animation: blink 0.7s steps(1) infinite;
        }

        @keyframes blink {
            50% {
                opacity: 0;
            }
        }

        .container{
            width: 75%;
            height: 100%;
            padding: 20px 20px;
            right: 2px;
            left: 2px;
            bottom: 2px;
            top: 4px;
            transition: 0.3s ease;
            background-color: rgb(205, 192, 253);
            position: absolute;
            backdrop-filter: blur(10px);
            border-radius: 10px;
            outline: none;
            border: 2px solid transparent;
            top: 20%;
            left: 10%;
            bottom: 10px;
            transition: 0.3s;
            overflow: hidden;
        }

        .container:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container:hover{
            /* transform: scale(1.1);*/
            transition: 2s;
            box-shadow: 0px 10px 10px #9f9fa0;
        }

        .container .username{
            padding-left: 6px;
            margin: 0 10%;
            outline: none;
            border: 2px solid transparent;
            border-radius: 5px;
            height: 8%;
            width: 50%;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
        }

        .container .email{
            padding-left: 6px;
            margin: 0 30%;
            outline: none;
            border: 2px solid transparent;
            border-radius: 5px;
            height: 8%;
            width: 50%;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
        }

        .container .password{
            padding-left: 6px;
            margin: 0 10%;
            outline: none;
            border: 2px solid transparent;
            border-radius: 5px;
            height: 8%;
            width: 50%;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
        }

        .container .username{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .username:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .email{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .email:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .password{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .password:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .login{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
            margin: 0 23%;
            width: 35%;
            height: 8%;
            outline: none;
            border-radius: 5px;
            border: 2px solid transparent;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            font-size: 15px;
            cursor: pointer;
        }

        .container .login:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .idbox{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .idbox:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .friend{
            background: rgba(255, 255, 255, 0.425);
            transition: 0.3s;
        }

        .container .friend:focus{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .toggle-password{
            border-radius: 20px;
            transition: 0.3s;
        }

        .container .toggle-password:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .bigger-circle{
            height: 300px;
            width: 300px;
            border-radius: 50%;
            margin: 0 25%;
        }

        .container .bigger-circle .circle{
            width: 200px;
            height: 200px;
            background-color: rgb(160, 146, 241);
            border-radius: 50%;
            margin: 0 25%;
            background-image: url('clickedImage.jpg');
            background-position: center;
        }

        .container .bigger-circle .circle:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }

        .container .bigger-circle .add{
            height: 60px;
            width: 60px;
            border-radius: 50%;
            background-color: rgb(144, 128, 233);
            text-align: center;
            justify-content: center;
            color: beige;
            font-size: 50px;
            font-weight: bolder;
            position: absolute;
            left: 47%;
            bottom: 70%;
            cursor: pointer;
        }

        .container .bigger-circle .add:hover{
            border: 2px solid transparent;
            box-shadow: 0px 10px 10px rgb(120, 97, 252);
        }
    </style>
</head>
<body>
    <form action="/create" method="post">
        <h1 class="text-bank">
            <span id="typed-text"></span><span class="cursor">|</span>
        </h1>

        <div class="container">
            <div class="bigger-circle">
                <div class="circle"></div><br>
                <div class="add" onclick="message()">+
                    <video src=""></video>
                </div><br>
            </div>
            <input type="text" name="username" placeholder="User Name" class="username"><br><br>
            <input type="email" name="email" placeholder="Email" class="email"><br><br>
            <input type="password" name="password" placeholder="Password" class="password" id="password-dispaly">
            <span class="toggle-password" onclick="togglePassword()" style="cursor: pointer;margin-left: 5px; color: rgb(24, 25, 26); font-size: 25px;">👁</span><br><br>
            <input type="submit" value="Sign Up" class="login"><br><br><br>
            <span style="font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; margin: 7px 20%;">Already have an account! <a href="/" style="outline: none; border: 2px solid transparent; background: transparent; font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; color: blue; cursor: pointer;">Login</a>
        </div>
    </form>

    <form action="/create-account" method="post">
        <canvas class="create">
            <div>
                <p style="font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; margin: 7px 20%;">Don't have an  account?<input type="submit" value="Create Account" style="outline: none; border: 2px solid transparent; background: transparent; font-size: 15px; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; color: blue; cursor: pointer;"></span></p>
            </div>
        </canvas>
    </form>
    <script>
    const phrases = ["Create Your Account. ", "Go To Login Page. ", "Create Your Account Hear To Login. "];
    let i = 0;
    let j = 0;
    let currentPhrase = [];
    let isDeleting = false;
    let isEnd = false;

    function loop() {
        const typedText = document.getElementById('typed-text');

        isEnd = false;
        typedText.innerHTML = currentPhrase.join('');

        if (i < phrases.length) {

            if (!isDeleting && j <= phrases[i].length) {
                currentPhrase.push(phrases[i][j]);
                j++;
            }

            if (isDeleting && j <= phrases[i].length) {
                currentPhrase.pop();
                j--;
            }

            if (j === phrases[i].length) {
                isEnd = true;
                isDeleting = true;
            }

            if (isDeleting && j === 0) {
                currentPhrase = [];
                isDeleting = false;
                i++;
                if (i === phrases.length) {
                    i = 0;
                }
            }
        }

        const speed = isEnd ? 1000 : isDeleting ? 50 : 100;
        setTimeout(loop, speed);
    }

    loop();
        function togglePassword(){
        let passwordField = document.getElementById("password-dispaly");
        passwordField.type = passwordField.type === "password"?"text":"password";
    }

    function message(){
        alert('Button Clicked');
        console.log('Button Clicked')
    }
    </script>
</body>
</html>
'''

@app.route('/create', methods= ['POST'])
def create():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    #id = request.form['ids']
    #friend = request.form['friend']
    '''createDatabase = User(id= id,name = username, email= email, password= password, friends= friend)
    db.session.add(createDatabase)
    db.session.commit()'''
    if bod.create(name= username, email= email, password= password):
        return login_page()

    else:
        return '<script>alert("User Already Exist")</script>'

@app.route('/dashboard', methods= ['GET'])
def dashboard() -> str:
    #return f"Welcome {session['username']}!"
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bank of Divyanshu Dashboard</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #f4f4f4;
    }

    header {
      background-color: #654de4;
      color: white;
      padding: 20px;
      text-align: center;
    }

    .search-container {
            width: 300px;
            margin: 50px auto;
            position: relative;
            border-radius: 10px;
            background: white;
            outline: none;
            border: 2px solid transparent;
            outline: none;
        }

        #searchInput {
            width: 100%;
            padding: 10px;
            font-size: 16px;
        }

        .suggestions {
            position: absolute;
            top: 40px;
            width: 100%;
            border: 1px solid #ccc;
            background: white;
            z-index: 10;
        }

        .suggestion-item {
            padding: 8px;
            cursor: pointer;
        }

        .suggestion-item:hover {
            background-color: #f0f0f0;
        }

    .menu-icon {
        font-size: 28px;
        cursor: pointer;
        position: absolute;
        top: 20px;
        left: 20px;
    }
      /* Sidebar */
      .sidebar {
        height: 100%;
        width: 0;
        position: fixed;
        z-index: 2;
        top: 0;
        left: 0;
        background-color: #034281;
        overflow-x: hidden;
        transition: 0.3s;
        padding-top: 60px;
      }
    .sidebar a {
        padding: 12px 25px;
        text-decoration: none;
        font-size: 18px;
        color: #ecf0f1;
        display: block;
      }
    .sidebar a:hover {
        background-color: #34495e;
      }

      .closebtn {
        position: absolute;
        top: 20px;
        right: 25px;
        font-size: 30px;
        color: white;
        cursor: pointer;
    }

    .auto-text {
      font-weight: bold;
      font-size: 24px;
    }

    .container {
      padding: 30px;
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      justify-content: center;
    }

    .card {
      background-color: white;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      padding: 20px;
      flex: 1 1 250px;
      max-width: 300px;
      text-align: center;
    }

    .card h2 {
      color: #333;
    }

    .card p {
      color: #777;
    }

    .logout-btn {
      margin-top: 20px;
      padding: 10px 20px;
      background-color: crimson;
      border: none;
      color: white;
      font-weight: bold;
      border-radius: 5px;
      cursor: pointer;
    }

    .logout-btn:hover {
      background-color: darkred;
    }

    .chatbot {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: white;
      border: 1px solid #ccc;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      width: 300px;
      max-height: 400px;
      display: flex;
      flex-direction: column;
    }

    .chatbot-header {
      background: #654de4;
      color: white;
      padding: 10px;
      text-align: center;
      border-radius: 10px 10px 0 0;
    }

    .chatbot-body {
      flex: 1;
      padding: 10px;
      overflow-y: auto;
      font-size: 14px;
    }

    .chatbot-footer {
      display: flex;
      border-top: 1px solid #ddd;
    }

    .chatbot-footer input {
      flex: 1;
      padding: 10px;
      border: none;
      border-radius: 0 0 0 10px;
    }

    .chatbot-footer .send-btn {
      padding: 10px;
      border: none;
      background: #654de4;
      color: white;
      border-radius: 0 0 10px 0;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <header>
    <span class="menu-icon" onclick="openSidebar()">☰</span>
    <div>Welcome to <span class="auto-text"></span></div>
  </header>

  <!-- Sidebar -->
  <div id="mySidebar" class="sidebar">
    <a href="javascript:void(0)" class="closebtn" onclick="closeSidebar()">×</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/">Login</a>
    <a href="/create.html">Create Account</a>
    <a href="/chatbot.html">Chat With AI</a>
    <a href="/chat.html">Chat With Friend's</a>
    <a href="/stock.html">Stock Marcket</a>
    <a href="/setting.html">Setting</a>
    <a href="#">Loan Help</a>
    <a href="/creator.html">Creator</a>
  </div>

  <div class="search-container">
    <input type="text" id="searchInput" placeholder="Search stocks...">
    <div id="suggestions" class="suggestions"></div>
  </div>

  <div class="container">
    <div class="card">
      <h2>Account Balance</h2>
      <p>₹50,000.00</p>
    </div>
    <div class="card">
      <h2>Recent Transactions</h2>
      <p>• ₹500 to Aman<br>• ₹1200 from Paytm</p>
    </div>
    <div class="card">
      <h2>Quick Links</h2>
      <p><a href="#">Send Money</a> | <a href="/setting.html">Settings</a></p>
    </div>
  </div>

  <form methods="post" action="/">
  <div style="text-align: center;">
    <input type="submit" value="Logout" class="logout-btn">
  </div>
    </form>

  <!-- Chatbot -->
  <div class="chatbot">
    <div class="chatbot-header">AI Assistant</div>
    <div class="chatbot-body" id="chatbot-body">
      <div><strong>Bot:</strong> Hello! How can I help you? (Login / Create Account / Take Loan)</div>
    </div>

    <div class="chatbot-footer">
        <input type="text" id="chat-input" placeholder="Ask something..." name="textbox" onkeypress="handleKeyPress(event)">
        <input type="submit" value="Send" class="send-btn" onclick="sendMessage()" id='button'>
    </div>
  </div>

  <script>
    const searchInput = document.getElementById('searchInput');
    const suggestionsBox = document.getElementById('suggestions');

    searchInput.addEventListener('input', () => {
        const query = searchInput.value;
        if (query.length === 0) {
            suggestionsBox.innerHTML = '';
            return;
        }

        fetch(`/autocomplete?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = '';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.classList.add('suggestion-item');
                    div.textContent = item;
                    div.onclick = () => {
                        searchInput.value = item;
                        suggestionsBox.innerHTML = '';
                    };
                    suggestionsBox.appendChild(div);
                });
            });
    });

    const autoText = ["Bank of Divyanshu.", "BOD.", "Bank Platform."];
    let aIndex = 0;
    let charIndex = 0;
    let currentText = "";
    let isDeleting = false;

    function typeText() {
      const display = document.querySelector(".auto-text");
      const fullText = autoText[aIndex];

      if (isDeleting) {
        currentText = fullText.substring(0, charIndex--);
      } else {
        currentText = fullText.substring(0, charIndex++);
      }

      display.textContent = currentText;

      if (!isDeleting && charIndex === fullText.length) {
        isDeleting = true;
        setTimeout(typeText, 1000);
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        aIndex = (aIndex + 1) % autoText.length;
        setTimeout(typeText, 300);
      } else {
        setTimeout(typeText, isDeleting ? 50 : 100);
      }
    }
    typeText();

    function sendMessage() {
      const input = document.getElementById('chat-input');
      const userMessage = input.value.trim();
      if (!userMessage) return;

      const chatbotBody = document.getElementById('chatbot-body');
      const userDiv = document.createElement('div');
      userDiv.innerHTML = `<strong>You:</strong> ${userMessage}`;
      chatbotBody.appendChild(userDiv);

      const botDiv = document.createElement('div');
      let response = "I didn't understand that.";
      if (userMessage.toLowerCase().includes("login")) {
        response = "To login, enter your ID and password on the login page.Or <a href='/'>Click hear to login.</a>";
      } else if (userMessage.toLowerCase().includes("create account")) {
        response = "To create an account, click 'Sign Up' and fill your details.Or <a href='/create.html'>Click hear to login.</a>";
      } else if (userMessage.toLowerCase().includes("loan")) {
        response = "To take a loan, go to 'Loan Section' and submit your KYC.";
      } else if (userMessage.toLowerCase().includes("hello")) {
        response = "Hello! How can I help you today?";
      }else if (userMessage.toLowerCase().includes("hi")) {
        response = "Hi 🖐! How can I help you today?";
      }else if (userMessage.toLowerCase().includes("bye")) {
        response = "Bye 🖐! Have a great day😊.";
      }else if (userMessage.toLowerCase().includes("thanks")) {
        response = "Your welcome, I'm gland to help you.";
      }else if (userMessage.toLowerCase().includes("ok")) {
        response = "😊";
      }else if (userMessage.toLowerCase().includes("😊")) {
        response = "😊";
      }else if (userMessage.toLowerCase().includes("🤨")) {
        response = "What's happend, you have any doubt.";
      }else if (userMessage.toLowerCase().includes("nice to meet you")) {
        response = "Me too...";
      }else if (userMessage.toLowerCase().includes("😂")) {
        response = "On what topic you where laughing!";
      }else if (userMessage.toLowerCase().includes("😴")) {
        response = "Bye 🖐, Good Night🌙.<br>Have a sweet dream😴";
      }else if (userMessage.toLowerCase().includes("how are you")) {
        response = "I'm fine you";
      }else if (userMessage.toLowerCase().includes("me too")) {
        response = "Oh, that's good!";
      }else if (userMessage.toLowerCase().includes("i also")) {
        response = "Oh, that's good!";
      }else if (userMessage.toLowerCase().includes("nice to meet you")) {
        response = "Me too. <br>How can I help you today.";
      }else if (userMessage.toLowerCase().includes("how to login")) {
        response = "To login, go to login page fill all the details and click 'login' button.";
      }else if (userMessage.toLowerCase().includes("how to create an account")) {
        response = "To create account, go to create account page fill all the details and click 'Sign Up' Button";
      }else if (userMessage.toLowerCase().includes("good night")) {
        response = "Bye 🖐, Good Night🌙.<br>Have a sweet dream😴";
      }else if (userMessage.toLowerCase().includes("your name")) {
        response = "My name is PYAI, I'm your AI Assistant.<br>I am here to help you to How to take Loan, How can you create your account, How can you login, etc.";
      }else if (userMessage.toLowerCase().includes("hlo")) {
        response = "Hello! How can I help you today?";
      }else if (userMessage.toLowerCase().includes("who are you")) {
        response = "I'm your AI Assistant.<br>I am here to help you";
      }else if (userMessage.toLowerCase().includes("open chat room")) {
        response = "To open AI Assistant chat room <a href='/chatbot.html'> Click Here</a>.";
      }

      botDiv.innerHTML = `<strong>Bot:</strong> ${response}`;
      chatbotBody.appendChild(botDiv);
      chatbotBody.scrollTop = chatbotBody.scrollHeight;
      input.value = "";
    }

    function openSidebar() {
        document.getElementById("mySidebar").style.width = "250px";
    }
    function closeSidebar() {
        document.getElementById("mySidebar").style.width = "0";
    }

    function handelKeyPress(event){
        if (event.key === "Enter"){
            sendMessage();
        }
    }
  </script>
</body>
</html>

'''

stock_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'BABA', 'INTC', 'Login', 'Sign In', 'Settings', 'Talk with AI', 'AI Chat Room', 'Chat with your friends', 'Creator', 'Loan Help', 'Doubt']

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').upper()
    results = [s for s in stock_list if query in s]
    return jsonify(results)

@app.route('/marcket.html')
def SuperMarts():
    pass

@app.route('/chat.html', methods= ['GET'])
def ChattingPage():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ChatApp | Dashboard</title>
  <style>
  body {
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
  background: linear-gradient(to right, #1c92d2, #f2fcfe);
  display: flex;
  height: 100vh;
}

.container {
  display: flex;
  width: 100%;
}

.sidebar {
  width: 25%;
  background: #2c3e50;
  color: white;
  padding: 20px;
  overflow-y: auto;
}

.friend {
  background: #34495e;
  margin: 10px 0;
  padding: 15px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.friend:hover {
  background: #3c6382;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: #ffffffcc;
  backdrop-filter: blur(5px);
}

#chatWith {
  margin-bottom: 10px;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 10px;
  background: #fafafa;
  margin-bottom: 15px;
}

.input-area {
  display: flex;
  gap: 10px;
}

.input-area input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #aaa;
}

.input-area button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background: #1c92d2;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}

.msg {
  margin: 5px 0;
}
</style>
  <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
</head>
<body>
  <div class="container">
    <div class="sidebar">
      <h2>Friends</h2>
      {% for friend, history in friends.items() %}
        <div class="friend" onclick="selectFriend('${{ friend }}')">
          <strong>${{ friend }}</strong>
          <p>Note: ${{ history[-1].message if history else 'No note yet' }}</p>
        </div>
      {% endfor %}
    </div>

    <div class="chat-area">
      <h2 id="chatWith">Chat</h2>
      <div id="chat-box" class="chat-box"></div>
      <form action='/server' methods= 'post'>
      <div class="input-area">
        <input id="message-input" type="text" placeholder="Type a message...">
        <input type='Submit' value='Send' name='message' onclick="sendMessage()">
      </div>
      </form>
    </div>
  </div>

  <script>
    const socket = io();
    let currentFriend = "";

    function selectFriend(friend) {
      currentFriend = friend;
      document.getElementById('chatWith').innerText = "Chat with " + friend;
      document.getElementById("chat-box").innerHTML = "";
      socket.emit("join", { friend: friend });
    }

    function sendMessage() {
      const msg = document.getElementById("message-input").value;
      if (msg && currentFriend) {
        socket.emit("send_message", {
          sender: "You",
          message: msg,
          friend: currentFriend
        });
        appendMessage("You", msg);
        document.getElementById("message-input").value = "";
      }
    }

    socket.on("receive_message", function(data) {
      if (data.sender !== "You") {
        appendMessage(data.sender, data.message);
      }
    });

    function appendMessage(sender, message) {
      const box = document.getElementById("chat-box");
      const msgDiv = document.createElement("div");
      msgDiv.className = "msg";
      msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
      box.appendChild(msgDiv);
      box.scrollTop = box.scrollHeight;
    }
  </script>
</body>
</html>
'''

@socketio.on("message")
def handle_message(msg):
    print(f"Received message: {msg}")
    send(msg, broadcast=True)  # Broadcast to all users

# Run Flask app with threading
def run_app():
    socketio.run(app, debug=True, host="0.0.0.0")

@app.route('/chatbot.html', methods=['GET'])
def chat():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Assistant</title>
    <style>
        body{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #f5f5f5;
        }

        header {
            background-color: transparent;
            color: black;
            padding: 20px;
            text-align: center;
        }

    .menu-icon {
        font-size: 28px;
        cursor: pointer;
        position: absolute;
        top: 20px;
        left: 20px;
    }
      /* Sidebar */
      .sidebar {
        height: 100%;
        width: 0;
        position: fixed;
        z-index: 2;
        top: 0;
        left: 0;
        background-color: #034281;
        overflow-x: hidden;
        transition: 0.3s;
        padding-top: 60px;
      }
    .sidebar a {
        padding: 12px 25px;
        text-decoration: none;
        font-size: 18px;
        color: #ecf0f1;
        display: block;
      }
    .sidebar a:hover {
        background-color: #34495e;
      }

      .closebtn {
        position: absolute;
        top: 20px;
        right: 25px;
        font-size: 30px;
        color: white;
        cursor: pointer;
    }

    .auto-text {
      font-weight: bold;
      font-size: 24px;
    }

        .chat-container{
            width: 300px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header{
            background: #0078ff;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
        }

        .chat-box{
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }

        .chat-box::-webkit-scrollbar{
            width: 5px;
        }

        .chat-box::-webkit-scrollbar-thumb{
            background: #ccc;
            border-radius: 5px;
        }

        .bot-message, .user-message{
            max-width: 75%;
            padding: 8px 12px;
            margin: 5px;
            border-radius: 10px;
            word-wrap: break-word;
        }

        .bot-message{
            background: #e1f5fe;
            align-self: flex-start;
        }

        .user-message{
            background: #dff8d8;
            align-self: flex-end;
        }

        .chat-input{
            display: flex;
            border-top: 1px solid #ddd;
            padding: 10px;
        }

        .chat-input input{
            flex: 1;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            outline: none;
        }

        .chat-input button{
            padding: 8px 15px;
            margin-left: 5px;
            border: none;
            background: #0078ff;
            color: white;
            cursor: pointer;
        }

        .chat-input button:hover{
            background:  #0056c1;
        }
    </style>
</head>
<body>
    <header>
    <span class="menu-icon" onclick="openSidebar()">☰</span>
    <div><span class="auto-text"></span></div>
  </header>

  <!-- Sidebar -->
  <div id="mySidebar" class="sidebar">
    <a href="javascript:void(0)" class="closebtn" onclick="closeSidebar()">×</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/">Login</a>
    <a href="/create.html">Create Account</a>
    <a href="/chatbot.html">Chat With AI</a>
    <a href="/chat.html">Chat With Friend's</a>
    <a href="/stock.html">Stock Marcket</a>
    <a href="/setting.html">Setting</a>
    <a href="#">Loan Help</a>
    <a href="/creator.html">Creator</a>
  </div>

    <div class="chat-container">
        <div class="chat-header">AI Assistant</div>
        <div class="chat-box" id="chatBox">
            <div class="bot-message">Hello 🖐! How can I help you today?</div>
        </div>
        <div class="chat-input">
            <input type="text" name="input-message" id="userInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        const chatBox = document.getElementById('chatBox');
        const userInput = document.getElementById('userInput');

        function sendMessage(){
            let message = userInput.value.trim();
            if (message === "")return;

            let userMessage = document.createElement("div");
            userMessage.className = "user-message";
            userMessage.innerText = message;
            chatBox.appendChild(userMessage);

            userInput.value = "";

            chatBox.scrollTop = chatBox.scrollHeight;

            setTimeout(() => {
                botResponse(message);
            }, 1000);
        }

            function botResponse(userMessage){
                let botReply = getBotResponse(userMessage.toLowerCase());

                let botMessage = document.createElement("div");
                botMessage.className = "bot-message"
                botMessage.innerText = botReply;

                chatBox.appendChild(botMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function getBotResponse(message){
                let response = "I didn't understand that.";
      if (message.toLowerCase().includes("login")) {
        response = "To login, enter your ID and password on the login page.";
      } else if (message.toLowerCase().includes("create account")) {
        response = "To create an account, click 'Sign Up' and fill your details.";
      } else if (message.toLowerCase().includes("loan")) {
        response = "To take a loan, go to 'Loan Section' and submit your KYC.";
      } else if (message.toLowerCase().includes("hello")) {
        response = "Hello! How can I help you today?";
      }else if (message.toLowerCase().includes("hi")) {
        response = "Hi 🖐! How can I help you today?";
      }else if (message.toLowerCase().includes("bye")) {
        response = "Bye 🖐! Have a great day😊.";
      }else if (message.toLowerCase().includes("thanks")) {
        response = "Your welcome, I'm gland to help you.";
      }else if (message.toLowerCase().includes("ok")) {
        response = "😊";
      }else if (message.toLowerCase().includes("😊")) {
        response = "😊";
      }else if (message.toLowerCase().includes("🤨")) {
        response = "What's happend, you have any doubt.";
      }else if (message.toLowerCase().includes("nice to meet you")) {
        response = "Me too...";
      }else if (message.toLowerCase().includes("😂")) {
        response = "On what topic you where laughing!";
      }else if (message.toLowerCase().includes("😴")) {
        response = "Bye 🖐, Good Night🌙.Have a sweet dream😴";
      }else if (message.toLowerCase().includes("how are you")) {
        response = "I'm fine you";
      }else if (message.toLowerCase().includes("me too")) {
        response = "Oh, that's good!";
      }else if (userMessage.toLowerCase().includes("i also")) {
        response = "Oh, that's good!";
      }else if (message.toLowerCase().includes("nice to meet you")) {
        response = "Me too. How can I help you today.";
      }else if (message.toLowerCase().includes("how to login")) {
        response = "To login, go to login page fill all the details and click 'login' button.";
      }else if (message.toLowerCase().includes("how to create an account")) {
        response = "To create account, go to create account page fill all the details and click 'Sign Up' Button";
      }else if (message.toLowerCase().includes("good night")) {
        response = "Bye 🖐, Good Night🌙.Have a sweet dream😴";
      }else if (message.toLowerCase().includes("your name")) {
        response = "My name is PYAI, I'm your AI Assistant. I am here to help you to How to take Loan, How can you create your account, How can you login, etc.";
      }else if (message.toLowerCase().includes("hlo")) {
        response = "Hello! How can I help you today?";
      }else if (message.toLowerCase().includes("who are you")) {
        response = "I'm your AI Assistant. I am here to help you.";
      }else if (message.toLowerCase().includes("open chat room")) {
        response = "To open AI Assistant chat room <a href='/chatbot.html'> Click Here</a>.";
      }else if (message.toLowerCase().includes("yo")) {
        response = "🤘 🤘 🤘...";
      }else if (message.toLowerCase().includes("yoo")) {
        response = "🤘 🤘 🤘...";
      }else if (message.toLowerCase().includes("op")) {
        response = "😊";
      }else if (message.toLowerCase().includes("👍")) {
        response = "Thank's";
      }else if (message.toLowerCase().includes("😥")) {
        response = "Don't be feel sad it's ok 😊";
      }else if (message.toLowerCase().includes("😭")) {
        response = "What's happen? Why are you craying? What's the matter?";
      }else if (message.toLowerCase().includes("😠")) {
        response = "Why are you so angry? What's the matter, feel free to ask any thing";
      }else if (message.toLowerCase().includes("wait")) {
        response = "Ok 👍.";
      }else if (message.toLowerCase().includes("good")) {
        response = "😊";
      }

      return response;
    }

            function handleKeyPress(event){
                if (event.key === "Enter"){
                    sendMessage()
                }
            }
    function openSidebar() {
        document.getElementById("mySidebar").style.width = "250px";
    }
    function closeSidebar() {
        document.getElementById("mySidebar").style.width = "0";
    }

    const autoText = ["Chat with your AI Assistant.", "Ask any doubt.", " Your AI Assistant welcome you."];
    let aIndex = 0;
    let charIndex = 0;
    let currentText = "";
    let isDeleting = false;

    function typeText() {
      const display = document.querySelector(".auto-text");
      const fullText = autoText[aIndex];

      if (isDeleting) {
        currentText = fullText.substring(0, charIndex--);
      } else {
        currentText = fullText.substring(0, charIndex++);
      }

      display.textContent = currentText;

      if (!isDeleting && charIndex === fullText.length) {
        isDeleting = true;
        setTimeout(typeText, 1000);
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        aIndex = (aIndex + 1) % autoText.length;
        setTimeout(typeText, 300);
      } else {
        setTimeout(typeText, isDeleting ? 50 : 100);
      }
    }
    typeText();
    </script>
</body>
</html>
'''

@app.route('/chatbot', methods= ['POST'])
def ChatBot():
    question = request.form.get('textbox').lower()
    response = "I'm not sure how to help with that."

    if not question:
        flash("Please type something before sending.", "error")
    elif question.lower() == "hello":
        flash("Hi there! How can I assist you?", "success")
    else:
        flash("Processing your request...", "info")

    return jsonify({"reply": response})
    '''return redirect('/')'''

@app.route('/stock.html')
def StockMarcket():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Stock Market Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            margin-top: 50px;
        }
        input {
            padding: 8px;
            font-size: 16px;
        }
        button {
            padding: 8px 12px;
            font-size: 16px;
            cursor: pointer;
        }
        canvas {
            margin-top: 30px;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <h1>📈 Stock Market Viewer</h1>
    <input type="text" id="symbol" placeholder="Enter Stock Symbol (e.g. AAPL)">
    <button onclick="fetchStock()">Get Data</button>

    <canvas id="stockChart"></canvas>

    <script>
        let chart;

        function fetchStock() {
            const symbol = document.getElementById('symbol').value;

            fetch('/get_stock', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({symbol})
            })
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('stockChart').getContext('2d');

                if (chart) chart.destroy(); // destroy previous chart

                chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.dates,
                        datasets: [{
                            label: `${symbol.toUpperCase()} Stock Price`,
                            data: data.prices,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1,
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: false
                            }
                        }
                    }
                });
            });
        }
    </script>
</body>
</html>
'''

@app.route('/setting.html')
def Setting():
    if request.method == "POST":
        session['theme'] = request.form.get('theme')
        session['font_size'] = request.form.get('font_size')
        session['brightness'] = request.form.get('brightness')
        session['accent_color'] = request.form.get('accent_color')
        return redirect(url_for("settings"))
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Settings - My Bank App</title>
  <style>
  :root {
  --bg-color: #ffffff;
  --text-color: #1f2937;
  --font-size: 16px;
  --brightness: 100%;
  --accent-color: #4CAF50;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  font-size: var(--font-size);
  filter: brightness(var(--brightness));
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  transition: all 0.3s ease;
}

    .menu-icon {
        font-size: 28px;
        cursor: pointer;
        position: absolute;
        top: 20px;
        left: 20px;
    }
      /* Sidebar */
      .sidebar {
        height: 100%;
        width: 0;
        position: fixed;
        z-index: 2;
        top: 0;
        left: 0;
        background-color: #034281;
        overflow-x: hidden;
        transition: 0.3s;
        padding-top: 60px;
      }
    .sidebar a {
        padding: 12px 25px;
        text-decoration: none;
        font-size: 18px;
        color: #ecf0f1;
        display: block;
      }
    .sidebar a:hover {
        background-color: #34495e;
      }

      .closebtn {
        position: absolute;
        top: 20px;
        right: 25px;
        font-size: 30px;
        color: white;
        cursor: pointer;
    }

.settings-card {
  background: #f3f4f6;
  padding: 30px 25px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 320px;
  transition: all 0.3s ease;
}

.settings-card h2 {
  margin-bottom: 20px;
  font-size: 24px;
  text-align: center;
}

.setting-group {
  margin-bottom: 18px;
}

.setting-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

.setting-group select,
.setting-group input[type="range"],
.setting-group input[type="color"] {
  width: 100%;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ccc;
  outline: none;
  transition: all 0.2s ease;
}

.btn-group {
  text-align: center;
  margin-top: 20px;
}

.btn-group button {
  background-color: var(--accent-color);
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-group button:hover {
  background-color: #3e8e41;
}
</style>
</head>
<body>
  <header>
    <span class="menu-icon" onclick="openSidebar()">☰</span>
  </header>

  <!-- Sidebar -->
  <div id="mySidebar" class="sidebar">
    <a href="javascript:void(0)" class="closebtn" onclick="closeSidebar()">×</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/">Login</a>
    <a href="/create.html">Create Account</a>
    <a href="/chatbot.html">Chat With AI</a>
    <a href="/stock.html">Stock Marcket</a>
    <a href="/setting.html">Setting</a>
    <a href="#">Loan Help</a>
    <a href="/creator.html">Creator</a>
  </div>

  <div class="settings-card">
    <h2>⚙️ Settings</h2>

    <div class="setting-group">
      <label for="theme-select">🌗 Theme</label>
      <select id="theme-select">
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
    </div>

    <div class="setting-group">
      <label for="font-size-select">🔠 Font Size</label>
      <select id="font-size-select">
        <option value="small">Small</option>
        <option value="medium" selected>Medium</option>
        <option value="large">Large</option>
      </select>
    </div>

    <div class="setting-group">
      <label for="brightness-slider">💡 Brightness</label>
      <input type="range" id="brightness-slider" min="50" max="150" value="100">
    </div>

    <div class="setting-group">
      <label for="accent-color-picker">🎨 Accent Color</label>
      <input type="color" id="accent-color-picker" value="#4CAF50">
    </div>

    <div class="btn-group">
      <button onclick="resetSettings()">Reset</button>
    </div>
  </div>

  <script>
  function applySettings() {
  const theme = localStorage.getItem('theme') || 'light';
  const fontSize = localStorage.getItem('fontSize') || '16px';
  const brightness = localStorage.getItem('brightness') || '100%';
  const accentColor = localStorage.getItem('accentColor') || '#4CAF50';

  document.documentElement.style.setProperty('--bg-color', theme === 'dark' ? '#111827' : '#ffffff');
  document.documentElement.style.setProperty('--text-color', theme === 'dark' ? '#f3f4f6' : '#1f2937');
  document.documentElement.style.setProperty('--font-size', fontSize);
  document.documentElement.style.setProperty('--brightness', brightness + '%');
  document.documentElement.style.setProperty('--accent-color', accentColor);

  document.getElementById('theme-select').value = theme;
  document.getElementById('font-size-select').value = fontSize === '14px' ? 'small' : fontSize === '18px' ? 'large' : 'medium';
  document.getElementById('brightness-slider').value = parseInt(brightness);
  document.getElementById('accent-color-picker').value = accentColor;
}

function updateSetting(key, value) {
  localStorage.setItem(key, value);
  applySettings();
}

document.addEventListener('DOMContentLoaded', () => {
  applySettings();

  document.getElementById('theme-select').addEventListener('change', e => {
    updateSetting('theme', e.target.value);
  });

  document.getElementById('font-size-select').addEventListener('change', e => {
    const sizeMap = {
      small: '14px',
      medium: '16px',
      large: '18px'
    };
    updateSetting('fontSize', sizeMap[e.target.value]);
  });

  document.getElementById('brightness-slider').addEventListener('input', e => {
    updateSetting('brightness', e.target.value);
  });

  document.getElementById('accent-color-picker').addEventListener('input', e => {
    updateSetting('accentColor', e.target.value);
  });
});

function resetSettings() {
  localStorage.clear();
  applySettings();
}

    function openSidebar() {
        document.getElementById("mySidebar").style.width = "250px";
    }
    function closeSidebar() {
        document.getElementById("mySidebar").style.width = "0";
    }

</script>
</body>
</html>

'''

@app.context_processor
def inject_settings():
    # Inject settings into every template
    return dict(
        theme=session.get("theme", "light"),
        font_size=session.get("font_size", "medium"),
        brightness=session.get("brightness", "100"),
        accent_color=session.get("accent_color", "#4CAF50")
    )

@app.route('/loan.html')
def Loan():
    pass

@app.route('/creator.html')
def Creator():
    #creator = CreatorProfile.query.first()
    '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creator Profile</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #1c92d2, #f2fcfe); text-align: center; }
        .profile-container { width: 60%; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
        .profile-pic { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; margin: 10px; }
        .social-links a { text-decoration: none; margin: 5px; color: #1c92d2; font-size: 18px; }
    </style>
</head>
<body>

    <div class="profile-container">
        <img src="{{ creator.profile_pic }}" alt="Profile Picture" class="profile-pic">
        <h1>{{ creator.name }}</h1>
        <p>{{ creator.bio }}</p>
        <h3>Projects</h3>
        <p>{{ creator.projects }}</p>
        <h3>Connect with me</h3>
        <div class="social-links">
            {% for key, value in creator.social_links | fromjson.items() %}
                <a href="{{ value }}" target="_blank">{{ key }}</a>
            {% endfor %}
        </div>
    </div>

</body>
</html>
'''

@app.route('/stock', methods= ['GET'])
def stock():
    symbol = request.json['symbol']
    stock = yf.Ticker(symbol)
    hist = stock.history(period="7d")  # Last 7 days

    dates = hist.index.strftime('%Y-%m-%d').tolist()
    prices = hist['Close'].tolist()

    return jsonify({'dates': dates, 'prices': prices})

if __name__ == "__main__":
    app.run(debug=False, host= '0.0.0.0', port= 8000)