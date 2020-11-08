import unittest
import requests


class GameTest(unittest.TestCase):
    api = 'http://localhost:8000'
    game = '/newgame'
    def register_user_for_game(self):
        # Register user
        requests.post(self.api + self.register,
                      data='{ "username": "usergame", "email": "usergame@gmail.com", "password": "123456" }')

    def test_newgame(self):
        response = requests.post(self.api + self.game,
                                 data='{ "name":"game", "max_players":"5", "email":"usergame@gmail.com"}')
        self.assertEqual(200, response.status_code)

    def test_game_exist(self):
        response = requests.post(self.api + self.game,
                                 data='{ "name":"exist", "max_players":"5", "email":"usergame@gmail.com"}')
        self.assertEqual(401, response.status_code)

    def test_game_whit_email_invalid(self):
        response = requests.post(self.api + self.game,
                                 data='{ "name":"game", "max_players":"5", "email":"usergame@gmail.com"}')
        self.assertEqual(401, response.status_code)

if __name__ == '__main__':
    unittest.main()
