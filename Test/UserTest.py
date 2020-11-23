import unittest
import requests
import json


class UserTest(unittest.TestCase):
    api = 'http://localhost:8000'
    register = '/signup'
    login = '/token'
    save_image = '/upload_image'
    change_pass = '/change_password'
    send_mail = '/send_email'
    validate_email = '/validate/'

    def test_send_mail(self):
        response2 = requests.post(self.api + self.register,
                          data='{"alias": "gonzalo", "email": "user_doesnt_exist1@gmail.com", "password": "123456"}')
        response = requests.post(self.api + self.send_mail, params={"user_email": "user_doesnt_exist1@gmail.com"})
        response3 = requests.post(self.api + self.register,
                                  data='{"alias": "leandro", "email": "user_doesnt_exist2@unc.edu.ar", "password": "123456"}')
        response4 = requests.post(self.api + self.send_mail, params={"user_email": "user_doesnt_exist2@unc.edu.ar"})
        self.assertEqual(200,response.status_code)

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
        self.assertEqual(422, response.status_code)

    # TEST LOGIN ENDPOINT
    def test_login_user(self):
        # Register user
        requests.post(self.api + self.register,
                      data='{"alias": "user_seven", "email": "user_seven@gmail.com", "password": "123456"}')
        # Login user
        response = requests.post(self.api + self.login,
                                 data={"username": "user_seven@gmail.com", "password": "123456"})
        self.assertEqual(200, response.status_code)

    def test_save_image(self):
        r5 = requests.post(self.api + self.register,
                           data='{"alias": "user_mock", "email": "user_mock@gmail.com", "password": "123456"}')

        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_mock@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]

        r7 = requests.get(self.api + self.validate_email + token_val)

        response1 = requests.post(self.api + self.login,
                                  data={"username": "user_mock@gmail.com", "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        type = resp_token["token_type"]
        data2 = {"photo" : "www.fakehost/image"}
        r2 = requests.post(self.api + self.save_image, params=data2, headers={'Content-Type': 'application/json',
                                                                               'Authorization': 'Bearer {}'.format(
                                                                                   token)})
        self.assertEqual(200, r2.status_code)


    def test_change_alias_ok(self):
        # Register user
        r5 = requests.post(self.api + self.register,
                      data='{"alias": "user_alias", "email": "user_alias@gmail.com", "password": "123456"}')
        # Send Mail
        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_alias@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]
        # Validate Email
        r7 = requests.get(self.api + self.validate_email + token_val)
        # Login
        response1 = requests.post(self.api + self.login,
                                  data={"username": 'user_alias@gmail.com', "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        params1 = {"alias": "alias_change"}
        r2 = requests.post(self.api + '/change_alias', params=params1, headers={'Content-Type': 'application/json',
                                                                                'Authorization': 'Bearer {}'.format(
                                                                                    token)})
        self.assertEqual(200, r2.status_code)

    def test_change_alias_great(self):
        # Register user
        r5 = requests.post(self.api + self.register,
                      data='{"alias": "user_alias_1", "email": "user_alias_1@gmail.com", "password": "123456"}')
        # Send Mail
        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_alias_1@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]
        # Validate Email
        r7 = requests.get(self.api + self.validate_email + token_val)
        # Login
        response1 = requests.post(self.api + self.login,
                                  data={"username": 'user_alias_1@gmail.com', "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        params1 = {"alias": "alias_changegreat"}
        r2 = requests.post(self.api + '/change_alias', params=params1, headers={'Content-Type': 'application/json',
                                                                                'Authorization': 'Bearer {}'.format(
                                                                                    token)})
        self.assertEqual(401, r2.status_code)

    def test_change_alias_les(self):
        # Register user
        r5 = requests.post(self.api + self.register,
                      data='{"alias": "user_alias_2", "email": "user_alias_2@gmail.com", "password": "123456"}')
        # Send Mail
        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_alias_2@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]
        # Validate Email
        r7 = requests.get(self.api + self.validate_email + token_val)
        # Login
        response1 = requests.post(self.api + self.login,
                                  data={"username": 'user_alias_2@gmail.com', "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        params1 = {"alias": "als"}
        r2 = requests.post(self.api + '/change_alias', params=params1, headers={'Content-Type': 'application/json',
                                                                                'Authorization': 'Bearer {}'.format(
                                                                                    token)})
        self.assertEqual(401, r2.status_code)

    def test_change_alias_email_not_verified(self):
        # Register user
        r5 = requests.post(self.api + self.register,
                      data='{"alias": "user_alias_3", "email": "user_alias_3@gmail.com", "password": "123456"}')

        # Login
        response1 = requests.post(self.api + self.login,
                                  data={"username": 'user_alias_3@gmail.com', "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        params1 = {"alias": "other_alias"}
        r2 = requests.post(self.api + '/change_alias', params=params1, headers={'Content-Type': 'application/json',
                                                                                'Authorization': 'Bearer {}'.format(
                                                                                    token)})
        self.assertEqual(401, r2.status_code)

    def test_change_password_ok(self):
        r5 = requests.post(self.api + self.register,
                      data='{"alias": "user_eigth", "email": "user_eigth@gmail.com", "password": "123456"}')

        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_eigth@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]

        r7 = requests.get(self.api + self.validate_email + token_val)

        response1 = requests.post(self.api + self.login,
                                 data={"username": "user_eigth@gmail.com", "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        type = resp_token["token_type"]
        data2 = {"old_password": "123456", "new_password": "secret123",
                                         "confirm_new_password": "secret123" }
        r2 = requests.post(self.api + self.change_pass, params=data2, headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(200, r2.status_code)

    def test_change_password_unauthorized(self):
        r5 = requests.post(self.api + self.register,
                           data='{"alias": "user_nine", "email": "user_nine@gmail.com", "password": "123456"}')
        data2 = {"old_password": "123456", "new_password": "secret123",
                 "confirm_new_password": "secret123"}
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2VpZ3RoQGdtYWlsLmNvbSIsImV4cCI6MTYwNTk4NDQ2N30.TP86rS08g58icByU8XmSjue68GaKfCKUJSFqL0JuQ"
        r2 = requests.post(self.api + self.change_pass, params=data2, headers={'Content-Type': 'application/json',
                                                                               'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(401, r2.status_code)

    def test_change_password_email_not_verified(self):
        r5 = requests.post(self.api + self.register,
                           data='{"alias": "user_ten", "email": "user_ten@gmail.com", "password": "123456"}')

        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_ten@gmail.com"})

        response1 = requests.post(self.api + self.login,
                                  data={"username": "user_ten@gmail.com", "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        type = resp_token["token_type"]
        data2 = {"old_password": "123456", "new_password": "secret123",
                 "confirm_new_password": "secret123"}
        r2 = requests.post(self.api + self.change_pass, params=data2, headers={'Content-Type': 'application/json',
                                                                               'Authorization': 'Bearer {}'.format(
                                                                                   token)})
        self.assertEqual(400, r2.status_code)

    def test_change_password_doesnt_match(self):
        r5 = requests.post(self.api + self.register,
                           data='{"alias": "user_eleven", "email": "user_eleven@gmail.com", "password": "123456"}')

        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_eleven@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]

        r7 = requests.get(self.api + self.validate_email + token_val)

        response1 = requests.post(self.api + self.login,
                                  data={"username": "user_eleven@gmail.com", "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        type = resp_token["token_type"]
        data2 = {"old_password": "123456", "new_password": "secret123",
                 "confirm_new_password": "secret1234"}
        r2 = requests.post(self.api + self.change_pass, params=data2, headers={'Content-Type': 'application/json',
                                                                               'Authorization': 'Bearer {}'.format(
                                                                                   token)})
        self.assertEqual(404, r2.status_code)

    def test_change_password_old_password_worng(self):
        r5 = requests.post(self.api + self.register,
                           data='{"alias": "user_twelve", "email": "user_twelve@gmail.com", "password": "123456"}')

        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_twelve@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]
        r7 = requests.get(self.api + self.validate_email + token_val)
        response1 = requests.post(self.api + self.login,
                                  data={"username": "user_twelve@gmail.com", "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        type = resp_token["token_type"]
        data2 = {"old_password": "1234567", "new_password": "secret123",
                 "confirm_new_password": "secret123"}
        r2 = requests.post(self.api + self.change_pass, params=data2, headers={'Content-Type': 'application/json',
                                                                               'Authorization': 'Bearer {}'.format(
                                                                                   token)})
        self.assertEqual(404, r2.status_code)

    def test_change_password_old_equal_to_new(self):
        r5 = requests.post(self.api + self.register,
                           data='{"alias": "user_thirteen", "email": "user_thirteen@gmail.com", "password": "123456"}')

        r6 = requests.post(self.api + self.send_mail, params={"user_email": "user_thirteen@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]
        r7 = requests.get(self.api + self.validate_email + token_val)
        response1 = requests.post(self.api + self.login,
                                  data={"username": "user_thirteen@gmail.com", "password": "123456"})
        resp_token = json.loads(response1.text)
        token = resp_token["access_token"]
        type = resp_token["token_type"]
        data2 = {"old_password": "1234567", "new_password": "1234567",
                 "confirm_new_password": "secret123"}
        r2 = requests.post(self.api + self.change_pass, params=data2, headers={'Content-Type': 'application/json',
                                                                               'Authorization': 'Bearer {}'.format(
                                                                                   token)})
        self.assertEqual(404, r2.status_code)



if __name__ == '__main__':
    unittest.main()
