import mysql.connector
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_bcrypt import Bcrypt  
from flask_login import  UserMixin, login_user, LoginManager, login_required, current_user, logout_user


newapp = Flask(__name__)
bcrypt = Bcrypt(newapp)
newapp.config['SECRET_KEY'] = 'sql@Prism1920'

def get_db_connection():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password= "sql@Prism1920",
        database = "BugSearch"
    )
    return mydb
my_db=get_db_connection()
# create login manager
login_manager = LoginManager()
login_manager.init_app(newapp)

# user class with usermixin
class User(UserMixin):
    def __init__(self,user_id, email_id, passcode, username):
        self.user_id = user_id
        self.email_id = email_id
        self.passcode = passcode
        self.username = username

    @staticmethod
    def find_by_email_id(email_id):
        cursor = my_db.cursor(dictionay=True)
        query = "SELECT * FROM users WHERE email_id = %s"
        cursor.execute(query, (email_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(*row)
        return None

    @staticmethod
    def get(user_id):
        cursor = my_db.cursor()
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return User(*row)
        return None

    @staticmethod
    def create(email_id, passcode, username):
        cursor = my_db.cursor()
        hashed_passcode =bcrypt.generate_password_hash(passcode)
        query = "INSERT INTO users (email_id, passcode, name) VALUES (%s, %s, %s)"
        cursor.execute(query, (email_id, hashed_passcode, username))
        user_id=cursor.lastrowid
        my_db.commit()
        cursor.close()
        return User(user_id=user_id, email_id=email_id,passcode=hashed_passcode, username=username)

    def check_passcode(self, passcode):
        return bcrypt.check_password_hash(self.passcode, passcode)









# create user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

def get_user(user_id=None,email_id=None,username=None,passcode=None):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    if user_id:
        cur.execute('SELECT * FROM Users WHERE user_id = %s',(user_id,))
    if email_id:
        cur.execute('SELECT * FROM Users WHERE email_id = %s',(email_id,))
    if username:
        if passcode:
            passcode  = bcrypt.generate_passcode_hash(passcode)
            cur.execute("SELECT * FROM Users WHERE username=%s AND passcode=%s", (username, passcode))
        else:
            cur.execute('SELECT * FROM Users WHERE username = %s',(username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user 

def get_userid(user_id=None,email_id=None,username=None,passcode=None):
    user=get_user()
    return user['user_id']

    
@newapp.route('/',methods=["GET"])
def login_home():
    return render_template('login_home.html')


@newapp.route('/users/<int:user_id>/user_home',methods=["GET",])
def user_home(user_id):
    user = get_user(user_id=user_id)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM Questions')
    questions = cur.fetchall()
    conn.close()
    return render_template('user_home.html', user=user, questions=questions)

@newapp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email_id = request.form['email_id']
        user1 = get_user(email_id=email_id)
        username = request.form['username']
        user2 = get_user(username=username)
        passcode = request.form['passcode']
        if not email_id:
            flash('email_id address is required!')
        if not username:
            flash('Username is required!')
        if not passcode:
            flash('Please set passcode!')
        if user1 is not None :
            flash('This email_id address is already registered, please login!')
        if user2 is not None :
            flash('Username already exists please enter other username!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            passcode  = bcrypt.generate_password_hash(passcode)
            cur.execute('INSERT INTO Users (email_id, username, passcode) VALUES (%s, %s, %s)',(email_id, username, passcode))
            cur.execute('SELECT LAST_INSERT_ID()')
            user_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return redirect(url_for('user_home', user_id=user_id))
    return render_template('signup.html')


@newapp.route("/login",methods=["GET","POST"])
def userlogin():
    if (request.method=="POST"):
        username=request.form["username"]
        passcode=request.form["passcode"]
        if not username:
            flash("Username is required")
        if not passcode:
            flash("Password is required")
        else:
            user=get_user(username=username,passcode=passcode)
            if user is None:
                flash("Incorrect passcode or username")
                return render_template('login.html')
            elif (session[user["user_id"]]==user['user_id']):
                flash("Already login")
                return redirect(url_for('user_home',user_id=user['user_id']))
            else:
                flash("Login successfully")
                session[user['user_id']] = user['user_id'] 
                return redirect(url_for('user_home',user_id=user['user_id']))
    return render_template("login.html")

            
@newapp.route("/help",methods=["GET",])
def help_page():
    return render_template("help_page.html")

@newapp.route("/forgot_passcode",methods=["GET"])
def forgot_passcode():  
    return render_template('forgot_passcode.html')







if __name__=="__main__":
    newapp.run(debug=True)