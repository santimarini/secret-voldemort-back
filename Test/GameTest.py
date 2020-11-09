import unittest
import requests


class GameTest(unittest.TestCase):
    api = 'http://localhost:8000'
    join_game= '/game/game_name'
    next_turn = '/next_turn'
    post_dir = '/game'
    is_started = '/game/is_started'
    min_and_dir = '/dirmin_elect'
    
    def test_next_turn_ok(self):
        game_name = {"game_name" : "game_name"}
        response = requests.post(self.api + self.next_turn,
                                params=game_name)
        print(response.url)
        print(response.reason)
        self.assertEqual(200,response.status_code)

    def test_next_turn_inexistent_game(self):
        game_name = {"game_name" : "asd"}
        response = requests.post(self.api + self.next_turn,
                                params=game_name)
        print(response.url)
        self.assertEqual(400,response.status_code)

    def test_next_turn_game_not_started(self):
        game_name = {"game_name" : "game_name_not_started"}
        response = requests.post(self.api + self.next_turn,
                                params=game_name)
        print(response.url)
        self.assertEqual(400,response.status_code)

    def test_post_dir_ok(self):
        parameters = {"game_name" : "game_name", "dir" : 2}
        response = requests.put(self.api + self.post_dir,
                                 params=parameters)
        print(response.url)
        self.assertEqual(200, response.status_code)

    def test_post_dir_game_not_started(self):
        parameters = {"game_name" : "game_name_not_started", "dir" : 2}
        response = requests.put(self.api + self.post_dir,
                                 params=parameters)
        print(response.url)
        self.assertEqual(400, response.status_code)

    def test_post_dir_inexistent_game(self):
        parameters = {"game_name": "asd", "dir": 2}
        response = requests.put(self.api + self.post_dir,
                                params=parameters)
        print(response.url)
        self.assertEqual(400, response.status_code)

    def test_post_dir_inexistent_player(self):
        parameters = {"game_name" : "game_name", "dir" : -1}
        response = requests.put(self.api + self.post_dir,
                                 params=parameters)
        print(response.url)
        self.assertEqual(400, response.status_code)

    def test_is_started_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.api + self.is_started,
                                params=game_name)
        print(response.url)
        self.assertEqual(200,response.status_code)

    def test_is_started_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.api + self.is_started,
                                params=game_name)
        print(response.url)
        self.assertEqual(400, response.status_code)

    def test_obtain_elect_min_and_dir_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.api + self.min_and_dir,
                                params=game_name)
        print(response.url)
        self.assertEqual(200, response.status_code)

    def test_obtain_elect_min_and_dir_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.api + self.min_and_dir,
                                params=game_name)
        print(response.url)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
