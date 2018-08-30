"""
Models for the Battleship application.
"""
from django.db import models

# Create your models here.


class Game(models.Model):
    """
    Game of battleship

    """
    start_date = models.DateTimeField('date started')
    is_over = models.BooleanField(default=False)


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
        (CARRIER, 'CRUISER'),
        (BATTLESHIP, 'BATTLESHIP'),
        (CRUISER, 'CRUISER'),
        (SUBMARINE, 'SUBMARINE'),
        (DESTROYER, 'DESTROYER')
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    orientation = models.CharField(max_length=2,
                                   choices=ORIENTATION_CHOICES,
                                   default=HORIZONTAL)
    tile_size = models.IntegerField(choices=TYPE_CHOICES, default=0)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        """
        String representation of a ship

        """
        return "ship orientation:{0} tiles:{1}".format(self.orientation, self.tile_size)


class Tile(models.Model):
    """
    Tile related to a given ship in a given game

    """
    ship = models.ForeignKey(Ship, null=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    hit = models.BooleanField(default=False)
    row = models.IntegerField()
    column = models.IntegerField()

    def __str__(self):
        """
        """

        return "Row:{0} column:{1} hit:{2}".format(self.row, self.column, self.hit)


class Play(models.Model):
    """
    Record of each play in a game of battleship

    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_row = models.IntegerField()
    play_col = models.IntegerField()
    result = models.CharField(max_length=6)

    def __str__(sefl):
        """
        """
        return "Play--> row:{0} column:{1} result:{2}".format(self.row, self.column, self.result)
