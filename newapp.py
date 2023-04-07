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
login_manager.login_view = 'login'
login_manager.id_attribute = 'get_id'


# user class with usermixin
class User(UserMixin):
    def __init__(self, user_id , email_id, passcode, username):
        
        self.user_id = user_id
        self.email_id = email_id
        self.passcode = passcode
        self.username = username

    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def find_by_email_id(email_id):
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT user_id,passcode,username,email_id FROM users WHERE email_id = %s"
        cursor.execute(query, (email_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(*row)
        return None

    
    @staticmethod
    def find_by_username(username):
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT user_id,passcode,username,email_id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(*row)
        return None

    
    @staticmethod
    def get(user_id):
        cursor = my_db.cursor()
        query = "SELECT user_id,passcode,username,email_id FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return User(*row)

    @staticmethod
    def create(email_id, passcode, username):
        cursor = my_db.cursor()
        hashed_passcode =bcrypt.generate_password_hash(passcode)
        query = "INSERT INTO users (email_id, passcode, username) VALUES (%s, %s, %s)"
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
#------------------update into database---------------------
# def post_questions():

    
# -------------logged user--------------------------------

@login_required
@newapp.route('/users/user_home',methods=["GET",])
def user_home():
    user=current_user
    # cur = my_db.cursor(dictionary=True)
    # cur.execute('SELECT * FROM Questions')
    # questions = cur.fetchall()
    return render_template('user_home.html')

@login_required
@newapp.route('/logout',methods=['GET',])
def logout():
    logout_user()
    return redirect(url_for('userlogin'))

# @login_required
# @newapp.route("/users/help",methods=["GET",])
# def user_help():
#     return render_template("user_help.html")




# @login_required
# @newapp.route('/users/questions',methods=['GET','POST','UPDATE','DELETE'])
# def user_question():
#      if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         tags=request.form['tags']
#         if not title:
#             flash('Title is required.', 'error')
#         elif not content:
#             flash('Content is required.', 'error')
#         elif not tags:
#             flash('tags required.', 'error')
#         else:
#             question = Question(title=title, content=content, author=current_user)
#             db.session.add(question)
#             db.session.commit()
#             flash('Question posted successfully!', 'success')
#             return redirect(url_for('main.home'))



@login_required
@newapp.route('/users/all_users',methods=["GET",])
def all_users():
    return render_template('all_users.html')

@login_required
@newapp.route("/users/badges",methods=["GET",])
def badges():
    return render_template('badges.html')

@login_required
@newapp.route('/users/bookmarks',methods=['GET',])
def user_bookmarks():
    return render_template('bookmarks.html')

@login_required
@newapp.route("/users/complete_your_profile",methods=["GET",'POST'])
def complete_your_profile():
    return render_template("complete_your_profile.html")

@login_required
@newapp.route('/users/dashboard', methods=['GET',])
def dashboard():
    return render_template("dashboard.html")

@login_required
@newapp.route("/users/followers", methods=["GET",])
def followers():
    return render_template("followers.html")

@login_required
@newapp.route("/users/following", methods=["GET",])
def following():
    return render_template("following.html")


@login_required
@newapp.route('/users/help_with_login',methods=['GET',])
def help_with_login():
    return render_template('help_with_login.html')

@login_required
@newapp.route("/users/questions",methods=["GET","POST","DELETE"])
def questions():
    return render_template('posted_questions.html')

@login_required
@newapp.route("/users/comments",methods=["GET","POST","DELETE"])
def comments():
    return render_template('posted_comments.html')

@login_required
@newapp.route("/users/answers",methods=["GET","POST","DELETE"])
def answers():
    return render_template('posted_answers.html')

@login_required
@newapp.route('/users/recommendations',methods=['GET',])
def recommendations():
    return render_template('recommendations.html')

@login_required
@newapp.route('/users/tags',methods=['GET',])
def tags_login():
    return render_template('tag_login.html')

@login_required
@newapp.route('/users/trending',methods=['GET',])
def trending():
    return render_template('trending.html')

@newapp.route('/signup', methods=('GET', 'POST'))
def signup():
    if(current_user.is_authenticated):
        return redirect(url_for('user_home'))
    elif request.method == 'POST':
        email_id = request.form['email_id']
        username = request.form['username']
        passcode = request.form['passcode']
        if not email_id:
            flash('email_id address is required!')
        elif not username:
            flash('Username is required!')
        elif not passcode:
            flash('Please set passcode!')
        elif (User.find_by_email_id(email_id)) is not None :
            flash('This email_id address is already registered, please login!')
        elif (User.find_by_username(username)) is not None :
            flash('Username already exists please enter other username!')
        else:
            user=User.create(username=username,email_id=email_id,passcode=passcode)
            login_user(user)
            return redirect(url_for('user_home'))
    return render_template('signup.html')



@newapp.route("/login",methods=["GET","POST"])
def userlogin():
    if(current_user.is_authenticated):
        return redirect(url_for('user_home'))
    elif (request.method=="POST"):
        username=request.form["username"]
        passcode=request.form["passcode"]
        remember = True if request.form.get('remember') else False
        if not username:
            flash("Username is required")
        if not passcode:
            flash("Password is required")
        else:
            user=User.find_by_username(username=username)
            if (user is None) or (user.check_passcode(passcode=passcode)) :
                flash("Incorrect passcode or username")
                return render_template('login.html')
            else:
                flash("Login successfully")
                login_user(user,remember=remember) 
                return redirect(url_for('user_home'))
    return render_template("login.html")

@newapp.route('/help',methods=["GET",])
def help():
    return render_template("help.html")
            
@newapp.route('/tags',methods=['GET',])
def tags():
    return render_template('tags.html')

@newapp.route("/forgot_password",methods=["GET"])
def forgot_password():  
    return render_template('password_reset_1.html')

@newapp.route("/reset_password",methods=["GET",'POST'])
def reset_password():
    return render_template('password_reset_2.html')

@newapp.route('/search',methods=["GET"])
def search_without_login():
    return render_template('search_without_login.html')

@newapp.route('/',methods=["GET"])
def homepage():
    return render_template('index.html')





if __name__=="__main__":
    newapp.run(debug=True)