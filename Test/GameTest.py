import unittest
import requests
import json

class GameTest(unittest.TestCase):
    api = 'http://localhost:8000'
    join_game= '/game/game_name'
    next_turn = '/next_turn'
    post_dir = '/game'
    is_started = '/game/is_started'
    min_and_dir = '/dirmin_elect'
    game = '/newgame'
    start = '/start'
    show_games = '/show_games'
    avada_kedavra = '/avada_kedavra'
    register = '/signup'
    send_mail = '/send_email'
    validate_email = '/validate/'
    login = '/token'

    def test_next_turn_ok(self):
        game_name = {"game_name" : "game_name"}
        response = requests.post(self.api + self.next_turn,
                                params=game_name)

        self.assertEqual(200,response.status_code)

    def test_next_turn_inexistent_game(self):
        game_name = {"game_name" : "asd"}
        response = requests.post(self.api + self.next_turn,
                                params=game_name)
        detail = {"detail" : "inexistent game"}
        self.assertEqual(detail,json.loads(response.text))
        self.assertEqual(400,response.status_code)

    def test_next_turn_game_not_started(self):
        game_name = {"game_name" : "game_name_not_started"}
        response = requests.post(self.api + self.next_turn,
                                params=game_name)
        detail = {"detail": "game is not started"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400,response.status_code)

    def test_post_dir_ok(self):
        parameters = {"game_name" : "game_name", "dir" : 2}
        response = requests.put(self.api + self.post_dir,
                                 params=parameters)
        self.assertEqual(200, response.status_code)

    def test_post_dir_game_not_started(self):
        parameters = {"game_name" : "game_name_not_started", "dir" : 2}
        response = requests.put(self.api + self.post_dir,
                                 params=parameters)
        detail = {"detail": "game is not started"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_post_dir_inexistent_game(self):
        parameters = {"game_name": "asd", "dir": 2}
        response = requests.put(self.api + self.post_dir,
                                params=parameters)
        detail = {"detail": "inexistent game"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_post_dir_inexistent_player(self):
        parameters = {"game_name" : "game_name", "dir" : -1}
        response = requests.put(self.api + self.post_dir,
                                 params=parameters)
        detail = {"detail": "player doesn't exist"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_obtain_elect_min_and_dir_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.api + self.min_and_dir,
                                params=game_name)
        self.assertEqual(200, response.status_code)

    def test_obtain_elect_min_and_dir_game_not_started(self):
        game_name = {"game_name": "game_name_not_started"}
        response = requests.get(self.api + self.min_and_dir,
                                params=game_name)
        detail = {"detail": "game is not started"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_obtain_elect_min_and_dir_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.api + self.min_and_dir,
                                params=game_name)
        detail = {"detail": "inexistent game"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)
        

    def register_user_for_game(self):
        # Register user
        requests.post(self.api + self.register,
                      data='{ "alias": "usergame", "email": "usergame@gmail.com", "password": "123456" }')

    def test_newgame(self):
        r5 = requests.post(self.api + self.register,
                      data='{ "alias": "usergame1", "email": "usergame1@gmail.com", "password": "123456" }')
        # Send Mail
        r6 = requests.post(self.api + self.send_mail, params={"user_email": "usergame1@gmail.com"})
        resp_token_val = json.loads(r6.text)
        token_val = resp_token_val["token_val"]

        # Validate Email
        r7 = requests.get(self.api + self.validate_email + token_val)
        # Login
        response = requests.post(self.api + self.login,
                                 data={"username": "usergame1@gmail.com", "password": "123456"})
        # Create Game
        response2 = requests.post(self.api + self.game, data='{"username":"usergame1@gmail.com", "password": "123456"}',
                                 params={ "name":"game_test_new", "max_players":"5"})
        self.assertEqual(200, response.status_code)

    def test_game_exist(self):
        response = requests.post(self.api + self.game,
                                 data='{ "name":"exist", "max_players":"5", "email":"usergame@gmail.com"}')
        self.assertEqual(401, response.status_code)

    def test_game_whit_email_invalid(self):
        response = requests.post(self.api + self.game,
                                 data='{ "name":"game_email", "max_players":"5", "email":"usergame@gmail.com"}')
        self.assertEqual(401, response.status_code)

    def test_start_game(self):
        response = requests.post(self.api + self.start, params={ "game_name": "game_test_start" })
        self.assertEqual(200, response.status_code)

    def test_start_game_not_exists(self):
        response = requests.post(self.api + self.start, params={ "game_name": "gameNotExist" })
        self.assertEqual(404, response.status_code)

    def test_show_games(self):
        response = requests.get(self.api + self.show_games)
        games = {'games_list': [{'id': 2, 'name': 'game_name_not_started', 'players': 3, 'max_players': 10},\
                                {'id': 3, 'name': 'game_name_test', 'players': 0, 'max_players': 5}]}
        self.assertEqual(games,json.loads(response.text))
        self.assertEqual(200,response.status_code)

    def test_avada_kedavra_ok(self):
        response = requests.post(self.api + self.start, params={ "game_name": "game_init_test_7" })
        resp_start = json.loads(response.text)
        player_id = resp_start["players"][1]["id"]
        response1 = requests.get(self.api + self.avada_kedavra, params= {"game_name": "game_init_test_7", "victim": player_id})
        self.assertEqual(200, response1.status_code)

    def test_avada_kedavra_game_doesnt_exist(self):
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_doesnt_exist", "victim": 12345})
        self.assertEqual(400, response1.status_code)

    def test_avada_kedavra_game_not_started(self):
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_8", "victim": 12345})
        self.assertEqual(400, response1.status_code)

    def test_avada_kedavra_player_not_in_game(self):
        response = requests.post(self.api + self.start, params={"game_name": "game_init_test_9"})
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_9", "victim": 55654})
        self.assertEqual(400, response1.status_code)

    def test_avada_kedavra_player_already_death(self):
        response = requests.post(self.api + self.start, params={ "game_name": "game_init_test_10" })
        resp_start = json.loads(response.text)
        player_id = resp_start["players"][1]["id"]
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params= {"game_name": "game_init_test_10", "victim": player_id})
        response2 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_10", "victim": player_id})
        self.assertEqual(401, response2.status_code)

if __name__ == '__main__':
    unittest.main()
