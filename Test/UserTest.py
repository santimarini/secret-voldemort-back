import unittest
import requests


class UserTest(unittest.TestCase):
    api = 'http://localhost:8000'
    register = '/signup'
    login = '/token'

    # TEST REGISTER ENDPOINT
    def test_new_user(self):
        response = requests.post(self.api + self.register,
                                 data = '{ "alias": "user_one", "email": "user_one@gmail.com", "password": "123456" }')
        self.assertEqual(200, response.status_code)

    def test_short_name(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "us", "email": "usr@gmail.com", "password": "123456"}')
        self.assertEqual(404, response.status_code)

    def test_great_name(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "aaaaaaaaaaaaa", "email": "user_two@gmail.com", "password": "123456"}')
        self.assertEqual(404, response.status_code)

    def test_great_password(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_three", "email": "user_three@gmail.com", "password": "1234567891234"}')
        self.assertEqual(404, response.status_code)

    def test_less_password(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_four", "email": "user_four@gmail.com", "password": "12"}')
        self.assertEqual(404, response.status_code)

    def test_great_email(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_four", "email": "user_five_epic_great_@gmail.com", "password": "1234"}')
        self.assertEqual(404, response.status_code)

    def test_invalid_email(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alis": "user_six", "email": "user_six", "password": "123456" }')
        self.assertEqual(404, response.status_code)

    # TEST LOGIN ENDPOINT
    def test_login_user(self):
        # Register user
        requests.post(self.api + self.register,
                      data='{"alias": "user_seven", "email": "user_seven@gmail.com", "password": "123456"}')
        # Login user
        response = requests.post(self.api + self.login,
                                 data='{"username": "user_seven@gmail.com", "password": "123456"}')
        self.assertEqual(200, response.status_code)
        
    

if __name__ == '__main__':
    unittest.main()