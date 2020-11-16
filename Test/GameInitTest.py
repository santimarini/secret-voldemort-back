import unittest
import requests
import json
import sys
import os

sys.path.insert(1, '/home/joaquin/secret-voldemort-back/database')
try:
    os.remove('/home/joaquin/secret-voldemort-back/database/database.sqlite')
except OSError:
    pass
from database import *


class GameInitTest(unittest.TestCase):
    api = 'http://localhost:8000'
    start = '/start'
    def test_vote_gob_true(self):
        # Start game
        requests.post(self.api + self.start, params={ "game_name": "game_init_test" })
        # Init turn
        requests.post(self.api + '/next_turn', params= {"game_name": "game_init_test"})
        # Dir
        requests.put(self.api + '/game', params= {"game_name": "game_init_test", "dir": 7})
        # Vote
        #for i in range(5):
        response = requests.put(self.api + '/game/game_init_test/vote', params= {"game_name": "game_init_test", "vote": True})
        resp_json = json.loads(response.text)
        self.assertEqual({'cant_vote': 1, 'vote': True, 'vote_less': 4}, resp_json)

    def test_vote_gob_false(self):
        # Start game
        requests.post(self.api + self.start, params={ "game_name": "game_init_test_2" })
        # Init turn
        requests.post(self.api + '/next_turn', params= {"game_name": "game_init_test_2"})
        # Dir
        requests.put(self.api + '/game', params= {"game_name": "game_init_test_2", "dir": 12})
        # Vote
        response = requests.put(self.api + '/game/game_init_test_2/vote', params= {"game_name": "game_init_test_2", "vote": False})
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
                                params={"card_id": id_to_discard,"game_name": "game_init_test_3"})
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
                                params={"card_id": id_to_discard,"game_name": "game_init_test_4"})
        if is_card_discard(id_to_discard):
            response = requests.get(self.api + '/cards/draw_two_cards',
                                    params={"game_name": "game_init_test_4"})
            resp_cards = json.loads(response.text)
            # Get id
            id_to_discard = resp_cards["cards_list"][1]["id"]
            # Discard dir
            response = requests.put(self.api + '/cards/discard_dir', params={"card_id": id_to_discard, "game_name": "game_init_test_4"})
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
                                params={"card_id": -1,"game_name": "game_init_test_5"})
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
                                params={"card_id": id_to_discard,"game_name": "game_init_test_6"})
        if is_card_discard(id_to_discard):
            response = requests.get(self.api + '/cards/draw_two_cards',
                                    params={"game_name": "game_init_test_6"})
            response = requests.put(self.api + '/cards/discard_dir', params={"card_id": -100, "game_name": "game_init_test_6"})
            self.assertEqual(404, response.status_code)
        else:
            self.assertEqual(404, response.status_code)

        def test_divination(self):
            # Start game
            requests.post(self.api + self.start, params={"game_name": "game_init_test_7"})
            # Init turn
            requests.post(self.api + '/next_turn', params={"game_name": "game_init_test_7"})
            # Dir
            requests.put(self.api + '/game', params={"game_name": "game_init_test_7", "dir": 22})
            # Vote and Gob Elect
            for i in range(5):
                requests.put(self.api + '/game/game_init_test_7/vote',
                             params={"game_name": "game_init_test_7", "vote": True})
            # Get cards
            list_of_cards_id = get_cards_in_game("game_init_test_7")
            cards_to_proclaim = list(filter(lambda x: card_to_dict(x)["loyalty"] == 'Death Eaters', list_of_cards_id))
            # Proclaim
            for i in range(3):
                proclaim(cards_to_proclaim[i])
            response = requests.get(self.api + '/cards/draw_three_cards', params={"game_name": "game_init_test_7"})
            self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
