import unittest
import requests
import json


class CardsTest(unittest.TestCase):
    localhost = 'http://localhost:8000'
    three_cards = '/cards/draw_three_cards'
    two_cards = '/cards/draw_two_cards'
    proclaim = '/cards/proclaim'

    def test_draw_three_cards_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.localhost + self.three_cards,
                                params=game_name)
        self.assertEqual(200, response.status_code)

    def test_draw_three_cards_game_not_started(self):
        game_name = {"game_name": "game_name_not_started"}
        response = requests.get(self.localhost + self.three_cards,
                                params=game_name)
        detail = {"detail": "game is not started"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_draw_three_cards_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.localhost + self.three_cards,
                                params=game_name)
        detail = {"detail": "inexistent game"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_draw_two_cards_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.localhost + self.two_cards,
                                params=game_name)
        self.assertEqual(200, response.status_code)

    def test_draw_two_cards_game_not_started(self):
        game_name = {"game_name": "game_name_not_started"}
        response = requests.get(self.localhost + self.two_cards,
                                params=game_name)
        detail = {"detail": "game is not started"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_draw_two_cards_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.localhost + self.two_cards,
                                params=game_name)
        detail = {"detail": "inexistent game"}
        self.assertEqual(detail, json.loads(response.text))
        self.assertEqual(400, response.status_code)

    def test_proclaim_card_ok(self):
        response = requests.get(self.localhost + self.three_cards, params={"game_name": "game_name"})
        resp_cards = json.loads(response.text)
        id_to_proclam = resp_cards["cards_list"][1]["id"]
        parameters = {"game_name": "game_name", "card_id": id_to_proclam}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(200, response.status_code)

    def test_proclaim_card_inexistent_card(self):
        parameters = {"game_name": "game_name", "card_id": -1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(400, response.status_code)

    def test_proclaim_card_inexistent_game(self):
        parameters = {"game_name": "asdasd", "card_id": 1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(400, response.status_code)

    def test_proclaim_card_game_not_started(self):
        parameters = {"game_name": "game_not_started", "card_id": 1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
