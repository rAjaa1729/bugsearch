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
login_manager.id_attribute ='get_id'

#-------different class object---------------
# user class with usermixin
class User(UserMixin):
    def __init__(self, user_id , email_id, passcode, username,creation_date,profile_image_url,reputation_points,about,badge,nfollowing,nfollower):
        
        self.user_id = user_id
        self.email_id = email_id
        self.passcode = passcode
        self.username = username
        self.creation_date=creation_date
        self.profile_image_url=profile_image_url
        self.reputation_points=reputation_points
        self.about=about
        self.badge=badge
        self.nfollowing=nfollowing
        self.nfollower=nfollower
        
    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def find_by_email_id(email_id):
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email_id = %s"
        cursor.execute(query, (email_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(*row)
        return None

    
    @staticmethod
    def find_by_username(username):
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
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

    @staticmethod
    def create(email_id, passcode, username):
        cursor = my_db.cursor()
        hashed_passcode =bcrypt.generate_password_hash(passcode).decode('utf-8')
        query = "INSERT INTO users (email_id, passcode, username) VALUES (%s, %s, %s)"
        cursor.execute(query, (email_id, hashed_passcode, username))
        my_db.commit()
        user_id=cursor.lastrowid
        query="SELECT * FROM USERS WHERE user_id=%s"
        cursor.execute(query,(user_id,))
        row=cursor.fetchone()
        my_db.commit()
        cursor.close()
        return User(*row)
    
    @staticmethod
    def update_profile(user,about,profile_image_url,tags):
        cursor=my_db.cursor(dictionary=True)
        query="UPDATE Users SET about=%s,profile_image_url=%s WHERE user_id=%s"
        val=(about,profile_image_url,user.user_id)
        cursor.execute(query,val) 
        my_db.commit()
        cursor.execute("SELECT * FROM Users WHERE user_id=%s",(user.user_id,))
        row=cursor.fetchone()
        cursor.close()
        # i am not handling tags till now
        return User(*row)


#---questions class----
class Question():
    def __init__(self,question_id,title,body,answer_id,user_id,score,creation_date,upvotes,downvotes,answer_count,comment_count):
        self.question_id=question_id 
        self.title=title 
        self.body=body 
        self.answer_id=answer_id 
        self.user_id=user_id 
        self.score=score 
        self.creation_date=creation_date 
        self.comment_count=comment_count 
        self.answer_count=answer_count 
        self.upvotes=upvotes 
        self.downvotes=downvotes
    @staticmethod
    def post_question(title,body,tags):
        cursor=my_db.cursor(dictionary=True)
        query="INSERT INTO QUESTIONS (title,body,user_id) VALUES(%s,%s,%s)"
        cursor=my_db.execute(query,(title,body,current_user.user_id))
        question_id=cursor.lastrowid
        my_db.commit()
        for tag in tags:
            query="INSERT INTO Questiontags (tag_id,question_id) VALUES(%s,%s)"
            cursor.execute(query,(tag.tag_id,question_id))
        cursor.close()
        my_db.commit()
        if question_id is None:
            return "failed", 400
        else:
            return "Successfully posted",200
        
    # for deleting question by question_id
    # @staticmethod
    # def delete_question_by_id(question_id):
        
    
    #finding question by using its question_id
    @staticmethod
    def find_by_question_id(question_id):
        query="SELECT * FROM Questions WHERE question_id=%s"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id))
        row=cursor.fetchone()
        if row:
            return Question(*row)
        return None
    
    #sorted by creation date finding comments of question
    @staticmethod
    def get_comments_by_question_id(question_id):
        query = "SELECT * FROM Comments WHERE post_id = %s AND post_type = %s ORDER BY creation_date ASC LIMIT 5"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id,"question"))
        comments=cursor.fetchall()
        cursor.close()
        if comments:
            return comments
        return None
        
    #sorted by creation_date finding answers of question_id
    @staticmethod
    def find_answers_by_question_id(question_id):
        query = "SELECT * FROM Answers WHERE question_id = %s ORDER BY creation_date ASC LIMIT 5"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,question_id)
        answers=cursor.fetchall()
        cursor.close()
        if answers:
            return answers
        return None
    
    #finding accepted answer of that question using question object
    @staticmethod
    def get_accepted_answer_of_question_id(question):
        answer_id=question.answer_id
        query = "SELECT * FROM Answers WHERE answer_id = %s "
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,answer_id)
        answer=cursor.fetchone()
        cursor.close()
        if answer:
            return Answer(*answer)
        return None
    
        
# -----class for Answer object--------------
class Answer():
    def __init__(self,question_id,body,answer_id,user_id,score,creation_date,upvotes,downvotes,comment_count):
        self.question_id=question_id 
        self.body=body 
        self.answer_id=answer_id 
        self.user_id=user_id 
        self.score=score 
        self.creation_date=creation_date 
        self.comment_count=comment_count 
        self.upvotes=upvotes 
        self.downvotes=downvotes

    @staticmethod
    def post_answer(question_id,body):
        cursor=my_db.cursor(dictionary=True)
        query="INSERT INTO Answers (body,user_id,question_id) VALUES(%s,%s,%s)"
        cursor=my_db.execute(query,(body,current_user.current_user.user_id,question_id))
        answer_id=cursor.lastrowid
        my_db.commit()
        cursor.close()
        if answer_id is None:
            return "failed", 400
        else:
            return "Successfully posted",200
    
    @staticmethod
    def find_by_answer_id(answer_id):
        query="SELECT * FROM Answers WHERE answer_id=%s"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(answer_id))
        row=cursor.fetchone()
        if row:
            return Answer(*row)
        return None
    
    # sorted by creation_date finding comments of answer using using answer_id
    @staticmethod
    def get_comments_by_answer_id(answer_id):
        query = "SELECT * FROM Comments WHERE post_id = %s AND post_type = %s ORDER BY creation_date ASC LIMIT 5"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(answer_id,"answer"))
        comments=cursor.fetchall()
        cursor.close()
        if comments:
            return comments
        return None 
# ----comments class-----------------

class Comment():
    def __init__(self,comment_id,body,creation_date,user_id,post_id,post_type):
        self.comment_id=comment_id
        self.body=body
        self.user_id=user_id
        self.creation_date=creation_date
        self.post_id=post_id
        self.post_type=post_type

    @staticmethod
    def post_comment(post_id,post_type,body):
        cursor=my_db.cursor(dictionary=True)
        query="INSERT INTO Comments (body,user_id,post_id,post_type) VALUES(%s,%s,%s,%s)"
        cursor=my_db.execute(query,(body,current_user.current_user.user_id,post_id,post_type))
        comment_id=cursor.lastrowid
        my_db.commit()
        cursor.close()
        if comment_id is None:
            return "failed", 400
        else:
            return "Successfully posted",200 
    


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
    # cur = my_db.cursor(dictionary=True)
    # cur.execute('SELECT * FROM Questions')
    # questions = cur.fetchall()
    return render_template('user_home.html',user=current_user)

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
def all_users(user):
    return render_template('all_users.html',user=user)

@login_required
@newapp.route("/users/badges",methods=["GET",])
def badges(user):
    return render_template('badges.html',user=user)

@login_required
@newapp.route('/users/bookmarks',methods=['GET',])
def bookmarks(user):
    return render_template('bookmarks.html',user=user)

@login_required
@newapp.route("/users/complete_your_profile",methods=["GET",'POST'])
def complete_your_profile():
    if request.method=='POST':
        # image_url=request.form['profile_image_url']
        profile_image_url = request.form.get('profile_image_url', '')
        about=request.form['about']
        tags=request.form['tags']
        user=User.update_profile(user=current_user,profile_image_url  = profile_image_url,tags=tags,about=about)
        return redirect(url_for('user_home',user=user))
    return render_template("complete_your_profile.html",user=current_user)

@login_required
@newapp.route('/users/dashboard', methods=['GET',])
def dashboard(user):
    return render_template("dashboard.html",user=user)

@login_required
@newapp.route("/users/followers", methods=["GET",])
def followers(user):
    return render_template("followers.html",user=user)

@login_required
@newapp.route("/users/following", methods=["GET",])
def following(user):
    return render_template("following.html",user)


@login_required
@newapp.route('/users/help_with_login',methods=['GET',])
def help_with_login():
    return render_template('help_with_login.html',user=current_user)

@login_required
@newapp.route("/users/questions",methods=["GET","POST","DELETE"])
def questions(user):
    return render_template('posted_questions.html',user=user)

@login_required
@newapp.route("/users/comments",methods=["GET","POST","DELETE"])
def comments(user):
    return render_template('posted_comments.html',user)

@login_required
@newapp.route("/users/answers",methods=["GET","POST","DELETE"])
def answers(user):
    return render_template('posted_answers.html',user=user)

@login_required
@newapp.route('/users/recommendations',methods=['GET',])
def recommendations(user):
    return render_template('recommendations.html',user=user)

@login_required
@newapp.route('/users/tags',methods=['GET',])
def tags_login(user):
    return render_template('tag_login.html',user=user)

@login_required
@newapp.route('/users/trending',methods=['GET',])
def trending(user):
    return render_template('trending.html',user=user)

@newapp.route('/signup', methods=('GET', 'POST'))
def signup():
    # if(current_user.is_authenticated):
    #     return redirect(url_for('user_home'))
    if request.method == 'POST':
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
            return redirect(url_for('complete_your_profile'))
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
            if (user is None):
                flash("Incorrect passcode ")
                return render_template('login.html')
            elif (bcrypt.check_password_hash(user.passcode,passcode)):
                flash("Incorrect password ")
                return render_template('login.html')
            else:
                flash("Login successfully")
                login_user(user,remember=remember) 
                return redirect(url_for('user_home',user=user))
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