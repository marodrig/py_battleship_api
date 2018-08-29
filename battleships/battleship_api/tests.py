"""
Tests for the Battleship application
"""
import datetime

from django.test import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
from django.utils import timezone

from .models import Game, Tile, Ship

# Create your tests here.


class APIViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Game.objects.create(start_date=timezone.now())

    @classmethod
    def tearDownTestData(cls):
        pass

    def test_create_game(self):
        response = self.client.post(reverse('games'))
        self.assertEqual(response.status_code, 200)

    def test_get_request_for_games(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)

    def test_get_detail_for_game(self):
        response = self.client.get(reverse('get_game', kwargs={'game_id': int(1)}))
        self.assertEqual(response.status_code, 200)

    def test_place_ship(self):
        url = reverse('place_ship', kwargs={'game_id': int(1)})
        response = self.client.post(url, {'orientation': Ship.HORIZONTAL,
                                          'type': Ship.CRUISER,
                                          'row': 1,
                                          'column': 0})
        self.assertEqual(response.status_code, 200)
