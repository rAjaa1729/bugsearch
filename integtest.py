import unittest
from unittest.mock import patch, Mock
from newapp import newapp, get_db_connection, User, load_user


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = newapp.test_client()
        self.db = get_db_connection()

    def test_register_login_logout(self):
        with self.client:
            response = self.client.post('/signup', data=dict(
                email_id='test@example.com',
                passcode='password',
                username='test'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Account created successfully. Please login.' in response.data)

            response = self.client.post('/login', data=dict(
                email_id='test@example.com',
                passcode='password'
            ), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Logged in successfully.' in response.data)

            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Logged out successfully.' in response.data)

    def test_user_home(self):
        with self.client:
            response = self.client.get('/users/user_home', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'User Home' in response.data)

    # def test_all_users(self):
    #     with self.client:
    #         response = self.client.get('/users/all_users', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(b'All Users' in response.data)

    # def test_badges(self):
    #     with self.client:
    #         response = self.client.get('/users/badges', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(b'Badges' in response.data)

    # def test_bookmarks(self):
    #     with self.client:
    #         response = self.client.get('/users/bookmarks', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(b'Bookmarks' in response.data)

    def test_complete_your_profile(self):
        with self.client:
            response = self.client.post('/users/complete_your_profile', data=dict(
                about='Test User',
                profile_image_url='https://example.com/image.png',
                tags='test'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Profile updated successfully.' in response.data)

if __name__ == '__main__':
    unittest.main()

