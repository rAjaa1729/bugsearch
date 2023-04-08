import unittest
from unittest.mock import patch,Mock

# from newapp import Question
from newapp import User
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
        self.user_id = 21
        self.email_id = "aastha@gmail.com"
        self.passcode = "aastha"
        self.username = "Aastha"
        self.creation_date= "2023-04-08 12:00:00"
        self.profile_image_url= "https://www.figma.com/file/7KFxGA0vLIeYhf85DahLUR/image/bd3feba159b8d237ee735e750cdc1002ebf458e1"
        self.reputation_points= 21
        self.about="Hi"
        self.badge="Gold"
        self.nfollowing=21
        self.nfollowers=21
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
        self.assertEqual(q.nfollowers ,self.nfollowers)

    def test_find_by_email_id_success(self):
        result=User.find_by_email_id(email_id="aastha@gmail.com")
        self.assertIsInstance(result, User)
        self.assertEqual(result.email_id, "aastha@example.com")
        self.assertEqual(result.username, "Aastha")

    def test_find_by_username_success(self):
        result=User.find_by_username(username="Aastha")
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "Aastha")
        # self.assertEqual(result.username, "Test User")

    def test_get(self):
        result=User.get(user_id=21)
        self.assertIsInstance(result,User)
        self.assertEqual(result.get,21)
        self.assertEqual(result.username,"Aastha")

    def test_create(self):
        result=User.create(email_id="aastha@gmail.com",passcode="aastha",username="Aastha")
        self.assertIsInstance(result,User)
        self.assertEqual(result.email_id,"aastha@gmail.com")
        self.assertEqual(result.username,"Aastha")
        self.assertEqual(result.passcode,"aastha")
        cursor = self.my_db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (result.user_id,))
        row = cursor.fetchone()
        cursor.close()
        expected_user = User(*row)
        self.assertEqual(result, expected_user)

    # def test_update_profile(self):
    #     # result=User.update_profile(user,about,profile_image_url,tags)
    #     # self.assertIsInstance(result,User)
    #     # self.assertEqual(result.update_profile,21)
    #     # self.assertEqual(result.username,)
    #     updated_user = User.update_profile(user, self.about, self.profile_image_url, self.tags)

    #     # Verify that the User object was updated correctly
    #     self.assertEqual(updated_user.user_id, self.user.user_id)
    #     self.assertEqual(updated_user.username, self.username)
    #     self.assertEqual(updated_user.email, self.user.email)
    #     self.assertEqual(updated_user.about, self.about)
    #     self.assertEqual(updated_user.profile_image_url, self.profile_image_url)
    #     self.assertEqual(updated_user.tags, self.tags)  # Assuming that tags are added correctly in the method

    #     # Verify that the changes were made in the database
    #     cursor = self.my_db.cursor(dictionary=True)
    #     cursor.execute("SELECT * FROM Users WHERE user_id=%s", (1,))
    #     row = cursor.fetchone()
    #     cursor.close()
    #     self.assertEqual(row['user_id'], self.user.user_id)
    #     self.assertEqual(row['name'], self.user.name)
    #     self.assertEqual(row['email'], self.user.email)
    #     self.assertEqual(row['about'], self.about)
    #     self.assertEqual(row['profile_image_url'], self.profile_image_url)





        # return super().setUp()
# class TestQuestion(unittest.TestCase):
#     def setUp(self):
#         self.question_id = 123
#         self.title = "Example question"
#         self.body = "This is an example question"
#         self.answer_id = 456
#         self.user_id = 789
#         self.score = 21
#         self.creation_date = "2023-04-08 12:00:00"
#         self.upvotes = 21
#         self.downvotes = 21
#         self.answer_count = 21
#         self.comment_count = 21
#         self.tags = [{'tag_id': 1}, {'tag_id': 2}]


    # def test_init(self):
    #     q = Question(question_id=self.question_id, title=self.title, body=self.body, answer_id=self.answer_id,
    #                  user_id=self.user_id, score=self.score, creation_date=self.creation_date, upvotes=self.upvotes,
    #                  downvotes=self.downvotes, answer_count=self.answer_count, comment_count=self.comment_count)
    #     self.assertEqual(q.question_id, self.question_id)
    #     self.assertEqual(q.title, self.title)
    #     self.assertEqual(q.body, self.body)
    #     self.assertEqual(q.answer_id, self.answer_id)
    #     self.assertEqual(q.user_id, self.user_id)
    #     self.assertEqual(q.score, self.score)
    #     self.assertEqual(q.creation_date, self.creation_date)
    #     self.assertEqual(q.upvotes, self.upvotes)
    #     self.assertEqual(q.downvotes, self.downvotes)
    #     self.assertEqual(q.answer_count, self.answer_count)
    #     self.assertEqual(q.comment_count, self.comment_count)

    # def test_post_question_success(self):
    #     result=Question.post_question(title="Example question",body="This is an example question",tags=[{'tag_id': 1}, {'tag_id': 2}])
    #     self.assertEqual(result,"Successfully posted")
    # def test_find_by_question_id(self):
    #     result=Question.find_by_question_id(question_id=123)
    #     self.assertIsInstance(result, Question)
    #     self.assertEqual(result.question_id, 123)

    # mock the database cursor and execute method
        # cursor_mock = MagicMock()
        # cursor_mock.lastrowid = 123
        # cursor_mock.execute.return_value = cursor_mock

        # # mock the database connection and cursor
        # my_db_mock = MagicMock()
        # my_db_mock.cursor.return_value = cursor_mock

        # # create a mock current user
        # current_user_mock = MagicMock()
        # current_user_mock.user_id = 456

        # # call the post_question method using the class name
        # result = Question.post_question(self.title, self.body, self.tags)

        # # check that the database was called correctly
        # my_db_mock.cursor.assert_called_once_with(dictionary=True)
        # cursor_mock.execute.assert_called_once_with(
        #     "INSERT INTO QUESTIONS (title,body,user_id) VALUES(%s,%s,%s)",
        #     (self.title, self.body, current_user_mock.user_id))
        # cursor_mock.execute.assert_called_once_with(
        #     "INSERT INTO Questiontags (tag_id,question_id) VALUES(%s,%s)",
        #     (1, 123))
        # cursor_mock.execute.assert_called_once_with(
        #     "INSERT INTO Questiontags (tag_id,question_id) VALUES(%s,%s)",
        #     (2, 123))
        # cursor_mock.close.assert_called_once()
        # my_db_mock.commit.assert_called_once()

        # # check that the result is "Successfully posted"
        # self.assertEqual(result, "Successfully posted")


# class TestUpdateProfile(unittest.TestCase):

