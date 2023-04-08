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

    def test_all_users(self):
        with self.client:
            response = self.client.get('/users/all_users', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'All Users' in response.data)
    
    def test_followers(self):
        with self.client:
            response = self.client.get('/users/followers', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'followers' in response.data)
    
    def test_following(self):
        with self.client:
            response = self.client.get('/users/following', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'following' in response.data)
    
    def test_dashboard(self):
        with self.client:
            response = self.client.get('/users/dashboard', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'userprofile' in response.data)
    
    def test_trendig(self):
        with self.client:
            response = self.client.get('/users/trending', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'trending' in response.data)

    def test_recommendations(self):
        with self.client:
            response = self.client.get('/users/recommendations', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'recommendations' in response.data)

    def test_badges(self):
        with self.client:
            response = self.client.get('/users/badges', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Badges' in response.data)

    def test_bookmarks(self):
        with self.client:
            response = self.client.get('/users/bookmarks', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Bookmarks' in response.data)

    def test_help_with_login(self):
        with self.client:
            response = self.client.get('/users/help_with_login', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'help_with_login' in response.data)
    
    def test_help(self):
        with self.client:
            response = self.client.get('/help', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'help' in response.data)
    
    def test_homepage(self):
        with self.client:
            response = self.client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'homepage' in response.data)
    
    def test_search(self):
        with self.client:
            response = self.client.get('/search', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'search' in response.data)

    def test_forgot_password(self):
        with self.client:
            response = self.client.get('/forgot_password', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'forgot_password' in response.data)

    def test_reset_password(self):
        with self.client:
            response = self.client.get('/reset_password', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'reset_password' in response.data)

    def test_tags(self):
        with self.client:
            response = self.client.get('/tags', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'tags' in response.data)


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

