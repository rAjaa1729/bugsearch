import unittest
from unittest.mock import patch,Mock

# from newapp import Question
from newapp import User
# from newapp import Answer
# from newapp import Comment
import mysql.connector
def get_db_connection():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password= "sql@Prism1920",
        database = "BugSearch"
    )
    return mydb
my_db=get_db_connection()


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user_id = 0
        self.email_id = "aastha@gmail.com"
        self.passcode = "aastha"
        self.username = "Aastha"
        self.creation_date= "2023-04-08 12:00:00"
        self.profile_image_url= "https://www.figma.com/file/7KFxGA0vLIeYhf85DahLUR/image/bd3feba159b8d237ee735e750cdc1002ebf458e1"
        self.reputation_points= 0
        self.about="Hi"
        self.badge="Gold"
        self.nfollowing=0
        self.nfollowers=0
        self.my_db=my_db
    def test_init(self):
        q = User(user_id=self.user_id,email_id=self.email_id,passcode=self.passcode,username=self.username,creation_date=self.creation_date,profile_image_url=self.profile_image_url,reputation_points=self.reputation_points,about=self.about,badge=self.badge,nfollowers=self.nfollowers,nfollowing=self.nfollowing)
        self.assertEqual(q.user_id, self.user_id)
        self.assertEqual(q.passcode, self.passcode)
        self.assertEqual(q.username, self.username)
        self.assertEqual(q.email_id, self.email_id)
        self.assertEqual(q.profile_image_url, self.profile_image_url)
        self.assertEqual(q.reputation_points, self.reputation_points)
        self.assertEqual(q.creation_date, self.creation_date)
        self.assertEqual(q.about, self.about)
        self.assertEqual(q.badge, self.badge)
        self.assertEqual(q.nfollowing, self.nfollowing)
        self.assertEqual(q.nfollowers, self.nfollowers)

    def test_find_by_email_id_success(self):
        result=User.find_by_email_id(email_id="aastha@gmail.com")
        self.assertIsInstance(result, User)
        self.assertEqual(result.email_id, "aastha@gmail.com")
        self.assertEqual(result.username, "Aastha")

    def test_find_by_username_success(self):
        result=User.find_by_username(username="Aastha")
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "Aastha")
        # self.assertEqual(result.username, "Test User")

    def test_get(self):
        result=User.get(user_id=0)
        self.assertIsInstance(result,User)
        self.assertEqual(result.user_id,0)
        self.assertEqual(result.username,"Aastha")

    def test_create(self):
        result=User.create(email_id="aastha@gmail.com",passcode="aastha",username="Aastha")
        self.assertIsInstance(result,User)
        self.assertEqual(result.email_id,"aastha@gmail.com")
        self.assertEqual(result.username,"Aastha")
        self.assertEqual(result.passcode,"aastha")
        cursor = self.my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (result.user_id,))
        row = cursor.fetchone()
        cursor.close()
        expected_user = User(**row)
        self.assertEqual(result, expected_user)

    def test_update_profile(self):
        result=User.update_profile(user=self,about=self.about,profile_image_url=self.profile_image_url,tags="javascript")
        self.assertIsInstance(result,User)
        # self.assertEqual(result.update_profile,0)
        self.assertEqual(result.about,"Hi")
        self.assertEqual(result.profile_image_url,"https://www.figma.com/file/7KFxGA0vLIeYhf85DahLUR/image/bd3feba159b8d237ee735e750cdc1002ebf458e1")

class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.question_id = 123
        self.title = "Example question"
        self.body = "This is an example question"
        self.answer_id = 456
        self.user_id = 789
        self.score = 0
        self.creation_date = "2023-04-08 12:00:00"
        self.upvotes = 0
        self.downvotes = 0
        self.answer_count = 0
        self.comment_count = 0
        self.tags = [{'tag_id': 1}, {'tag_id': 2}]
        self.my_db=my_db

    def test_init(self):
        q = Question(question_id=self.question_id, title=self.title, body=self.body, answer_id=self.answer_id,
                     user_id=self.user_id, score=self.score, creation_date=self.creation_date, upvotes=self.upvotes,
                     downvotes=self.downvotes, answer_count=self.answer_count, comment_count=self.comment_count)
        self.assertEqual(q.question_id, self.question_id)
        self.assertEqual(q.title, self.title)
        self.assertEqual(q.body, self.body)
        self.assertEqual(q.answer_id, self.answer_id)
        self.assertEqual(q.user_id, self.user_id)
        self.assertEqual(q.score, self.score)
        self.assertEqual(q.creation_date, self.creation_date)
        self.assertEqual(q.upvotes, self.upvotes)
        self.assertEqual(q.downvotes, self.downvotes)
        self.assertEqual(q.answer_count, self.answer_count)
        self.assertEqual(q.comment_count, self.comment_count)

    def test_post_question_success(self):
        result=Question.post_question(title="Example question",body="This is an example question",tags=[{'tag_id': 1}, {'tag_id': 2}])
        self.assertEqual(result,"Successfully posted")
    def test_find_by_question_id(self):
        result=Question.find_by_question_id(question_id=123)
        self.assertIsInstance(result, Question)
        self.assertEqual(result.question_id, 123)
    def test_get_comments_by_question_id(self):
        result=Question.get_comments_by_question_id(question_id=123)
        cursor = self.my_db.cursor()
        cursor.execute("SELECT * FROM Comments WHERE post_id = %s AND post_type = %s", (self,"question"))
        comments = cursor.fetchall()
        cursor.close()
        self.assertEqual(result, comments)

    def test_find_answers_by_question_id(self):
        result=Question.find_answers_by_question_id(question_id=123)
        cursor = self.my_db.cursor()
        cursor.execute("SELECT * FROM Answers WHERE post_id = %s AND post_type = %s", (self,"question"))
        answers = cursor.fetchall()
        cursor.close()
        self.assertEqual(result, answers)
    
    def test_get_accepted_answer_of_question_id(self):
        result=Question.get_accepted_answer_of_question_id(question=self)
        self.assertIsInstance(result, Answer)
        self.assertEqual(result.question_id, 123)



class TestAnswer(unittest.Testcase):
    def setUp(self):
        self.question_id=456
        self.body="This is body" 
        self.answer_id=2345
        self.user_id=21 
        self.score=0 
        self.creation_date="2023-04-08 12:00:00"
        self.comment_count=0
        self.upvotes=0 
        self.downvotes=0
        self.my_db=my_db
    def test_post_answer(self):
        result=Answer.post_answer(question_id=456,body="This is body")
        self.assertEqual(result,"Successfully posted")
    
    def test_find_by_answer_id(self):
        result=Answer.find_by_answer_id(answer_id=2345)
        self.assertIsInstance(result, Answer)
        self.assertEqual(result.answer_id, 2345)

    def test_get_comments_by_answer_id(self):
        result=Answer.get_comments_by_answer_id(answer_id=123)
        cursor = self.my_db.cursor()
        cursor.execute("SELECT * FROM Comments WHERE post_id = %s AND post_type = %s", (self,"answer"))
        comments = cursor.fetchall()
        cursor.close()
        self.assertEqual(result, comments)


class TestComment(unittest.TestCase):
    def setup(self):
        self.comment_id=123
        self.body="This is body"
        self.user_id=0
        self.creation_date="2023-04-08 12:00:00"
        self.post_id=0
        self.post_type="answer"
    
    def test_post_comment(self):
        result=Comment.post_comment(post_id=0,post_type="answer",body="This is body")
        self.assertEqual(result,"Successfully posted")


