import unittest
import requests
import json


class UserTest(unittest.TestCase):
    api = 'http://localhost:8000'
    register = '/signup'
    login = '/token'
    save_image = '/upload_image'

    # TEST REGISTER ENDPOINT
    def test_new_user(self):
        response = requests.post(self.api + self.register,
                                 data = '{ "alias": "user_one", "email": "user_one@gmail.com", "password": "123456" }')
        rest_json = json.loads(response.text)
        self.assertEqual({'email': 'user_one@gmail.com'},rest_json)

    def test_short_alias(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "us", "email": "usr@gmail.com", "password": "123456"}')
        self.assertEqual(404, response.status_code)

    def test_great_alias(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "aaaaaaaaaaaaaaaaa", "email": "user_two@gmail.com", "password": "123456"}')
        self.assertEqual(404, response.status_code)

    def test_great_password(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_three", "email": "user_three@gmail.com", "password": "12345678912345678"}')
        self.assertEqual(404, response.status_code)

    def test_less_password(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_four", "email": "user_four@gmail.com", "password": "123"}')
        self.assertEqual(404, response.status_code)

    def test_great_email(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_four", "email": "user_five_epic_great_@gmail.com", "password": "1234"}')
        self.assertEqual(404, response.status_code)

    def test_invalid_email(self):
        response = requests.post(self.api + self.register,
                                 data='{ "alias": "user_six", "email": "user_six", "password": "123456" }')
        self.assertEqual(404, response.status_code)

    # TEST LOGIN ENDPOINT
    def test_login_user(self):
        # Register user
        requests.post(self.api + self.register,
                      data='{"alias": "user_seven", "email": "user_seven@gmail.com", "password": "123456"}')
        # Login user
        response = requests.post(self.api + self.login,
                                 params={"username": "user_seven@gmail.com", "password": "123456"})
        self.assertEqual(200, response.status_code)
        
    def test_save_image(self):
        response = requests.post(self.api + self.login,
                                 params={"photo" : "www.fakehost/image"})
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
