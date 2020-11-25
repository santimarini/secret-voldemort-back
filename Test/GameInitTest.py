import unittest
import requests
import json
import sys
import os
from mock_database import DATABASE_PATH

sys.path.insert(1, DATABASE_PATH)

from database import *


class GameInitTest(unittest.TestCase):
    api = 'http://localhost:8000'
    start = '/start'

    def test_vote_gob_true(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test", "dir": 7})
        # Vote
        # for i in range(5):
        response = requests.put(self.api + '/game/game_init_test/vote',
                                params={"game_name": "game_init_test", "vote": True})
        resp_json = json.loads(response.text)
        self.assertEqual({'cant_vote': 1, 'vote': True, 'vote_less': 4}, resp_json)

    def test_vote_gob_false(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_2"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_2"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test_2", "dir": 12})
        # Vote
        response = requests.put(self.api + '/game/game_init_test_2/vote',
                                params={"game_name": "game_init_test_2", "vote": False})
        resp_json = json.loads(response.text)
        self.assertEqual({'cant_vote': 1, 'vote': False, 'vote_less': 4}, resp_json)

    def test_discard_min(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_3"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_3"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test_3", "dir": 12})
        # Vote and Gob Elect
        for i in range(5):
            requests.put(self.api + '/game/game_init_test_3/vote',
                         params={"game_name": "game_init_test_3", "vote": True})
        # Draw cards
        response = requests.get(self.api + '/cards/draw_three_cards', params={"game_name": "game_init_test_3"})
        resp_cards = json.loads(response.text)
        id_to_discard = resp_cards["cards_list"][1]["id"]
        response = requests.put(self.api + '/cards/discard_min',
                                params={"card_id": id_to_discard, "game_name": "game_init_test_3"})
        if is_card_discard(id_to_discard):
            self.assertEqual(200, response.status_code)
        else:
            self.assertEqual(404, response.status_code)

    def test_discard_dir(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_4"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_4"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test_4", "dir": 18})
        # Vote and Gob Elect
        for i in range(5):
            requests.put(self.api + '/game/game_init_test_4/vote',
                         params={"game_name": "game_init_test_4", "vote": True})
        # Draw cards
        response = requests.get(self.api + '/cards/draw_three_cards', params={"game_name": "game_init_test_4"})
        resp_cards = json.loads(response.text)
        id_to_discard = resp_cards["cards_list"][1]["id"]
        # Discard min
        response = requests.put(self.api + '/cards/discard_min',
                                params={"card_id": id_to_discard, "game_name": "game_init_test_4"})
        if is_card_discard(id_to_discard):
            response = requests.get(self.api + '/cards/draw_two_cards',
                                    params={"game_name": "game_init_test_4"})
            resp_cards = json.loads(response.text)
            # Get id
            id_to_discard = resp_cards["cards_list"][1]["id"]
            # Discard dir
            response = requests.put(self.api + '/cards/discard_dir',
                                    params={"card_id": id_to_discard, "game_name": "game_init_test_4"})
            if is_card_discard(id_to_discard):
                self.assertEqual(200, response.status_code)
            else:
                self.assertEqual(404, response.status_code)
        else:
            self.assertEqual(404, response.status_code)

    def test_discard_card_not_available_min(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_5"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_5"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test_5", "dir": 12})
        # Vote and Gob Elect
        for i in range(5):
            requests.put(self.api + '/game/game_init_test_5/vote',
                         params={"game_name": "game_init_test_5", "vote": True})
        # Draw cards
        response = requests.get(self.api + '/cards/draw_three_cards', params={"game_name": "game_init_test_5"})
        resp_cards = json.loads(response.text)
        response = requests.put(self.api + '/cards/discard_min',
                                params={"card_id": -1, "game_name": "game_init_test_5"})
        self.assertEqual(404, response.status_code)

    def test_discard_card_not_available_dir(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_6"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_6"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test_6", "dir": 18})
        # Vote and Gob Elect
        for i in range(5):
            requests.put(self.api + '/game/game_init_test_6/vote',
                         params={"game_name": "game_init_test_6", "vote": True})
        # Draw cards
        response = requests.get(self.api + '/cards/draw_three_cards', params={"game_name": "game_init_test_6"})
        resp_cards = json.loads(response.text)
        id_to_discard = resp_cards["cards_list"][1]["id"]
        # Discard min
        response = requests.put(self.api + '/cards/discard_min',
                                params={"card_id": id_to_discard, "game_name": "game_init_test_6"})
        if is_card_discard(id_to_discard):
            response = requests.get(self.api + '/cards/draw_two_cards',
                                    params={"game_name": "game_init_test_6"})
            response = requests.put(self.api + '/cards/discard_dir',
                                    params={"card_id": -100, "game_name": "game_init_test_6"})
            self.assertEqual(404, response.status_code)
        else:
            self.assertEqual(404, response.status_code)

    def test_divination(self):
        # Start game

        requests.post(self.api + self.start, params={"game_name": "game_init_test_9"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_9"})
        # Dir
        requests.put(self.api + '/game', params={"game_name": "game_init_test_9", "dir": 22})
        # Vote and Gob Elect
        for i in range(5):
            requests.put(self.api + '/game/game_init_test_9/vote',
                         params={"game_name": "game_init_test_9", "vote": True})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_test_9")
        cards_to_proclaim = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
        # Proclaim
        for i in range(3):
            proclaim(cards_to_proclaim[i])
        response = requests.get(self.api + '/cards/draw_three_cards', params={"game_name": "game_init_test_9"})
        self.assertEqual(200, response.status_code)

    def test_caos_not_started(self):
        response0 = requests.get(self.api + '/caos',
                                 params={"game_name": "game_init_aa1"})
        self.assertEqual(401, response0.status_code)

    def test_caos_not_exist(self):
        response0 = requests.get(self.api + '/caos',
                                 params={"game_name": "game_not_exist"})
        self.assertEqual(401, response0.status_code)

    def test_caos_ok(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_aa2"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_aa2"})
        response0 = requests.get(self.api + '/caos',
                                 params={"game_name": "game_init_aa2"})
        resp_caos = json.loads(response0.text)
        if "box" in  resp_caos:
            self.assertEqual(200, response0.status_code)
        else:
            self.assertEqual(200, 401)

    def test_caos_shuffle_cards(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_aa3"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_aa3"})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_aa3")
        # Discard
        for i in list_of_cards_id:
            discard(i)
        response0 = requests.get(self.api + '/caos',
                                 params={"game_name": "game_init_aa3"})
        resp_caos = json.loads(response0.text)
        if "box" in  resp_caos:
            self.assertEqual(200, response0.status_code)
        else:
            self.assertEqual(200, 401)

    def test_caos_finished_game(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_aa4"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_aa4"})
        # Get cards
        list_of_cards_id = get_cards_in_game("game_init_aa4")
        cards_dead = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
        # Proclaim dead Eaters
        for i in range(5):
            proclaim(cards_dead[i])
            box_id = get_next_box(cards_dead[i], "game_init_aa4")
            box = get_box(box_id)
            set_used_box(box_id)
        cards_of = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Fenix Order', list_of_cards_id))
        for i in range(4):
            proclaim(cards_of[i])
            box_id = get_next_box(cards_of[i], "game_init_aa4")
            box = get_box(box_id)
            set_used_box(box_id)
        # Caos
        response0 = requests.get(self.api + '/caos',
                                 params={"game_name": "game_init_aa4"})
        resp_caos = json.loads(response0.text)
        if "end_date" in  resp_caos:
            self.assertEqual(200, response0.status_code)
        else:
            self.assertEqual(200, 401)

    def test_crucio(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a1"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a1"})
        # Get list of player
        response0 = requests.get(self.api + '/get_players',
                                 params={"game_name": "game_init_test_a1"})
        resp_list0 = json.loads(response0.text)
        # List of players for crucio
        response1 = requests.get(self.api + '/list_of_crucio',
                            params={"game_name": "game_init_test_a1", "player_id": resp_list0["players_list"][0]["id"]})
        resp_list = json.loads(response1.text)
        response2 = requests.get(self.api + '/crucio',
                                 params={"game_name": "game_init_test_a1", "player_id": resp_list["list_players"][0]["id"]})
        response2_dict = json.loads(response2.text)
        if "loyalty" in response2_dict:
            self.assertEqual(200, 200)
        else:
            self.assertEqual(200, response2.status_code)

    def test_crucio_player_already_bewitched(self):
        # Start game
        requests.post(self.api + self.start, params={"game_name": "game_init_test_a2"})
        # Init turn
        requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_a2"})
        # Get list of player
        response0 = requests.get(self.api + '/get_players',
                                 params={"game_name": "game_init_test_a1"})
        resp_list0 = json.loads(response0.text)
        # List of players for crucio
        response1 = requests.get(self.api + '/list_of_crucio',
                            params={"game_name": "game_init_test_a2", "player_id": resp_list0["players_list"][0]["id"]})
        resp_list = json.loads(response1.text)
        response2 = requests.get(self.api + '/crucio',
                                 params={"game_name": "game_init_test_a2", "player_id": resp_list["list_players"][0]["id"]})
        response2_dict = json.loads(response2.text)
        if "loyalty" in response2_dict:
            response4 = requests.get(self.api + '/crucio',
                                     params={"game_name": "game_init_test_a2",
                                             "player_id": resp_list["list_players"][0]["id"]})
            self.assertEqual(401, response4.status_code)
        else:
            self.assertEqual(500, response2.status_code)

    def test_list_crucio_game_not_exist(self):
        response1 = requests.get(self.api + '/list_of_crucio',
                                 params={"game_name": "never_exist", "player_id": 30})
        self.assertEqual(401, response1.status_code)

    def test_list_crucio_not_started(self):
        response1 = requests.get(self.api + '/list_of_crucio',
                                 params={"game_name": "game_test_new", "player_id": 30})
        self.assertEqual(401, response1.status_code)

if __name__ == '__main__':
    unittest.main()
