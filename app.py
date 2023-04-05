import mysql.connector
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt()

def get_db_connection():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "142857",
        database = "BugSearch"
    )
    return mydb

def get_user(user_id=None,email_id=None,username=None,passcode=None):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    if user_id:
        cur.execute('SELECT * FROM Users WHERE user_id = %s',(user_id,))
    if email_id:
        cur.execute('SELECT * FROM Users WHERE email_id = %s',(email_id,))
    if username:
        if passcode:
            cur.execute("SELECT * FROM Users WHERE username=%s AND passcode=%s", (username, passcode))
        else:
            cur.execute('SELECT * FROM Users WHERE username = %s',(username,))
    user = cur.fetchone()
    conn.close()
    return user 

app = Flask(__name__)
app.config['SECRET_KEY'] = '142857'

@app.route('/')
def login_home():
    return render_template('login_home.html')

@app.route('/<int:user_id>/home')
def user_home(user_id):
    user = get_user(user_id=user_id)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM Questions')
    questions = cur.fetchall()
    conn.close()
    return render_template('user_home.html', user=user, questions=questions)

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email_id = request.form['email_id']
        user1 = get_user(email_id=email_id)
        username = request.form['username']
        user2 = get_user(username=username)
        password = request.form['password']
        if not email_id:
            flash('Email address is required!')
        elif not username:
            flash('Username is required!')
        elif not password:
            flash('Please set password!')
        elif user1 is not None :
            flash('This email address is already registered, please login!')
        elif user2 is not None :
            flash('Username already exists please enter other username!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            passcode = bcrypt.generate_password_hash(password)
            cur.execute('INSERT INTO Users (email_id, username, passcode) VALUES (%s, %s, %s)',
                            (email_id, username, passcode))
            cur.execute('SELECT LAST_INSERT_ID()')
            user_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return redirect(url_for('user_home', user_id=user_id))
    return render_template('signup.html')
        

@app.route("/login", methods=("GET","POST"))
def login():
    if (request.method=="POST"):
        username=request.form['username']
        password=request.form['password']
        if not username:
            flash("Username is required!")
        elif not password:
            flash("Password is required!")
        else:
            user = get_user(username=username)
            if user is None:
                flash("No such user exists!")
            else:
                verify_pw = bcrypt.check_password_hash(user['passcode'], password)
                if verify_pw == False:
                    flash("Incorrect password or username")
                else:
                    user_id = user['user_id']
                    return redirect(url_for('user_home', user_id=user_id))
    return render_template('login.html')



            

                






