"""
Controllers for the Battleship application

"""
import random

from django.db import DatabaseError, DataError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

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
        response = HttpResponse()
        response['location'] = "battleship/api/v1/games/{0}/".format(game.pk)
        return response
    elif request.method == 'GET':
        games_list = Game.objects.all()
        return HttpResponse(serialize('json', games_list))


def get_game(request, game_id):
    """
    Returns a row from the Games table for the given game_id    

    """
    if request.method == 'GET':
        game_inst = get_object_or_404(Game, pk=game_id)
        return HttpResponse(serialize('json', game_inst.ship_set.all()))


@csrf_exempt
def place_ship(request, game_id):
    """
    Randomly populates the game with 5 ships.

    """
    game_inst = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        game_inst = get_object_or_404(Game, pk=game_id)
        if game_inst.ship_set.count() < 5:
            rand_ship_type = random.sample([x[0] for x in Ship.TYPE_CHOICES],
                                           len(Ship.TYPE_CHOICES))
            for ship_type in rand_ship_type:
                rand_orientation = random.choice(Ship.ORIENTATION_CHOICES)
                game_inst.ship_set.create(orientation=rand_orientation,
                                          tile_size=ship_type)
            
            placed_tiles_set = set()
            for ship in game_inst.ship_set.all():
                add_tile(ship, placed_tiles_set)
        else:
            return HttpResponse('All ships placed.')
        return JsonResponse({'ships_placed': game_inst.ship_set.count()})
    if request.method == 'GET':
        data = {'rel': 'Ships',
                'method': 'POST',
                'Error': 'Not allowed to see ships!'}
        return JsonResponse(status=404, data=data)


def add_tile(ship_inst, placed_tiles_set):
    """
    Places ship in randomized tiles.

    """
    valid_range = [x for x in range(1, 11)]
    if isinstance(ship_inst, Ship):
        while ship_inst.tile_set.count() < ship_inst.tile_size:
            row, column = random.choice(valid_range), random.choice(valid_range)
            if (row, column) in placed_tiles_set and valid_tile(ship_inst, row, column):
                continue
            else:
                placed_tiles_set.add((row, column))
                ship_inst.tile_set.create(game=ship_inst.game,
                                          row=row,
                                          column=column)
                for _ in range(ship_inst.tile_size - 1):
                    if ship_inst.orientation == Ship.HORIZONTAL:
                        column += 1
                    elif ship_inst.orientation == Ship.VERTICAL:
                        row += 1
                    ship_inst.tile_set.create(game=ship_inst.game, row=row, column=column)
                    placed_tiles_set.add((row, column))


def valid_tile(ship_inst, row, column):
    """
    Validates if starting from this tile the position will be valid.

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
        return HttpResponse(serialize('json', game_inst.tile_set.all()))


def get_ship_detail(request, game_id, ship_id):
    """
    Returns the detail of a ship

    """
    if request.method == 'GET':
        ship_inst = get_object_or_404(Ship, pk=ship_id)
        return HttpResponse(serialize('json', ship_inst))
    else:
        return HttpResponse("Error")


def torpedo(request, game_id):
    """
    Checks if a torpedo has hit a tile belonging to a ship

    """
    if request.method == 'GET':
        row = int(request.GET.get('row', -1))
        column = int(request.GET.get('column', -1))
        game_inst = get_object_or_404(Game, pk=game_id)
        tile_inst = None
        data = {}
        if game_inst.is_over:
            data['status'] = 'You won!'
        num_sunked_ships = int(game_inst.ship_set.filter(is_alive=False).count())
        if num_sunked_ships == 5:
            game_inst.is_over = True
            game_inst.save()
        try:
            tile_inst = game_inst.tile_set.get(row=row,
                                               column=column,
                                               hit=False)
        except Tile.DoesNotExist:
            data['status'] = 'Miss, try again.'
        if tile_inst:
            tile_inst.hit = True
            tile_inst.save()
            data['status'] = 'Hit!'
            return JsonResponse(status=200, data=data)
        update_sunked_ships(game_inst)
        return JsonResponse(status=404, data=data)


def update_sunked_ships(game_inst):
    """
        Checks the number of hits on a ship to see if it's floating

    """
    for ship in game_inst.ship_set.all():
        num_hits = int(ship.tile_set.filter(hit=True).count())
        if num_hits == int(ship.tile_size):
            ship.is_alive = False
            ship.save()
