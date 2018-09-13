import datetime

from django.test import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
from django.utils import timezone

from ..models import Game, ShipCoordinates, Ship


class APITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        game_inst = Game.objects.create(start_date=timezone.now())
        ship_inst = game_inst.ship_set.create(orientation=Ship.HORIZONTAL,
                                              length=Ship.CARRIER,
                                              is_alive=True)
        ship_inst.shipcoordinates_set.create(hit=False, row=int(1), column=int(1))

    @classmethod
    def tearDownTestData(cls):
        pass

    # def test_get_request_for_games(self):
    #     response = self.client.get(reverse('games'))
    #     self.assertEqual(response.status_code, 200)

    # def test_get_detail_for_game(self):
    #     response = self.client.get(reverse('get_game', kwargs={'game_id': int(1)}))
    #     self.assertEqual(response.status_code, 200)

    # def test_place_ship(self):
    #     url = reverse('place_ship', kwargs={'game_id': int(1)})
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_torpedo_hit(self):
    #     url = reverse('torpedo', kwargs={'game_id': int(1)})
    #     data = {'row': int(1), 'column': int(1)}
    #     response = self.client.get(url, data)
    #     self.assertEqual(response.status_code, 200)

    # def test_missed_shot(self):
    #     url = reverse('torpedo', kwargs={'game_id': int(1)})
    #     data = {'row': int(3), 'column': int(4)}
    #     response = self.client.get(url, data)
    #     self.assertEqual(response.status_code, 404)