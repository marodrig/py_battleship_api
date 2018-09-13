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

    def test_get_request_for_games(self):
        response = self.client.get(reverse('game-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_method_for_games(self):
        url = reverse('get_post_games')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 405)

    def test_post_request_for_games(self):
        response = self.client.post(reverse('get_post_games'))
        self.assertEqual(response.status_code, 200)

    def test_delete_request_for_games(self):
        url = reverse('get_delete_patch_game', kwargs={'game_id': int(1)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_get_request_for_game_ships(self):
        url = reverse('get_post_game_ships', kwargs={'game_id': int(1)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_request_for_game_ships(self):
        url = reverse('get_post_game_ships', kwargs={'game_id': int(1)})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_get_request_for_live_ships(self):
        url = reverse('get_alive_ships', kwargs={'game_id': int(1)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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
