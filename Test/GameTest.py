import unittest
import requests
import json
import sys

from mock_database import DATABASE_PATH

sys.path.insert(1, DATABASE_PATH)

from database import *


class GameTest(unittest.TestCase):
    api = 'http://localhost:8000'
    join_game = '/game/game_name'
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
        game_name = {"game_name": "game_name"}
        response = requests.post(self.api + self.next_turn,
                                 params=game_name)

        self.assertEqual(200, response.status_code)

    def test_next_turn_inexistent_game(self):
        game_name = {"game_name": "asd"}
        response = requests.post(self.api + self.next_turn,
                                 params=game_name)
        detail = {"detail": "inexistent game"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_next_turn_game_not_started(self):
        game_name = {"game_name": "game_name_not_started"}
        response = requests.post(self.api + self.next_turn,
                                 params=game_name)
        detail = {"detail": "game is not started"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_post_dir_ok(self):
        parameters = {"game_name": "game_name", "dir": 2}
        response = requests.put(self.api + self.post_dir,
                                params=parameters)
        self.assertEqual(200, response.status_code)

    def test_post_dir_game_not_started(self):
        parameters = {"game_name": "game_name_not_started", "dir": 2}
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
        parameters = {"game_name": "game_name", "dir": -1}
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
                                  params={"name": "game_test_new", "max_players": "5"})
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
        response = requests.post(self.api + self.start, params={"game_name": "game_test_start"})
        self.assertEqual(200, response.status_code)

    def test_start_game_not_exists(self):
        response = requests.post(self.api + self.start, params={"game_name": "gameNotExist"})
        self.assertEqual(404, response.status_code)

    def test_show_games(self):
        response = requests.get(self.api + self.show_games)
        self.assertEqual(200, response.status_code)

    def test_avada_kedavra_ok(self):
        response = requests.post(self.api + self.start, params={"game_name": "game_init_test_7"})
        resp_start = json.loads(response.text)
        player_id = resp_start["players"][1]["id"]
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_7", "victim": player_id})
        self.assertEqual(200, response1.status_code)

    def test_avada_kedavra_game_doesnt_exist(self):
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_doesnt_exist", "victim": 12345})
        self.assertEqual(400, response1.status_code)

    def test_avada_kedavra_game_not_started(self):
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_8", "victim": 12345})
        self.assertEqual(400, response1.status_code)

    def test_avada_kedavra_player_already_death(self):
        response = requests.post(self.api + self.start, params={"game_name": "game_init_test_10"})
        resp_start = json.loads(response.text)
        player_id = resp_start["players"][1]["id"]
        response1 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_10", "victim": player_id})
        response2 = requests.get(self.api + self.avada_kedavra,
                                 params={"game_name": "game_init_test_10", "victim": player_id})
        self.assertEqual(401, response2.status_code)

    def test_list_imperius(self):
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a3"})
        response = requests.get(self.api + "/list_imperius", params={"game_name": "game_init_test_a3"})
        resp_json = json.loads(response.text)
        if "players_spellbinding" in resp_json:
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(200, 401)

    def test_imperius_ok(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a4"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a4"})
        set_elect_min(get_turn_by_gamename("game_init_test_a4"), 103)
        set_elect_dir(get_turn_by_gamename("game_init_test_a4"), 104)
        # List imperius
        response = requests.get(self.api + "/list_imperius", params={"game_name": "game_init_test_a4"})
        resp_json = json.loads(response.text)
        if "players_spellbinding" in resp_json:
            # Imperius
            id_imperius_min = resp_json["players_spellbinding"][0]["id"]
            response1 = requests.post(self.api + "/imperius",
                                      params={"game_name": "game_init_test_a4", "new_min_id": id_imperius_min})
            self.assertEqual(200, response1.status_code)
        else:
            self.assertEqual(200, 401)

    def test_imperius_game_not_exist(self):
        response = requests.post(self.api + "/imperius", params={"game_name": "game_init_test_a4", "new_min_id": 0})
        self.assertEqual(400, response.status_code)

    def test_imperius_game_not_started(self):
        response = requests.post(self.api + "/imperius", params={"game_name": "game_init_test_8", "new_min_id": 0})
        self.assertEqual(400, response.status_code)

    def test_imperius_player_not_exist(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a5"})
        response = requests.post(self.api + "/imperius", params={"game_name": "game_init_test_a5", "new_min_id": 0})
        self.assertEqual(400, response.status_code)

    def test_finished_imperius(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a6"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a6"})
        set_elect_min(get_turn_by_gamename("game_init_test_a6"), 108)
        set_elect_dir(get_turn_by_gamename("game_init_test_a6"), 109)
        # List imperius
        response = requests.get(self.api + "/list_imperius", params={"game_name": "game_init_test_a6"})
        resp_json = json.loads(response.text)
        if "players_spellbinding" in resp_json:
            # Imperius
            id_imperius_min = resp_json["players_spellbinding"][0]["id"]
            response1 = requests.post(self.api + "/imperius",
                                      params={"game_name": "game_init_test_a6", "new_min_id": id_imperius_min})
            response1 = requests.post(self.api + "/finish_imperius", params={"game_name": "game_init_test_a6"})
            self.assertEqual(200, response1.status_code)
        else:
            self.assertEqual(200, 401)

    def test_finished_imperius_game_not_exist(self):
        response = requests.post(self.api + "/finish_imperius", params={"game_name": "game_notexist"})
        self.assertEqual(400, response.status_code)

    def test_finished_imperius_game_not_started(self):
        response = requests.post(self.api + "/finish_imperius", params={"game_name": "game_init_test_8"})
        self.assertEqual(400, response.status_code)

    def test_expelliarmus_less_5_proclamation(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a7"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a7"})
        response = requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a7", "vote": True})
        self.assertEqual(401, response.status_code)

    def test_expelliarmus_one_vote_positive(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a8"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a8"})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_test_a8")
        cards_dead = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
        # Proclaim dead Eaters
        for i in range(5):
            proclaim(cards_dead[i])
            box_id = get_next_box(cards_dead[i], "game_init_test_a8")
            set_used_box(box_id)
        # Expelliarmus
        response = requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a8", "vote": True})
        self.assertEqual(200, response.status_code)

    def test_expelliarmus_one_vote_negative(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a9"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a9"})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_test_a9")
        cards_dead = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
        # Proclaim dead Eaters
        for i in range(5):
            proclaim(cards_dead[i])
            box_id = get_next_box(cards_dead[i], "game_init_test_a9")
            set_used_box(box_id)
        # Expelliarmus
        response = requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a9", "vote": False})
        self.assertEqual(200, response.status_code)

    def test_expelliarmus_ok(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a10"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a10"})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_test_a10")
        cards_dead = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
        # Proclaim dead Eaters
        for i in range(5):
            proclaim(cards_dead[i])
            box_id = get_next_box(cards_dead[i], "game_init_test_a10")
            set_used_box(box_id)
        # Expelliarmus
        requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a10", "vote": True})
        response = requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a10", "vote": True})
        self.assertEqual(200, response.status_code)

    def test_expelliarmus_not_accept(self):
        # Start
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a11"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a11"})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_test_a11")
        cards_dead = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
        # Proclaim dead Eaters
        for i in range(5):
            proclaim(cards_dead[i])
            box_id = get_next_box(cards_dead[i], "game_init_test_a11")
            set_used_box(box_id)
        # Expelliarmus
        requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a11", "vote": True})
        response = requests.put(self.api + "/expelliarmus", params={"game_name": "game_init_test_a11", "vote": False})
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
