import datetime

from django.test import TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse
from django.utils import timezone

from ..models import Game, ShipCoordinate, Ship


class APITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        game_inst = Game.objects.create(start_date=timezone.now())
        ship_inst = game_inst.ship_set.create(orientation=Ship.HORIZONTAL,
                                              length=Ship.CARRIER,
                                              is_alive=True,
                                              )
        ship_inst.shipcoordinate_set.create(hit=False,
                                            ship_row=int(1),
                                            ship_col=int(1),
                                            )

    @classmethod
    def tearDownTestData(cls):
        pass

    def test_get_request_for_games(self):
        response = self.client.get(reverse('game-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_request_for_games(self):
        response = self.client.post(reverse('game-list'))
        self.assertEqual(response.status_code, 200)
