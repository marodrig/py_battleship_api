"""
Models for the Battleship application.
"""
import random

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Django models below.


class Game(models.Model):
    """
    Game of battleship

    """
    NUMBER_SHIPS_ALLOWED = 5

    start_date = models.DateTimeField('date started', auto_now_add=True)
    is_over = models.BooleanField(default=False)

    def rand_init_ships(self):
        """
        """
        while self.ship_set.count() < self.NUMBER_SHIPS_ALLOWED:
            rand_ship_type = random.sample([x[0] for x in Ship.TYPE_CHOICES],
                                           len(Ship.TYPE_CHOICES))
            ships_list = []
            for ship_type in rand_ship_type:
                rand_orientation = random.choice(Ship.ORIENTATION_CHOICES)
                ship_object = Ship(game=self,
                                   orientation=rand_orientation[0],
                                   length=ship_type)
                ships_list.append(ship_object)
            Ship.objects.bulk_create(ships_list)
            for ship in self.ship_set.all():
                ship.rand_ship_position()

    def update_state(self):
        """
        Check's if the game is over

        """
        numb_ships_left = self.ship_set.filter(is_alive=True).count()
        if numb_ships_left == 0:
            self.is_over = True

    def build_board(self):
        """
        Generates a dictionary with all the ships coordinates

        :return game_board: Dictionary representation of ship locations
        :game_board type: dictionary

        """
        game_board = {}
        game_coordinates = self.shipcoordinate_set.all()
        for coordinate in game_coordinates:
            coord_tuple = (coordinate.ship_row, coordinate.ship_col)
            game_board[coord_tuple] = coordinate.hit
        return game_board

    def check_hit(self, game_board, row, column):
        """
        """
        hit_tuple = (row, column)
        return hit_tuple in game_board


class Ship(models.Model):
    """
    Ship in a game of battleship

    """
    # Orientation choices
    HORIZONTAL = 'HR'
    VERTICAL = 'VR'
    ORIENTATION_CHOICES = (
        (HORIZONTAL, 'Horizontal'),
        (VERTICAL, 'Vertical')
    )
    # Using the ship type to set the number of tiles
    CARRIER = 5
    BATTLESHIP = 4
    CRUISER = 3
    SUBMARINE = 3
    DESTROYER = 2
    TYPE_CHOICES = (
        (CARRIER, 'CARRIER'),
        (BATTLESHIP, 'BATTLESHIP'),
        (CRUISER, 'CRUISER'),
        (SUBMARINE, 'SUBMARINE'),
        (DESTROYER, 'DESTROYER')
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )
    orientation = models.CharField(
        max_length=2,
        choices=ORIENTATION_CHOICES,
        default=HORIZONTAL,
    )
    length = models.IntegerField(
        choices=TYPE_CHOICES,
        default=0
    )
    is_alive = models.BooleanField(default=True)

    def rand_ship_position(self):
        """
        """
        used_coordinates_set = set()
        valid_range = [x for x in range(ShipCoordinate.MIN_COORDINATE,
                                        ShipCoordinate.MAX_COORDINATE)]
        while self.shipcoordinate_set.count() < self.length:
            row, column = random.choice(valid_range), random.choice(valid_range)
            if (row, column) not in used_coordinates_set:
                used_coordinates_set.add((row, column))
                self.shipcoordinate_set.create(
                    game=self.game,
                    ship_row=row,
                    ship_col=column)
                coords_list = []
                for x in range(self.length - 1):
                    if self.orientation == Ship.HORIZONTAL:
                        column += 1
                    elif self.orientation == Ship.VERTICAL:
                        row += 1
                    ship_coord_obj = ShipCoordinate(
                        ship=self,
                        game=self.game,
                        ship_row=row,
                        ship_col=column)
                  
                    used_coordinates_set.add((row, column))
                    coords_list.append(ship_coord_obj)
                ShipCoordinate.objects.bulk_create(coords_list)

    def get_num_hits(self):
        """
        """
        return self.shipcoordinate_set.filter(hit=True).count()

    def update_state(self):
        """
        """
        num_hits = self.shipcoordinate_set.filter(hit=True).count()
        if num_hits == self.length:
            self.is_alive = False

    def __str__(self):
        """
        String representation of a ship

        """
        return "ship orientation:{0} tiles:{1}".format(
            self.orientation,
            self.length,
        )

    def add_coord(self, row, column):
        """
        """
        # TODO check for repeated coordinates
        if self.shipcoordinate_set.all().count() < self.length:
            self.shipcoordinate_set.create(
                ship_row=row,
                ship_col=column,
                hit=False)
        else:
            raise ValidationError(_('No more coordinates allowed.'))


def validate_coordinate(value):
    """
    Method used to validate a coordinate

    """
    if value > ShipCoordinate.MAX_COORDINATE or value < ShipCoordinate.MIN_COORDINATE:
        raise ValidationError('Value must be between {0} and {1}.'.format(
            ShipCoordinate.MIN_COORDINATE,
            ShipCoordinate.MAX_COORDINATE))


class ShipCoordinate(models.Model):
    """
    Tile related to a given ship in a given game

    """
    MIN_COORDINATE = 1
    MAX_COORDINATE = 10

    ship = models.ForeignKey(
        Ship,
        null=True,
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        Game,
        null=True,
        on_delete=models.CASCADE,
    )
    hit = models.BooleanField(default=False)
    ship_row = models.IntegerField(validators=[validate_coordinate])
    ship_col = models.IntegerField(validators=[validate_coordinate])

    def __str__(self):
        """
        """

        return "Row: {0} column: {1} hit: {2}".format(
            self.ship_row,
            self.ship_col,
            self.hit,
            )
