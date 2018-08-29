from django.db import models

# Create your models here.


class Game(models.Model):
    start_date = models.DateTimeField('date started')
    is_over = models.BooleanField(default=False)


class Ship(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    orientation = models.CharField(max_length=2)
    ship_style = models.CharField(max_length=32)
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
