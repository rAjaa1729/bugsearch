import unittest
from unittest.mock import MagicMock

from newapp import User,Question

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
    def test_init(self):
        q = User(self.user_id,self.email_id,self.passcode,self.username,self.creation_date,self.profile_image_url,self.reputation_points,self.about,self.badge,self.nfollowers,self.nfollowing)
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
        result=User.find_by_email_id("aastha@gmail.com")
        self.assertIsInstance(result, User)
        self.assertEqual(result.email_id, "test@example.com")
        self.assertEqual(result.username, "Aastha")
    def test_find_by_username_success(self):
        result=User.find_by_username("Aastha")
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "Aastha")
        # self.assertEqual(result.username, "Test User")