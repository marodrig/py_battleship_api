"""
Tests the models in the battleship application

"""

from django.test import TestCase
from django.utils import timezone

from ..models import Game, Ship, ShipCoordinate

# Create your tests here.


class BaseTest(TestCase):
    """
    Base class for test cases of thise module

    """

    def setUp(self):
        self.game_inst = Game.objects.create(start_date=timezone.now())

    def tearDown(self):
        self.game_inst.delete()


class TestOfModels(BaseTest):
    """
    Class used to test Django's ORM models for this application.

    """

    def test_game_is_created(self):
        """
        """
        self.assertIsNotNone(self.game_inst)

    def test_ships_are_placed_randomly(self):
        """
        """
        self.game_inst.rand_init_ships()
        number_placed_ships = self.game_inst.ship_set.all().count()
        self.assertEqual(5, number_placed_ships)

    def test_no_repeated_carriers_in_random_ships(self):
        """
        """
        self.game_inst.rand_init_ships()
        carriers_ships_qs = self.game_inst.ship_set.filter(length=Ship.CARRIER)
        self.assertEqual(1, carriers_ships_qs.count())

    def test_no_repeated_battleships_in_random_ships(self):
        """
        """
        self.game_inst.rand_init_ships()
        battleships_ships_qs = self.game_inst.ship_set.filter(
            length=Ship.BATTLESHIP
            )
        self.assertEqual(1, battleships_ships_qs.count())

    def test_no_repeated_cruisers_in_random_ships(self):
        """
        """
        self.game_inst.rand_init_ships()
        cruisers_ships_qs = self.game_inst.ship_set.filter(
            length=Ship.CRUISER
            )
        self.assertEqual(2, cruisers_ships_qs.count())

    def test_no_repeated_submarines_in_random_ships(self):
        """
        """
        self.game_inst.rand_init_ships()
        submarines_ships_qs = self.game_inst.ship_set.filter(
            length=Ship.SUBMARINE
            )
        self.assertEqual(2, submarines_ships_qs.count())

    def test_no_repeated_destroyers_in_random_ships(self):
        """
        """
        self.game_inst.rand_init_ships()
        destroyers_ships_qs = self.game_inst.ship_set.filter(
            length=Ship.DESTROYER
            )
        self.assertEqual(1, destroyers_ships_qs.count())

    def test_game_state_is_updated(self):
        """
        """
        self.game_inst.rand_init_ships()
        for ship in self.game_inst.ship_set.all():
            ship.is_alive = False
        self.game_inst.update_state()
        self.assertFalse(self.game_inst.is_over)

    def test_ship_is_created(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.CARRIER,
            is_alive=True)
        self.assertIsNotNone(ship_inst)

    def test_adds_coordinates(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.CARRIER,
            is_alive=True)
        ship_inst.add_coord(1, 2)
        number_coordinates = ship_inst.shipcoordinate_set.all().count()
        self.assertEqual(1, number_coordinates)

    def test_randomized_ship_coordinates_for_CARRIER(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.CARRIER,
            is_alive=True)
        ship_inst.rand_ship_position()
        number_coordinates = ship_inst.shipcoordinate_set.all().count()
        self.assertEqual(Ship.CARRIER, number_coordinates)

    def test_randomized_ship_coordinates_for_BATTLESHIP(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.BATTLESHIP,
            is_alive=True)
        ship_inst.rand_ship_position()
        number_coordinates = ship_inst.shipcoordinate_set.all().count()
        self.assertEqual(Ship.BATTLESHIP, number_coordinates)

    def test_randomized_ship_coordinates_for_CRUISER(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.CRUISER,
            is_alive=True)
        ship_inst.rand_ship_position()
        number_coordinates = ship_inst.shipcoordinate_set.all().count()
        self.assertEqual(Ship.CRUISER, number_coordinates)

    def test_randomized_ship_coordinates_for_SUBMARINE(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.SUBMARINE,
            is_alive=True)
        ship_inst.rand_ship_position()
        number_coordinates = ship_inst.shipcoordinate_set.all().count()
        self.assertEqual(Ship.SUBMARINE, number_coordinates)

    def test_randomized_ship_coordinates_for_DESTROYER(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.DESTROYER,
            is_alive=True)
        ship_inst.rand_ship_position()
        number_coordinates = ship_inst.shipcoordinate_set.all().count()
        self.assertEqual(Ship.DESTROYER, number_coordinates)

    def test_no_hits_on_ship(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.DESTROYER,
            is_alive=True)
        ship_inst.rand_ship_position()
        number_hits = ship_inst.get_num_hits()
        self.assertEqual(0, number_hits)

    def test_all_hits_on_ship(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.DESTROYER,
            is_alive=True)
        ship_inst.rand_ship_position()
        for coord in ship_inst.shipcoordinate_set.all():
            coord.hit = True
            coord.save()
        number_hits = ship_inst.get_num_hits()
        self.assertEqual(Ship.DESTROYER, number_hits)

    def test_update_state_of_ship(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.DESTROYER,
            is_alive=True)
        ship_inst.rand_ship_position()
        for coord in ship_inst.shipcoordinate_set.all():
            coord.hit = True
            coord.save()
        ship_inst.update_state()
        self.assertFalse(ship_inst.is_alive)

    def test_create_ship_coordinates(self):
        """
        """
        ship_inst = self.game_inst.ship_set.create(
            orientation=Ship.HORIZONTAL,
            length=Ship.CARRIER,
            is_alive=True)
        coord_inst = ship_inst.shipcoordinate_set.create(
            ship_row=1,
            ship_col=1,
            hit=False
        )
        self.assertIsNotNone(coord_inst)
