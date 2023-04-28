import mysql.connector
# import openai
# import os
# from monkeylearn import MonkeyLearn
# import logging
from flask import Flask, render_template, request, url_for, flash, redirect,jsonify
from werkzeug.exceptions import abort
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
from threading import Thread 
import jwt 
import json 
import requests 
from datetime import datetime, timedelta



# from flask_bcrypt import Bcrypt  
# import hashlib
from flask_login import  UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_mail import Message, Mail 
# hashfun=hashlib.new("SHA256")

newapp = Flask(__name__)
newapp.config['DEBUG'] = True
newapp.config['MAIL_SERVER'] = 'smtp.iitd.ac.in'
newapp.config['MAIL_PORT'] = 25
newapp.config['MAIL_USE_TLS'] = True
newapp.config['MAIL_USE_SSL'] = False 
newapp.config['MAIL_DEBUG'] =True
newapp.config['MAIL_USERNAME'] = "cs1210566@iitd.ac.in"
newapp.config['MAIL_DEFAULT_SENDER'] = "cs1210566@iitd.ac.in"
newapp.config['MAIL_PASSWORD'] = "dec2e841"
mail = Mail(newapp)
# bcrypt = Bcrypt()
newapp.config['SECRET_KEY'] = 'sql@Prism1920'
# openai.api_key = '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'


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

# create user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# @newapp.route('/search/openai', methods=["GET"])
# def providemessages():
#     print("rajdnklf;asdjfk")
#     query = request.form['search']  # get the value of the query parameter
#     print(query)
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=query,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )
#     message = response.choices[0].text.strip()
#     return render_template('check.html',message=message)



#-------different class object---------------
# user class with usermixin
class User(UserMixin):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.email_id = kwargs.get('email_id')
        self.passcode = kwargs.get('passcode')
        self.username = kwargs.get('username')
        self.creation_date = kwargs.get('creation_date')
        self.profile_image_url = kwargs.get('profile_image_url')
        self.reputation_points = kwargs.get('reputation_points')
        self.about = kwargs.get('about')
        self.badge = kwargs.get('badge')
        self.nfollowing = kwargs.get('nfollowing')
        self.nfollowers = kwargs.get('nfollowers')
        
    def get_id(self):
        return str(self.user_id)
    
    @staticmethod
    def find_by_email_id(email_id):
        my_db=get_db_connection()
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE email_id = %s"
        cursor.execute(query, (email_id,))
        row = cursor.fetchone()
        my_db.close()
        if row:
            return User(**row)
        return None

    
    @staticmethod
    def find_by_username(username):
        my_db=get_db_connection()
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE username = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        # cursor.close()
        my_db.close()
        if row:
            return User(**row)
        return None

    
    @staticmethod
    def get(user_id):
        my_db=get_db_connection()
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        # cursor.close()
        my_db.close()
        if row:
            return User(**row)
        return None

    @staticmethod
    def create(email_id, passcode, username):
        my_db=get_db_connection()
        cursor = my_db.cursor(dictionary=True)
        # hashed_passcode=bcrypt.hashpw(passcode.encode('utf-8'), bcrypt.gensalt())
        hashed_passcode=passcode
        query = "INSERT INTO Users (email_id, passcode, username) VALUES (%s, %s, %s)"
        cursor.execute(query, (email_id, hashed_passcode, username))
        my_db.commit()
        user_id=cursor.lastrowid
        query="SELECT * FROM Users WHERE user_id=%s"
        cursor.execute(query,(user_id,))
        row=cursor.fetchone()
        # my_db.commit()
        # cursor.close()
        my_db.close()
        return User(**row)
    
    @staticmethod
    def update_profile(user,about,profile_image_url,tags):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="UPDATE Users SET about=%s,profile_image_url=%s WHERE user_id=%s"
        val=(about,profile_image_url,user.user_id)
        cursor.execute(query,val) 
        my_db.commit()
        cursor.execute("SELECT * FROM Users WHERE user_id=%s",(user.user_id,))
        row=cursor.fetchone()
        my_db.close()
        return User(**row)
    
    @staticmethod
    def find_followers(user_id):
        my_db=get_db_connection()
        query = "SELECT follower_id FROM Followertags WHERE following_id = %s ORDER BY creation_date DESC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(user_id,))
        fol_id=cursor.fetchall()
        u_list=[]
        my_db.close()
        print(fol_id)
        for f_id in fol_id:
            u_list.append(User.get(f_id['follower_id']))
        return u_list

    @staticmethod
    def find_followings(user_id):
        print("raja is here")
        my_db=get_db_connection()
        query = "SELECT following_id FROM Followertags WHERE follower_id = %s ORDER BY creation_date DESC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(user_id,))
        foll_id=cursor.fetchall()
        u_list=[]
        print(foll_id)
        my_db.close()
        for f_id in foll_id:
            u_list.append(User.get(f_id['follower_id']))
        print(u_list)
        return u_list
    
    @staticmethod
    def get_reset_token(username):
        return jwt.encode({'reset_password': username, 'exp': datetime.utcnow() + timedelta(minutes = 30)}, key=newapp.config['SECRET_KEY'])

    @staticmethod
    def set_password(username,passcode):
        my_db=get_db_connection()
        cursor = my_db.cursor(dictionary=True)
        query = "UPDATE Users SET passcode = %s WHERE username = %s"
        cursor.execute(query, (passcode,username,))
        my_db.commit()
        my_db.close()
        user = User.find_by_username(username)
        if user.passcode == passcode: return 1
        else: return 0
        

    @staticmethod
    def find_allusers():
        my_db=get_db_connection()
        cursor = my_db.cursor(dictionary=True)
        query = "SELECT * FROM Users ORDER BY username ASC LIMIT 4"
        cursor.execute(query)
        users=cursor.fetchall()
        u_list=[]
        for u in users:
            u_list.append(User(**u))
        return u_list

#---questions class----
class Question():
    def __init__(self,**kwargs):
        self.question_id=kwargs.get('question_id')
        self.title=kwargs.get('title') 
        self.body=kwargs.get('body')
        self.answer_id=kwargs.get('answer_id') 
        self.user_id=kwargs.get('user_id') 
        self.score=kwargs.get('score') 
        self.creation_date=kwargs.get('creation_date') 
        self.comment_count=kwargs.get('comment_count') 
        self.answer_count=kwargs.get('answer_count') 
        self.upvotes=kwargs.get('upvotes') 
        self.downvotes=kwargs.get('downvotes')
    
    @staticmethod
    def post_question(title,body,tags,user_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="INSERT INTO Questions (title,body,user_id) VALUES(%s,%s,%s)"
        cursor.execute(query,(title,body,user_id))
        my_db.commit()
        question_id=cursor.lastrowid
        query="SELECT * FROM Questions WHERE question_id=%s"
        cursor.execute(query,(question_id,))
        question=cursor.fetchone()
        for tag_name in tags:
            query="INSERT INTO Questiontags (tag_name,question_id) VALUES(%s,%s)"
            cursor.execute(query,(tag_name,question_id))
            my_db.commit()
            cursor.fetchall()
        my_db.close()
        return Question(**question)
        
    # for deleting question by question_id
    @staticmethod
    def delete_question_by_id(question_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="DELETE FROM Questions WHERE question_id=%s"
        cursor.execute(query,(question_id,))
        my_db.commit()
        my_db.close()
        return "successfully deleted" 
    
    #finding question by using its question_id
    @staticmethod
    def find_by_question_id(question_id):
        my_db=get_db_connection()
        query="SELECT * FROM Questions WHERE question_id=%s"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id,))
        row=cursor.fetchone()
        my_db.close()
        if row:
            return Question(**row)
        return None
    
    #sorted by creation date finding comments of question
    @staticmethod
    def get_comments_by_question_id(question_id):
        my_db=get_db_connection()
        query = "SELECT * FROM Question_comments WHERE question_id = %s ORDER BY creation_date ASC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id,))
        comments=cursor.fetchall()
        my_db.close()
        l_comments=[]
        for comment in comments:
            l_comments.append(Question_Comment(**comment))
        return l_comments
        
    #sorted by creation_date finding answers of question_id
    @staticmethod
    def find_answers_by_question_id(question_id):
        my_db=get_db_connection()
        query = "SELECT * FROM Answers WHERE question_id = %s ORDER BY creation_date ASC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id,))
        answers=cursor.fetchall()
        my_db.close()
        l_answers=[]
        for answer in answers:
            l_answers.append(Answer(**answer))
        return l_answers
    
    #finding accepted answer of that question using question object
    @staticmethod
    def get_accepted_answer_of_question_id(question):
        my_db=get_db_connection()
        answer_id=question.answer_id
        query = "SELECT * FROM Answers WHERE answer_id = %s "
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(answer_id,))
        answer=cursor.fetchone()
        my_db.close()
        if answer:
            return Answer(**answer)
        return None
    
    @staticmethod
    def find_question_by_user_id(user_id):
        my_db=get_db_connection()
        query = "SELECT * FROM Questions WHERE user_id = %s ORDER BY creation_date DESC"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(user_id,))
        questions=cursor.fetchall()
        my_db.close()
        q_list=[]
        for q in questions:
            q_list.append(Question(**q))
        return q_list

    @staticmethod
    def find_trending_ques():
        my_db=get_db_connection()
        query = "SELECT * FROM Questions ORDER BY creation_date DESC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query)
        questions=cursor.fetchall()
        my_db.close()
        q_list=[]
        for q in questions:
            q_list.append(Question(**q))
        return q_list
    
    # recommended on basis of now of upvotes
    @staticmethod
    def find_recommend_ques():
        my_db=get_db_connection()
        query = "SELECT * FROM Questions ORDER BY upvotes DESC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query)
        questions=cursor.fetchall()
        my_db.close()
        q_list=[]
        for q in questions:
            q_list.append(Question(**q))
        return q_list
   
# -----class for Answer object--------------
class Answer():
    def __init__(self,**kwargs):
        self.question_id=kwargs.get('question_id') 
        self.body=kwargs.get('body')  
        self.answer_id=kwargs.get('answer_id')  
        self.user_id=kwargs.get('user_id')  
        self.score=kwargs.get('score')  
        self.creation_date=kwargs.get('creation_date')  
        self.comment_count=kwargs.get('comment_count')  
        self.upvotes=kwargs.get('upvotes')  
        self.downvotes=kwargs.get('downvotes') 
    @staticmethod
    def post_answer(user_id,question_id,body):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="INSERT INTO Answers (body,user_id,question_id) VALUES(%s,%s,%s)"
        cursor.execute(query,(body,user_id,question_id))
        answer_id=cursor.lastrowid
        my_db.commit()
        query = "UPDATE Questions SET answer_count = answer_count + 1 WHERE question_id = %s"
        cursor.execute(query, (question_id,))
        my_db.commit()
        my_db.close()
        if answer_id is None:
            return "failed", 400
        else:
            return "Successfully posted",200
    
    @staticmethod
    def find_by_answer_id(answer_id):
        my_db=get_db_connection()
        query="SELECT * FROM Answers WHERE answer_id=%s"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(answer_id,))
        row=cursor.fetchone()
        my_db.close()
        if row:
            return Answer(**row)
        return None
    
    # sorted by creation_date finding comments of answer using using answer_id
    @staticmethod
    def get_comments_by_answer_id(answer_id):
        my_db=get_db_connection()
        query = "SELECT * FROM Answer_comments WHERE answer_id = %s ORDER BY creation_date ASC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(answer_id,))
        comments=cursor.fetchall()
        my_db.close()
        l_comments=[]
        for comment in comments:
            l_comments.append(Answer_Comment(**comment))
        return l_comments
    
    @staticmethod
    def delete_answer_by_id(answer_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="DELETE FROM Answers WHERE answer_id=%s"
        cursor.execute(query,(answer_id,))
        my_db.commit()
        my_db.close()
        return "successfully deleted"
    
    @staticmethod
    def find_answer_by_user_id(user_id):
        my_db=get_db_connection()
        query = "SELECT * FROM answers WHERE user_id = %s ORDER BY creation_date DESC LIMIT 10"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(user_id,))
        answers=cursor.fetchall()
        my_db.close()
        a_list=[]
        for a in answers:
            a_list.append(Answer(**a))
        return a_list
    
    @staticmethod
    def find_ans_by_ques_id(question_id):
        my_db=get_db_connection()
        query = "SELECT * FROM Answers WHERE question_id = %s ORDER BY creation_date DESC"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id,))
        answers=cursor.fetchall()
        my_db.close()
        a_list=[]
        for a in answers:
            a_list.append(Answer(**a))
        return a_list
# ----comments class-----------------

class Question_Comment():
    def __init__(self,**kwargs):
        # self.question_comment_id=kwargs.get('question_comment_id')
        self.body=kwargs.get('body')
        # self.user_id=kwargs.get('user_id')
        self.creation_date=kwargs.get('creation_date')
        # self.qustion_id=kwargs.get('question_id')

    @staticmethod
    def post_qcomment(question_id,user_id,body):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="INSERT INTO Question_comments (body,user_id,question_id) VALUES(%s,%s,%s)"
        cursor.execute(query,(body,user_id,question_id))
        qcomment=cursor.fetchone()
        my_db.commit()
        query = "UPDATE Questions SET comment_count = comment_count + 1 WHERE question_id = %s"
        cursor.execute(query, (question_id,))
        my_db.commit()
        my_db.close()
        if qcomment is None:
            return "failed", 400
        else:
            return "Successfully posted",200 
        
    # @staticmethod
    # def find_qcomment_by_id(question_comment_id):
    #     my_db=get_db_connection()
    #     cursor=my_db.cursor(dictionary=True)
    #     query="SELECT * FROM Question_comments WHERE question_comment_id=%s "
    #     cursor.execute(query,(question_comment_id,))
    #     row =cursor.fetchone()
    #     if row is None:
    #         return Question_Comment(**row)
    #     return None
    
    @staticmethod
    def find_qcomment_by_id(question_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT body FROM Question_comments WHERE question_id=%s ORDER BY CREATION_DATE DESC"
        cursor.execute(query,(question_id,))
        row =cursor.fetchall()
        return row
  
class Answer_Comment():

    def __init__(self,**kwargs):
        # self.answer_comment_id=kwargs.get('answer_comment_id')
        self.body=kwargs.get('body')
        # self.user_id=kwargs.get('user_id')
        self.creation_date=kwargs.get('creation_date')
        # self.answer_id=kwargs.get('answer_id')

    @staticmethod
    def post_acomment(answer_id,user_id,body):
            my_db=get_db_connection()
            cursor=my_db.cursor(dictionary=True)
            query="INSERT INTO Answer_comments (body,user_id,answer_id) VALUES(%s,%s,%s)"
            cursor.execute(query,(body,user_id,answer_id))
            acomment=cursor.fetchone()
            my_db.commit()
            query="UPDATE Answers  SET comment_count=comment_count+1 WHERE answer_id=%s"
            cursor.execute(query,(answer_id,))
            my_db.commit() 
            my_db.close()
            if acomment is None:
                return "failed", 400
            else:
                return "Successfully posted",200

    @staticmethod
    def find_acomment_by_id(answer_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT body FROM Answer_comments WHERE answer_id =%s ORDER BY creation_date DESC"
        cursor.execute(query,(answer_id,))
        row =cursor.fetchall()
        return row
        
class Tag():
    def __init__(self,**kwargs):
        self.tag_id=kwargs.get('tag_id')
        self.tag_name=kwargs.get('tag_name')
        self.about=kwargs.get('about')
        self.creation_date=kwargs.get('creation_date')

    @staticmethod
    def find_all_tags():
        my_db=get_db_connection()
        query="SELECT tag_name FROM Tags ORDER BY tag_name ASC;"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query)
        row=cursor.fetchall()
        my_db.close() 
        # tag_list=[]
        # for tag in row:
        #     tag_list.append(Tag(**tag))
        # return tag_list
        return row
    
    @staticmethod
    def find_tags_by_question_id(question_id):
        my_db=get_db_connection()
        query="SELECT tag_name FROM Questiontags WHERE question_id= %s ;"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query,(question_id,))
        tag_names=cursor.fetchall()
        # all_tags=[]
        # for tag in tag_names:
        #     all_tags.append(Tag(**tag))
        # return all_tags
        return tag_names
    
    @staticmethod
    def find_by_keyword(keyword):
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzlhMzI4NjQtNjdiZS00NGE4LThhNTYtNzdmNGFkY2I5OWE1IiwidHlwZSI6ImFwaV90b2tlbiJ9.xWWB4F4usgqj5_HQ-kPG34qKsFuaWheeOBWCCSCELMk"}
        url ="https://api.edenai.run/v2/text/keyword_extraction"
        payload={"providers": "amazon", "language": "en", "text": keyword}
        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        print(result['amazon']['items']) 
        keyword_list = result['amazon']['items']
        keyword_string = " ".join(keyword_list)
        my_db=get_db_connection()
        query = "SELECT * FROM Questions WHERE MATCH(title,body) AGAINST (%s IN NATURAL LANGUAGE MODE)"
        cursor=my_db.cursor(dictionary=True)
        cursor.execute(query, (keyword_string,))
        questions=cursor.fetchall()
        my_db.close()
        q_list=[]
        for q in questions:
            q_list.append(Question(**q))
        return q_list

class QVote:
    def __init__(self,**kwargs):
        self.vote_type=kwargs.get('vote_type')
        self.question_id=kwargs.get('question_id')
        self.user_id=kwargs.get('user_id')

    @staticmethod
    def Qfindvote(user_id,question_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT * FROM Question_votes WHERE user_id=%s AND question_id=%s"
        cursor.execute(query,(user_id,question_id))
        vote=cursor.fetchone()
        my_db.close()
        if(vote is None):
            return ("neutral")
        else:
            return vote['vote_type']

    @staticmethod
    def Qupdatevote(user_id,question_id,voting):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT vote_type FROM Question_votes WHERE user_id=%s AND question_id=%s"
        cursor.execute(query,(user_id,question_id))
        vote=cursor.fetchone()
        # my_db.close()
        if(vote is None):
            if(voting=='up'):
                query="INSERT INTO Question_votes (user_id,question_id,vote_type) values(%s,%s,%s)"
                cursor.execute(query,(user_id,question_id,'upvote'))
                my_db.commit()
                query = "UPDATE Questions SET upvotes = upvotes + 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'upvote'
            else:
                query="INSERT INTO Question_votes (user_id,question_id,vote_type) values(%s,%s,%s)"
                cursor.execute(query,(user_id,question_id,'downvote'))
                my_db.commit()
                query = "UPDATE Questions SET downvotes = downvotes + 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'downvote'
        elif (vote['vote_type']=='neutral'):
            if(voting=='up'):
                query = "UPDATE Question_votes SET vote_type = %s WHERE user_id = %s AND question_id = %s"
                cursor.execute(query, ('upvote', user_id, question_id))
                my_db.commit()
                query = "UPDATE Questions SET upvotes = upvotes + 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'upvote'
            else:
                query = "UPDATE Question_votes SET vote_type = %s WHERE user_id = %s AND question_id = %s"
                cursor.execute(query, ('downvote', user_id, question_id))
                my_db.commit()
                query = "UPDATE Questions SET downvotes = downvotes + 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'downvote'

        elif (vote['vote_type']=='upvote'):
            if(voting=='up'):
                query = "UPDATE Question_votes SET vote_type = %s WHERE user_id = %s AND question_id = %s"
                cursor.execute(query, ('neutral', user_id, question_id))
                my_db.commit()
                query = "UPDATE Questions SET upvotes = upvotes - 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'neutral'
            else:
                query = "UPDATE Question_votes SET vote_type = %s WHERE user_id = %s AND question_id = %s"
                cursor.execute(query, ('downvote', user_id, question_id))
                my_db.commit()
                query = "UPDATE Questions SET upvotes = upvotes - 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                query = "UPDATE Questions SET downvotes = downvotes + 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'downvote'
        else:
            if(voting=='down'):
                query = "UPDATE Question_votes SET vote_type = %s WHERE user_id = %s AND question_id = %s"
                cursor.execute(query, ('neutral', user_id, question_id))
                my_db.commit()
                query = "UPDATE Questions SET downvotes = downvotes - 1  WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'neutral'
            else:
                query = "UPDATE Question_votes SET vote_type = %s WHERE user_id = %s AND question_id = %s"
                cursor.execute(query, ('upvote', user_id, question_id))
                my_db.commit()
                query = "UPDATE Questions SET upvotes = upvotes + 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                query = "UPDATE Questions SET downvotes = downvotes - 1 WHERE question_id = %s"
                cursor.execute(query, (question_id,))
                my_db.commit()
                my_db.close()
                return 'upvote'

class AVote:
    def __init__(self,**kwargs):
        self.vote_type=kwargs.get('vote_type')
        self.answer_id=kwargs.get('answer_id')
        self.user_id=kwargs.get('user_id')

    @staticmethod
    def Afindvote(user_id,answer_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT * FROM Answer_votes WHERE user_id=%s AND answer_id=%s"
        cursor.execute(query,(user_id,answer_id))
        vote=cursor.fetchone()
        my_db.close()
        if(vote['vote_type'] is None):
            return ("neutral")
        else:
            return vote['vote_type']
        

    @staticmethod
    def Aupdatevote(user_id,answer_id,voting):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT vote_type FROM Answer_votes WHERE user_id=%s AND answer_id=%s"
        cursor.execute(query,(user_id,answer_id))
        vote=cursor.fetchone()
        # my_db.close()
        if(vote is None):
            if(voting=='up'):
                query="INSERT INTO Answer_votes (user_id,answer_id,vote_type) values(%s,%s,%s)"
                cursor.execute(query,(user_id,answer_id,'upvote'))
                my_db.commit()
                query = "UPDATE Answers SET upvotes = upvotes + 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'upvote'
            else:
                query="INSERT INTO Answer_votes (user_id,answer_id,vote_type) values(%s,%s,%s)"
                cursor.execute(query,(user_id,answer_id,'downvote'))
                my_db.commit()
                query = "UPDATE Answers SET downvotes = downvotes + 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'downvote'
        elif (vote['vote_type']=='neutral'):
            if(voting=='up'):
                query = "UPDATE Answer_votes SET vote_type = %s WHERE user_id = %s AND answer_id = %s"
                cursor.execute(query, ('upvote', user_id, answer_id))
                my_db.commit()
                query = "UPDATE Answers SET upvotes = upvotes + 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'upvote'
            else:
                query = "UPDATE Answer_votes SET vote_type = %s WHERE user_id = %s AND answer_id = %s"
                cursor.execute(query, ('downvote', user_id, answer_id))
                my_db.commit()
                query = "UPDATE Answers SET downvotes = downvotes + 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'downvote'

        elif (vote['vote_type']=='upvote'):
            if(voting=='up'):
                query = "UPDATE Answer_votes SET vote_type = %s WHERE user_id = %s AND answer_id = %s"
                cursor.execute(query, ('neutral', user_id, answer_id))
                my_db.commit()
                query = "UPDATE Answers SET upvotes = upvotes - 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'neutral'
            else:
                query = "UPDATE Answer_votes SET vote_type = %s WHERE user_id = %s AND answer_id = %s"
                cursor.execute(query, ('downvote', user_id, answer_id))
                my_db.commit()
                query = "UPDATE Answers SET upvotes = upvotes - 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                query = "UPDATE Answers SET downvotes = downvotes + 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'downvote'
        else:
            if(voting=='down'):
                query = "UPDATE Answer_votes SET vote_type = %s WHERE user_id = %s AND answer_id = %s"
                cursor.execute(query, ('neutral', user_id, answer_id))
                my_db.commit()
                query = "UPDATE Answers SET downvotes = downvotes - 1  WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'neutral'
            else:
                query = "UPDATE Answer_votes SET vote_type = %s WHERE user_id = %s AND answer_id = %s"
                cursor.execute(query, ('upvote', user_id, answer_id))
                my_db.commit()
                query = "UPDATE Answers SET upvotes = upvotes + 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                query = "UPDATE Answers SET downvotes = downvotes - 1 WHERE answer_id = %s"
                cursor.execute(query, (answer_id,))
                my_db.commit()
                my_db.close()
                return 'upvote'
        
class QBookmark:
    def __init__(self,**kwargs):
        self.creation_date=kwargs.get('creation_date')
        self.question_id=kwargs.get('question_id')
        self.user_id=kwargs.get('user_id')


    @staticmethod
    def Qfindbookmark(user_id,question_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT * FROM Question_bookmarks WHERE user_id=%s AND question_id=%s"
        cursor.execute(query,(user_id,question_id))
        vote=cursor.fetchone()
        if(vote is None):
            return ('no')
        else:
            return ('yes')
        
    @staticmethod
    def Qupdatebookmark(user_id,question_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT * FROM Question_bookmarks WHERE user_id=%s AND question_id=%s"
        cursor.execute(query,(user_id,question_id))
        bookmark=cursor.fetchone()
        print("bookmark",bookmark)
        if bookmark is None:
            print("nobe")
            query="INSERT INTO Question_bookmarks (user_id,question_id) values(%s,%s)"
            cursor.execute(query,(user_id,question_id))
            # cursor.fetchone()
            my_db.commit()
            # query="SELECT * FROM Question_bookmarks WHERE user_id=%s AND question_id=%s"
            # cursor.execute(query,(user_id,question_id))
            # bkq=cursor.fetchone()
            my_db.close()
            # print("bkq",bkq)
            return ({"bookmark":"yes"})
        else:
            print('what is the issue')
            query="DELETE FROM Question_bookmarks WHERE user_id=%s AND question_id=%s"
            cursor.execute(query,(user_id,question_id))
            my_db.commit()
            my_db.close()
            return ({"bookmark":"no"})
    @staticmethod
    def Qfindmarked(user_id):
        print('Raja kumar')
        print(user_id)
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query = "SELECT question_id FROM Question_bookmarks WHERE user_id = %s ORDER BY creation_date DESC LIMIT 10"
        cursor.execute(query,(user_id,))
        l_qid=cursor.fetchall()
        print("checing for bookmarks")
        print(l_qid)
        q_list=[]
        for id in l_qid:
            question=Question.find_by_question_id(id['question_id']) # fix the typo here
            q_list.append(question)
        return q_list



        # bookmark=cursor.fetchone()

class ABookmark:
    def __init__(self,**kwargs):
        self.creation_time=kwargs.get('vote_type')
        self.answer_id=kwargs.get('answer_id')
        self.user_id=kwargs.get('user_id')

    @staticmethod
    def Afindbookmark(user_id,answer_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT * FROM Answer_bookmarks WHERE user_id=%s AND answer_id=%s"
        cursor.execute(query,(user_id,answer_id))
        vote=cursor.fetchone()
        my_db.close()
        if(vote is None):
            return ("no")
        else:
            return ('yes')
    
    @staticmethod
    def Aupdatebookmark(user_id,answer_id):
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query="SELECT * FROM Answer_bookmarks WHERE user_id=%s AND answer_id=%s"
        cursor.execute(query,(user_id,answer_id))
        bookmark=cursor.fetchone()
        print("bookmark",bookmark)
        if bookmark is None:
            print("nobe")
            query="INSERT INTO Answer_bookmarks (user_id,answer_id) values(%s,%s)"
            cursor.execute(query,(user_id,answer_id))
            # cursor.fetchone()
            my_db.commit()
            # query="SELECT * FROM Answer_bookmarks WHERE user_id=%s AND answer_id=%s"
            # cursor.execute(query,(user_id,answer_id))
            # bkq=cursor.fetchone()
            my_db.close()
            return ({"bookmark":"yes"})
        else:
            print('what is the issue')
            query="DELETE FROM Answer_bookmarks WHERE user_id=%s AND answer_id=%s"
            cursor.execute(query,(user_id,answer_id))
            my_db.commit()
            my_db.close()
            return ({"bookmark":"no"})
        
    @staticmethod
    def Afindmarked(user_id):
        print('Raja kumar')
        print(user_id)
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query = "SELECT answer_id FROM Answer_bookmarks WHERE user_id = %s ORDER BY creation_date DESC LIMIT 10"
        cursor.execute(query,(user_id,))
        l_qid=cursor.fetchall()
        print("checing for aanswes bookmarks")
        print(l_qid)
        q_list=[]
        for id in l_qid:
            print(id)
            answer=Answer.find_by_answer_id(id['answer_id']) # fix the typo here
            q_list.append(answer)
        return q_list

    


    

#------------------update into database---------------------
# required functions 



    
# -------------logged user--------------------------------

@login_required
@newapp.route('/users/user_home',methods=["GET",])
def user_home():
    # if(current_user.is_authenticated):
    # cur = my_db.cursor(dictionary=True)
    # cur.execute('SELECT * FROM Questions')
    # questions = cur.fetchall()
    if request.method=="POST":
        keyword = request.form['keyword']
        return redirect(url_for('search_login' ,keyword=keyword))

    return render_template('user_home.html',user=current_user)

@login_required
@newapp.route('/logout',methods=['GET',])
def logout():
    logout_user()
    return redirect(url_for('userlogin'))



@login_required
@newapp.route('/users/all_users',methods=["GET",])
def all_users():
    u_list=User.find_allusers()
    return render_template('all_users.html',user=current_user,u_list=u_list)

@login_required
@newapp.route("/users/badges",methods=["GET",])
def badges():
    return render_template('badges.html',user=current_user)

@login_required
@newapp.route('/users/bookmarks',methods=['GET',])
def bookmarks():
    q_list=QBookmark.Qfindmarked(user_id=current_user.user_id)
    a_list=ABookmark.Afindmarked(user_id=current_user.user_id)
    return render_template('bookmarks.html',user=current_user,q_list=q_list,a_list=a_list)

@login_required
@newapp.route("/users/complete_your_profile",methods=["GET",'POST'])
def complete_your_profile():
    if request.method=='POST':
        profile_image_url = request.form.get('profile_image_url', '')
        about=request.form['about']
        tags=request.form['tags']
        user=User.update_profile(user=current_user,profile_image_url  = profile_image_url,tags=tags,about=about)
        return redirect(url_for('user_home',user=user))
    return render_template("complete_your_profile.html",user=current_user)

@login_required
@newapp.route('/users/dashboard', methods=['GET',])
def dashboard():
    return render_template("dashboard.html",user=current_user)
# follower and following functions
@login_required
@newapp.route("/users/followers", methods=["GET",])
def followers():
    return render_template("followers.html",user=current_user,follower_list=User.find_followers(current_user.user_id))

@login_required
@newapp.route("/users/following", methods=["GET",])
def following():
    return render_template("following.html",user=current_user,following_list=User.find_followings(current_user.user_id))


@login_required
@newapp.route('/users/help_with_login',methods=['GET',])
def help_with_login():
    return render_template('help_with_login.html',user=current_user)

#  question related posting
@login_required
@newapp.route('/users/questions',methods=['GET','POST'])
def post_question():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        selected_tags = request.form.getlist('tags[]')
        question_id=Question.post_question(title=title, body=body,tags=selected_tags, user_id=current_user.user_id)
        if question_id:
            return redirect(url_for('posted_questions'))
    return render_template('post_question.html',user=current_user,tag_list=Tag.find_all_tags())


@login_required
@newapp.route('/users/questions/<int:question_id>',methods=["GET",])
def find_question(question_id):
    question=Question.find_by_question_id(question_id=question_id)
    return render_template('present_question.html',user=current_user,question=question,l_tags=Tag.find_tags_by_question_id(question_id),l_ans=Answer.find_ans_by_ques_id(question_id))


@login_required
@newapp.route('/users/questions/<int:question_id>/answers',methods=['GET','POST'])
def post_answer(question_id):
    if request.method=="POST":
        body=request.form['body']
        answer=Answer.post_answer(user_id=current_user.user_id,body=body,question_id=question_id)
        return redirect(url_for('find_question',question_id=question_id))
    return render_template('post_answer.html',question_id=question_id,user=current_user)


@login_required
@newapp.route('/users/questions/<int:question_id>/answers/<int:answer_id>/comments',methods=['GET','POST'])
def post_answer_comment(question_id,answer_id):
    if request.method=="POST":
        body=request.form['body']
        id=current_user.user_id
        print(body)
        Answer_Comment.post_acomment(user_id=id,body=body,answer_id=answer_id)
        return redirect(url_for('find_question',question_id=question_id)) 
    return render_template('post_acomment.html',answer_id=answer_id,question_id=question_id)
    
@login_required
@newapp.route('/users/questions/<int:question_id>/comments',methods=['GET','POST'])
def post_question_comment(question_id):
    if request.method=="POST":
        body=request.form['body']
        if not body:
            flash('Content is required.')
        else:
            id=current_user.user_id
            Question_Comment.post_qcomment(user_id=id,body=body,question_id=question_id)
            return redirect(url_for('find_question',question_id=question_id))
    return render_template('post_qcomment.html',question_id=question_id) 


            
@login_required
@newapp.route("/users/posted_questions",methods=["GET","POST","DELETE"])
def posted_questions():
    id=current_user.user_id
    q_list=Question.find_question_by_user_id(user_id=id)
    # print(q_list[0].title)
    return render_template('posted_questions.html',q_list=Question.find_question_by_user_id(user_id=id),user=current_user)


@login_required
@newapp.route('/users/recommendations',methods=['GET',])
def recommendations():
    q_list=Question.find_recommend_ques()
    return render_template('recommendations.html',user=current_user,q_list=q_list)

@login_required
@newapp.route('/users/tags',methods=['GET',])
def tags_login():
    return render_template('tag_login.html',user=current_user)

@login_required
@newapp.route('/users/trending',methods=['GET',])
def trending():
    q_list=Question.find_trending_ques()
    return render_template('trending.html',user=current_user,q_list=q_list)

@login_required
@newapp.route('/users/search',methods=['GET',])
def search_login(keyword):
    q_list = Question.find_by_keyword(keyword) 
    return render_template('search_with_login.html',user=current_user,q_list=q_list)

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
            # hashfun.update(passcode.encode())
            # hashed_password=hashfun.hexdigest()
            # hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()
            if (user is None):
                flash("Incorrect passcode ")
                return render_template('login.html')
            # elif (bcrypt.checkpw(passcode.encode('utf-8'), user.passcode)):
            elif (passcode!=user.passcode):
                flash("Incorrect password ")
                return render_template('login.html')
            else:
                flash("Login successfully")
                login_user(user,remember=remember) 
                return redirect(url_for('user_home'))
    return render_template("login.html")

@newapp.route('/help',methods=["GET",])
def help():
    if(current_user.is_authenticated):
        return render_template("help_with_login.html")
    return render_template("help.html")
            
@newapp.route('/tags',methods=['GET',])
def tags():
    return render_template('tags.html')

def send_email(newapp, msg):
    with newapp.app_context():
        mail.send(msg)
        # return 1
       

@newapp.route("/forgot_password",methods=["GET","POST"])
def forgot_password():  
    if request.method=="POST":
        username = request.form['username']
        email_id = request.form['email_id']
        user = User.find_by_email_id(email_id)
        if (user!=None and User.find_by_username(username)==user):
            token = user.get_reset_token(username)
            msg=Message()
            msg.subject = "Password Recovery Mail"
            msg.recipients = [email_id]
            # msg.sender = newapp.config['MAIL_DEFAULT_SENDER']
            # msg.body = "Click here to reset your password:\n"
            url = request.host_url + url_for('reset_password',username=username,token=token)
            # newapp.logger.warning(url)
            msg.html = render_template('reset_password_mail.html',url=url)
            Thread(target=send_email, args=(newapp,msg)).start()
            # mail.send(msg)
            flash('email successfully sent!')
        else:
            flash('user does not exist!')
        render_template('password_reset_1.html')
    return render_template('password_reset_1.html')

@newapp.route("/reset_password/<string:username>/<string:token>",methods=["GET",'POST'])
def reset_password(username, token):
    if request.method=="POST":
        password1 = request.form['password1']
        password2 = request.form['password2']
        if (password1!=password2):
            flash("Passwords do not match!")
        else:
            reset = User.set_password(username,password1)
            if reset==1: flash("Password reset successfully!")
            else: flash("Something went wrong :(")
    return render_template('password_reset_2.html', username=username, token=token)


@newapp.route('/search',methods=["GET"])
def search_without_login():
    return render_template('search_without_login.html')

@newapp.route('/',methods=["GET","POST"])
def homepage():
    if request.method=="POST":
        searchKeyword = request.form['keyword']
        return redirect(url_for('search_without_login' ,keyword=searchKeyword))

    return render_template('index.html')


# handling upvote downvote bookmark
@login_required
@newapp.route('/checking',methods=['GET','POST'])
def handlechecking():
    return render_template('check.html')
# Handling voting system using javascript

@login_required
@newapp.route('/Qloadvote', methods=['GET', 'POST'])
def Qloadvote():
    if request.method == 'GET':
        # Handle GET request
        data = request.args
        question_id = data.get('question_id')
        # user_id = data.get('user_id')
        user_id=current_user.user_id
        print("raja kuamr ")
        print(question_id,user_id)
        votetype=QVote.Qfindvote(user_id=user_id, question_id=question_id)
        bookmark=QBookmark.Qfindbookmark(user_id=user_id,question_id=question_id)
        print()
        return jsonify({"votetype":votetype,"bookmark":bookmark,"q":question_id,"u":user_id})
    
    # elif request.method == 'POST':
    #     # Handle POST request
    #     data = request.get_json()
    #     question_id = data.get('question_id')
    #     user_id = current_user.user_id
    #     QVote.findvote(user_id=user_id, question_id=question_id)
    #     return jsonify({"votetype": "neutral"})
@login_required
@newapp.route('/updatevote', methods=['GET', 'POST'])
def updatevote():
    if request.method == 'POST':
        # Handle GET request
        data = request.get_json()
        post_id = data.get('post_id')
        user_id = current_user.user_id
        vote_type=data.get('vote_type')
        post_type=data.get('post_type')
        print("raja kumar in updatevote",post_id,vote_type,post_type)
        if(post_type=='question'):
            print("i am hwer in question")
            vote=QVote.Qupdatevote(user_id=user_id,question_id=post_id,voting=vote_type)
            ObQ=Question.find_by_question_id(question_id=post_id)
            score=(ObQ.upvotes-ObQ.downvotes)
            upvotes=ObQ.upvotes
            downvotes=ObQ.downvotes
            print({"vote_type":vote,"upvotes":upvotes,"downvotes":downvotes,"score":score})
            print('raj a hi')
        else:
            vote=AVote.Aupdatevote(user_id=user_id,answer_id=post_id,voting=vote_type)
            ObQ=Answer.find_by_answer_id(answer_id=post_id)
            score=(ObQ.upvotes-ObQ.downvotes)
            upvotes=ObQ.upvotes
            downvotes=ObQ.downvotes
            print({"vote_type":vote,"upvotes":upvotes,"downvotes":downvotes,"score":score})
        return jsonify({"vote_type":vote,"upvotes":upvotes,"downvotes":downvotes,"score":score})

@login_required
@newapp.route('/updatebookmark',methods=['GET','POST'])
def udpatebookmark():
    if request.method=='POST':
        data=request.get_json()
        post_id=data.get('post_id')
        post_type=data.get('post_type')
        user_id=current_user.user_id
        print("my name is raha kumart")
        print(user_id,post_id,post_type)
        if(post_type=='answer'):
            B=ABookmark.Aupdatebookmark(user_id=user_id,answer_id=post_id)
        else:
            B=QBookmark.Qupdatebookmark(user_id=user_id,question_id=post_id)
        print(B)
        return jsonify({"bookmark":B['bookmark']})

@login_required
@newapp.route('/getcomments',methods=['GET','POST'])
def getcomments():
    if request.method=='POST':
        data=request.get_json()
        post_id=data.get('post_id')
        post_type=data.get('post_type')
        print("i am here what are you doing")
        print(post_id,post_type)
        if(post_type=='answer'):
            ac_list=Answer_Comment.find_acomment_by_id(answer_id=post_id)
            print(ac_list)
            print('answers')
            return jsonify(ac_list)
        else: 
            qc_list=Question_Comment.find_qcomment_by_id(question_id=post_id)
            print(qc_list)
            print('questions')
            return jsonify(qc_list) 
    else:
        return jsonify({'body':'my name is raja'})

@login_required
@newapp.route('/updatefollow',methods=['GET','POST'])
def udpatefollow():
    if request.method=='POST':
        data=request.get_json()
        id=data.get('user_id')
        user_id=current_user.user_id
        # db interaciton
        my_db=get_db_connection()
        cursor=my_db.cursor(dictionary=True)
        query='SELECT * FROM Followertags WHERE follower_id = %s AND following_id=%s ' 
        cursor.execute(query,(user_id,id))
        row=cursor.fetchone()
        if(row is None):
            query="INSERT INTO Followertags (follower_id,following_id) VALUES(%s,%s)"
            cursor.execute(query,(user_id,id))
            my_db.commit()
            query='UPDATE Users SET nfollowing=nfollowing+1 WHERE user_id=%s'
            cursor.execute(query,(user_id,))
            my_db.commit()
            query='UPDATE Users SET nfollowers=nfollowers+1 WHERE user_id=%s'
            cursor.execute(query,(id,))
            my_db.commit()
            my_db.close()
            return jsonify({'fstatus':'follow'})
        else:
            query="DELETE FROM Followertags WHERE follower_id=%s AND following_id=%s"
            cursor.execute(query,(user_id,id))
            my_db.commit()
            query='UPDATE Users SET nfollowing=nfollowing-1 WHERE user_id=%s'
            cursor.execute(query,(user_id,))
            my_db.commit()
            query='UPDATE Users SET nfollowers=nfollowers-1 WHERE user_id=%s'
            cursor.execute(query,(id,))
            my_db.commit()
            my_db.close()
            return jsonify({'fstatus':'unfollow'})



































# helper functions




if __name__=="__main__":
    newapp.run(debug=True)


