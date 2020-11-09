import unittest
import requests

class CardsTest(unittest.TestCase):
    localhost = 'http://localhost:8000'
    three_cards = '/cards/draw_three_cards'
    two_cards = '/cards/draw_two_cards'
    proclaim = '/cards/proclaim'

    def test_draw_three_cards_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.localhost + self.three_cards,
                                params=game_name)
        self.assertEqual(200,response.status_code)

    def test_draw_three_cards_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.localhost + self.three_cards,
                                params=game_name)
        self.assertEqual(400,response.status_code)

    def test_draw_two_cards_ok(self):
        game_name = {"game_name": "game_name"}
        response = requests.get(self.localhost + self.two_cards,
                                params=game_name)
        self.assertEqual(200,response.status_code)

    def test_draw_two_cards_inexistent_game(self):
        game_name = {"game_name": "asdasd"}
        response = requests.get(self.localhost + self.two_cards,
                                params=game_name)
        self.assertEqual(400,response.status_code)

    def test_proclaim_card_ok(self):
        parameters = {"game_name": "game_name", "card_id" : 1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(200,response.status_code)

    def test_proclaim_card_inexistent_card(self):
        parameters = {"game_name": "game_name", "card_id" : -1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(400,response.status_code)

    def test_proclaim_card_inexistent_game(self):
        parameters = {"game_name": "asdasd", "card_id" : 1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(400,response.status_code)

    def test_proclaim_card_game_not_started(self):
        parameters = {"game_name": "game_not_started", "card_id": 1}
        response = requests.put(self.localhost + self.proclaim,
                                params=parameters)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
