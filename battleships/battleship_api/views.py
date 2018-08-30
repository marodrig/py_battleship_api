"""
Controllers for the Battleship application

"""
import random

from django.db import DatabaseError, DataError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Game, Play, Ship, Tile

# Create your views here.


def games(request):
    """
    Creates a new entry in the Games table for a POST request
    Returns all the rows in the Games table for a GET request
    """
    if request.method == 'POST':
        game = Game.objects.create(start_date=timezone.now())
        return HttpResponse("Game created: {}".format(game.pk))
    elif request.method == 'GET':
        games_list = Game.objects.all()
        return HttpResponse(games_list[:10])


def get_game(request, game_id):
    """
    Returns a row from the Games table for the given game_id    

    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        return HttpResponse("Date: {}".format(game_inst.start_date))


def place_ship(request, game_id):
    """
    Randomly populates the game with 5 ships.

    """
    game_inst = get_object_or_404(Game, pk=game_id)
    # use a set to keep track of placed ships
    # use ship_set count to keep track of the number of ship.
    # keep a set of tuples for the tiles created.
    # randomly pick a starting front location, increase row or column 
    # depending on orientation.
    if request.method == 'POST':
        game_inst = get_object_or_404(Game, pk=game_id)
        if game_inst.ship_set.count() == 5:
            return HttpResponse('All ships places.')
        else:
            picked_classes = random.sample([x[0] for x in Ship.TYPE_CHOICES], 
                                           len(Ship.TYPE_CHOICES))
            for ship_type in picked_classes:
                rand_orientation = random.choice(Ship.ORIENTATION_CHOICES)
                game_inst.ship_set.create(orientation=rand_orientation,
                                          tile_size=ship_type)
            
            for ship in game_inst.ship_set.all():
                add_tile(ship)

        return HttpResponse("Placed ships:{}".format(game_inst.ship_set.count()))


def add_tile(ship_inst):
    """
    """
    valid_range = [x for x in range(1, 11)]
    placed_tiles_set = set()
    if isinstance(ship_inst, Ship):
        row, column = random.choice(valid_range), random.choice(valid_range)
        if (row, column) in placed_tiles_set:
            pass
        else:
            placed_tiles_set.add((row, column))
            ship_inst.tile_set.create(row=row, column=column)
            if ship_inst.orientation == 'HR':
                for _ in range(ship_inst.tile_size):
                    column += 1
                    ship_inst.tile_set.create(row=row, column=column)
            else:
                for _ in range(ship_inst.tile_size):
                    row += 1
                    ship_inst.tile_set.create(row=row, column=column)


def get_ship_detail(request, game_id, ship_id):
    """
    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        return HttpResponse("Ship: {}".format(ship_inst.pk))
    else:
        return HttpResponse("Error")


def torpedo(request, game_id):
    """
    """
    if request.method == 'GET':
        row = request.GET.get('row', -1)
        column = request.GET.get('column', -1)
        get_object_or_404(Tile, row=row, column=column)
        return HttpResponse('Hit')
