"""
Controllers for the Battleship application

"""
import random

from django.db import DatabaseError, DataError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Game, Play, Ship, Tile

# Create your views here.


@csrf_exempt
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
        for ship in game_inst.ship_set.all():
            print("Ship: {0}".format(ship))
        return HttpResponse("Date: {}".format(game_inst.start_date))


@csrf_exempt
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
        if game_inst.ship_set.count() < 5:
            picked_classes = random.sample([x[0] for x in Ship.TYPE_CHOICES], 
                                           len(Ship.TYPE_CHOICES))
            for ship_type in picked_classes:
                rand_orientation = random.choice(Ship.ORIENTATION_CHOICES)
                game_inst.ship_set.create(orientation=rand_orientation,
                                          tile_size=ship_type)
            
            placed_tiles_set = set()
            for ship in game_inst.ship_set.all():
                print(ship)
                add_tile(ship, placed_tiles_set)
        else:
            return HttpResponse('All ships places.')
        return HttpResponse("Placed ships:{}".format(game_inst.ship_set.count()))


def add_tile(ship_inst, placed_tiles_set):
    """
    """
    valid_range = [x for x in range(1, 11)]
    if isinstance(ship_inst, Ship):
        while ship_inst.tile_set.count() < ship_inst.tile_size:
            row, column = random.choice(valid_range), random.choice(valid_range)
            if (row, column) in placed_tiles_set and valid_tile(ship_inst, row, column):
                continue
            else:
                placed_tiles_set.add((row, column))
                ship_inst.tile_set.create(row=row, column=column)
                if ship_inst.orientation == Ship.HORIZONTAL:
                    for _ in range(ship_inst.tile_size - 1):
                        column += 1
                        ship_inst.tile_set.create(row=row, column=column)
                        placed_tiles_set.add((row, column))
                else:
                    for _ in range(ship_inst.tile_size - 1):
                        row += 1
                        ship_inst.tile_set.create(row=row, column=column)
                        placed_tiles_set.add((row, column))


def valid_tile(ship_inst, row, column):
    """
    """
    if ship_inst.orientation == Ship.HORIZONTAL:
        return column + ship_inst.tile_size <= 10
    elif ship_inst.orientation == Ship.VERTICAL:
        return row + ship_inst.tile_size <= 10


def get_tiles(request, game_id, ship_id):
    """
    Gets tiles of a given ship for a given game

    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        for ship in game_inst.ship_set.all():
            print(ship)
            for tile in ship.tile_set.all():
                print(tile)
        return HttpResponse(game_inst.ship_set.all())


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
        row = int(request.GET.get('row', -1))
        column = int(request.GET.get('column', -1))
        print("row: {0} column: {1}".format(row, column))
        tile_inst = get_object_or_404(Tile, row=row, column=column)
        tile_inst.hit = True
        return HttpResponse()
