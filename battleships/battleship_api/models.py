"""
Models for the Battleship application.
"""
from django.db import models

# Create your models here.


class Game(models.Model):
    start_date = models.DateTimeField('date started')
    is_over = models.BooleanField(default=False)


class Ship(models.Model):
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


class Tile(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    hit = models.BooleanField(default=False)
    row = models.IntegerField()
    column = models.IntegerField()


class Play(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_row = models.IntegerField()
    play_col = models.IntegerField()
    result = models.CharField(max_length=6)
