import datetime

from django.test import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
from django.utils import timezone

from ..models import Game, ShipCoordinate, Ship


class BaseTest(TestCase):
    """
    Base class for test cases for this  module

    """

    def setUp(self):
        self.game_inst = Game.objects.create(start_date=timezone.now())
        self.ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.CARRIER,
            is_alive=True,
        )
        self.ship_inst.shipcoordinate_set.create(
            hit=False,
            ship_row=int(1),
            ship_col=int(1),
        )

    def tearDown(self):
        self.game_inst.delete()
        self.ship_inst.delete()


class TestOfAPIEndpoints(BaseTest):
    """
    Class used to test REST API endpoints

    """

    def test_get_request_for_games(self):
        response = self.client.get(reverse('game-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_request_for_games(self):
        response = self.client.post(reverse('game-list'))
        self.assertEqual(response.status_code, 201)

    def test_get_request_for_game_details(self):
        url = reverse('game-details', args=(self.game_inst.pk, ))
        # self.client.post(url, data = {})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_game_details(self):
        url = reverse('game-details', args=(self.game_inst.pk, ))
        response = self.client.put(url, data={'is_over': True})
        self.assertEquals(response.status_code, 200)

    def test_delete_request_game_details(self):
        url = reverse('game-details', kwargs={'pk': int(1)})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 204)

    def test_get_alive_ship_list(self):
        url = reverse('get_alive_ships', args=(self.game_inst.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
